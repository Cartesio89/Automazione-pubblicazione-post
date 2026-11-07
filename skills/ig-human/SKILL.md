---
name: ig-human
description: >-
  Toglie l'impronta da macchina da qualsiasi bozza in italiano (trattini lunghi,
  parole e cliché da IA, caratteri invisibili da filigrana) e la valuta con un
  pannello di cinque controlli prima di pubblicarla. Usala quando un testo deve
  suonare umano, quando l'utente dice "umanizza", "suona come scritto dall'IA?",
  "togli i trattini lunghi", "sa di ChatGPT", "ripulisci questo testo", o prima di
  mostrare all'utente qualsiasi didascalia, script, commento, risposta o DM.
---

# ig-human

In questa cartella ci sono due strumenti e funzionano davvero. Usali. Non
valutare a occhio.

```bash
python3 humanize.py bozza.txt --report         # lo ripulisce, mostra cosa è cambiato
python3 detect.py bozza.txt                    # gli dà un punteggio, cinque controlli
python3 detect.py prima.txt dopo.txt           # dimostra la differenza
```

(Su Windows, se `python3` non esiste, usa `python` oppure `py`.)

Entrambi leggono `slop.json`: 207 voci di lessico da IA (108 parole e 99 frasi)
con sostituzioni in italiano normale, 18 classi di caratteri invisibili, 11
sostituzioni tipografiche e 18 segnali strutturali. Si può modificare: se
l'utente ha una parola che usa sempre e che il lessico gli toglie, cancellala dal
file. Le voci con `"regex": true` conservano la desinenza (così "sfruttiamo"
diventa "usiamo", non "usare").

**Onestà sul lessico italiano.** È scritto da zero sui cliché tipici dei testi
italiani generati da IA e sui calchi dall'inglese ("al fine di", "in continua
evoluzione", "un vero e proprio game changer"), ma NON è stato calibrato su
testi italiani reali né confrontato con rilevatori reali. Le sostituzioni sono
scelte per non rompere genere e numero, però rileggi sempre il risultato. Le
soglie di `detect.py` sono stime analitiche adattate dall'inglese: usalo per
confrontare due versioni della stessa bozza, non come numero assoluto.

## Perché su Instagram conta più di quanto sembri

Le didascalie sono corte e gli script si dicono a voce alta. Una riga che suona
scritta in una didascalia di 600 caratteri pesa di più della stessa riga in un
saggio, e una voce fuori campo che nessuno potrebbe dire in modo naturale si nota
al primo ciak. Il rischio qui non è un rilevatore che segnala il post. Il rischio
è una persona che scorre oltre qualcosa che sembra un brand, o un creator che
inciampa nel proprio script.

## Cosa viene corretto in automatico

**1. Caratteri invisibili.** Spazi e giunzioni a larghezza zero, word joiner,
trattini soffici, byte-order mark, caratteri tag Unicode, separatori invisibili,
spazi non separabili e stretti. Una tastiera non li produce. Sopravvivono al
copia-incolla, sono invisibili in ogni editor e sono la cosa più meccanica nel
testo generato. `humanize.py` li cancella tutti, compreso ogni altro carattere di
formato Unicode a cui non ha dato un nome.

**2. Tipografia.** Trattino lungo in virgola, trattino medio in trattino,
virgolette ricurve in dritte, puntini di sospensione in tre punti, pallino in
trattino. Le caporali « » non si toccano. Il passaggio sul trattino lungo è quello
che conta: lo trasforma in virgola e poi ripulisce la doppia punteggiatura e i
punti orfani che lascia.

**3. Il lessico da IA.** "approfondire", "sfruttare", "fondamentale",
"imprescindibile", "innovativo", "in un mondo frenetico", "al fine di", "un vero
game changer", più il blocco per Instagram: "fermati un attimo", "nel video di
oggi", "segui per altri contenuti", "tagga qualcuno che ne ha bisogno",
"battere l'algoritmo". Ognuno sostituito con una parola normale o cancellato,
rispettando le maiuscole e lasciando intatti gli URL.

## Cosa NON viene corretto in automatico

I segnali strutturali vengono **segnalati, non riscritti**, perché cambiare la
forma di una frase richiede giudizio:

- "Non è solo X, è Y" e "non solo X ma anche Y"
- "Non si tratta di X, si tratta di Y"
- Triadi "X, Y e Z"
- Righe retoriche di una parola: "Il risultato?"
- Il preambolo da video: "in questo video ti mostro"
- Elenchi puntati con emoji
- Tre o più parole in maiuscolo di fila
- Muri di hashtag
- Esche da riflesso: "segui per altri contenuti", "tagga qualcuno che", "doppio tap se"
- "Sblocca il tuo potenziale" e "livello successivo"
- Aggettivi da brochure: "all'avanguardia", "a 360 gradi", "mozzafiato", "imperdibile"

Quell'elenco è compito tuo. Riscrivi a mano ogni riga segnalata, mantenendo il
significato, poi rilancia `detect.py`. È la parte che porta il punteggio da DA
RIVEDERE a PASSA, ed è la parte che uno script non sa fare.

## I cinque controlli

`detect.py` valuta cinque segnali da 0 a 100, più alto è più umano:

| controllo | cosa misura | com'è la macchina |
| --- | --- | --- |
| VARIAZIONE | variazione della lunghezza delle frasi | tutte le frasi lunghe uguale |
| SPECIFICITÀ | numeri, nomi, marcatori concreti ogni 100 parole | nomi astratti, nessuna cifra |
| DENSITÀ SLOP | voci del lessico ogni 100 parole | vocabolario da stock |
| IMPRONTA | invisibili, trattini lunghi, virgolette ricurve ogni 1.000 caratteri | tipograficamente perfetto |
| VOCE | marcatori di parlato, persona, segnali strutturali | niente parlato, rivelazioni messe in scena |

Il verdetto pesa la media al 60% e il **singolo controllo più debole** al 40%,
perché un solo segnale basta. PASSA richiede un totale di 70+ senza nessun
controllo sotto 55.

Nota sull'italiano: le elisioni (l'idea, dell'anno) sono normali a ogni registro e
non contano come segnale umano; l'apostrofo ricurvo non conta come impronta
perché lo produce la correzione automatica del telefono; il soggetto spesso non
si esprime, quindi nella VOCE si contano anche i pronomi deboli (mi, ti, ci, vi).

## Dillo con onestà

Sono cinque euristiche locali modellate sui segnali su cui puntano i rilevatori
pubblici. Girano interamente sul computer dell'utente e non viene caricato niente.
**Non** sono GPTZero, Originality, Copyleaks, Winston o Turnitin, non chiamano
quelle API e non possono promettere quei verdetti. Correggere ciò che misurano
tende a spostare anche quei numeri, perché misurano le stesse cose di fondo. Quella
è l'affermazione. Non farne una più grande a nome dell'utente e non dire mai a un
utente che il suo testo è non rilevabile.

## Ordine delle operazioni

1. `humanize.py bozza.txt -o pulito.txt --report`
2. Leggi le segnalazioni strutturali. Riscrivi tu quelle righe.
3. `detect.py bozza.txt pulito.txt` per mostrare prima e dopo.
4. Se il verdetto non è PASSA, correggi il controllo più debole indicato
   nell'output e ricomincia. Due giri sono normali. Cinque vogliono dire che la
   bozza è scritta a formula, e la soluzione è un'altra bozza, non altri passaggi.
5. Mostra all'utente il testo ripulito e il punteggio. Mai il punteggio da solo.
