# tools/file_mapper.py

import os

SUPPORTED_EXTENSIONS = {".py", ".java", ".tf", ".yaml", ".js", ".ts"}

def map_files(root_dir: str) -> dict:
    """
    Walk through the directory recursively and return a dict mapping file paths to their content.
    """
    files_map = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        files_map[file_path] = f.read()
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return files_map
