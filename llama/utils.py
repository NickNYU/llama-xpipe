import os


def is_local_storage_files_ready(persist_dir: str) -> bool:
    return os.path.exists(persist_dir) and len(os.listdir(persist_dir)) != 0
