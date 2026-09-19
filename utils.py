import os


def display_name(source_path: str) -> str:
    """把存储的文件路径变成人类可读的讲义名，去掉 uploads_ 前缀"""
    name = os.path.basename(source_path)
    if name.startswith("uploads_"):
        name = name[len("uploads_"):]
    return name
