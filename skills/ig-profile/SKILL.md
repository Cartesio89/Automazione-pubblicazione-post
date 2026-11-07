---
name: ig-profile
description: >-
  Dà un punteggio su 100 a un profilo Instagram secondo una griglia in 12 punti e
  riscrive le parti che perdono punti: campo nome, bio, link, in evidenza, i tre
  fissati, griglia. Usala quando l'utente dice "ottimizza il mio profilo", "sistema
  la mia bio", "valuta il mio Instagram", "perché non mi seguono", o incolla il suo
  profilo e chiede come si legge.
---

# ig-profile

Quasi tutti ottimizzano la cosa sbagliata. Il profilo non è una vetrina che la
gente sfoglia. È una **schermata di decisione**, a cui si arriva da un reel, e ha
circa tre secondi per rispondere a una domanda: qui ce n'è dell'altro, ed è per me?

## Input

Chiedi all'utente di incollare o fotografare: il campo nome, l'handle, la bio,
dove punta il link, i nomi delle storie in evidenza, cosa è fissato e le prime nove
copertine della griglia. Uno screenshot della parte alta del profilo più le prime
due righe della griglia basta per un primo giro.

Non accedere a Instagram al posto suo.

## Dai il punteggio

Leggi `rubric.json` in questa cartella. Dodici voci, 100 punti, ognuna con come
appaiono i punti pieni e come di solito fallisce. Valuta ogni voce, mostra la
tabella, dai il totale. Sii onesto. La maggior parte dei profili al primo giro
finisce sui 30-40 punti e un punteggio generoso non serve a niente.

```
PUNTEGGIO PROFILO  38/100          (esempio del formato)

  campo nome         2/12   solo il nome, nessuna parola che qualcuno cerca
  prima riga bio     3/12   tre sostantivi e un'emoji di caffè
  i tre fissati      0/10   niente fissato
  in evidenza        2/8    "Varie", "Vita", "2023"
  leggibilità griglia 4/8   sei copertine su nove sono una faccia a metà frase
  ...
```

## Poi riscrivi, in quest'ordine

Correggi in ordine decrescente di punti persi. Non riscrivere tutto insieme:
l'utente deve davvero andare a cambiare ognuna di queste cose.

**1. Il campo nome (30 caratteri).** La riga in grassetto sotto la foto, non
l'handle. È il campo con cui la ricerca di Instagram fa il confronto, e la maggior
parte degli account ci mette un nome e basta. Formato che funziona:
`{Nome} | {cosa fai, con parole che si cercano}`. Dai tre opzioni. Es.:
`Marco Rossi | Consulente partita IVA`, scelto con le parole che un italiano
scriverebbe nella ricerca.

**2. Prima riga della bio.** Per chi è e cosa cambia. Non un titolo di lavoro, non
aggettivi, non un elenco di identità separate da barre. Il resto dei 150 caratteri
porta una prova o un'offerta semplice.

**3. I tre fissati.** Tre posti, tre compiti diversi: la prova migliore, la
spiegazione più chiara dell'offerta, la migliore presentazione della persona. È la
correzione con la leva più alta di tutto il profilo e richiede quattro tocchi. Una
griglia senza fissati mostra l'ultima cosa pubblicata, che è un testa o croce.

**4. Le storie in evidenza.** Da quattro a sei, con i nomi delle domande che fa un
acquirente: Prezzi, Risultati, Come funziona, Chi sono. Non "Varie". Elimina il
resto.

**5. Il link.** Una sola destinazione coerente con ciò che la bio ha appena
promesso. Ne sono ammessi cinque; due è già un menu e un menu converte peggio di una
porta.

**6. Le copertine della griglia.** Le prime nove in miniatura. Le copertine dei
reel si scelgono, non si lasciano al fotogramma uno qualsiasi. Quattro parole di
testo su una copertina rendono la griglia leggibile a colpo d'occhio.

## Output

Tabella dei punteggi, poi le riscritture come blocchi pronti da copiare in ordine
di priorità, ciascuna passata in `/ig-human`. Rivaluta alla fine e mostra la
differenza onestamente. Se la riscrittura arriva a 84 e non a 98, di' 84, e di' cosa
serve per il resto, che di solito è una griglia, l'abitudine alle storie e un post
fissato che non esiste ancora. Niente di tutto questo è una riscrittura.

Questa skill non salva niente su Instagram. L'utente modifica ogni campo.
