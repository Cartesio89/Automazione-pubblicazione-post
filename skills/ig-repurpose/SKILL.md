---
name: ig-repurpose
description: >-
  Trasforma un solo contenuto lungo (un video di YouTube, un podcast, una diretta,
  una newsletter, un articolo o una chiamata con un cliente) in una settimana di
  reel e caroselli in italiano. Usala quando l'utente dice "riutilizza questo",
  "trasformalo in reel", "ho un video/podcast/trascrizione", "tagliamolo a pezzi",
  o incolla qualcosa di lungo e lo vuole su Instagram.
---

# ig-repurpose

Un buon contenuto lungo contiene da quattro a sei post. La maggior parte della
gente ne estrae uno e butta via il resto.

## Input

Una trascrizione, un articolo, una newsletter, uno script, il riassunto di una
chiamata, una diretta. Se l'utente dà un URL e questa sessione ha uno strumento di
trascrizione, usalo; altrimenti chiedigli di incollare. Leggi tutto prima di
estrarre qualsiasi cosa.

Se la fonte è un video dell'utente, chiedi anche il file. Un Reel costruito sulle
sue riprese batte uno costruito sulle sue parole lette di nuovo.

Se la fonte è un contenuto in italiano parlato (podcast, diretta), la trascrizione
automatica spesso sbaglia nomi propri, numeri e termini tecnici inglesi: controllali
con l'utente prima di usarli in un reel.

## Estrai, non riassumere

Il riassunto di un video non è un Reel. Nessuno vuole il riassunto. Scorri il
contenuto e tira fuori le cose che stanno in piedi da sole:

| cosa estrarre | cos'è |
| --- | --- |
| **Affermazioni** | ogni frase che farebbe partire una discussione |
| **Numeri** | ogni cifra, costo, durata, percentuale |
| **Storie** | ogni momento con una persona, una scena e un costo |
| **Meccanismi** | ogni "il modo in cui funziona davvero è..." |
| **Errori** | ogni ammissione di qualcosa andato male |
| **Frasi** | ogni frase già citabile così com'è |

Elenca ciò che hai trovato, con i conteggi, prima di scrivere qualsiasi cosa. Se il
contenuto dà meno di quattro elementi, è magro, e anche quattro post spremuti da lì
saranno magri. Dillo.

## Poi scegli il formato per ogni estratto

Non tutto è un Reel.

- **Affermazione, errore, storia** vanno in un Reel. Hanno bisogno di una voce e di
  una faccia.
- **Meccanismo, elenco numerato** vanno in un carosello. Hanno bisogno di essere
  riletti.
- **Una frase citabile** va in un fotogramma di storia, non in un post.

## Poi costruisci la settimana

Ogni estratto diventa un post e ogni post sta in piedi completamente da solo. Chi
guarda non ha visto la fonte e non la vedrà mai. Non scrivere mai "come ho detto
nel mio ultimo video". Il post è la cosa.

Assegna a ciascuno una formula di hook da `ig-reel/hooks.json` e variale. Cinque
post dalla stessa fonte con la stessa forma di hook sembrano una fabbrica di
contenuti, perché lo sono.

Se la fonte è un video dell'utente, **usa le riprese vere**. La clip in cui ha detto
la cosa, con la reazione vera dentro, batte una nuova registrazione ogni volta.
Taglia sulla frase, non sul respiro.

Ordina nella settimana in modo che l'affermazione più forte venga per prima, la
storia arrivi a metà settimana e il meccanismo per ultimo, quando chi ha apprezzato
i precedenti lo sta aspettando.

## Output

(Esempio del formato: i conteggi vengono dalla lettura della fonte, non inventarli.)

```
FONTE: "Perché abbiamo eliminato le chiamate di scoperta" (podcast da 42 min, 8.900 parole)

TROVATI  5 affermazioni, 9 numeri, 3 storie, 4 meccanismi, 2 errori, 7 frasi citabili

SETTIMANA
MAR  REEL      #2  Il Comando Negativo   Smetti di fare chiamate di scoperta
                                         usa la clip del minuto 14:20, lui ride alla fine
MER  CAROSELLO     Didascalia B          Il modulo da 4 domande che ha sostituito la chiamata
VEN  REEL      #21 Attacco a Metà Frase  "...ed è lì che mi ha chiesto il rimborso, nove giorni dopo"
DOM  REEL      #5  Il Tempo Che Crolla   Sei ore a settimana indietro, un link cancellato

Di' "scrivi martedì" e lo preparo.
```

Poi prepara su richiesta, uno alla volta, ciascuno passando da `/ig-reel` e
`/ig-human`. Non scaricare quattro script finiti in una volta. Suoneranno tutti
uguali e l'utente non ne girerà nessuno.
