"""
Generic Document Structure Detector
"""
from typing import List

from app.schemas.ocr import OCRTextBlock
from app.schemas.structure import StructuredDocument
from .base import BaseDocumentDetector


class GenericDocumentDetector(BaseDocumentDetector):

    def detect(self, blocks: List[OCRTextBlock]) -> StructuredDocument:

        return StructuredDocument(
            document_type="generic",
            blocks=[],
            total_blocks=0
        )

    def detect(self, blocks: List[OCRTextBlock]) -> StructuredDocument:
        global nlp

        if nlp is None:
            nlp = spacy.load("en_core_web_sm")
            
        if not blocks:
            return StructuredDocument(document_type="generic", blocks=[], total_blocks=0)

        # 1. Extract Mathematical / Geometric Features
        features = extract_geometric_features(blocks)

        structured_blocks = []
        has_title = False

        # 2. Iterate and classify each block
        for idx, block in enumerate(blocks):
            feat = features[idx]
            text = block.text

            # NLP Analysis
            doc = nlp(text)
            # A line is mostly noun chunks/proper nouns if it has very few verbs
            verb_count = len([token for token in doc if token.pos_ == "VERB"])
            is_noun_phrase = verb_count == 0

                        # Classification Logic
            block_type = BlockType.PARAGRAPH
            level = 0

            text_lower = text.lower()

            # Better Title Detection
            title_score = 0

            if idx == 0:
                title_score += 3

            if any(keyword in text_lower for keyword in [
                "overview",
                "summary",
                "introduction",
                "report",
                "document",
                "structure",
                "project",
                "analysis"
            ]):
                title_score += 3

            if feat["is_largest"]:
                title_score += 2

            if feat["is_short"]:
                title_score += 1

            if not has_title and title_score >= 5:
                block_type = BlockType.TITLE
                has_title = True

            elif any(
                text_lower.startswith(prefix)
                for prefix in [
                    "problem statement",
                    "objective",
                    "conclusion",
                    "abstract"
                ]
            ):
                block_type = BlockType.HEADING
                level = 1

            elif (
                (feat["is_large"] or feat["is_all_caps"])
                and feat["is_short"]
                and is_noun_phrase
            ):
                block_type = BlockType.HEADING
                level = 1

            elif feat["starts_with_number"] and feat["is_short"]:
                block_type = BlockType.SUBHEADING
                level = 2

            elif feat["starts_with_bullet"]:
                block_type = BlockType.LIST_ITEM

            else:
                block_type = BlockType.PARAGRAPH
            
            # Final override

            text_lower = text.lower().strip()

            if (
                text_lower.startswith("domain:")
                or text_lower.startswith("sub-domain:")
                or text_lower.startswith("project title:")
            ):
                block_type = BlockType.PARAGRAPH
                level = 0
           
            # Create AST Node
            struct_block = StructuredBlock(
                id=idx + 1,
                type=block_type,
                text=text,
                level=level,
                metadata={
                    "confidence": block.confidence,
                    "height": feat["height"],
                    "indent": feat["indent"]
                }
            )
            structured_blocks.append(struct_block)

        return StructuredDocument(
            document_type="generic",
            blocks=structured_blocks,
            total_blocks=len(structured_blocks)
        )
