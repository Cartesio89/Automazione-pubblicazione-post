---
name: ig-plan
description: >-
  Costruisce la settimana su Instagram: cosa pubblicare, in che formato, quando e
  con chi interagire. Usala quando l'utente dice "pianifica la mia settimana",
  "cosa dovrei pubblicare", "calendario editoriale", "non ho niente da
  pubblicare", o vuole un calendario di pubblicazione e un elenco di interazioni.
---

# ig-plan

La sala di controllo. Tutto il resto di questo pacchetto esegue; questa decide cosa
viene eseguito. Lanciala una volta a settimana, sempre lo stesso giorno.

## Input

Se esistono `~/.claude/instagram/voice.md`, `swipe.md` e `log.md` (su Windows:
`%USERPROFILE%\.claude\instagram\`), leggili. Lo swipe file è la prova diretta
dell'utente, da `/ig-viral`, su quali formule stanno funzionando adesso nella sua
nicchia, e vale più di qualsiasi cosa in questo file. Il log evita che il piano
ripeta un tema delle ultime due settimane.

Se non esistono, chiedi quattro cose e scrivile:

1. Cosa vende l'utente, e a chi.
2. I tre o quattro temi per cui vuole essere conosciuto.
3. Cosa è successo davvero questa settimana: una chiamata con un cliente, un
   numero, un errore, una cosa costruita, una discussione. È da qui che nascono i
   post.
4. Dieci account a cui vale la pena essere visibili.

## Cosa pubblicare

Da quattro a cinque post a settimana, e almeno tre sono Reel. I Reel sono l'unico
formato di Instagram che raggiunge in modo affidabile chi non segue l'account. I
caroselli vanno in profondità con chi lo segue già. Le storie sono quotidiane e si
pianificano a parte.

Mescola nella settimana, mai due dello stesso tipo di fila:

| tipo | quota | compito |
| --- | --- | --- |
| **Prova** | 1 a settimana | qualcosa che è successo, con un numero. Reel. |
| **Insegna** | da 1 a 2 a settimana | una cosa che chi guarda può fare oggi. Reel o carosello. |
| **Opinione** | 1 a settimana | una posizione che potrebbe farti perdere follower. Reel. |
| **Storia** | 1 ogni due settimane | una scena con un costo. Reel. |
| **Offerta** | 1 ogni due settimane | cosa vendi, detto chiaramente, senza scusarti. Carosello o storie. |

Per ogni slot dai: il tema, l'angolo specifico preso da ciò che è successo davvero
questa settimana, il formato e il numero della formula di hook da
`ig-reel/hooks.json`. Non un argomento, un angolo. "L'IA" non è un piano. "Il
preventivo che abbiamo perso perché la bozza aveva un trattino lungo" è un Reel.

## Quando pubblicare

Pubblica quando il pubblico dell'utente è sveglio e non al lavoro. Per la maggior
parte dei pubblici consumer è la prima serata, ora italiana; per un pubblico
business, la mattina presto.

Ma dillo chiaramente: **l'ora conta molto meno dei primi due secondi.** Instagram
continuerà a mostrare un Reel per giorni se rende, e seppellirà uno ben
programmato che non rende. Se l'utente ottimizza gli orari prima che i suoi hook
funzionino, sta lucidando la cosa sbagliata, e glielo devi dire.

Ancora gli orari al fuso del pubblico, non dell'utente, se sono diversi.

## Il giro di interazioni, che non è facoltativo

20 minuti al giorno, prima di pubblicare, non dopo. Costruisci un elenco di 10:

- **5 di portata** - account con un pubblico che l'utente vuole, dove un buon
  commento viene visto. Commenta presto, prima che il thread arrivi a 200.
- **3 pari** - stessa dimensione, stesso campo. È il gruppo che ricambia.
- **2 acquirenti** - persone che potrebbero davvero comprare. Commenta per
  settimane prima di qualsiasi DM, e non fare mai promozione in un commento.

Passa l'elenco a `/ig-comment`.

## Output

(Esempio del formato: ora e contenuti sono illustrativi, non una raccomandazione di calendario provata.)

```
SETTIMANA DEL 15 SETTEMBRE

LUN  solo interazioni  (20 min, elenco sotto)
MAR  19:30  REEL       PROVA     #5  Il Tempo Che Crolla - preventivo da 5 ore a 20 minuti
MER  solo storie + interazioni
GIO  19:00  CAROSELLO  INSEGNA   Didascalia B           - la clausola spiegata in 4 slide
VEN  19:30  REEL       OPINIONE  #2  Il Comando Negativo - smetti di fare chiamate di scoperta
SAB  -
DOM  18:00  REEL       STORIA    #21 Attacco a Metà Frase - l'email di rimborso

STORIE  ogni giorno, da 3 a 5 fotogrammi, box domande il giovedì.

INTERAZIONI  (5 portata / 3 pari / 2 acquirenti)
  ...

Di' "scrivi martedì" e lo preparo.
```

Scrivi il piano in `~/.claude/instagram/plan.md` così le altre skill possono
leggerlo. Non viene programmato né pubblicato niente da nessuna parte. È un piano e
lo esegue l'utente.
