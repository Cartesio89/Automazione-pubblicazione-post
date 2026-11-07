#!/usr/bin/env python3
"""
beats.py - trasforma lo script di un Reel in una scaletta temporizzata prima di registrare
(versione italiana).

Stima quanto ci vuole a dire ogni riga, le impila in timecode e segnala le
quattro cose che uccidono un Reel in montaggio: un hook che supera i tre
secondi, una battuta abbastanza lunga da far andare via chi guarda, una serie di
righe senza niente di concreto, e una durata totale che non corrisponde a
quella che avevi detto di voler fare.

I tempi sono una stima dal numero di parole a un certo ritmo di parole al
minuto. Bastano per pianificare un montaggio, non sostituiscono la registrazione.
Il ritmo predefinito qui è 150 parole al minuto: è una STIMA ANALITICA per
l'italiano (parole più lunghe dell'inglese, quindi meno parole al minuto), NON
una misura. Cronometrati una volta mentre leggi uno script ad alta voce e
imposta il tuo valore con --wpm (e in templates/voice.md).

Uso
  python3 beats.py script.txt
  python3 beats.py script.txt --target 30
  python3 beats.py script.txt --wpm 170 --target 45
  pbpaste | python3 beats.py -
  python3 beats.py script.txt --json
"""

import argparse
import json
import re
import sys

WORD_RE = re.compile(r"[\w$€%'’-]+")
SENT_RE = re.compile(r"(?:[^.!?]|(?<=\d)\.(?=\d))+[.!?]*")
# Concreto = un numero (anche a parole), un importo o un nome proprio a metà frase.
PROPER_RE = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-ZÀ-Þ][a-zà-ÿ]{2,}\b", re.MULTILINE)
NUMBER_RE = re.compile(
    r"[€$]\s?\d|\d[\d.,]*\s?(?:€|euro)\b|\b\d[\d.,]*\b"
    r"|\b(?:zero|due|tre|quattro|cinque|sette|otto|nove|dieci|venti|trenta|cento|mille|mila|milione|milioni)\b",
    re.IGNORECASE)
STOPWORDS = {
    "il", "lo", "la", "i", "gli", "le", "un", "uno", "una", "di", "a", "da", "in",
    "con", "su", "per", "tra", "fra", "e", "ed", "o", "ma", "se", "che", "chi",
    "cui", "non", "è", "sono", "era", "ero", "ho", "hai", "ha", "abbiamo", "hanno",
    "mi", "ti", "ci", "vi", "si", "ne", "li", "io", "tu", "lui", "lei", "noi",
    "voi", "loro", "mio", "mia", "tuo", "tua", "suo", "sua", "del", "dello",
    "della", "dei", "degli", "delle", "al", "allo", "alla", "ai", "agli", "alle",
    "dal", "dallo", "dalla", "dai", "dagli", "dalle", "nel", "nello", "nella",
    "nei", "negli", "nelle", "sul", "sullo", "sulla", "sui", "sugli", "sulle",
    "come", "più", "così", "anche", "poi", "già", "solo", "molto", "tutto",
    "tutti", "tutte", "ogni", "questo", "questa", "quello", "quella", "cosa",
    "sei", "fa", "fai", "può", "puoi", "devi", "deve", "qui", "lì", "ora", "poco",
}

HOOK_WINDOW = 3.0        # secondi. Oltre, il pollice ha già deciso.
MAX_BEAT = 4.0           # secondi su una sola idea senza cambiare cosa c'è a schermo.
ABSTRACT_RUN = 3         # battute di fila senza niente di verificabile.


def words(text):
    # "18.000 euro" e "2,5" si pronunciano come una parola, quindi sono una parola.
    return WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d)", "", text))


def norm(token):
    """Minuscolo e senza elisione: "l'idea" -> "idea"."""
    return re.split(r"['’]", token.lower().strip("'’"))[-1]


def pretty(token):
    """Rimette il separatore delle migliaia, all'italiana, per la visualizzazione."""
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1.", token)


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def concrete_count(text):
    return len(NUMBER_RE.findall(text)) + len(PROPER_RE.findall(text))


