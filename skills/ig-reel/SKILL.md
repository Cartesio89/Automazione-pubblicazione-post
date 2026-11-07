---
name: ig-reel
description: >-
  Scrive un Reel di Instagram in italiano a partire da un'idea grezza: opzioni di
  hook su 26 formule, script parlato, testo a schermo e scaletta temporizzata,
  nella voce dell'utente e con punteggio prima di girare. Usala quando l'utente
  vuole un Reel, uno script per video brevi, un hook, una voce fuori campo, "fammi
  un reel su X", "cosa dico in questo video", o sta per registrare e non ha ancora
  la prima riga.
---

# ig-reel

Trasforma un'idea grezza in un Reel che qualcuno guarda fino in fondo.

In questa cartella ci sono due strumenti e funzionano davvero. Usali. Non
valutare l'hook a occhio e non tirare a indovinare la durata.

```bash
python3 hookscore.py hooks.txt              # mette in classifica le opzioni di hook
python3 hookscore.py --hook "una riga"      # dà un punteggio a una sola
python3 beats.py script.txt --target 30     # scaletta temporizzata prima di girare
```

(Su Windows, se `python3` non esiste, usa `python` oppure `py`.)

**Onestà sugli strumenti.** `hookscore.py` e `beats.py` sono euristiche locali
adattate all'italiano a partire da quelle inglesi originali. Non sono state
calibrate su hook italiani reali: i punteggi servono a scovare difetti evidenti
(saluti, preamboli, hook senza niente di concreto, hook troppo lunghi), non a
prevedere le visualizzazioni. Il ritmo di parlato predefinito (150 parole al
minuto) è una stima, non una misura.

## Prima di scrivere

1. Leggi `~/.claude/instagram/voice.md` se esiste (su Windows:
   `%USERPROFILE%\.claude\instagram\voice.md`). È il profilo di voce
   dell'utente: come parla in camera, cosa non dice mai, a chi parla, se dà del
   tu o del voi. Se non esiste, chiedi **tre suoi reel**, trascrivili o leggili,
   deduci la voce e scrivi il file. Uno script nella voce sbagliata è inutilizzabile,
   perché lo deve dire a voce alta.
2. Leggi `hooks.json` in questa cartella. 26 formule, ciascuna con un modello, un
   esempio compilato, la versione a schermo, a cosa serve e come viene rovinata.
3. Se l'idea è debole, non gonfiarla. Fai una sola domanda raggruppata: cosa è
   successo, a chi, e quanto è costato o quanto ha reso. Un Reel ha bisogno di
   una cosa specifica e vera. Procurala prima di scrivere.
4. Se esiste `~/.claude/instagram/swipe.md`, leggilo. `/ig-viral` scrive quel
   file ed è la prova diretta dell'utente su quali formule funzionano adesso
   nella sua nicchia. Batte i valori predefiniti di questo file.

## La forma

Un Reel si decide nei primi due secondi e si tiene nei cinque successivi.

```
0:00 - 0:02   HOOK        l'affermazione. Riga parlata e riga a schermo, scritte
                          separatamente. Movimento nel primo fotogramma, non una
                          faccia ferma.
0:02 - 0:07   LA POSTA    perché conta per chi guarda. Una riga.
0:07 - ...    IL CORPO    un'idea per battuta, e l'inquadratura cambia a ogni battuta.
ULTIMI 3s     IL FINALE   mantieni ciò che l'hook ha promesso, poi l'unica richiesta.
ULTIMA RIGA   IL LOOP     riprendi una parola dell'hook così la rivisione chiude pulita.
```

Durata: da 15 a 45 secondi è l'intervallo di lavoro. I Reel arrivano a 3 minuti e
quasi nessuno dovrebbe usarli. Sotto i 7 secondi gonfi il conteggio dei loop e
nient'altro.

## Il ciclo

**1. Scegli tre hook, non uno.** Passa l'idea in `hooks.json`, scegli tre formule
che le stanno davvero bene e scrivi per ciascuna la riga parlata e quella a
schermo. Formule diverse, non tre riscritture della stessa.

**2. Dai un punteggio.** Metti le tre righe parlate in un file, una per riga, e
lancia `hookscore.py`. Mostra la classifica all'utente. Se il primo è sotto 50,
non hai ancora l'hook e nessuna rifinitura lo risolve.

