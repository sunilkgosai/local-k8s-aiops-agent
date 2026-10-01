from pathlib import Path
def load_runbooks():
    d=Path(__file__).parent/"runbooks"
    return {p.stem:p.read_text(encoding="utf-8") for p in d.glob("*.md")}
