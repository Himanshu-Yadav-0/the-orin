from pathlib import Path

def get_dir_files(path:str) -> list:
    directory = Path(path)
    files = [file.name for file in directory.rglob("*") if file.is_file()]
    return files


