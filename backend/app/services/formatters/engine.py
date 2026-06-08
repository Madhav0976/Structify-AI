"""
Format Engine (Factory)

Resolves requested format string to the correct Formatter strategy.
"""
from app.schemas.structure import StructuredDocument
from .base import BaseFormatter
from .markdown import MarkdownFormatter
from .docx_formatter import DocxFormatter
from .pdf_formatter import PdfFormatter

class FormatEngine:
    def __init__(self):
        # Register formatters here
        self.formatters = {
            "markdown": MarkdownFormatter(),
            "docx": DocxFormatter(),
            "pdf": PdfFormatter(),
            # Future formatters will be added here:
            # "study_notes": StudyNotesFormatter(),
            # "linkedin": LinkedInFormatter(),
        }

    def format_document(self, document: StructuredDocument, format_type: str = "markdown") -> str | bytes:
        """
        Retrieves the requested formatter and formats the document.
        Defaults to 'markdown' if an unknown format is requested.
        """
        formatter = self.formatters.get(format_type.lower(), self.formatters["markdown"])
        return formatter.format(document)
