import os
from pathlib import Path


def load_project_env():
    """Load .env from repo root/cwd, with a manual fallback if python-dotenv is unavailable."""
    root = Path(__file__).resolve().parents[1]
    candidates = [root / ".env", Path.cwd() / ".env"]

    for path in candidates:
        try:
            from dotenv import load_dotenv

            load_dotenv(path, override=False)
        except Exception:
            pass

    # Manual fallback for environments where python-dotenv is missing/broken.
    if os.getenv("PINECONE_API_KEY"):
        return
    for path in candidates:
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except Exception:
            continue
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip().lstrip("\ufeff")
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
