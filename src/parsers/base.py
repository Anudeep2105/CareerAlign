from abc import ABC, abstractmethod
import os

class BaseParser(ABC):
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        """Extract text from the given file path."""
        pass
