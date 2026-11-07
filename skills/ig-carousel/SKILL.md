---
name: ig-carousel
description: >-
  Costruisce un carosello di Instagram in italiano: la copertina che si guadagna lo
  scorrimento, il testo slide per slide e i file 1080x1350 da caricare. Usala
  quando l'utente dice "carosello", "slide", "post da scorrere", "trasformalo in un
  carosello", o ha un'idea a elenco o a passaggi che morirebbe come immagine
  singola.
---

# ig-carousel

I caroselli sono il formato con la permanenza più alta sulla griglia, perché uno
scorrimento è un'interazione e una scrollata no. Hanno anche una seconda chance:
Instagram può mostrare di nuovo un carosello partendo da una slide successiva a chi
non ha interagito la prima volta, quindi anche la slide due deve reggersi da sola.

Il formato premia un'idea spezzata in passaggi. Punisce una didascalia tagliata a
pezzi.

## Quando usarlo al posto di un Reel

Usa un carosello quando l'idea ha **sequenza e va riletta**: passaggi, uno schema
in più parti, un prima e dopo, un elenco che vale uno screenshot. Usa un Reel
quando l'idea ha movimento, una faccia, o un finale che va visto mentre accade.

Se l'idea è un'unica affermazione, non è nessuno dei due. Passala a `/ig-reel` e
dillo.

## Struttura

Da 6 a 10 slide. Il tetto è 20 e 20 è quasi sempre un libro che nessuno finisce.
Sotto 5 lo scorrimento non parte.

```
1         COPERTINA  l'hook. 6 parole o meno, a una dimensione leggibile nella
                     griglia in miniatura. Sotto, una riga di promessa.
2         LA POSTA   perché conta, in una frase. Questa slide è anche una seconda
                     copertina, quindi non può essere preparazione.
da 3 a N  UN'IDEA PER SLIDE. Un titolo di 3-7 parole, al massimo 25 parole sotto.
                     Se una slide richiede un paragrafo, sono due slide.
N+1       RIEPILOGO  tutto in forma di elenco. È la slide da screenshot.
ULTIMA    CTA        una azione. Salva, commenta una parola chiave, oppure segui. Una.
```

## Regole per il testo delle slide

- **La copertina è l'80% del risultato.** Sei parole. Grandi. Niente nel resto del
  mazzo salva una copertina che nessuno scorre.
- **Progetta per il ritaglio della griglia.** La griglia del profilo ritaglia in un
  rettangolo verticale più alto che largo, e il rapporto esatto è cambiato più di
  una volta. Costruisci a 1080x1350 e tieni il testo della copertina ben dentro il
  centro, lontano 120 pixel dai bordi su ogni lato, e il ritaglio smette di contare.
- **Numera le slide** (3/8). Il completamento sale quando si vede la fine.
- **Nessuna slide è un paragrafo.** Se non si dice in 25 parole, spezzala.
- **La slide di riepilogo è quella che la gente salva e manda.** Gli invii sono il
  segnale più forte che si può guadagnare. Falla autonoma e leggibile senza contesto.
- **L'handle su ogni slide**, piccolo, in un angolo in basso. Gli screenshot
  viaggiano senza di te.
- **Testo alternativo almeno sulla copertina.** Lo leggono gli screen reader e
  Instagram.
- **Italiano su schermo piccolo:** le parole italiane sono più lunghe di quelle
  inglesi, quindi un titolo da 6 parole occupa più spazio. Controlla che nessuna
  riga vada a capo male e non spezzare le parole con il trattino.

## Costruire i file

Instagram vuole 1080x1350 (4:5), JPEG o PNG, fino a 20 elementi. Costruiscili in
HTML e stampa ogni slide:

```bash
# una <section> per slide, 1080x1350, page-break-after: always
# poi Chrome headless --print-to-pdf, o qualsiasi convertitore HTML-immagine che usi già
```

Scrivi l'HTML con `width:1080px; height:1350px`, un solo colore d'accento e un
carattere non sotto i 32px, perché si legge su un telefono a un terzo della
dimensione reale. Se il progetto ha una skill di brand o un design system, usalo e
non inventare una palette. Imposta `<html lang="it">` e un font con le lettere
accentate (à è é ì ò ù).

## Output

Prima il testo slide per slide, come elenco numerato che l'utente può leggere in
dieci secondi e correggere prima che venga generato qualsiasi file. Poi la
**didascalia**, che per un carosello è il Compito B di `/ig-caption`: qui la
didascalia lavora, perché la copertina ha già usato le sue sei parole.

Passa entrambi in `/ig-human`. Costruisci i file solo dopo che l'utente ha
approvato il testo.

```
CAROSELLO  ·  8 slide          (esempio del formato)

1  COPERTINA  LA CLAUSOLA DA 18.000 €
              Una riga che ora metto in ogni contratto.
2  POSTA      Ho approvato il lavoro. Nove giorni dopo mi hanno chiesto indietro i soldi.
3             COSA DICE
              Pagamento alla consegna, non all'approvazione.
...
7  RIEPILOGO  Tutte e quattro le righe, in ordine.
8  CTA        Scrivimi CONTRATTO in DM e ti mando la clausola completa.

Didascalia: Compito B, hook nella riga 1, una richiesta, 3 hashtag.
```

Non viene caricato niente. L'utente pubblica.
