from pathlib import Path



from fastapi import Depends, FastAPI, HTTPException


from pydantic import BaseModel, Field

from app.services import comment_operations
from app.services.analyse_pdf import show_comment_data
from app.services.file_loader import load_pdf_file




class FileRequest(BaseModel):
    path: str = Field(
        ...,
        description="Repository-relative path to a local .pdf file.",
        examples=["data/example_1.pdf"],
    )

app = FastAPI(
    title="FastAPI Text File Boilerplate",
    description="A minimal API that loads a local .pdf file from the repository and returns its content.",
    version="0.1.0"
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "FastAPI is running. Call POST /file with a JSON body to load a repository pdf file."
    }


@app.post("/analyze_pdf_comments")
def analyze_pdf_comments(request: FileRequest) -> dict[str, str]:
    try:
        pdf = load_pdf_file(request.path)
    except (ValueError, IsADirectoryError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    show_comment_data(pdf,print_info=True)


    return {"path": request.path}

@app.post("/fixComments")
def fix_comments(request: FileRequest) -> dict[str, str]:

    pdf = load_pdf_file(request.path)

    request_path = Path(request.path)
    output_path = Path("output") / request_path.name

    # code to detect and fix comments

    # end code to detect and fix comment
    pdf.save(output_path)


    return {"path": request.path}