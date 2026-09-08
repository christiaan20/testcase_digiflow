# testcase_digiflow

A minimal FastAPI boilerplate that loads a local `.pdf` file from the repository and returns its content through an API endpoint.

## Project structure

- `app/main.py` - FastAPI entrypoint
- `app/services/file_loader.py` - file loading helper
- `data/sample.pdf` - local pdf file read by the API
- `tests/test_main.py` - basic API tests

## Install

### Powershell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Bash
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```powershell
uvicorn app.main:app --reload
```

Then open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/file`

## Example request

Send a `POST` request to `/file` with a repository-relative `.pdf` path in JSON:

```json
{
  "path": "data/sample.pdf"
}
```

Example response:

```json
{
  "path": "data/sample.pdf",
  "content": "Hello from the repository pdf file!\nThis content is loaded by FastAPI.\n"
}
```

The `/file` endpoint reads the requested local `.pdf` file, prints the pdf content to the server console, and returns it as JSON.

Accepted paths must:

- be relative to the repository root
- stay inside the repository
- point to a `.pdf` file

## Test

```powershell
pytest
```
