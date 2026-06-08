"""
Markdown Formatter

Converts the Structured AST into standard Markdown.
"""

from app.schemas.structure import StructuredDocument, BlockType
from .base import BaseFormatter


class MarkdownFormatter(BaseFormatter):

    def format(self, document: StructuredDocument) -> str:
        lines = []

        for block in document.blocks:

            text = block.text.strip()

            if block.type == BlockType.TITLE:
                lines.append(f"# {text}")
                lines.append("")

            elif block.type == BlockType.HEADING:

                # Smart heading parsing
                if ":" in text:
                    heading, value = text.split(":", 1)

                    lines.append(f"## {heading.strip()}")
                    lines.append(value.strip())
                    lines.append("")
                else:
                    lines.append(f"## {text}")
                    lines.append("")

            elif block.type == BlockType.SUBHEADING:

                if ":" in text:
                    heading, value = text.split(":", 1)

                    lines.append(f"### {heading.strip()}")
                    lines.append(value.strip())
                    lines.append("")
                else:
                    lines.append(f"### {text}")
                    lines.append("")

            elif block.type == BlockType.LIST_ITEM:

                if not text.startswith(("-", "*", "•")):
                    text = f"- {text}"

                lines.append(text)

            elif block.type == BlockType.PARAGRAPH:

                lines.append(text)
                lines.append("")

            else:
                lines.append(text)

        return "\n".join(lines)