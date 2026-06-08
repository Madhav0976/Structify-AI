"""
Base Detector Strategy Interface
"""
from abc import ABC, abstractmethod
from typing import List

from app.schemas.ocr import OCRTextBlock
from app.schemas.structure import StructuredDocument

class BaseDocumentDetector(ABC):
    """
    Abstract base class for all document detectors.
    Allows us to scale to ResumeDetector, ReportDetector, etc.
    """

    @abstractmethod
    def detect(self, blocks: List[OCRTextBlock]) -> StructuredDocument:
        """Process OCR blocks into a structured AST."""
        pass
