#!/usr/bin/env python3
"""
detect.py - pannello di cinque controlli che stima quanto una bozza sembri
scritta da una macchina (versione italiana).

Cos'è:  cinque euristiche locali modellate sui segnali che i rilevatori
pubblici misurano davvero: variazione della lunghezza delle frasi, concretezza,
vocabolario da stock, impronta tipografica e voce. Ogni punteggio è calcolato
sul tuo computer, solo dal testo. Non viene caricato niente.

Cosa NON è:  GPTZero, Originality, Copyleaks, Winston o Turnitin. Non chiama le
loro API e non può promettere il loro verdetto. Intercetta le cose su cui si
basano tutti, ed è per questo che correggerle tende a spostare anche i loro
numeri, ma l'unica affermazione onesta è quella di questa riga.

ATTENZIONE, versione italiana: soglie e lessici sono STIME ANALITICHE adattate
dall'originale inglese, NON calibrate su testi italiani reali. Usa il punteggio
per confrontare due versioni della stessa bozza (modalità confronto), non come
numero assoluto.

Ogni controllo restituisce un punteggio UMANO da 0 a 100. Più alto è meglio.

Uso
  python3 detect.py bozza.txt
  pbpaste | python3 detect.py -
  python3 detect.py bozza.txt --json
  python3 detect.py prima.txt dopo.txt      # confronta due bozze
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

# Il punto tra due cifre ("18.000") non chiude una frase.
SENT_RE = re.compile(r"(?:[^.!?\n]|(?<=\d)\.(?=\d))+[.!?]*")
WORD_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*")

# In italiano le elisioni (l'idea, dell'anno, c'è) sono normali a ogni registro:
# non sono un segnale di scrittura umana come le contrazioni inglesi. Il
# sostituto usato qui sono i marcatori di parlato, che un testo da modello
# raramente contiene. Stima non calibrata.
COLLOQUIALI = re.compile(
    r"\b(?:cioè|boh|tipo|mica|magari|insomma|vabbè|vabbe|dai|figurati|"
    r"diciamo|ecco|beh|mah|uff|ahah|ahaha|macché|mannaggia|accidenti|"
    r"sinceramente|onestamente|un po'|po')\b", re.IGNORECASE)
# L'italiano non esprime sempre il soggetto: la persona sta nel verbo. Per questo
# si contano anche i pronomi deboli (mi, ti, ci, vi) e i possessivi.
PRONOMI = re.compile(
    r"\b(?:io|me|mi|mio|mia|miei|mie|noi|ci|nostro|nostra|nostri|nostre|"
    r"tu|te|ti|tuo|tua|tuoi|tue|voi|vi|vostro|vostra|vostri|vostre)\b", re.IGNORECASE)
NUMERI = re.compile(r"\b\d[\d.,]*%?|[€$]\s?\d")
# In italiano mesi, giorni e lingue sono minuscoli: una maiuscola a metà frase è
# quasi sempre un nome proprio, quindi il segnale è più affidabile che in inglese.
PROPRI = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-ZÀ-Þ][a-zà-ÿ]{2,}\b", re.MULTILINE)


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Mappa value su 0-100 dove `human` -> 100 e `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def entry_pattern(entry):
    if entry.get("regex"):
        body = entry["find"]
    else:
        body = re.escape(entry["find"]).replace(r"\ ", r"\s+")
    tail = "" if body.endswith("'") else r"(?!\w)"
    return re.compile(r"(?<!\w)(?:" + body + r")" + tail, re.IGNORECASE)


def check_burstiness(text):
    """Gli umani variano molto la lunghezza delle frasi. I modelli scrivono pari."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "troppo corto per giudicare"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variazione {cv:.2f} su {len(lens)} frasi (vorresti 0.55+)"


def check_specificity(text):
    """Numeri, nomi e sostantivi concreti. Lo slop è astratto."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "troppo corto per giudicare"
    per100 = 100 / len(w)
    hits = len(NUMERI.findall(text)) + len(set(PROPRI.findall(text)))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} marcatori concreti, {density:.1f} ogni 100 parole (vorresti 4+)"


def check_slop(text, lex):
    """Densità di vocabolario da stock rispetto al lessico."""
    text = text.replace("’", "'")
    w = words(text)
    if not w:
        return 50.0, "vuoto"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        n = len(entry_pattern(entry).findall(text))
        if n:
            hits += n
            found.append((entry.get("label") or entry["find"]).split(" ->")[0])
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} termini da stock, {density:.1f} ogni 100 parole"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Caratteri che una tastiera da telefono non produce.

    L'apostrofo ricurvo (') e le virgolette singole NON si contano: in italiano
    l'apostrofo è ovunque e la correzione automatica del telefono lo rende
    ricurvo, quindi sarebbe un falso positivo su qualsiasi testo scritto a mano.
    """
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "“”")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisibili, {em} trattini lunghi, {curly} virgolette ricurve, "
              f"{ellip} puntini ricurvi, {nbsp} spazi rigidi")
    return score, detail


def check_voice(text, lex):
    """Parlato, persona e le forme che i modelli usano di default."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "troppo corto per giudicare"
    per100 = 100 / len(w)
    colloquial = len(COLLOQUIALI.findall(text)) * per100
    person = len(PRONOMI.findall(text)) * per100
    tells = 0
    names = []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(colloquial, human=1.5, machine=0.0) * 0.35
             + scale(person, human=8.0, machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("elenco-uniforme")
    detail = (f"{colloquial:.1f} marcatori di parlato, {person:.1f} pronomi personali "
              f"ogni 100 parole, {tells} segnale/i strutturale/i")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["VARIAZIONE", "SPECIFICITÀ", "DENSITÀ SLOP", "IMPRONTA", "VOCE"]


def run(text, lex):
    results = {}
    results["VARIAZIONE"] = check_burstiness(text)
    results["SPECIFICITÀ"] = check_specificity(text)
    results["DENSITÀ SLOP"] = check_slop(text, lex)
    results["IMPRONTA"] = check_fingerprint(text)
    results["VOCE"] = check_voice(text, lex)
    scores = [results[c][0] for c in CHECKS]
    # Il controllo più debole trascina il verdetto: a un rilevatore basta un segnale.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASSA" if overall >= 70 and min(scores) >= 55 else (
        "DA RIVEDERE" if overall >= 50 else "SEGNALATO")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PANNELLO RILEVAMENTO IA" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 66), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 66, file=out)
    print(f"  {'PUNTEGGIO':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "PASSA":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Segnale più debole: {weakest}. Sistema quello per primo.", file=out)
    print("", file=out)


def main():
    for _s in (sys.stdout, sys.stderr, sys.stdin):      # Windows: console non UTF-8
        try:
            _s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="Stima quanto una bozza sembri scritta da una macchina.")
    ap.add_argument("input", nargs="?", default="-", help="file, oppure - per stdin")
    ap.add_argument("compare", nargs="?", help="secondo file, per vedere prima/dopo")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "PASSA" else 1)


if __name__ == "__main__":
    main()
