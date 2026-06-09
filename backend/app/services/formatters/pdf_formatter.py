"""
PDF Formatter

Converts the Structured AST into a PDF Document.
Returns the binary bytes of the document.
"""
from fpdf import FPDF
from app.schemas.structure import StructuredDocument, BlockType
from .base import BaseFormatter

class PdfFormatter(BaseFormatter):
    def format(self, document: StructuredDocument) -> bytes:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # We use built-in fonts for simplicity (Helvetica)
        
        # Header
        pdf.set_font("helvetica", "B", 10)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 10, f"Structify AI - {document.document_type.title()} Document", align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
        # Reset color
        pdf.set_text_color(0, 0, 0)
        
        for block in document.blocks:
            if block.type == BlockType.TITLE:
                pdf.set_font("helvetica", "B", 24)
                # Multi_cell handles text wrapping if the title is long
                pdf.multi_cell(0, 12, block.text, align="C", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(8)
                
            elif block.type == BlockType.HEADING:
                pdf.set_font("helvetica", "B", 18)
                pdf.multi_cell(0, 10, block.text, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(4)
                
            elif block.type == BlockType.SUBHEADING:
                pdf.set_font("helvetica", "B", 14)
                pdf.multi_cell(0, 8, block.text, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(2)
                
            elif block.type == BlockType.LIST_ITEM:
                pdf.set_font("helvetica", "", 12)
                text = block.text
                if not any(text.startswith(c) for c in ["-", "*", "1.", "2."]):
                    text = f"- {text}"
                # Indent bullet points slightly
                pdf.set_x(15)
                pdf.multi_cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(2)
                
            elif block.type == BlockType.PARAGRAPH:
                pdf.set_font("helvetica", "", 12)
                pdf.multi_cell(0, 6, block.text, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(4)
                
            else:
                pdf.set_font("helvetica", "", 12)
                pdf.multi_cell(0, 6, block.text, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(4)
                
        # output() with no filename returns a bytearray
        return pdf.output()
