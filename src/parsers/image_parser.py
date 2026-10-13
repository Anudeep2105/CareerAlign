import pytesseract
from PIL import Image
from .base import BaseParser

class ImageParser(BaseParser):
    def extract_text(self, file_path: str) -> str:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image).strip()
