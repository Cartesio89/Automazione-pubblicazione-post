#!/usr/bin/env python3
"""
hookscore.py - dà un punteggio alla prima riga di un reel su cinque proprietà
che gli hook forti hanno in comune, e mette in classifica un gruppo di hook.

Cos'è:  cinque euristiche locali, calcolate sul tuo computer solo dal testo.
Misurano proprietà che gli hook che tengono l'attenzione tendono ad avere:
una lunghezza che si dice in meno di tre secondi, un elemento concreto,
qualcosa in gioco, il punto forte all'inizio e non alla fine, e uno spettatore
a cui rivolgersi.

Cosa NON è:  un predittore di visualizzazioni.

ATTENZIONE, versione italiana. Lo scorer originale (inglese, di Jake
Schincariol) è stato testato su 74 hook reali: separa un hook vero da uno
scritto apposta male con AUC 0.83, ma separa i successi di un creator dai suoi
flop con AUC 0.56 (0.50 è una moneta). Questa versione italiana ha lessici,
regex e soglie ADATTATI ALL'ITALIANO, ma NON è stata testata su hook italiani
reali: quei numeri non valgono qui. Controlla solo cose che si vedono a occhio:
saluti, preamboli, hook senza niente di concreto, hook troppo lunghi.
Non ti dirà quale di due hook decenti andrà meglio. Fidati del grafico di
retention più che di questo script.

Ogni controllo restituisce da 0 a 100. Più alto è meglio.

Uso
  python3 hookscore.py hooks.txt              # un hook per riga, in classifica
  python3 hookscore.py --hook "Ho perso 18.000 euro per una clausola mancante."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py hooks.txt --json
"""

import argparse
import json
import re
import statistics
import sys

# Velocità di parlato. Parole italiane più lunghe delle inglesi: a parità di
# ritmo, meno parole al minuto. 150 è una STIMA ANALITICA non misurata. Se ti
# cronometri una volta mentre leggi uno script, correggila qui.
PAROLE_AL_SECONDO = 150 / 60.0

LET = "A-Za-zÀ-ÖØ-öø-ÿ"
WORD_RE = re.compile(r"[" + LET + r"0-9$€%'-]+")
NUMBER_RE = re.compile(
    r"[€$]\s?\d[\d.,]*"                                  # denaro, intero
    r"|\b\d[\d.,]*\s?"                                   # una cifra, con o
    r"(?:%|€|k\b|x\b|euro\b|or[ae]\b|min(?:uti|uto)?\b"  # senza unità
    r"|secondi?\b|giorni?\b|settimane?\b|mesi?\b|anni?\b"
    r"|mila\b|milioni?\b)?",
    re.IGNORECASE)
