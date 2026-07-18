import os
import zipfile
from pathlib import Path
from uuid import uuid4

from backend.schemas import RepositoryFile

# Directories to ignore
IGNORED_DIRS = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    "dist",
    "build",
    "target",
    ".next",
    "coverage",
    ".pytest_cache",
    ".mypy_cache",
}

# Binary/media extensions to ignore
IGNORED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".svg",
    ".ico",
    ".pdf",      # Support later
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".zip",
    ".tar",
    ".gz",
    ".rar",
    ".7z",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".class",
    ".jar",
    ".pyc",
    ".o",
    ".obj",
    ".bin",
    ".mp3",
    ".wav",
    ".mp4",
    ".avi",
    ".mov",
}

# Language detection (metadata only)
LANGUAGE_MAP = {
    ".py": "Python",
    ".go": "Go",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TSX",
    ".jsx": "JSX",
    ".java": "Java",
    ".kt": "Kotlin",
    ".c": "C",
    ".cpp": "C++",
    ".h": "C Header",
    ".hpp": "C++ Header",
    ".cs": "C#",
    ".php": "PHP",
    ".rb": "Ruby",
    ".swift": "Swift",
    ".scala": "Scala",
    ".rs": "Rust",
    ".lua": "Lua",
    ".proto": "Protocol Buffers",
    ".sql": "SQL",
    ".md": "Markdown",
    ".txt": "Text",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".json": "JSON",
    ".xml": "XML",
    ".html": "HTML",
    ".css": "CSS",
    ".sh": "Shell",
}


def extract_zip(zip_path: str, extract_to: str) -> str:
    """Extract the uploaded repository ZIP."""
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)

    return extract_to


def should_skip(file_path: Path) -> bool:
    """Return True if file should be skipped."""
    return file_path.suffix.lower() in IGNORED_EXTENSIONS


def detect_language(file_path: Path) -> str:
    """Detect language from filename/extension."""

    special_files = {
        "Dockerfile": "Docker",
        "Makefile": "Make",
        "go.mod": "Go Modules",
        "go.sum": "Go Modules",
        "package.json": "Node",
        "package-lock.json": "Node",
        "requirements.txt": "Python",
        "pyproject.toml": "Python",
        ".env": "Environment",
    }

    if file_path.name in special_files:
        return special_files[file_path.name]

    return LANGUAGE_MAP.get(file_path.suffix.lower(), "Unknown")


def read_file(file_path: Path) -> str:
    """Read a UTF-8 text file."""

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except (UnicodeDecodeError, PermissionError):
        return ""

    except Exception:
        return ""


def walk_repository(root_path: str) -> list[RepositoryFile]:
    """Traverse repository and collect readable files."""

    repository: list[RepositoryFile] = []

    for current_dir, dirs, files in os.walk(root_path):

        # Ignore unwanted directories
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:

            path = Path(current_dir) / file

            if should_skip(path):
                continue

            content = read_file(path)

            if not content.strip():
                continue

            repository.append(
                RepositoryFile(
                    file_id=str(uuid4()),
                    path=str(path.relative_to(root_path)),
                    filename=path.name,
                    extension=path.suffix.lower(),
                    language=detect_language(path),
                    content=content,
                    size=len(content),
                )
            )

    return repository


def load_repository(zip_path: str) -> list[RepositoryFile]:
    """
    Repository loading pipeline.

    ZIP
      ↓
    Extract
      ↓
    Walk Repository
      ↓
    Read Text Files
      ↓
    Return Repository Files
    """

    extract_dir = Path("uploads/extracted")

    extract_dir.mkdir(parents=True, exist_ok=True)

    extract_zip(zip_path, str(extract_dir))

    return walk_repository(str(extract_dir))