# Assignment 1 - Processo e Sviluppo del Software

## Membri
- Ficara Damiano (919386)
- Ricci Claudio (918956)
- Toli Emilio ()

## Introduzione
Il primo Assignment del corso di Processo e Sviluppo del Software si pone come obiettivo la realizzazione di una Pipeline CI/CD che automatizzi il processo di manutenzione di un'applicazione seguendo l'insieme di pratiche DEVOPS, mirando ad abbreviare il ciclo di vita di sviluppo di un sistema e soprattutto fornendo una consegna continua di software qualitativamente elevato.

## Applicazione
L'obiettivo principale dell'assignment non è l'implementazione dell'applicazione in sé. Pertanto, è stata scelta la realizzazione di un sistema estremamente semplice denominato "Views Counter". Questo sistema fa uso del database Firebase per tenere traccia del numero di visualizzazioni effettuate da ciascun utente all'interno del sistema.

All'avvio dell'applicazione, agli utenti viene richiesto di specificare il proprio nome. L'applicazione verifica quindi se tale nome è già presente nel database. Nel caso affermativo, il sistema incrementa il conteggio delle visualizzazioni associate a quell'utente e restituisce il valore aggiornato. Se, invece, si tratta della prima volta in cui quel nome viene inserito, il sistema restituisce un valore iniziale di 1.

## Stages
Di seguito vengono elencate le fasi da implementare necessarie allo svolgimento dell'assignment:
- Build
- Verify
- Unit-test
- Integration-test
- Package
- Release
- Deploy

### Prerequisiti
In questa sezione, vengono forniti alcuni prerequisiti che vengono eseguiti prima dell'avvio dello script con le fasi elencate in precedenza:
- La pipeline utilizza l'immagine Docker Python più recente come base, definita come segue: `image: python:latest`.
- Viene definita una variabile globale denominata `PIP_CACHE_DIR`, il cui percorso è impostato su `"$CI_PROJECT_DIR/.cache/pip"`.\\
L'utilizzo della cache in una pipeline riveste un ruolo fondamentale nel migliorare l'efficienza, la velocità e la coerenza del processo di sviluppo del software. Tale pratica consente di ottimizzare l'uso delle risorse e garantisce un flusso di lavoro più agevole.
- Inoltre, viene attivato un ambiente virtuale per isolare tutte le operazioni Python all'interno del progetto. Questo ambiente consente di installare e gestire le dipendenze specifiche per il progetto senza interferire con il sistema globale.

### Build
La compilazione del progetto avviene mediante il comando seguente:\\
`pip install -r requirements.txt`\\
Questo metodo consente di semplificare il processo di installazione delle librerie esterne richieste per l'esecuzione dell'applicazione. Al posto di elencare manualmente tutte le librerie e le rispettive versioni, vengono specificate nel file di testo "requirements.txt" le librerie necessarie. Se a fianco del nome della libreria non è specificata nessuna versione, significa che si prende quella più recente.

### Verify
La fase di "verify" nella pipeline di sviluppo utilizza due comandi per eseguire controlli di qualità del codice e identificare possibili problematiche di sicurezza prima di procedere ulteriormente nello sviluppo dell'applicazione. I comandi eseguiti sono:
- `prospector`, il quale esegue l'analisi statica del codice alla ricerca di possibili problemi di stile, conformità alle linee guida di codifica, e altre metriche di qualità del codice.
- `bandit` strumento di analisi statica progettato specificamente per la ricerca di vulnerabilità di sicurezza nel codice Python. Esegue un controllo approfondito del codice alla ricerca di possibili debolezze e vulnerabilità, segnalando qualsiasi potenziale problema di sicurezza che richiede attenzione.

### Unit-test
Un test di unità ha lo scopo di verificare il corretto funzionamento di una singola unità di codice, come un metodo, una funzione o una classe, in modo indipendente dal resto del sistema. In questo contesto, è stato creato un file denominato *test_unit.py* contenente una funzione di test. Questa funzione verifica il collegamento al database, restituendo `True` se la connessione è attiva.\\
Per eseguire il test di unità all'interno di una pipeline, è possibile utilizzare il seguente comando:\\
`pytest tests/test_unit.py`\\
Questo comando fa uso della libreria di testing pytest per eseguire il test specifico contenuto nel file *test_unit.py*. Il risultato dell'esecuzione fornirà un responso sul corretto funzionamento del collegamento al database. Se il test restituisce `True`, indica che il collegamento è attivo, confermando il successo del test e la validità della connessione al database.


### Integration-test
