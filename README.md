# testcase_digiflow

A minimal FastAPI boilerplate that loads a local `.pdf` file from the repository and returns its content through an API endpoint.

## Project structure

- `app/main.py` - FastAPI entrypoint
- `app/services/file_loader.py` - file loading helper
- `app/services/comment_operations.py` - comment operations with pikepdf
- `app/services/analyse_pdf.py` - prints the properties of comments in a pdf
- `data/*` - local pdf files read by the API
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

- `http://127.0.0.1:8000/docs`  
There you will find a documentation page where you can test the API's as shown below
## Example request
### analyze_pdf_comments
Send a `POST` request to `/analyze_pdf_comments` with a repository-relative `.pdf` path in JSON:

```json
{
  "path": "data/sample1.pdf"
}
```

Example response:

```json
{
  "path": "data/example_1.pdf"
}
```

The `/analyze_pdf_comments` endpoint reads the requested local `.pdf` file, prints the pdf annotation information to the server console.

### fixComments
Send a `POST` request to `/fixComments` with a repository-relative `.pdf` path in JSON:

```json
{
  "path": "data/sample1.pdf"
}
```

Example response:

```json
{
  "path": "data/example_1.pdf"
}
```

The `/fixComments` endpoint reads the requested local `.pdf` file and writes a copy of it to the output directory.  
This API needs to be completed to detect invisible comments and fix them.

Accepted paths must:

- be relative to the repository root
- stay inside the repository
- point to a `.pdf` file

## Test

```powershell
pytest
```
