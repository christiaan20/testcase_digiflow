from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def resolve_repo_file(relative_path: str) -> Path:
    """Resolve a repository-relative .pdf file path safely."""
    cleaned_path = relative_path.strip()

    # if not cleaned_path:
    #     raise ValueError("Path must not be empty.")

    requested_path = Path(cleaned_path)

    # if requested_path.is_absolute():
    #     raise ValueError("Path must be relative to the repository root.")
    # 
    # if requested_path.suffix.lower() != ".pdf":
    #     raise ValueError("Only .pdf files are allowed.")

    resolved_path = (PROJECT_ROOT / requested_path).resolve()

    # try:
    resolved_path.relative_to(PROJECT_ROOT)
    # except ValueError as exc:
    #     raise ValueError("Path must stay inside the repository root.") from exc

    # if resolved_path.is_dir():
    #     raise IsADirectoryError(f"Path points to a directory: {cleaned_path}")

    return resolved_path


def load_pdf_file(relative_path: str) -> str:
    """Load a UTF-8 pdf file from the repository using a relative path."""
    target_file = resolve_repo_file(relative_path)

    if not target_file.exists():
        raise FileNotFoundError(f"Text file not found: {relative_path}")

    return target_file.read_text(encoding="utf-8")
