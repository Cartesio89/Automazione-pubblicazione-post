---
name: ig-comment
description: >-
  Scrive commenti, in italiano, ai post e ai reel di altre persone su Instagram
  che sembrino di una persona con un'opinione e non di un bot. Usala quando
  l'utente incolla un post o un reel e vuole un commento, dice "commenta questo",
  "interagisci con questo", "cosa scrivo qui", o vuole una serie per il suo giro
  quotidiano di interazioni.
---

# ig-comment

Commentare sono i venti minuti con la leva più alta su Instagram e i più facili da
fare male. Un commento in alto sotto un reel da 40.000 views viene visto da più
persone della maggior parte dei post degli account stessi, ed è l'unico punto in
cui uno sconosciuto può toccare e arrivare direttamente a un profilo.

Un commento generico è peggio di nessun commento. Costa un tocco che non porta da
nessuna parte e segna l'account come un account da gruppo di scambio di
interazioni agli occhi dell'unica persona la cui opinione contava: il creator.

## Input

L'utente incolla il testo del post o del reel, o uno screenshot, con il nome
dell'account. Se dà un URL che non puoi aprire, chiedigli di incollare. Non usare
uno strumento di navigazione per fare scraping del feed e non pubblicare niente.

## I nove tipi di commento

Scegli in base a cosa è davvero il post. Non ripiegare mai sul tipo 1.

| # | tipo | quando | forma |
| --- | --- | --- | --- |
| 1 | **Aggiungi un dato** | il post fa un'affermazione che puoi sostenere con un numero | "Da noi uguale: il 40% di..." |
| 2 | **Aggiungi il caso mancante** | il post ha ragione ma è incompleto | "Vale finché {condizione}." |
| 3 | **Disaccordo rispettoso** | pensi davvero che sia sbagliato | nomina prima l'accordo, poi il bivio |
| 4 | **Estendi una riga** | una riga è quella buona | citala, costruiscici sopra |
| 5 | **La vera domanda** | il post ha saltato la parte difficile | una domanda, precisa |
| 6 | **Lo scontrino** | hai fatto la cosa che descrivono | cosa è successo, due frasi |
| 7 | **La correzione** | c'è un errore di fatto | abbi ragione, sii breve, gentile, sicuro |
| 8 | **Il cambio di cornice** | fatti giusti, cornice sbagliata | "Un altro modo di leggerlo:" |
| 9 | **La battuta** | il post non ha bisogno di niente, vuoi esserci | sotto le 10 parole, deve far ridere o essere vera |

## Regole

- **Da una a tre frasi.** I commenti di Instagram si leggono in una colonna stretta
  sotto un video. Un paragrafo viene ripiegato dietro "altro" e nessuno lo tocca.
- **Non iniziare mai con** "Bellissimo post", "Che bello", "Grande!", "Verissimo",
  "Top!", "Complimenti", "Aggiudicato", "Ne avevo bisogno oggi", "Questo 👏", né con
  il nome del creator seguito da un punto esclamativo. Sono tutti invisibili.
- **Niente commenti di sole emoji** e niente emoji come primo carattere.
- **Non riassumere mai il reel.** Tutti quelli che guardano l'hanno appena visto.
- **Un'idea.** Un commento con due punti sembra un dirottamento.
- **Di' la cosa specifica.** Se il commento potrebbe stare sotto qualsiasi post
  sull'argomento, non è un commento, è rumore.
- **Mai promuoversi.** Né l'offerta, né il link, né "passa dal mio profilo". È il
  modo più rapido di essere bloccati proprio dalla persona che volevi raggiungere.
- **Presto conta più qui che altrove.** Un commento nella prima ora su un reel che
  poi viaggia viene portato con sé.
- **Registro:** dai del tu o del voi come nella voce dell'utente (`voice.md`). Se
  il creator è un'azienda o una persona molto più anziana nel settore, resta
  cordiale ma non troppo confidenziale. Niente "ciao ciao" né "carissimo".

## Output

Dai **due opzioni di tipo diverso**, con etichetta, più una riga su quale
pubblicheresti e perché. Passa entrambe in `/ig-human` prima: i commenti sono
corti, quindi un trattino lungo o una frase fatta pesano in proporzione più che in
una didascalia.

```
OPZIONI DI COMMENTO  (sotto il reel di @account sui prezzi)      (esempio del formato)

[6 · Scontrino]
Noi li abbiamo alzati del 40% lo scorso marzo e abbiamo perso un solo cliente,
quello che occupava metà della posta. Ci sono voluti otto mesi per non
averne più paura.

[3 · Disaccordo rispettoso]
D'accordo sull'ancoraggio. Dove farei resistenza è farlo a progetto in corso.
Noi l'abbiamo provato e ci è costato un rinnovo che sarebbe andato bene.

Pubblica il primo. Cede qualcosa e ha dentro un numero.
```

## Modalità serie

Per un giro di interazioni, chiedi da 5 a 10 post incollati come testo in un unico
messaggio, restituisci un commento per ciascuno in un solo blocco e tieni una nota
in corso in `~/.claude/instagram/log.md` di chi è stato commentato questa
settimana. Commentare gli stessi tre account ogni giorno si vede e sembra
esattamente ciò che è.

## Mai

Non pubblicare in automatico, non automatizzare i commenti e non usare uno
strumento di navigazione per pubblicare al posto dell'utente. L'interazione
automatica viola i Termini d'uso di Instagram e fa bloccare le azioni degli
account. Questa skill scrive il commento. L'utente lo pubblica.