PRICE_RE = re.compile(r"[€$]\s?\d|\d[\d.,]*\s?(?:€|euro)\b", re.IGNORECASE)
PROPER_RE = re.compile(r"(?<!^)\b[A-ZÀ-ÖØ-Þ][a-zà-öø-ÿ]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Gli hook parlati dicono i numeri a voce. "Zero euro" e "ventimila" sono
# concreti quanto "0€" e "20.000", e contare solo le cifre li mancava.
# "uno" e "primo" mancano di proposito: sono riempitivi molto più spesso che
# quantità. "sei" manca perché è anche "tu sei".
SPOKEN_NUMBERS = {
    "zero", "due", "tre", "quattro", "cinque", "sette", "otto", "nove",
    "dieci", "undici", "dodici", "quindici", "venti", "trenta", "quaranta",
    "cinquanta", "sessanta", "settanta", "ottanta", "novanta", "cento",
    "mille", "mila", "milione", "milioni", "miliardo", "miliardi",
    "dozzina", "metà", "doppio", "doppia", "triplo", "tripla",
}
MONEY_WORDS = {
    "euro", "euri", "dollari", "dollaro", "soldi", "centesimi", "percento",
    "milionario", "miliardario", "fatturato", "ricavi", "profitto", "utile",
    "stipendio", "affitto", "mutuo", "bolletta", "prezzo",
}

# Parole che mettono qualcosa in gioco. Un hook senza nessuna di queste è
# un'affermazione; un hook con una è un motivo per continuare a guardare.
STAKES = {
    "stop", "basta", "mai", "sbagliato", "sbagliata", "sbagliati", "sbagliate",
    "sbaglio", "sbagli", "sbagliare", "errore", "errori", "perso", "persa",
    "persi", "perse", "perdere", "perdendo", "perdi", "costato", "costata",
    "costati", "costa", "costano", "costi", "rotto", "rotta", "fallito",
    "fallita", "fallimento", "fallire", "nessuno", "nessuna", "no", "non",
    "né", "smetti", "smettila", "smettere", "mollare", "mollato", "licenziato",
    "licenziata", "cancellato", "cancellata", "cancella", "ucciso", "uccide",
    "sostituito", "sostituita", "sostituisce", "tagliato", "battuto", "gratis",
    "gratuito", "gratuita", "pagato", "pagare", "paghi", "assunto", "assunta",
    "salvato", "vietato", "illegale", "peggior", "peggiore", "peggio", "odio",
    "odiato", "sprecato", "sprecata", "spreco", "truffa", "bugia", "mentito",
    "mente", "verità", "segreto", "nascosto", "nascosta", "rubato", "rubata",
    "prima", "finché", "invece", "ma", "tranne", "problema", "rischio",
    "pericolo", "attenzione", "rimpianto", "dovresti", "dovrei", "ancora",
    "già", "solo", "soltanto", "senza", "contro", "davvero",
}

# Aperture che bruciano il primo secondo senza dire niente.
WEAK_OPENERS = [
    "allora", "ok", "okay", "ehi", "ehilà", "ciao", "salve", "buongiorno",
    "buonasera", "ragazzi", "raga", "ragazze", "bene", "benvenuti",
    "benvenuto", "oggi", "praticamente", "onestamente",
    "senti", "ascolta", "ascoltate", "ehm", "dunque", "insomma", "cioè",
    "vedete", "vediamo", "voglio", "volevo", "vorrei", "una delle",
    "uno dei", "hai mai", "avete mai", "sai", "sapete", "in questo",
    "in questa", "nel video", "nel reel", "la cosa", "molte", "molti",
    "c'è", "ci sono", "questo è", "questa è", "se hai", "se avete", "sai che",
]

# Imperativi che si meritano la prima posizione.
IMPERATIVES = {
    "smetti", "smettila", "smettete", "basta", "stop", "ruba", "rubate",
    "copia", "copiate", "cancella", "prova", "provate", "guarda", "guardate",
    "leggi", "salva", "salvate", "usa", "usate", "costruisci", "fai", "fate",
    "scrivi", "scrivete", "manda", "mandate", "invia", "prendi", "iniziate",
    "inizia", "comincia", "molla", "mai", "sempre", "non", "metti", "controlla",
    "pubblica", "ricorda",
}

SECONDA_PERSONA = re.compile(
    r"\b(?:tu|te|ti|tuo|tua|tuoi|tue|voi|vi|vostro|vostra|vostri|vostre|"
    r"hai|sei|puoi|devi|vuoi|sai|fai|stai|avete|siete|potete|dovete|volete|"
    r"sapete|fate|state)\b", re.IGNORECASE)
PRIMA_PERSONA = re.compile(
    r"\b(?:io|mi|mio|mia|miei|mie|noi|ci|nostro|nostra|nostri|nostre|ho|ero|"
    r"sono|abbiamo|avevo|facevo)\b", re.IGNORECASE)

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:stop scrolling|ferma(?:ti)? (?:lo )?scroll(?:ing)?|"
                r"fermati(?: un (?:attimo|secondo|momento))?\b|non scrollare|"
                r"smetti di scrollare|basta scrollare|aspetta[,.]? non scrollare)"),
     "Apre con \"fermati\" o \"stop scrolling\". Chiedere attenzione dimostra che non te la sei guadagnata."),
    (re.compile(r"(?i)\b(?:in quest[oa] (?:video|reel)|nel (?:video|reel) di oggi|"
                r"oggi (?:ti|vi) (?:mostro|parlo|spiego|racconto|insegno|faccio vedere)|"
                r"(?:ti|vi) (?:mostro|spiego|insegno|faccio vedere) come)\b"),
     "Preambolo da video. Cancellalo e apri con il punto forte."),
    (re.compile(r"(?i)^\s*(?:ehi(?:lì|là)?|ciao|salve|buongiorno|buonasera|buondì|"
                r"ragazzi|raga|benvenut[oiae]|come va|che si dice)\b"),
     "Saluto. Nessuno è venuto nel feed per farsi salutare."),
    (HASHTAG_RE,
     "Hashtag nell'hook. Gli hashtag vanno in fondo alla didascalia, se proprio."),
    (EMOJI_RE,
     "Emoji nell'hook. Il testo a schermo in formato hook ha spazio per parole o per un'emoji, non per entrambe."),
]

CHECKS = ["LUNGHEZZA", "SPECIFICITÀ", "POSTA IN GIOCO", "ANTICIPO", "DESTINATARIO"]


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # "18.000" si pronuncia come una parola sola, quindi è una parola sola.
    text = text.replace("’", "'")
    return WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d)", "", text))


def norm(token):
    """Minuscolo e senza elisione: "l'errore" -> "errore", "c'è" -> "è"."""
    return re.split(r"'", token.lower().strip("'"))[-1]


