# spendwise
## Descrizione app
L'app spendwise è una semplice applicazione scritta in python per la gestione delle spese quotidiane.
Essa segue un architettura app+db. Il db è composto da una singola tabella spese contentente tutti i dettagli delle spese.
L'applicazione permette all'utente di aggiungere, modificare o eliminare una spesa dal db. Una volta inserite le spese, permette di conoscere il totale delle spese effettuate, stampandole in una tabella.

## Descrizione pipeline
La nostra pipeline è divisa nei seguenti stage:
* Build: Installa le dipendenze del progetto
* Verify: Esegue prospector e bandit in duo job differenti, per eseguire l'analisi statica e dinamica del codice    
          python.
* unit-test: Esegue i test d'unità sull'applicazione usando la libreria pytest.
* integration-test: Esegue i test d'Integrazione sull'applicazione usando la libreria pytest.
* package: Crea il pacchetto che verrà poi rilasciato negli stage successivi, utilizzando la libreria setuptools e 
           wheel.
* release: Rilascia il pacchetto utilizzando twine su PyPi.
* docs: Crea la documentazione del progetto utilizzando mkdocs e la pubblica su gitlab pages.

## Condizioni di esecuzione degli stage della pipeline
* Build: sempre.
* Verify: Quando viene modificato un file all'interno della directory app/* o un file di configurazione prospector o 
         bandit.
* unit-test: Quando viene modificato un file all'interno della directory app/* .
* integration-test: Quando viene modificato un file all'interno della directory app/* .
* package: Quando viene effettuato un commit con un tag associato.
* release: Quando viene effettuato un commit con un tag associato.
* docs: Quando viene modificato un file nella directory docs, o un file di configurazione mkdocs.yml

## Altre istruzioni
* before_script: viene eseguito prima di ogni stage eccetto il build e serve per installare le dipendenze presenti nella cache. 
* variables: dichiarazione delle variabili globali utilizzate nella pipeline
* cache: vengono specificate le directory usate per salvare i dati nella cache.

## Membri progetto
* Alberto Varisco 866109
* Mattia Milanese 869161
* Oscar Sacilotto 866040

## Link vari
   repository: https://gitlab.com/2023_assignment1_spendwise/spendwise
   docs: https://spendwise-2023-assignment1-spendwise-db02e21ef2c47c900d1903f51e.gitlab.io