# Instagram agent skill, versione italiana

Tredici skill di Claude che aiutano a gestire un account Instagram **in italiano**.
Gratis, licenza MIT, nessuna iscrizione, nessuna chiave API, niente da collegare.

> **Adattamento italiano non ufficiale** di
> [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)
> di Jake Schincariol (MIT). Le skill, gli script, i lessici, le 26 formule di hook e
> gli esempi sono stati riscritti per l'italiano, non tradotti parola per parola.
> Il credito dell'idea e della struttura è dell'autore originale.

Una scrive i tuoi Reel su 26 formule di hook e dà un punteggio all'hook prima che
tu sprechi un ciak. Una cerca i reel che funzionano davvero nella tua nicchia e li
ordina per quanto ciascuno ha battuto il proprio account. Una scrive la
didascalia e ti mostra esattamente cosa vede il feed prima di "... altro". Una dà un
punteggio su 100 al tuo profilo e riscrive ciò che perde punti. Una pianifica la
settimana.

E una è l'umanizzatore, il motivo per cui le altre sono utilizzabili: toglie da una
bozza i trattini lunghi, i cliché da testo generato e i caratteri invisibili da
filigrana, poi valuta ciò che resta con un pannello di cinque controlli.

**Non viene pubblicato niente finché non dici sì.** Queste skill scrivono. Pubblichi tu.

## Cosa è cambiato rispetto all'originale

| area | originale (inglese) | questa versione |
| --- | --- | --- |
| skill (13 `SKILL.md`) | inglese | riscritte in italiano, con trigger italiani nella descrizione |
| `hookscore.py` | lessici inglesi, `$`, soglie in parole inglesi | lessici italiani, `€`, numeri a parole ("ventimila"), 5-13 parole ideali invece di 5-12 |
| `hooks.json` | 26 formule + regex inglesi | 26 formule con esempi e regex italiani (tu/voi, "nessuno ti dice", "mi è costato"...) |
| `slop.json` | 154 voci inglesi | 207 voci italiane (108 parole, 99 frasi) + 18 segnali strutturali; le voci "regex" conservano la desinenza |
| `humanize.py` | regex ASCII | regex Unicode (accenti), "18.000" non chiude la frase, pulizia delle virgole adattata |
| `detect.py` | contrazioni inglesi | marcatori di parlato italiani; l'apostrofo ricurvo NON conta come impronta (in italiano è ovunque) |
| `caption.py` | CTA inglesi | richieste italiane ("scrivimi X in DM", "salvalo"), hashtag con accenti, taglio "... altro" |
| `beats.py` | 165 parole/min | 150 parole/min (stima), numeri e importi italiani |
| `swipe.py` | colonne inglesi | accetta anche intestazioni italiane (`follower`, `mediana`, `visualizzazioni`), separatore delle migliaia col punto |
| tutti i tool | | forzano l'output in UTF-8 (serve su Windows) |

## Installazione

Incolla questo in Claude:

```
Installa questa skill, poi conferma che /ig-reel funziona.
```

Oppure a mano, in Claude Code:

```bash
git clone https://github.com/Cartesio89/Automazione-publicazione-post.git
cp -r Automazione-publicazione-post/skills/ig-* ~/.claude/skills/
```

Su Windows (PowerShell):

```powershell
git clone https://github.com/Cartesio89/Automazione-publicazione-post.git
Copy-Item -Recurse Automazione-publicazione-post\skills\ig-* $env:USERPROFILE\.claude\skills\
```

Oppure come plugin:

```
/plugin marketplace add Cartesio89/Automazione-publicazione-post
/plugin install instagram-agent-it@instagram-agent-skill-it
```

Locale al progetto invece che globale: copia le stesse cartelle in
`.claude/skills/` della tua repo. Senza Claude Code: incolla un singolo `SKILL.md`
in cima a una chat e gira come modalità. Perdi i cinque strumenti Python, che sono
gran parte del senso di `/ig-reel` e `/ig-human`, ma il resto funziona.

**Python.** Gli script usano solo la libreria standard di Python 3 (nessun `pip
install`). Su Windows il comando può essere `python` o `py` invece di `python3`.
`swipe.py` cerca `hooks.json` in `../ig-reel/`: se copi le skill a mano, copia
anche `ig-reel` accanto a `ig-viral`.

Poi dedica dieci minuti a `templates/voice.md`. Copialo in
`~/.claude/instagram/voice.md` (Windows: `%USERPROFILE%\.claude\instagram\voice.md`)
e compilalo, oppure manda a Claude tre tuoi reel e di': "scrivi il mio voice.md da
questi". Ogni skill legge quel file. Su Instagram conta più che altrove, perché le
parole le devi dire a voce alta.

