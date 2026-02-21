import json

from app.config import settings

DATA_FILE = settings.data_dir / "issues.json"


def load_data() -> list[dict]:
    if DATA_FILE.exists():
        content = DATA_FILE.read_text()
        if content.strip():
            return json.loads(content)
    return []


def save_data(data: list[dict]) -> None:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, indent=2) + "\n")
