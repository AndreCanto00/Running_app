# Running_app

[![Makefile CI](https://github.com/AndreCanto00/Running_app/actions/workflows/makefile.yml/badge.svg)](https://github.com/AndreCanto00/Running_app/actions/workflows/makefile.yml)

## Descrizione

Running_app è un'applicazione per calcolare il carico di allenamento utilizzando diverse metriche come TRIMP, TRIMP_LT e HRRS. L'applicazione offre sia un'interfaccia a riga di comando (CLI) che un'API web basata su FastAPI.

## Installazione

Per installare le dipendenze necessarie, eseguire il seguente comando:

```sh
make install
```

## Uso

### CLI

Per utilizzare la CLI, eseguire uno dei seguenti comandi:

```sh
python loadCLI.py trimp
python loadCLI.py trimp_lt
python loadCLI.py hrrs
```

### API Web

Per avviare il server FastAPI, eseguire:

```sh
uvicorn main:app --host 0.0.0.0 --port 8080
```

L'API sarà disponibile all'indirizzo `http://localhost:8080`.

#### Endpoint

- `GET /`: Restituisce un messaggio di benvenuto.
- `POST /trimp/`: Calcola il valore TRIMP.
- `POST /trimp_lt/`: Calcola il valore TRIMP_LT.
- `POST /hrrs/`: Calcola il valore HRRS.

## Test

Per eseguire i test, utilizzare il seguente comando:

```sh
make test
```

## Formattazione e Linting

Per formattare il codice e controllare lo stile, eseguire:

```sh
make format
make lint
```

## Contributi

I contributi sono benvenuti! Sentiti libero di aprire issue e pull request.

## Licenza

Questo progetto è distribuito sotto la licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

## AWS App Runner

Per il deployment su AWS App Runner, utilizziamo il file `apprunner.yaml`. Questo file contiene le configurazioni necessarie per eseguire l'applicazione su AWS App Runner.

### Configurazione

Il file `apprunner.yaml` include le seguenti sezioni:

- `version`: La versione del file di configurazione.
- `runtime`: Il runtime utilizzato dall'applicazione (in questo caso, Python 3).
- `build`: I comandi necessari per costruire l'applicazione.
- `run`: Il comando per eseguire l'applicazione e la configurazione della rete.

### Esempio di `apprunner.yaml`

```yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - pip install -r requirements.txt
run:
  command: python -m uvicorn main:app --host 0.0.0.0 --port 8080
  network:
    port: 8080
```

### Deployment

Per effettuare il deployment su AWS App Runner, seguire questi passaggi:

1. Accedere alla console AWS e navigare su App Runner.
2. Creare un nuovo servizio App Runner.
3. Selezionare il repository del codice sorgente (ad esempio, GitHub) e configurare il collegamento.
4. Caricare il file `apprunner.yaml` come configurazione del servizio.
5. Avviare il servizio e attendere che il deployment sia completato.

Una volta completato, l'applicazione sarà disponibile all'indirizzo fornito da AWS App Runner.
