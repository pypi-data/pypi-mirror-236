
from pathlib import Path

PathLike = Path|str

def path_str(path:PathLike) -> str:
    return str(as_path(path).absolute())

def as_path(path:PathLike) -> Path:
    return Path(path).expanduser()