def check_length(text):
    """Un hook deve arrivare prima che il pollice si muova. Circa due secondi."""
    n = len(words(text))
    secs = n / PAROLE_AL_SECONDO
    chars = len(text.strip())
    # Stima analitica: l'italiano occupa circa il 15% in più dell'inglese per
    # dire la stessa cosa, quindi le soglie sono 13 parole e 70 caratteri
    # invece di 12 e 60.
    if 5 <= n <= 13:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 13) * 11)
    if chars > 70:                       # due righe di testo grande a schermo
        score -= 12
    return clamp(score), f"{n} parole, {chars} caratteri, ~{secs:.1f}s a voce (ideale 5-13 parole)"


def check_specificity(text):
    """Una cosa concreta batte tre astratte."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(PROPER_RE.findall(text))
    # Una parola già contata dentro un numero ("18.000 euro") non si conta due volte.
    resto = NUMBER_RE.sub(" ", text)
    low = [norm(w) for w in words(resto)]
    spoken = [w for w in low if w in SPOKEN_NUMBERS or w in MONEY_WORDS]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} elemento/i concreto/i" + (f": {found}" if found else
                   " - nessun numero, nessun nome, niente di verificabile"))


def check_stakes(text):
    """Tensione, costo, negazione. Qualcosa che lo spettatore può perdere."""
    hits = [norm(x) for x in words(text) if norm(x) in STAKES]
    markers = sorted(set(hits))
    if PRICE_RE.search(text):
        markers.append("un prezzo")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} segnale/i di tensione" + (f": {', '.join(markers[:4])}" if markers else
                                              " - in questa riga non c'è niente in gioco")
    return clamp(score), detail


def check_frontload(text):
    """La parola interessante non può stare in nona posizione."""
    w = words(text)
    if not w:
        return 0.0, "vuoto"
    raw = [x.lower().strip("'") for x in w]
    low = [norm(x) for x in w]
    opener = " ".join(raw[:2])
    penalty = 0
    hit_opener = None
    for weak in WEAK_OPENERS:
        if opener == weak or opener.startswith(weak + " ") or raw[0] == weak:
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or token in SPOKEN_NUMBERS or token in MONEY_WORDS
                or NUMBER_RE.match(w[i]) or (i and PROPER_RE.match(w[i]))):
            payload = i
            break
    if payload is None:
        base = 30.0
        where = "nessuna parola forte in tutta la riga"
    elif payload <= 3:
        base = 100.0
        where = f"punto forte alla parola {payload + 1}"
    elif payload <= 6:
        base = 70.0
        where = f"punto forte alla parola {payload + 1}, si può anticipare"
    else:
        base = 40.0
        where = f"punto forte alla parola {payload + 1}, troppo tardi"
    detail = where + (f"; apertura debole \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text):
    """Rivolto a uno spettatore, o sospeso nell'aria."""
    w = [norm(x) for x in words(text)]
    if SECONDA_PERSONA.search(text):
        return 100.0, "parla allo spettatore"
    if w and w[0] in IMPERATIVES:
        return 90.0, f"apre con un imperativo (\"{w[0]}\")"
    if PRIMA_PERSONA.search(text):
        return 70.0, "prima persona, nessuno spettatore nominato"
    return 35.0, "terza persona, non c'è nessuno nella stanza"


def run(text):
    results = {
        "LUNGHEZZA": check_length(text),
        "SPECIFICITÀ": check_specificity(text),
        "POSTA IN GIOCO": check_stakes(text),
        "ANTICIPO": check_frontload(text),
        "DESTINATARIO": check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # La proprietà più debole mette il tetto all'hook, stessa logica di
    # detect.py: una proprietà brutta basta perché il pollice continui a scorrere.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "FORTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "DEBOLE")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nPUNTEGGIO HOOK", file=out)
    print("=" * 66, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<15} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<15} {detail}", file=out)
    print("-" * 66, file=out)
    print(f"  {'PUNTEGGIO HOOK':<15} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  BLOCCANTE  {f}", file=out)
    if verdict != "FORTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Proprietà più debole: {weakest}. Sistema quella e rilancia.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nCLASSIFICA HOOK\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<7} {hook}", file=out)
        print(f"        più debole: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        bloccante: {f}", file=out)
    print("\nRegistra il primo. Se il primo è sotto 50, nessuno di questi è l'hook.\n",
          file=out)


def main():
    for _s in (sys.stdout, sys.stderr, sys.stdin):      # Windows: console non UTF-8
        try:
            _s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="Dà un punteggio a un hook di reel su cinque proprietà.")
    ap.add_argument("input", nargs="?", default="-", help="file con un hook per riga, oppure -")
    ap.add_argument("--hook", help="valuta un solo hook scritto da riga di comando")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("niente da valutare", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0])
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
