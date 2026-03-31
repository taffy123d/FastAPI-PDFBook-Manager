import os
from pathlib import Path
from typing import List
from app.core.config import STATIC_DIR

# PDF 文件夹路径
BOOK_PDF_DIR = os.path.join(STATIC_DIR, "book")


def get_all_pdf_files() -> List[str]:
    """
    扫描 static/book 目录，获取所有 PDF 文件名
    """
    if not os.path.exists(BOOK_PDF_DIR):
        os.makedirs(BOOK_PDF_DIR)
        return []
    
    pdf_files = []
    for filename in os.listdir(BOOK_PDF_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_files.append(filename)
    return pdf_files


def get_pdf_path(filename: str) -> str:
    """
    获取 PDF 文件的完整路径
    """
    return os.path.join(BOOK_PDF_DIR, filename)


def pdf_exists(filename: str) -> bool:
    """
    检查 PDF 文件是否存在
    """
    return os.path.exists(get_pdf_path(filename))