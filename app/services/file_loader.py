from pathlib import Path
from pikepdf import Name, Pdf

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def resolve_repo_file(relative_path: str) -> Path:
    """Resolve a repository-relative .pdf file path safely."""
    cleaned_path = relative_path.strip()
    requested_path = Path(cleaned_path)
    resolved_path = (PROJECT_ROOT / requested_path).resolve()


    resolved_path.relative_to(PROJECT_ROOT)

    return resolved_path


def load_pdf_file(relative_path: str) -> Pdf:
    """Load a UTF-8 pdf file from the repository using a relative path."""
    target_file = resolve_repo_file(relative_path)

    pdf = Pdf.open(target_file)


    if not target_file.exists():
        raise FileNotFoundError(f"Text file not found: {relative_path}")

    return pdf