def split_beats(raw, wps):
    """Una riga è una battuta, a meno che sia troppo lunga per esserlo."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if len(words(line)) / wps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        # Paragrafo lungo: spezzalo alla fine delle frasi perché i tempi
        # significhino qualcosa, e lascia che il rapporto dica che è stato spezzato.
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and len(words(candidate)) / wps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, wpm=150, target=None):
    wps = wpm / 60.0
    beats = split_beats(raw, wps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = len(words(text))
        dur = n / wps
        rows.append({
            "n": i + 1,
            "start": round(clock, 2),
            "dur": round(dur, 2),
            "words": n,
            "text": text,
            "concrete": concrete_count(text),
            "label": "",
            "flags": [],
        })
        clock += dur
    total = clock

    # Etichetta le posizioni strutturali attorno a cui è costruito un Reel.
    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "HOOK"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "HOOK" else "HOOK/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "META"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"l'hook dura {rows[0]['dur']:.1f}s, oltre il limite di {HOOK_WINDOW:.0f}s")
        notes.append(f"La battuta 1 richiede {rows[0]['dur']:.1f}s per essere detta. Portala a "
                     f"{int(HOOK_WINDOW * wps)} parole o meno, o l'hook arriva a decisione già presa.")
    if rows[0]["concrete"] == 0:
        notes.append("La battuta 1 non ha né un numero né un nome. Gli hook senza niente di "
                     "verificabile sono quelli che vengono scorsi.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f}s su una sola battuta")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"La/le battuta/e {', '.join(map(str, long_beats))} superano {MAX_BEAT:.0f}s. "
                     "Spezza la riga oppure cambia cosa c'è a schermo al suo interno. "
                     "Un'inquadratura ferma è dove la gente se ne va.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Le battute {start}-{r['n']} non hanno niente di concreto. "
                             "Metti un numero, un nome o un prezzo in una di loro.")
        else:
            run, start = 0, None

    # L'ultima riga ti riporta alla prima?
    first = {norm(w) for w in words(rows[0]["text"]) if norm(w) not in STOPWORDS}
    last = {norm(w) for w in words(rows[-1]["text"]) if norm(w) not in STOPWORDS}
    loop = sorted(pretty(w) for w in first & last)
    if loop:
        notes.append(f"Loop: l'ultima battuta ripete \"{', '.join(loop[:3])}\" dall'hook. "
                     "Le seconde visualizzazioni sono portata gratis.")
    else:
        notes.append("Nessun loop. L'ultima battuta non condivide nessuna parola con l'hook, "
                     "quindi il video finisce piatto. Riprendere una parola della battuta 1 "
                     "è il modo più economico per ottenere una rivisione.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"La durata è in linea ({total:.1f}s contro {target}s).")
        elif delta > 0:
            notes.append(f"{delta:.1f}s sopra l'obiettivo. Taglia circa {int(delta * wps)} parole.")
        else:
            notes.append(f"{-delta:.1f}s sotto l'obiettivo. Aggiungi {int(-delta * wps)} parole "
                         "oppure gira corto. Corto di solito è giusto.")

    return {
        "wpm": wpm, "target": target,
        "total_seconds": round(total, 2),
        "total_words": sum(r["words"] for r in rows),
        "beats": rows,
        "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"SCALETTA  ·  {a['total_words']} parole  ·  ~{a['total_seconds']:.1f}s "
            f"a {a['wpm']:g} parole/min" + (f"  ·  obiettivo {a['target']}s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<8}" if r["label"] else " " * 8
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<8}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    for _s in (sys.stdout, sys.stderr, sys.stdin):      # Windows: console non UTF-8
        try:
            _s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="Trasforma lo script di un Reel in una scaletta temporizzata.")
    ap.add_argument("input", nargs="?", default="-", help="file dello script, oppure - per stdin")
    ap.add_argument("--wpm", type=float, default=150,
                    help="ritmo di parlato in parole al minuto (default 150, stima non misurata)")
    ap.add_argument("--target", type=float, help="durata obiettivo in secondi")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, wpm=args.wpm, target=args.target)
    if not a:
        print("script vuoto", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