## Le tredici

| comando | cosa fa |
| --- | --- |
| `/ig-reel` | Un'idea in un Reel. Tre hook su [26 formule](skills/ig-reel/hooks.json), con punteggio, poi lo script, il testo a schermo e una scaletta temporizzata. |
| `/ig-viral` | Cerca cosa funziona nella tua nicchia, lo ordina per multiplo sulla mediana di ciascun account, dà un nome alla formula, scrive lo swipe file. |
| `/ig-caption` | La didascalia, controllata. Ti mostra i 125 caratteri che il feed mostra davvero prima del tocco. |
| `/ig-carousel` | Post da scorrere. La copertina che si guadagna lo scorrimento, il testo delle slide e i file 1080x1350. |
| `/ig-story` | La sequenza di storie quotidiana, quale adesivo fa quale lavoro, e il percorso verso il DM che parte da chi muove per primo. |
| `/ig-profile` | Dà un punteggio al profilo su una [griglia di 12 voci](skills/ig-profile/rubric.json) su 100, poi riscrive partendo da ciò che perde di più. |
| `/ig-plan` | La settimana. Cosa pubblicare, in che formato, quando, e i 10 account con cui interagire. |
| `/ig-human` | L'umanizzatore. Due script che girano davvero. Vedi sotto. |
| `/ig-comment` | Commenti ai post degli altri. Nove tipi, scelti in base a cosa è davvero il post. Mai "🔥🔥🔥". |
| `/ig-reply` | Il thread sotto il tuo post. Smista in parola chiave / lead / sostanza / domanda / sostegno / rumore, poi scrive in quest'ordine. |
| `/ig-dm` | La consegna della parola chiave, il primo messaggio, la proposta di collaborazione e i due solleciti. Due. |
| `/ig-repurpose` | Un video, un podcast o una newsletter in una settimana di reel e caroselli, ciascuno autonomo. |
| `/ig-audit` | Analisi di ciò che hai già pubblicato. Ordina per multiplo di scostamento e invii per copertura, non per views. |

## I cinque strumenti che girano davvero

Nessuna dipendenza, nessuna rete, niente caricato. Girano sul tuo computer, sul
tuo testo. Gli output qui sotto sono **reali**, prodotti dagli script italiani su
testi di prova (le frasi le ho scritte io, non sono dati di account reali).

### Hook

```bash
python3 hookscore.py hooks.txt              # ordina le opzioni
python3 beats.py script.txt --target 30     # cronometralo prima di girare
```

```
CLASSIFICA HOOK
==============================================================================
->  81.4 FORTE   Nessuno ti dice che i tuoi primi 30 reel sono destinati a f...
        più debole: POSTA IN GIOCO (70)
    81.4 FORTE   Ho perso 18.000 euro per una clausola mancante nel contratto.
        più debole: DESTINATARIO (70)
    21.2 DEBOLE  Fermati un attimo se vuoi crescere su Instagram nel 2026 🔥
        più debole: POSTA IN GIOCO (20)
        bloccante: Apre con "fermati" o "stop scrolling". Chiedere attenzione dimostra che non te la sei guadagnata.
        bloccante: Emoji nell'hook. Il testo a schermo in formato hook ha spazio per parole o per un'emoji, non per entrambe.
     5.4 DEBOLE  Ciao ragazzi, oggi volevo parlarvi di strategia dei contenuti
        più debole: ANTICIPO (0)
        bloccante: Saluto. Nessuno è venuto nel feed per farsi salutare.
```

`beats.py` stima quanto ci vuole a dire ogni riga, le impila in timecode e segnala
le quattro cose che uccidono un Reel in montaggio: un hook che supera i tre
secondi, una battuta abbastanza lunga da far andare via chi guarda, una serie di
righe senza niente di concreto, nessun ritorno alla prima riga.

```
SCALETTA  ·  78 parole  ·  ~31.2s a 150 parole/min  ·  obiettivo 30.0s
========================================================================
  0:00.0   2.8s  HOOK    Ho perso 18.000 euro per una clausola.
  0:02.8   6.0s          Me ne sono accorto a marzo, quando il cliente di Torino ha smesso di rispondere.
                         ^ 6.0s su una sola battuta
  0:08.8  13.6s  META    Ho riscritto il contratto da zero in due sere con l'avvocato Rossi, e non è stato gratis, ma ho evitato altri guai che non avevo previsto e che mi avrebbero fatto perdere ancora tempo.
                         ^ 13.6s su una sola battuta
  0:22.4   2.4s          Mai più "a discrezione del committente".
  0:24.8   6.4s  CTA     Apri il tuo contratto adesso, prima che sia lui a trovare te e la tua clausola.
                         ^ 6.4s su una sola battuta
------------------------------------------------------------------------
  - La/le battuta/e 2, 3, 5 superano 4s. Spezza la riga oppure cambia cosa c'è a schermo al suo interno. Un'inquadratura ferma è dove la gente se ne va.
  - Loop: l'ultima battuta ripete "clausola" dall'hook. Le seconde visualizzazioni sono portata gratis.
  - La durata è in linea (31.2s contro 30.0s).
```

