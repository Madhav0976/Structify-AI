from abc import ABC, abstractmethod
from app.schemas.structure import StructuredDocument

class BaseFormatter(ABC):
    """
    Abstract Base Class for all Document Formatters.
    Takes a StructuredDocument (AST) and converts it to a string string output.
    """
    
    @abstractmethod
    def format(self, document: StructuredDocument) -> str | bytes:
        """
        Convert the AST into a specific string format (Markdown) or binary format (DOCX/PDF).
        """
        pass
