---
name: ig-viral
description: >-
  Va a cercare i reel che funzionano davvero adesso nella nicchia dell'utente, li
  mette in classifica per quanto ciascuno ha battuto il proprio account, dà un
  nome alla formula di hook usata e ne ricava uno swipe file da cui girare. Usala
  quando l'utente dice "trova video virali", "cosa funziona adesso", "cosa
  pubblicano nella mia nicchia", "analizza questo account", "fammi uno swipe
  file", "perché questo reel fa numeri", o chiede cosa fare dopo e non ha prove
  con cui rispondere.
---

# ig-viral

La skill di ricerca. Tutto il resto di questo pacchetto scrive; questa va a
guardare. Lanciala una volta al mese, non ogni giorno. Le formule durano una
stagione.

In questa cartella c'è uno strumento e gira:

```bash
python3 swipe.py raccolti.tsv --out ~/.claude/instagram/swipe.md
```

(Su Windows, se `python3` non esiste, usa `python` oppure `py`; la cartella
dell'utente è `%USERPROFILE%\.claude\instagram\`.)

**Onestà sull'italiano.** Il nome della formula e il punteggio dell'hook usano
regex e lessici adattati all'italiano e non testati su hook italiani reali: aspetta
falsi negativi, che finiscono in "non classificato". Quella colonna va letta a mano.

## L'idea che rende utile tutto questo

**Le visualizzazioni grezze non sono una prova.** Un account da due milioni di
follower che fa 400.000 view ha avuto un martedì tranquillo. Un account da
quattromila follower che fa 400.000 view ha trovato qualcosa, e quel qualcosa si
può copiare.

Quindi qui tutto si ordina per **multiplo di scostamento**: view divise per la
mediana recente dello stesso account. Sopra 3x è un segnale. Sotto 1,5x è la
giornata normale di quell'account e non ti insegna niente, per quanto grande
sembri il numero.

Raccogli account **entro circa 10 volte la dimensione di quello dell'utente**. Una
formula che funziona a 2 milioni di follower spesso funziona perché è a 2 milioni
di follower.

## Passo 1: scegli gli account

Chiedi all'utente da 6 a 12 account, oppure proponili e fatti approvare:

- **4 diretti** - stessa nicchia, stessa offerta, leggermente avanti.
- **4 adiacenti** - altra nicchia, stesso pubblico. È qui che si prendono in
  prestito i formati prima che li abbia chiunque nella nicchia.
- **Da 2 a 4 fuori scala** - account molto più grandi, solo per il formato, mai per
  cadenza o tono.

Chiedigli anche di aprire la sua **raccolta Salvati**. È il corpus più rapido e più
pertinente che esista ed è già filtrato dal suo gusto.

Cerca anche nella lingua giusta: per una nicchia italiana, prendi account italiani.
Un formato che funziona in inglese non è detto che si traduca.

## Passo 2: vai a guardare

Usa lo strumento di navigazione che questa sessione ha davvero: un browser
integrato, un'estensione del browser collegata al Chrome dell'utente o uno
strumento di computer use. Non c'è un'API per questo e non serve, perché il volume
è abbastanza piccolo da essere letto.

**Regole non negoziabili:**

- **Non accedere mai a Instagram al posto dell'utente e non chiedere mai una
  password.** Se una pagina richiede il login, è l'utente a essere già connesso.
  Guida il suo browser con lui presente, oppure chiedigli di incollare.
- **Questo è leggere, non fare scraping.** Dieci account, una dozzina di reel
  ciascuno, a velocità umana. La raccolta automatica in volume viola i Termini
  d'uso di Instagram e fa bloccare le azioni degli account. Non costruire un
  crawler, non usare un servizio di scraping e non far girare questo in background.
- **Copia la formula, mai il video.** La forma dell'hook, la struttura, la durata,
  lo schema dei tagli. Non il loro script, non la loro voce, non il loro montaggio.
  Attribuisci ogni riga dello swipe file all'account da cui viene.

**Cosa raccogliere per ogni reel**, con le parole del creator:

| campo | note |
| --- | --- |
| account | handle |
| follower | dal profilo |
| mediana | guarda a occhio gli ultimi 12 reel e prendi il valore centrale delle view |
| views | questo reel |
| hook | la prima riga, parlata o a schermo, alla lettera, errori di grammatica compresi |
| a schermo | il primo cartello di testo, se diverso |
| durata | secondi |
| cta | cosa hanno chiesto alla fine |

La mediana è quella importante. Senza, torni a ordinare per numero di follower,
che è proprio la cosa che questa skill esiste per fermare.

**Quando Instagram non te ne mostra abbastanza:** la stessa grammatica di hook gira
su YouTube Shorts, dove le view e le trascrizioni sono pubbliche e non c'è nessun
login. È un secondo corpus legittimo, e l'hook parlato si ottiene più facilmente:

```bash
# view dei shorts di un canale
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@HANDLE/shorts" > canale.json

# la prima riga parlata di uno short, dai sottotitoli automatici
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "it.*" \
  --sub-format json3 -o hook "https://www.youtube.com/watch?v=VIDEO_ID"
```

Prendi ogni parola dei sottotitoli con un timestamp sotto i 3,0 secondi. Quello è
l'hook, come detto e non come scritto.

## Passo 3: mettilo in classifica

Compila un file separato da tabulazioni con una riga di intestazione e lancia lo
script:

```
account	follower	mediana	views	hook
@qualcuno	48000	11000	412000	nessuno ti dice che i primi 30 reel sono destinati a floppare
```

(Anche le intestazioni inglesi `followers`, `median` vanno bene.)

```bash
python3 swipe.py raccolti.tsv --out ~/.claude/instagram/swipe.md
```

Calcola il multiplo di scostamento, dà un nome alla formula usando le stesse 26
formule da cui scrive `/ig-reel`, dà un punteggio a ogni hook con `hookscore.py` e
stampa cosa separa il terzo migliore dal terzo peggiore.

## Passo 4: di' cosa significa, con cautela

Riporta tre cose e non di più:

1. **Quali formule sono sovra-rappresentate** nel terzo migliore, con i conteggi.
   Due formule che compaiono quattro volte ciascuna su sei account sono un
   risultato. Una che compare due volte no.
2. **Cosa hanno in comune strutturalmente i migliori** e i peggiori no: lunghezza
   dell'hook, se il finale è visivo, se il primo fotogramma si muove, dov'è la
   richiesta.
3. **Le righe non classificate.** Ogni hook che il classificatore non ha saputo
   nominare è rumore oppure una formula che non è ancora in `hooks.json`. Leggile
   a mano. È la colonna più preziosa dell'output ed è il motivo per cui lo script
   ne stampa il conteggio.

Poi dichiara la dimensione del campione e la fiducia con parole semplici. Quaranta
reel su sei account reggono un'affermazione. Dodici no, e dirlo è la differenza tra
ricerca e oroscopo.

## Passo 5: trasformalo in qualcosa da girare

Per le prime tre formule, scrivi **la versione dell'utente**: la sua storia, il suo
numero, nella forma che funziona. Passa ciascuna a `/ig-reel` con l'id della
formula già scelto.

Non restituire mai "fai un reel come questo". Restituisci una riga di hook che
potrebbe dire domani.

## Output

(Esempio del formato: i numeri vengono dallo script, non inventarli.)

```
SWIPE FILE  ·  7 reel  ·  7 account  ·  base: mediana dell'account

   60.0x  hook  54  #9  Il Furto                @c   180.000
   37.5x  hook  81  #3  Nessuno Te Lo Dice      @a   412.000
   30.0x  hook  52  #20 Il Permesso             @e    60.000
  ...

COSA FUNZIONA IN QUESTO GRUPPO
  terzo migliore per multiplo:  Il Furto x1, Nessuno Te Lo Dice x1
  punteggio hook mediano:       migliori 68  contro peggiori 15
  non classificati:             2 su 7. Leggili a mano.

LA TUA VERSIONE
  #3  "Nessuno ti dice che le prime 20 proposte sono fatte per perdere."
  ...
```

Scrivi lo swipe file in `~/.claude/instagram/swipe.md`. `/ig-reel` e `/ig-plan` lo
leggono entrambi, ed è questo il punto: dopo un solo giro, il resto del pacchetto
lavora sulle prove dell'utente invece che sui valori predefiniti.

Questa skill non pubblica, non segue, non mette like e non manda messaggi. Legge.
