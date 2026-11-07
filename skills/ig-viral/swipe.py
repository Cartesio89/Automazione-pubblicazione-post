#!/usr/bin/env python3
"""
swipe.py - mette in classifica i reel che hai raccolto in base a quanto hanno
battuto il loro stesso account, dà un nome alla formula di hook di ciascuno e
scrive lo swipe file (versione italiana).

Lo scopo di questo script è una sola correzione: le visualizzazioni grezze non
sono una prova. Un account da 2.000.000 di follower che fa 400.000 view ha avuto
una giornata tranquilla. Un account da 4.000 follower che fa 400.000 view ha
trovato qualcosa. Questo ordina per il multiplo rispetto alla base dell'account
stesso, che è l'unica versione di "è diventato virale" che dice qualcosa che si
può copiare.

L'input è un file separato da tabulazioni che compili mentre navighi, un reel per
riga, con una riga di intestazione che nomina le colonne:

    account   follower   mediana   views    hook
    @qualcuno 48000      11000     412000   nessuno ti dice che i primi 30 reel floppano

Le intestazioni inglesi (followers, median, views) vanno bene lo stesso.
`mediana` sono le view tipiche recenti di quell'account ed è la base migliore. Se
hai solo i `follower`, lascia fuori la mediana e lo script lo dichiara.
`hook` è la prima riga del reel, parlata o a schermo, con le loro parole.

ATTENZIONE: il punteggio dell'hook e il nome della formula usano regex adattate
all'italiano e NON testate su hook italiani reali. I reel che non rientrano in
nessuna formula finiscono in "non classificato": leggili a mano.

Uso
  python3 swipe.py raccolti.tsv
  python3 swipe.py raccolti.tsv --out ~/.claude/instagram/swipe.md
  python3 swipe.py raccolti.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "ig-reel", "hooks.json")
WORD_RE = re.compile(r"[\w$€%'’-]+")
ALIASES = {"followers": "followers", "follower": "followers", "seguaci": "followers",
           "median": "median", "mediana": "median",
           "views": "views", "view": "views", "visualizzazioni": "views",
           "account": "account", "profilo": "account", "hook": "hook"}

try:                                              # facoltativo: dà un punteggio anche agli hook
    sys.path.insert(0, os.path.join(HERE, "..", "ig-reel"))
    from hookscore import run as score_hook       # noqa: E402
except Exception:                                 # ig-viral copiato da solo
    score_hook = None


def fmt(n):
    """Numero con il punto come separatore delle migliaia."""
    return f"{n:,}".replace(",", ".")


def load_formulas(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("classify_order") or sorted(by_id)
    return [(by_id[i]["id"], by_id[i]["name"],
             re.compile(by_id[i]["match"], re.IGNORECASE)) for i in order if i in by_id]


def classify(hook, formulas):
    if not formulas:
        return None, "non classificato"
    hook = hook.replace("’", "'")
    for fid, name, pattern in formulas:
        if pattern.search(hook):
            return fid, name
    return None, "non classificato"


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    head = [ALIASES.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "followers", "views", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        if len(cells) < len(cols):
            cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        try:
            r["views"] = int(re.sub(r"[^\d]", "", r.get("views", "")) or 0)
        except ValueError:
            continue
        for k in ("followers", "median"):
            digits = re.sub(r"[^\d]", "", r.get(k, "") or "")
            r[k] = int(digits) if digits else None
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def analyse(rows, formulas):
    used_median = any(r.get("median") for r in rows)
    for r in rows:
        base = r.get("median") or r.get("followers") or 0
        r["baseline"] = base
        r["outlier"] = round(r["views"] / base, 2) if base else None
        r["formula_id"], r["formula"] = classify(r["hook"], formulas)
        r["words"] = len(WORD_RE.findall(r["hook"]))
        if score_hook:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    counts = {}
    for r in top:
        counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    return {
        "baseline": "mediana dell'account" if used_median else "numero di follower",
        "n": len(ranked),
        "accounts": len({r.get("account", "") for r in ranked}),
        "reels": ranked,
        "top_formulas": sorted(counts.items(), key=lambda kv: -kv[1]),
        "top_hook_score": med(top, "hook_score"),
        "bottom_hook_score": med(bottom, "hook_score"),
        "top_words": med(top, "words"),
        "bottom_words": med(bottom, "words"),
        "unclassified": sum(1 for r in ranked if r["formula"] == "non classificato"),
    }


def render(a, out=sys.stdout):
    head = (f"SWIPE FILE  ·  {a['n']} reel  ·  {a['accounts']} account  ·  "
            f"base: {a['baseline']}")
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "   ?"
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        print(f"  {mult:>7}  hook {score:>3}  {fid} {r['formula'][:26]:<26} "
              f"{r.get('account', '')[:16]:<16} {fmt(r['views']):>9}", file=out)
        print(f"           \"{r['hook'][:96]}\"", file=out)
    print("-" * max(len(head), 78), file=out)
    print("COSA FUNZIONA IN QUESTO GRUPPO", file=out)
    if a["top_formulas"]:
        print("  terzo migliore per multiplo:  "
              + ", ".join(f"{n} x{c}" for n, c in a["top_formulas"][:4]), file=out)
    if a["top_hook_score"] is not None:
        print(f"  punteggio hook mediano:       migliori {a['top_hook_score']:.0f}  "
              f"contro peggiori {a['bottom_hook_score']:.0f}", file=out)
    print(f"  lunghezza hook mediana:       migliori {a['top_words']} parole  "
          f"contro peggiori {a['bottom_words']} parole", file=out)
    print(f"  non classificati:             {a['unclassified']} su {a['n']}. Leggili a mano, "
          "è lì che si nasconde una formula che non hai ancora.", file=out)
    print("\n  Un gruppo raccolto a mano è un indizio, non una prova. Dodici reel non ti\n"
          "  mostrano niente; quaranta su sei account ti mostrano qualcosa. Raccoglierne\n"
          "  di più prima di crederci.\n", file=out)


def to_markdown(a):
    lines = ["# Swipe file", "",
             f"{a['n']} reel su {a['accounts']} account. "
             f"Ordinati per multiplo rispetto a: {a['baseline']}.", ""]
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "?"
        lines += [f"## {mult}  {r['formula']}  ({r.get('account', '')})",
                  f"- views: {fmt(r['views'])}  base: {fmt(r['baseline'])}",
                  f"- punteggio hook: {r['hook_score']}  parole: {r['words']}",
                  f"- hook: \"{r['hook']}\"", ""]
    return "\n".join(lines) + "\n"


def main():
    for _s in (sys.stdout, sys.stderr, sys.stdin):      # Windows: console non UTF-8
        try:
            _s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="Ordina i reel raccolti per multiplo rispetto alla base.")
    ap.add_argument("input", nargs="?", default="-", help="file TSV, oppure - per stdin")
    ap.add_argument("--hooks", default=HOOKS, help="percorso di ig-reel/hooks.json")
    ap.add_argument("--out", help="scrive anche lo swipe file in markdown qui")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("nessuna riga utilizzabile. Serve un file separato da tabulazioni con almeno views e hook.",
              file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.hooks)
    a = analyse(rows, formulas)
    if not formulas:
        print("nota: hooks.json non trovato, formule senza nome. Passa --hooks.", file=sys.stderr)
    if score_hook is None:
        print("nota: hookscore.py non importabile, punteggi hook saltati.", file=sys.stderr)

    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.out:
        path = os.path.expanduser(args.out)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_markdown(a))
        print(f"scritto {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