### La didascalia

```bash
python3 caption.py didascalia.txt --keywords "contratto freelance,clausola"
```

Instagram dà a una didascalia circa 125 caratteri nel feed e nasconde il resto
dietro un tocco. Quasi tutte le didascalie che falliscono falliscono lì. Quindi la
prima cosa che stampa è quella finestra, in un riquadro, come la legge uno
sconosciuto che scorre:

```
  COSA MOSTRA IL FEED
  +------------------------------------------------------+
  | Ho perso 18.000 euro per una clausola mancante. Una  |
  | sola riga nel contratto con un cliente di Torino.    |
  |                                                      |
  | Ecco come l'ho riscrit                               |
  +------------------------------------------- ... altro +

  PASS  LUNGHEZZA           269 / 2200 caratteri
  PASS  PRIMA RIGA          101 caratteri, arriva intera
  PASS  HOOK CONCRETO       2 numero/i o nome/i nella finestra visibile
  PASS  HASHTAG             3 hashtag: #contratti #freelance #partitaiva
  PASS  POSIZIONE HASHTAG   gli hashtag stanno sotto il taglio
  PASS  LINK                nessun link morto nel corpo
  PASS  UNA RICHIESTA       una sola call to action: scrivimi in DM
  PASS  EMOJI               0 emoji, 0.0 ogni 100 caratteri
  WARN  TERMINI DI RICERCA  1/2 presenti, 1 nella finestra visibile. Mancano: contratto freelance
------------------------------------------------------------------------
  VERDETTO  DA RIVEDERE
```

Applica il tetto attuale degli hashtag, che è **cinque per post**, non trenta.
Instagram l'ha ridotto il 18 dicembre 2025.

### L'umanizzatore

```bash
python3 humanize.py bozza.txt --report      # ripuliscila, mostra ogni modifica
python3 detect.py bozza.txt                  # valutala, cinque controlli
python3 detect.py prima.txt dopo.txt         # dimostra la differenza
```

**Cosa viene tolto in automatico:**

- **Caratteri invisibili.** Spazi e giunzioni a larghezza zero, word joiner, trattini
  soffici, byte-order mark, caratteri tag Unicode, separatori invisibili, spazi
  non separabili e stretti. La tua tastiera non li produce. Sopravvivono al
  copia-incolla e sono invisibili in ogni editor.
- **Tipografia.** Trattino lungo in virgola, trattino medio in trattino, virgolette
  ricurve in dritte, puntini in tre punti, più la punteggiatura orfana che resta.
- **Il lessico.** 207 voci tra parole e frasi, con sostituzioni in italiano normale
  che non rompono genere e numero ("sfruttiamo" → "usiamo", "innovative" →
  "nuove"). L'ultimo blocco è specifico di Instagram: "fermati un attimo", "nel
  video di oggi", "segui per altri contenuti", "tagga qualcuno che ne ha bisogno",
  "battere l'algoritmo". Sta in [`slop.json`](skills/ig-human/slop.json) ed è fatto
  per essere modificato.

**Cosa viene segnalato invece di corretto:** "Non è solo X, è Y", triadi "X, Y e
Z", il preambolo da video, elenchi puntati con emoji, tre parole in maiuscolo di
fila, muri di hashtag, esche da follow o tag, "sblocca il tuo potenziale", aggettivi
da brochure, lunghezza delle frasi uniforme. Cambiare la forma di una frase richiede
giudizio, quindi tornano indietro per essere riscritte invece di essere rovinate da
una regex.

Eseguito su una bozza scritta apposta per essere piena di cliché:

