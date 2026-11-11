# FastAPI VADER v1

A FastAPI version of [Pyronaut VADER v1](https://github.com/sachin-pikle/pyronaut-vader-v1), with the same review form, file preview, sample reviews, sentiment output, and JSON API.

## Dependencies

- CPython 3.14.3
- FastAPI 0.162.4
- Uvicorn 0.54.0 with standard extras
- `vaderSentiment` 3.3.2

These versions are pinned in `requirements.txt` and tested with this demo.

## Run

Select CPython 3.14.3 with `pyenv`, then create the project environment:

```bash
pyenv local 3.14.3
python --version
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`pyenv local` records the selection in `.python-version`. FastAPI uses CPython here; the Pyronaut demos use GraalPy.

Start the FastAPI application with Uvicorn:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
```

Open [http://localhost:8080](http://localhost:8080), choose a file under `samples/`, and select **Run VADER in FastAPI**. Press `Ctrl+C` in the terminal to stop the server.

## API

The browser posts the review text as JSON to the same endpoint as the Pyronaut version:

```bash
curl -X POST http://localhost:8080/api/reviews/analyze \
  -H 'Content-Type: application/json' \
  -d '{"text":"I love this coffee grinder. It works perfectly!"}'
```

Example response:

```json
{"label":"positive","compound":0.8655,"positive":0.592,"neutral":0.408,"negative":0.0}
```

Blank or whitespace-only review text returns `400 Bad Request`:

```bash
curl -i -X POST http://localhost:8080/api/reviews/analyze \
  -H 'Content-Type: application/json' \
  -d '{"text":""}'
```

## Implementation

FastAPI validates the JSON request and calls the sentiment function. Uvicorn serves the ASGI application. VADER returns the sentiment scores. The app labels compound scores of `0.05` or higher as **positive**, `-0.05` or lower as **negative**, and scores between them as **neutral**.

For an end-to-end performance comparison, run both apps on the same machine with the same requests and warm-up.

## Clean up

- Stop Uvicorn with `Ctrl+C`.
- If the project's `.venv` is active, deactivate it:

  ```bash
  deactivate
  ```

- From the project directory, remove the environment and Python cache:

  ```bash
  rm -rf .venv app/__pycache__
  ```

To set up and run the app again, follow the steps in [Run](#run).
