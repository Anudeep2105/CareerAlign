import docx
from .base import BaseParser

class DocxParser(BaseParser):
    def extract_text(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()