```
PANNELLO RILEVAMENTO IA
==================================================================
  VARIAZIONE    ########................  33.4
                variazione 0.38 su 10 frasi (vorresti 0.55+)
  SPECIFICITÀ   ###.....................  12.8
                1 marcatori concreti, 1.2 ogni 100 parole (vorresti 4+)
  DENSITÀ SLOP  ........................   0.0
                20 termini da stock, 24.1 ogni 100 parole (contenuti di valore, cosa ne pensi?, ecosistema, fondamentale, ...)
  IMPRONTA      #################.......  70.9
                0 invisibili, 1 trattini lunghi, 0 virgolette ricurve, 0 puntini ricurvi, 0 spazi rigidi
  VOCE          ##......................   7.0
                0.0 marcatori di parlato, 2.4 pronomi personali ogni 100 parole, 8 segnale/i strutturale/i [not-just, rocket, hashtag-wall, engagement-bait]
------------------------------------------------------------------
  PUNTEGGIO     ####....................  14.9   SEGNALATO

  Segnale più debole: DENSITÀ SLOP. Sistema quello per primo.
```

Dopo `humanize.py`, con le strutture segnalate ancora da riscrivere:

```
  14.9 SEGNALATO  ->  36.8 SEGNALATO   (+21.9)
```

Resta SEGNALATO, ed è corretto: il lessico e la tipografia sono a posto (densità
slop da 0 a 100), ma restano da riscrivere a mano la voce, le strutture e la
mancanza di cose concrete. Lo script non lo nasconde.

### Lo swipe file

```bash
python3 swipe.py raccolti.tsv --out ~/.claude/instagram/swipe.md
```

Le views grezze non sono una prova. Un account da 2.000.000 di follower che fa
400.000 views ha avuto un martedì tranquillo. Un account da 4.000 follower che fa
400.000 views ha trovato qualcosa. `swipe.py` ordina per il multiplo sulla mediana
di ciascun account, dà un nome alla formula di hook e stampa cosa separa il terzo
migliore dal terzo peggiore.

```
SWIPE FILE  ·  7 reel  ·  7 account  ·  base: mediana dell'account
==============================================================================
    60.0x  hook  54  #9  Il Furto                   @c                 180.000
           "Ruba questo follow-up di quattro righe, ci ho messo due anni"
    37.5x  hook  81  #3  Nessuno Te Lo Dice         @a                 412.000
           "Nessuno ti dice che i tuoi primi 30 reel sono destinati a floppare"
    30.0x  hook  52  #20 Il Permesso                @e                  60.000
           "Non ti serve una nicchia"
     3.5x  hook  30  #16 La Domanda Testuale        @f                   7.000
           "Come faccio a postare con costanza?"
     2.2x  hook  81  #1  La Confessione del Costo   @d                   9.000
           "Ho perso 18 mila euro per una clausola mancante"
     1.7x  hook  30  -   non classificato           @g                   5.000
           "Una riflessione sul mondo del marketing digitale"
     1.2x  hook   0  -   non classificato           @b               1.200.000
           "Ciao ragazzi, oggi vi mostro la mia routine del mattino"
------------------------------------------------------------------------------
COSA FUNZIONA IN QUESTO GRUPPO
  terzo migliore per multiplo:  Il Furto x1, Nessuno Te Lo Dice x1
  punteggio hook mediano:       migliori 68  contro peggiori 15
  lunghezza hook mediana:       migliori 12.0 parole  contro peggiori 8.5 parole
  non classificati:             2 su 7. Leggili a mano, è lì che si nasconde una formula che non hai ancora.
```

I sette reel e le views sono dati di prova inventati da me per far girare lo script
(non sono reel veri).

## Cosa NON è stato verificato, ed è la parte da leggere

Questa è la sezione più importante.

**1. I numeri di calibrazione dell'originale non valgono per l'italiano.** L'autore
originale dichiara di aver testato lo scorer su 74 hook reali di YouTube Shorts in
inglese: AUC 0,83 nel distinguere hook veri da hook scritti apposta male, ma solo
AUC 0,56 nel distinguere i successi di un creator dai suoi flop (0,50 è una
moneta). Sono suoi risultati (dati empirici, C), **non riprodotti da me** e riferiti
all'inglese. Questa versione italiana **non è stata testata su nessun hook
italiano reale**: i lessici, le regex e le soglie sono adattati a mano. I test che
ho fatto sono solo di coerenza interna (A: gli script girano e danno risultati
sensati su frasi che ho scritto io), non di validità.

**2. Il classificatore delle formule è testato in modo circolare.** Le 26 regex
italiane classificano ciascuna il proprio esempio nella formula giusta (26 su 26),
ma gli esempi li ho scritti io insieme alle regex. Su hook veri aspettati molti
"non classificato". Quella colonna è fatta per essere letta a mano.

**3. Le soglie sono stime, non misure.** Il ritmo di 150 parole al minuto, il
limite di 13 parole dell'hook, le soglie di `detect.py` (variazione delle frasi,
densità di concretezza, marcatori di parlato) sono stime analitiche (B) adattate
dall'inglese. `detect.py` serve a confrontare due versioni della stessa bozza, non
come punteggio assoluto. Cronometrati una volta e correggi `--wpm`.

