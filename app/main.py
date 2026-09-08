from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.services.file_loader import load_pdf_file


class FileRequest(BaseModel):
    path: str = Field(
        ...,
        description="Repository-relative path to a local .pdf file.",
        examples=["data/sample.pdf"],
    )

app = FastAPI(
    title="FastAPI Text File Boilerplate",
    description="A minimal API that loads a local .pdf file from the repository and returns its content.",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "FastAPI is running. Call POST /file with a JSON body to load a repository pdf file."
    }


@app.post("/file")
def read_file(request: FileRequest) -> dict[str, str]:
    try:
        content = load_pdf_file(request.path)
    except (ValueError, IsADirectoryError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    print(content)
    return {"path": request.path, "content": content}