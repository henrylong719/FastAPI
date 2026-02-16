from pathlib import Path

import json

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "issues.json"

def load_data() -> list[dict]:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            content = f.read()
            if content.strip():
                return json.loads(content)
        return []
    return []
    
def save_data(data: list[dict]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
        
        
        
        