**4. Il lessico non è calibrato.** Le sostituzioni sono scelte per non rompere
genere e numero, ma nessuno ha rilevato su testi italiani reali quali parole
tradiscono davvero un testo da IA. Rileggi sempre il risultato di `humanize.py`.

**5. Niente di tutto questo è stato provato su Instagram.** Nessun reel è stato
pubblicato e nessun risultato di visualizzazioni è stato misurato.

Se rieseguirai tutto su un corpus italiano più grande e otterrai un'altra
risposta, preferisco saperlo.

## Il testo piccolo, cioè la parte onesta

**Queste skill non pubblicano su Instagram.** Esiste una vera API di pubblicazione
di contenuti per gli account professionali, e richiede un'app sviluppatore Meta,
una Pagina collegata, un token a lunga durata e, per l'uso pubblico, la revisione
dell'app: non è una cosa che una skill possa consegnarti. Tutto ciò che la gente
usa per automatizzare pubblicazione, commenti, follow o DM è automazione del
browser o uno strumento di terze parti, e entrambi violano i
[Termini d'uso di Instagram](https://help.instagram.com/581066165581870) e fanno
bloccare le azioni degli account. Quindi ogni skill finisce allo stesso modo: un
blocco pronto da copiare, e lo pubblichi tu. Non è un limite aggiunto dopo, è il
progetto, ed è per questo che il cancello di approvazione è vero e non
un'impostazione.

L'unica eccezione sono le risposte automatiche a parola chiave nei DM, che
Instagram supporta con i propri strumenti e i partner approvati, e che scattano
solo dopo che qualcuno ha commentato per primo. `/ig-dm` dice dove sta quel confine.

**`/ig-viral` legge, non fa scraping.** Dieci account, una dozzina di reel
ciascuno, a velocità umana, con te alla guida del tuo browser. Non chiede mai la
tua password e non accede mai al posto tuo. La raccolta automatica in volume è ciò
che fa limitare gli account, e questo non è un crawler.

**I cinque controlli di rilevamento sono euristiche locali, non API di
rilevatori.** Sono modellati sui segnali su cui puntano i rilevatori pubblici e
girano interamente sulla tua macchina. Non sono GPTZero, Originality, Copyleaks,
Winston o Turnitin, non chiamano quei servizi e non possono promettere quei
verdetti. Nessuno può venderti onestamente il "non rilevabile".

**Il passaggio sui caratteri invisibili è reale ed è stretto.** Toglie i caratteri
a larghezza zero e di formato che finiscono nel testo generato e sopravvivono al
copia-incolla. È un'impronta vera e verificabile. Non è una dichiarazione di
sconfiggere uno schema crittografico di filigrana, e questa repo non la fa.

**Niente è inventato.** Nessuna metrica, cliente o risultato inventato finisce a
tuo nome. Se una bozza richiede un numero che non hai dato, torna con
`{{il tuo numero}}` dentro e una segnalazione, sempre.

**I numeri delle piattaforme invecchiano.** Il tetto degli hashtag è passato da 30 a
5 a dicembre 2025. Se qualcosa qui contraddice ciò che fa Instagram quando leggi,
ha ragione Instagram.

## File

```
skills/ig-reel/hooks.json          26 formule di hook: modello, esempio, riga a schermo,
                                   a cosa serve, come viene rovinata, e una regex match
skills/ig-reel/hookscore.py        il pannello di cinque proprietà dell'hook
skills/ig-reel/beats.py            da script a scaletta temporizzata
skills/ig-caption/caption.py       l'anteprima del taglio e il controllo della didascalia
skills/ig-human/slop.json          il lessico: 207 voci, 18 classi invisibili, 18 segnali strutturali
skills/ig-human/humanize.py        i tre passaggi di pulizia
skills/ig-human/detect.py          il pannello di cinque controlli
skills/ig-viral/swipe.py           ordinamento per scostamento e classificazione delle formule
skills/ig-profile/rubric.json      il punteggio del profilo su 100
templates/voice.md                 il tuo profilo di voce. Compilalo per primo.
```

## Credito

Idea, struttura, skill e script originali di Jake Schincariol,
[opusjake.ai](https://opusjake.ai), repo originale
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill).
Questa è un'adattamento in italiano, non ufficiale e non affiliato all'autore.

## Licenza

MIT, come l'originale (vedi `LICENSE`, che conserva il copyright dell'autore
originale). Prendilo, cambialo, usalo.
