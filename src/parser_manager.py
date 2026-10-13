import os
from .parsers.pdf_parser import PDFParser
from .parsers.docx_parser import DocxParser
from .parsers.image_parser import ImageParser

class ParserFactory:
    _parsers = {
        '.pdf': PDFParser(),
        '.docx': DocxParser(),
        '.doc': DocxParser(),
        '.jpg': ImageParser(),
        '.jpeg': ImageParser(),
        '.png': ImageParser(),
        '.txt': None # Handle separately as simple read
    }

    @classmethod
    def get_parser(cls, file_path: str):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.txt':
            return cls.TextParser()
        return cls._parsers.get(ext)

    class TextParser:
        def extract_text(self, file_path: str) -> str:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
