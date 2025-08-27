from typing import List, Dict
from datetime import date
from pathlib import Path

def files_import(root_path: Path, include_subdirs: bool = True):
    if not root_path.exists():
        raise FileNotFoundError(f"[读取文件 发生错误] 目录 {root_path} 不存在")
    if not root_path.is_dir():
        raise NotADirectoryError(f"[读取文件 发生错误] {root_path} 是文件而非目录")

    # 导入全部文件
    files_readerror = []
    if include_subdirs:
        files = []
        for p in root_path.rglob('*'):
            try:
                if p.is_file():
                    files.append(p)
            except:
                files_readerror.append(p)
    else:
        files = []
        for p in root_path.iterdir():
            try:
                if p.is_file():
                    files.append(p)
            except:
                files_readerror.append(p)
    
    # 按照文件后缀归类
    summary: Dict[str, List[Path]] = {}
    summary_readerror: Dict[str, List[Path]] = {}
    for f in files:
        suffix = f.suffix.lower()
        if suffix not in summary:
            summary[suffix] = []
        summary[suffix].append(f)
    for f in files_readerror:
        suffix = f.suffix.lower()
        if suffix not in summary_readerror:
            summary_readerror[suffix] = []
        summary_readerror[suffix].append(f)

    return summary, summary_readerror


def png_filter(files: List[Path]):
    png_valid, png_invalid = [], []
    for f in files:
        try:
            date.fromisoformat(f.stem)
            png_valid.append(f)
        except:
            png_invalid.append(f)
        
    return png_valid, png_invalid