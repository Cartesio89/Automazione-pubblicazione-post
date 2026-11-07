#!/usr/bin/env python3
"""
humanize.py - toglie l'impronta da macchina da una bozza (versione italiana).

Tre passaggi, in quest'ordine:

  1. INVISIBILI   cancella o normalizza i caratteri che una tastiera umana non
                  produce: zero-width joiner, word joiner, trattini soffici,
                  BOM, caratteri tag Unicode, spazi non separabili e stretti.
                  Sopravvivono al copia-incolla e sono il segnale più
                  meccanico di qualsiasi testo generato.
  2. TIPOGRAFIA   trattino lungo -> virgola, trattino medio -> trattino,
                  virgolette ricurve -> dritte, puntini di sospensione ->
                  tre punti, pallino -> trattino. Le caporali « » non si toccano.
  3. LESSICALE    sostituisce il lessico "da IA" di slop.json con parole
                  normali, rispettando le maiuscole e lasciando intatti gli URL.
                  Le voci con "regex": true conservano la desinenza, così
                  "sfruttiamo" diventa "usiamo" e non "usare".

I segnali strutturali ("non è solo X, è Y", triadi, muri di hashtag) vengono
SEGNALATI, mai riscritti in automatico: cambiare la forma di una frase richiede
giudizio, quindi è compito del modello, non di una regex.

Uso
  python3 humanize.py bozza.txt
  python3 humanize.py bozza.txt --report
  pbpaste | python3 humanize.py - --report        (su Windows: Get-Clipboard | python humanize.py - --report)
  python3 humanize.py bozza.txt --json
  python3 humanize.py bozza.txt -o pulito.txt

ATTENZIONE: il lessico italiano NON è calibrato su testi reali. Le sostituzioni
sono scelte per non rompere genere e numero, ma rileggi sempre il risultato.
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
# Il punto tra due cifre ("18.000") non chiude una frase.
SENT_RE = re.compile(r"(?:[^.!?\n]|(?<=\d)\.(?=\d))+[.!?]*")
LETTER = r"[^\W\d_]"


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def entry_pattern(entry):
    """Compila una voce del lessico. Voce letterale o, con "regex": true, regex."""
    if entry.get("regex"):
        body = entry["find"]
    else:
        body = re.escape(entry["find"]).replace(r"\ ", r"\s+")
    # (?<!\w) e (?!\w) al posto di \b: funzionano anche se la voce finisce con "?"
    # o inizia con un'elisione ("l'algoritmo").
    # Una voce che finisce con l'apostrofo ("immergiti nell'") è seguita da una lettera.
    tail = "" if body.endswith("'") else r"(?!\w)"
    return re.compile(r"(?<!\w)(?:" + body + r")" + tail, re.IGNORECASE)


def entry_label(entry):
    return entry.get("label") or entry["find"]


def _cp(spec):
    """'U+200B' -> '\\u200b';  'U+E0000-U+E007F' -> (inizio, fine)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """Sostituisce gli URL con segnaposto, così nessun passaggio riscrive un link."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    """Cancella o normalizza i caratteri invisibili. Restituisce (testo, hit)."""
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": entry["action"]})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Ogni carattere di formato (Cf) rimasto è invisibile per definizione.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "altri caratteri di formato invisibili", "count": len(stray),
                     "action": "delete"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n, "to": entry["to"].strip() or "(spazio)"})
        if ch == "—":
            # " parola — parola " e "parola—parola" diventano virgola + spazio.
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)      # 5–10  -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)            # usato come trattino lungo
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    # Una virgola inserita davanti a una punteggiatura già presente suona male.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def pass_lexical(text, lex):
    """Sostituisce parole e frasi da IA. Prima le più lunghe, così le frasi vincono."""
    hits = []
    entries = sorted(lex["phrases"] + lex["words"],
                     key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        pattern = entry_pattern(entry)
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": entry_label(entry),
                     "replace": "" if entry.get("regex") else (entry["replace"] or "(cancellato)"),
                     "count": len(found), "family": entry["family"]})
        if entry.get("regex"):
            text = pattern.sub(lambda m, e=entry: _match_case(m.group(0), m.expand(e["replace"])), text)
        else:
            text = pattern.sub(lambda m, e=entry: _match_case(m.group(0), e["replace"]), text)
    # Pulizia dopo le cancellazioni. Cancellare una proposizione intera lascia
    # punteggiatura orfana ("sistema. ." o una riga che ora inizia con una virgola),
    # e si legge peggio del cliché.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)       # uno spazio lasciato da una cancellazione.
                                                      # Rientri più profondi sono voluti.
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)      # un trattino lungo è diventato virgola,
                                                      # poi la proposizione dopo è sparita
    text = text.replace("...", "\x00ELL\x00")          # proteggi i veri puntini di sospensione
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Un trattino lungo diventato virgola, seguito da un connettivo, lascia uno
    # "splice" ("è utile, poi, è la prova che"). Promuovilo a punto fermo.
    # Insieme limitato apposta: "però"/"comunque" tra virgole sono italiano normale.
    text = re.sub(r",\s*(poi|quindi|alla fine|insomma)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    # Anche l'uniformità della lunghezza delle frasi è strutturale.
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Lunghezza delle frasi uniforme (variazione {cv:.2f})",
                "count": len(lens),
                "fix": "Spezza una frase a metà. Lasciane correre un'altra. Le macchine scrivono pari.",
            })
    return flags


def restore_capitals(original, text):
    """Cancellare un'apertura lascia minuscola la parola dopo.

    Si corregge solo per chi scrive le frasi con la maiuscola: una voce
    volutamente tutta minuscola è uno stile, non un artefatto, e urlarle sopra
    sarebbe esattamente ciò che questo script esiste per evitare.
    """
    starts = re.findall(r"(?:^|[.!?]\s+|\n)\s*(" + LETTER + ")", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(r"(?:^|(?<=[.!?] )|(?<=[.!?]\n)|(?<=\n))\s*(" + LETTER + ")",
                  lambda m: m.group(0)[:-1] + m.group(1).upper(), text)


def humanize(text, lex):
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "structures": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head("RAPPORTO HUMANIZE")
    print(f"{total} artefatti da macchina rimossi, "
          f"{len(report['structures'])} segnali strutturali da riscrivere", file=out)

    if report["invisible"]:
        head("1. CARATTERI INVISIBILI")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFIA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. LESSICO DA IA")
        for h in report["lexical"]:
            arrow = "" if "->" in h["find"] else f"  -> {h['replace']}"
            print(f"  {h['count']:>3}x  {h['find']}{arrow}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. SEGNALI STRUTTURALI  (non corretti in automatico - riscrivili tu)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("PULITO")
        print("  Niente da togliere.", file=out)
    print("", file=out)


def main():
    for _s in (sys.stdout, sys.stderr, sys.stdin):      # Windows: console non UTF-8
        try:
            _s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="Toglie l'impronta da macchina da una bozza.")
    ap.add_argument("input", nargs="?", default="-", help="file, oppure - per stdin")
    ap.add_argument("-o", "--out", help="scrive il testo pulito qui invece che su stdout")
    ap.add_argument("--report", action="store_true", help="stampa cosa è cambiato, su stderr")
    ap.add_argument("--json", action="store_true", help="emette {text, report} in JSON")
    ap.add_argument("--lexicon", default=LEX, help="percorso di slop.json")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"scritto {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
