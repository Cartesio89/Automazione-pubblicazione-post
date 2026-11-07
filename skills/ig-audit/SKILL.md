---
name: ig-audit
description: >-
  Analisi a posteriori di ciò che l'utente ha già pubblicato: quali reel hanno
  funzionato davvero, perché, e cosa smettere di fare. Usala quando l'utente incolla
  le statistiche di Instagram o i post passati e chiede "cosa funziona", "perché è
  andato male", "leggi le mie statistiche", "fai un audit dei miei contenuti", o
  vuole sapere cosa fare di più.
---

# ig-audit

L'unica fonte onesta di ciò che funziona per un account è quell'account. Ogni
regola di ogni guida a Instagram, comprese quelle di questo pacchetto, è
un'ipotesi di partenza. Gli ultimi 30 post dell'utente sono la prova.

## Input

Chiedi ciò che l'utente ha:

- Le statistiche per post: visualizzazioni, copertura, interazioni, tempo di
  visione, salvataggi, condivisioni, nuovi follower e la quota di copertura che
  viene da chi non ti segue. Vanno bene anche gli screenshot.
- Oppure il grafico di retention dei suoi reel migliori e peggiori recenti. Questo
  solo screenshot vale più di tutto il resto insieme.
- Oppure solo i post e le loro visualizzazioni, che bastano per un primo giro.

Leggi anche `~/.claude/instagram/log.md` se esiste (su Windows:
`%USERPROFILE%\.claude\instagram\log.md`), perché registra quale formula di hook
ha usato ogni post.

## Cosa misurare davvero

Le visualizzazioni grezze sono il numero meno utile della pagina, perché dipendono
soprattutto da quante persone già seguono l'account. Calcola invece questi e mostra
i passaggi:

| metrica | come | cosa ti dice |
| --- | --- | --- |
| **Multiplo di scostamento** | views / mediana delle views dello stesso account | se è stato un vero colpo o una giornata normale |
| **Copertura da non follower** | % di copertura da persone che non ti seguono | se è uscito dalla cerchia |
| **Tenuta a 3s** | spettatori ancora lì a 3s / spettatori partiti | se l'hook ha funzionato. È il voto dell'hook. |
| **Tempo medio di visione** | direttamente dalle statistiche | se la parte centrale ha funzionato |
| **Invii per copertura** | condivisioni / copertura | il segnale singolo più forte che puoi guadagnare. Un invio è una persona che ci mette il proprio nome. |
| **Follow per copertura** | nuovi follower / copertura | se il profilo ha convertito l'attenzione |

Ordina per multiplo di scostamento e per invii per copertura, non per views. Un
reel con 4.000 views e 90 invii ha battuto quello con 60.000 views e 11.

## Poi cerca lo schema

Con i primi cinque e gli ultimi cinque affiancati, cerca cosa li separa, e sii
pronto a concludere qualcosa che all'utente non piacerà:

- **Tenuta a 3 secondi.** Se i migliori e i peggiori differiscono qui, è l'hook e
  nient'altro, e tutto ciò che viene dopo è una distrazione.
- **Formula di hook.** Quali id di `ig-reel/hooks.json` ci sono nei primi cinque?
- **Formato.** Reel, carosello, immagine singola.
- **Durata.** Raggruppa in sotto 15s, da 15 a 30s, da 30 a 60s, oltre 60s.
- **Tema.**
- **Se l'utente ha risposto ai commenti nella prima ora.**
- **Giorno e ora.** Controllalo **per ultimo** e solo se il resto non mostra niente.
  Quasi mai è la causa ed è dove la gente vorrebbe che fosse.

Presenta il risultato come un'affermazione con la prova allegata, e di' quanto sei
sicuro. Con 30 post si vede uno schema. Con 6 no, e dirlo è meglio che inventarne
uno.

## La distinzione che fa risparmiare mesi

**Un reel che fa views e nessun follow non è un reel fallito, è un problema di
profilo.** Un reel che non fa views è un problema di hook. Separa le due cose
prima di consigliare qualsiasi cosa. Se la copertura da non follower è alta e i
follow per copertura sono bassi, smetti di riscrivere hook e vai a `/ig-profile`.

## Output

(Esempio del formato: i numeri vengono dalle statistiche dell'utente, non inventarli.)

```
AUDIT  ·  31 post  ·  12 giu - 5 set  ·  views mediane 4.100

PRIMI 5 PER MULTIPLO DI SCOSTAMENTO
  18,2x  #3  Nessuno Te Lo Dice   74.600 views  62% non follower  tenuta@3s 71%  128 invii
   6,4x  #1  Confessione Costo    26.300 views  48% non follower  tenuta@3s 64%   71 invii
  ...

ULTIMI 5
   0,3x  #11 Numerato              1.200 views   9% non follower  tenuta@3s 31%    2 invii
  ...

COSA DICONO I DATI
1. La tenuta a 3 secondi è tutta la storia. I primi cinque in media 66%, gli ultimi
   cinque 33%. Tutto il resto che ti preoccupa viene dopo i primi due secondi.
2. I post in cui eri tu quello che ci faceva la figura peggiore: media 8,1x contro
   0,9x per tutto il resto. n=5. È il segnale più forte e non c'è paragone.
3. Gli elenchi di strumenti fanno views e basta. Copertura alta, niente invii,
   niente follow. Tre dei tuoi ultimi cinque.
4. Il giorno della settimana non mostra niente. Le medie di martedì e venerdì
   stanno dentro il rumore. Smetti di ottimizzarlo.

SMETTI: gli elenchi.
FAI DI PIÙ: quelli con un costo che hai pagato e un numero attaccato.
```

Poi passa le conclusioni a `/ig-plan` così la settimana successiva si costruisce
sulle prove dell'utente e non sui valori predefiniti, e a `/ig-viral` così lo swipe
file viene filtrato sulle formule che funzionano per questo account in particolare.
