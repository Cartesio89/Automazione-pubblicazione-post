#!/usr/bin/env python3
"""
caption.py - controlla una didascalia di Instagram e mostra esattamente cosa
mostra il feed prima di "... altro" (versione italiana).

Instagram dà a una didascalia circa 125 caratteri nel feed e nasconde il resto
dietro un tocco. Quasi tutte le didascalie che falliscono falliscono lì: l'hook
è nella terza frase, o la prima riga è un saluto, o tutto inizia con un hashtag.
Questo script stampa la finestra visibile dentro un riquadro, così la leggi come
la legge uno sconosciuto che scorre, poi controlla le nove cose che valgono un
controllo.

Il taglio a 125 caratteri è un'approssimazione. Il numero reale cambia con il
dispositivo, la dimensione del carattere e dove cadono gli a capo: per questo
conviene lasciare un margine invece di una didascalia ingegnerizzata per finire
a 125. Cambialo con --truncate per provarne uno più stretto.

Uso
  python3 caption.py didascalia.txt
  python3 caption.py didascalia.txt --keywords "software preventivi,contratto cliente"
  pbpaste | python3 caption.py -
  python3 caption.py didascalia.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

LIMIT = 2200             # Limite massimo di una didascalia su Instagram.
TRUNCATE = 125           # Circa dove il feed taglia con "... altro".
HASHTAG_LIMIT = 5        # Tetto di Instagram per post o reel dal 18 dicembre 2025
                         # (prima era 30). Annunciato dall'account @Creators:
                         # usare meno hashtag (fino a 5) e più mirati, invece di
                         # tanti generici, può migliorare sia i risultati del
                         # contenuto sia l'esperienza delle persone.

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[\w.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|co|io|net|org|ai|app|it|eu)/\S*",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
# Concreto = un importo, un numero o un nome proprio a metà frase. In italiano
# mesi, giorni e lingue sono minuscoli, quindi una maiuscola interna è quasi
# sempre un nome vero.
CONCRETE_RE = re.compile(
    r"[€$]\s?\d|\d[\d.,]*\s?(?:€|euro)\b|\b\d[\d.,]*\b"
    r"|(?<![.!?]\s)(?<!^)\b[A-ZÀ-Þ][a-zà-ÿ]{2,}\b", re.MULTILINE)

ASKS = [
    (re.compile(r"\b[Cc]omment(?:a|ami|aci) (?:la parola |con la parola |\")?\"?[A-ZÀ-Þ0-9]{2,}\b"), "commenta una parola chiave"),
    (re.compile(r"(?i)\b(?:scrivimi|scrivici|mandami|mandaci)\b[^.\n]{0,15}\b(?:dm|direct|privato|messaggio)\b|\b(?:in|via) (?:dm|direct)\b"), "scrivimi in DM"),
    (re.compile(r"(?i)\bsalva(?:lo|la|telo|tela)\b|\bsalva (?:questo|questa|il post|il reel|per dopo)\b"), "salva"),
    (re.compile(r"(?i)\bcondivid(?:i|ete)(?:lo|la)?\b|\bmanda(?:lo|la|telo|tela) a\b|\binoltra(?:lo|la)?\b"), "condividi"),
    (re.compile(r"(?i)\bsegui(?:mi|ci)\b|\bsegui per\b|\bsegui (?:il|questo) (?:profilo|account)\b"), "segui"),
    (re.compile(r"(?i)\blink (?:in|nella) bio(?:grafia)?\b|\blink nel profilo\b|\bin bio\b"), "link in bio"),
    (re.compile(r"(?i)\bscorri\b|\bscorrete\b|\btocca (?:per|qui)\b"), "scorri o tocca"),
    (re.compile(r"(?i)\bdimmi\b|\bscrivimi (?:cosa|quale|come)\b|\bquale (?:preferisci|sceglieresti)\b|\bcosa (?:faresti|ne pensi)\b|\bche ne pensi\b|\bqual è (?:la tua|il tuo)\b"), "rispondi a una domanda"),
]

FILLER_TAGS = {"#viral", "#fyp", "#explore", "#explorepage", "#foryou", "#foryoupage",
               "#trending", "#instagood", "#love", "#follow", "#like4like", "#reels",
               "#reelsinstagram", "#viralreels", "#instadaily", "#perte", "#neiperte",
               "#reel", "#reelitalia", "#instagram", "#instaitalia", "#virale"}


def visible_window(text, cut):
    """Cosa mostra il feed. Instagram taglia a metà parola, quindi anche questo."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  COSA MOSTRA IL FEED", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... altro" if truncated else "(la didascalia sta tutta)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    text = text.rstrip()
    stripped = text.strip()
    chars = len(stripped)
    lines = [l for l in stripped.split("\n")]
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LUNGHEZZA", "FAIL" if chars > LIMIT else "PASS",
        f"{chars} / {LIMIT} caratteri" + (f", {chars - LIMIT} oltre il limite"
                                          if chars > LIMIT else ""))

    if not first_line:
        add("PRIMA RIGA", "FAIL", "la didascalia inizia con una riga vuota")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("PRIMA RIGA", "FAIL",
            "inizia con un hashtag o una menzione, cioè l'unica posizione che vale una frase")
    elif len(first_line) > cut:
        add("PRIMA RIGA", "WARN",
            f"{len(first_line)} caratteri, quindi viene tagliata a {cut} a metà pensiero. "
            "Va bene se il taglio è un cliffhanger, male se è una subordinata")
    else:
        add("PRIMA RIGA", "PASS", f"{len(first_line)} caratteri, arriva intera")

    add("HOOK CONCRETO", "PASS" if CONCRETE_RE.search(window) else "WARN",
        f"{len(CONCRETE_RE.findall(window))} numero/i o nome/i nella finestra visibile"
        + ("" if CONCRETE_RE.search(window) else " - niente di verificabile prima del tocco"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAG", "FAIL", f"{len(tags)} hashtag, sopra il tetto di Instagram di {HASHTAG_LIMIT}. "
                               "Quelli dopo il quinto non contano e il blocco sa di vecchio")
    elif len(tags) == HASHTAG_LIMIT and filler:
        add("HASHTAG", "WARN", f"{len(tags)} hashtag, al tetto, e "
                               f"{len(filler)} generici. Spendi i cinque su argomenti")
    elif filler:
        add("HASHTAG", "WARN", f"{len(tags)} hashtag, {len(filler)} generici "
                               f"({', '.join(filler[:3])}). Non descrivono niente")
    else:
        add("HASHTAG", "PASS", f"{len(tags)} hashtag" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("POSIZIONE HASHTAG", "PASS", "nessun hashtag da posizionare")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"(?!\w)", window) for t in tags):
        add("POSIZIONE HASHTAG", "WARN", "un hashtag sta dentro la finestra visibile, "
                                         "e spreca spazio del feed su un'etichetta")
    else:
        add("POSIZIONE HASHTAG", "PASS", "gli hashtag stanno sotto il taglio")

    add("LINK", "WARN" if links else "PASS",
        f"{len(links)} link nella didascalia, e le didascalie non sono cliccabili. "
        f"Spostalo in bio o in DM" if links else "nessun link morto nel corpo")

    if len(asks) == 1:
        add("UNA RICHIESTA", "PASS", f"una sola call to action: {asks[0]}")
    elif not asks:
        add("UNA RICHIESTA", "WARN", "nessuna call to action. Decidi a cosa serve questo post")
    else:
        add("UNA RICHIESTA", "WARN", f"{len(asks)} richieste ({', '.join(asks)}). "
                                     "Due richieste equivalgono a nessuna")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJI", "WARN" if density > 4 else "PASS",
        f"{len(emoji)} emoji, {density:.1f} ogni 100 caratteri"
        + (" - sembra decorazione" if density > 4 else ""))

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        in_window = [k for k in found if k.lower() in window.lower()]
        status = "PASS" if not missing else ("WARN" if found else "FAIL")
        add("TERMINI DI RICERCA", status,
            f"{len(found)}/{len(keywords)} presenti"
            + (f", {len(in_window)} nella finestra visibile" if found else "")
            + (f". Mancano: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "FAIL")
    warns = sum(1 for c in checks if c["status"] == "WARN")
    verdict = "DA CORREGGERE" if fails else ("DA RIVEDERE" if warns else "PRONTA")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"CONTROLLO DIDASCALIA  ·  {a['characters']} / {a['limit']} car.  ·  "
            f"{len(a['hashtags'])} hashtag  ·  {len(a['asks'])} richiesta/e")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<5} {c['check']:<19} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VERDETTO  {a['verdict']}\n", file=out)


def main():
    for _s in (sys.stdout, sys.stderr, sys.stdin):      # Windows: console non UTF-8
        try:
            _s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="Controlla una didascalia di Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="file della didascalia, oppure - per stdin")
    ap.add_argument("--truncate", type=int, default=TRUNCATE,
                    help=f"caratteri mostrati prima di '... altro' (default {TRUNCATE})")
    ap.add_argument("--keywords", default="", help="termini, separati da virgola, per cui vuoi essere trovato")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "PRONTA" else 1)


if __name__ == "__main__":
    main()