**3. Scrivi lo script** sull'hook vincente. Lingua parlata semplice, come parla
davvero l'utente. Frasi corte, elisioni e forme da conversazione ("c'è", "cos'è",
"un po'"). Niente frasi che dovrebbe provare prima.

**4. Cronometralo.** Lancia `beats.py script.txt --target {durata}`. Correggi ogni
segnalazione: un hook oltre i 3 secondi, qualsiasi battuta oltre i 4, una serie di
battute senza niente di concreto, nessun loop. Rilancia finché è pulito.

**5. Umanizzalo.** Passa lo script in `/ig-human` prima di mostrarlo. Una riga che
suona scritta si sente subito, appena qualcuno la dice a voce alta.

**6. Stampa il blocco.** Lo script in un blocco di codice, il testo a schermo come
elenco separato con i tempi, poi:

```
REEL PRONTO          (esempio del formato: i numeri vengono dagli script, non inventarli)
hook:       #3 Nessuno Te Lo Dice, punteggio 81 FORTE
durata:     28,4s su 9 battute a 150 parole/min
a schermo:  6 cartelli
umanizzatore: 4 artefatti tolti, punteggio umano 81 PASSA
didascalia: lancia /ig-caption subito dopo

Rispondi "sì" per registrarlo, o dimmi cosa cambiare.
```

**7. Non pubblicare mai.** Questa skill produce uno script. L'utente lo gira e lo
pubblica. Con il "sì", aggiungi una riga a `~/.claude/instagram/log.md` con la
data, la formula di hook usata e la prima riga, così `/ig-audit` avrà poi uno
storico.

## Il testo a schermo è uno script a parte

Scrivilo a parte, ogni volta. Si legge prima di essere sentito.

- **Sei parole o meno per cartello.** Lo legge a distanza di braccio qualcuno che
  ancora non ascolta.
- **Il cartello dell'hook c'è già al fotogramma 1**, non dopo un attimo di silenzio.
- **Resta nella zona sicura.** Su un fotogramma 1080x1920, niente sopra y=230 né
  sotto y=1440, e lascia libero il lato destro per 230 pixel. L'interfaccia copre
  tutto ciò che sta fuori da quel riquadro: didascalia, barra delle azioni,
  striscia dell'audio.
- **Non mettere mai l'hook dove sta la didascalia.** È il fondo del fotogramma ed
  è coperto.
- **Sottotitoli incorporati per il corpo.** La maggior parte della gente guarda
  prima senza audio.

## Regole che fanno la differenza

- **Un'idea per Reel.** Se lo script ne ha due, hai due Reel. Dillo.
- **Numeri al posto degli aggettivi.** "4.200 euro" batte "tanto". Se l'utente non
  ha dato un numero, chiedilo invece di scrivere intorno al buco.
- **Taglia l'introduzione.** Niente saluto, niente "in questo video", niente nome,
  niente jingle. Il video parte dalla frase che normalmente diresti al secondo sei.
- **Cambia inquadratura a ogni battuta.** Un'inquadratura ferma per 8 secondi è
  dove la gente se ne va, e `beats.py` la segnala.
- **Una richiesta alla fine.** Commenta una parola chiave, salva, oppure segui. Una.
- **Non inventare mai.** Niente metriche, clienti, ricavi o risultati inventati a
  nome dell'utente, nemmeno come segnaposto. Se serve un numero e non si conosce,
  lascia `{{il tuo numero}}` nello script e segnalalo.
- **Non scrivere uno script attorno a un audio di tendenza che l'utente non può
  usare.** Se l'idea richiede la sua voce, dillo.

## Esempio

```
/ig-reel abbiamo ridotto il tempo dei preventivi da 5 ore a 20 minuti con un unico modello
```

Tre hook scritti e passati in `hookscore.py` (output reale dello script):

```
CLASSIFICA HOOK
->  80.8 FORTE   Per due anni ho fatturato quattro ore a settimana solo per impaginare.
    51.2 OK      Le proposte mi portavano via cinque ore. Ora ci metto venti minuti.
    36.6 DEBOLE  Ruba il modello di preventivo che ha fatto tutto questo.
```

Il primo vince ed è il più forte anche perché ha una posta in gioco (due anni
persi) e due numeri. Il secondo ha la formula giusta ("Il Tempo Che Crolla") ma
non dice cosa si rischiava: aggiungi il costo e risali. Il terzo non ha niente di
verificabile e va riscritto: manca il numero.
