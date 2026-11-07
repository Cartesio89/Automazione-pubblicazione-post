---
name: ig-caption
description: >-
  Scrive la didascalia di Instagram in italiano (la riga che sopravvive al taglio
  "... altro", il corpo, l'unica richiesta, i termini di ricerca e gli hashtag) e
  la controlla prima della pubblicazione. Usala quando l'utente dice "scrivi la
  didascalia", "didascalia per questo", "cosa metto nella descrizione", ha un reel
  o un carosello pronto e gli serve il testo, o chiede degli hashtag.
---

# ig-caption

In questa cartella c'è uno strumento e gira:

```bash
python3 caption.py didascalia.txt
python3 caption.py didascalia.txt --keywords "preventivi per clienti,prezzi agenzia"
```

(Su Windows, se `python3` non esiste, usa `python` oppure `py`.)

Stampa la didascalia come la stampa il feed: i primi 125 caratteri in un riquadro,
tutto il resto dietro il tocco. Leggi quel riquadro prima di rileggere qualsiasi
altra cosa tu abbia scritto. Il taglio a 125 caratteri è un'approssimazione: il
numero reale cambia con dispositivo, dimensione del carattere e a capo.

## Prima di tutto, decidi che compito ha questa didascalia

È la decisione che rovina le didascalie quando si salta.

**Compito A: il video li ha già agganciati.** Un Reel porta il proprio hook nei
primi due secondi, parlato e a schermo. La didascalia non è un secondo hook, e
fargli concorrenza è il modo di perdere entrambi. Il suo compito è la richiesta,
il contesto che la rende sensata e le parole che la gente cerca.

**Compito B: la didascalia è il contenuto.** Una foto, un'immagine singola, la
copertina di un carosello che apre un anello. Qui la riga uno è l'hook e funziona
esattamente come l'hook di un Reel: concreta, corta, e tagliata su un precipizio e
non a metà proposizione.

Chiedi quale stai scrivendo. Se l'utente ha un Reel con un hook forte, scrivi A e
spiega perché.

## La forma

```
Riga 1      125 caratteri di spazio visibile. Compito A: la richiesta, in chiaro.
            Compito B: l'hook.
            Mai un saluto, mai un hashtag, mai un'emoji come primo carattere.
Corpo       paragrafi corti, una riga vuota tra l'uno e l'altro. Da due a sei.
            È qui che vivono i termini di ricerca.
La richiesta una. Commenta una parola chiave, salva, oppure scrivimi in DM. Una.
Hashtag     fino a cinque, su una riga a sé in fondo, oppure nessuno.
```

Il limite è 2.200 caratteri e quasi niente ne richiede 2.200. Una didascalia che si
guadagna il tocco e poi ne consegna 600 batte una che ne consegna 1.800.

## Hashtag, onestamente

Gli hashtag non sono più una leva di portata, e la piattaforma l'ha detto con una
modifica di prodotto. **Instagram ha limitato gli hashtag a cinque per post il 18
dicembre 2025**, da trenta, dicendo ai creator che usare meno hashtag (fino a 5) e
più mirati, invece di tanti generici, rende meglio. Il pacchetto originale
attribuisce ad Adam Mosseri, a febbraio 2025, l'affermazione che gli hashtag non
servono ad aumentare la portata e sono un'etichetta, non una leva di
distribuzione. Non l'ho verificata di persona: trattala come indicazione, non
come fatto.

Quindi: fino a cinque, specifici, come etichette di argomento. Se l'utente ha un
blocco di venti salvato nelle note, quel blocco è ormai zavorra e il controllo lo
boccia.

`#viral`, `#fyp`, `#perte`, `#neiperte`, `#reelitalia` non descrivono niente.
Toglili.

## I termini di ricerca contano più degli hashtag ormai

La ricerca di Instagram legge il testo della didascalia. Quindi la frase per cui
l'utente vuole essere trovato va nella didascalia come la scriverebbe una persona,
dentro una frase che si legge normalmente. "Preventivi per clienti" come parole
nella riga tre, non "#preventiviperclienti" in un blocco in fondo.

Chiedi due o tre di questi termini, poi passali al controllo:

```bash
python3 caption.py bozza.txt --keywords "preventivi per clienti,prezzi agenzia"
```

Cerca i termini come li scriverebbe un italiano, non tradotti dall'inglese:
"partita iva forfettaria", non "freelance tax regime".

## Regole

- **Niente link nella didascalia.** Le didascalie non sono cliccabili. Un URL nel
  corpo è testo morto che dice "non uso questa piattaforma". Bio o DM.
- **Una richiesta.** Due richieste equivalgono a nessuna. `caption.py` le conta.
- **La richiesta con parola chiave ha bisogno di una parola che la gente sappia
  scrivere.** Una parola, niente spazi, niente emoji, e dilla anche a voce nel
  video. "Scrivimi CONTRATTO in DM" funziona. "Scrivimi 'la guida al contratto'"
  no. Meglio una parola senza accenti né apostrofi.
- **Scrivi il primo commento a parte** se c'è un link. Dillo nella ricevuta.
- **Emoji come punteggiatura, non come decorazione.** Il controllo segnala tutto
  ciò che supera 4 ogni 100 caratteri.
- **Il testo alternativo vale 20 secondi.** Per caroselli e foto, scrivilo. Lo
  leggono gli screen reader e Instagram.

## Il ciclo

1. Decidi Compito A o Compito B e dì quale.
2. Scrivi la bozza.
3. Passala in `/ig-human`. Le didascalie sono corte, quindi qui lo slop si sente più
   che in qualsiasi altra parte del pacchetto.
4. Lancia `caption.py` con i termini di ricerca dell'utente. Correggi ogni FAIL.
   Decidi a voce alta su ogni WARN invece che in silenzio.
5. Stampa il blocco pronto da copiare, poi la ricevuta:

```
DIDASCALIA PRONTA          (esempio del formato: i valori vengono dallo script)
compito:    A - il reel porta l'hook
visibili:   118 di 125 caratteri usati prima del taglio
richiesta:  una, scrivimi CONTRATTO in DM
hashtag:    3
ricerca:    "preventivi per clienti" nella riga 3, "prezzi agenzia" nella riga 5
controllo:  PRONTA
```

Non viene pubblicato niente. L'utente la incolla.
