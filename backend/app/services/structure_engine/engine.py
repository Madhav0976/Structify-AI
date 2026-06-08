"""
Structure Engine Orchestrator

Acts as the Mediator:
1. Receives raw blocks and configuration.
2. Runs the RepairPipeline on text (if enabled).
3. Passes cleaned blocks to the GenericDocumentDetector.
"""
import logging
from typing import List

from app.schemas.ocr import OCRTextBlock
from app.schemas.structure import StructuredDocument
from .generic import GenericDocumentDetector
from app.services.error_repair import RepairPipeline
from app.services.classifier import DocumentClassifier
from app.config import settings

logger = logging.getLogger(__name__)

class StructureEngine:
    def __init__(self):
        # We can register more detectors here later (Resume, Report, etc.)
        self.detectors = {
            "generic": GenericDocumentDetector()
        }
        self.classifier = DocumentClassifier()

    def process(
        self, 
        blocks: List[OCRTextBlock], 
        doc_type: str = "auto",
        enable_repair: bool | None = None
    ) -> StructuredDocument:
        """
        Process OCR blocks using the appropriate strategy and repair pipeline.
        """
        
        # 1. Document Classification
        if doc_type == "auto":
            detected_type = self.classifier.classify(blocks)
            logger.info(f"Classifier detected document type: {detected_type}")
            doc_type = detected_type
            
        # 2. Determine if we should repair (Request flag overrides Global config)
        should_repair = settings.ENABLE_OCR_REPAIR if enable_repair is None else enable_repair
        
        # 2. Repair text if enabled
        if should_repair:
            logger.info(f"Running OCR Error Repair (Domain: {doc_type})...")
            pipeline = RepairPipeline(domain=doc_type)
            
            # We modify the block texts in place before passing to the detector.
            # (In a strict functional paradigm we'd create new blocks, but this is fine for AST).
            for block in blocks:
                original_text = block.text
                fixed_text = pipeline.fix_text(original_text)
                block.text = fixed_text
        else:
            logger.info("OCR Error Repair is DISABLED.")

        # 3. Fallback to generic detector if doc_type is unknown
        detector = self.detectors.get(doc_type, self.detectors["generic"])
        
        # 4. The detector receives the blocks (clean or dirty, it doesn't care!)
        structured_doc = detector.detect(blocks)
        
        # 5. Overwrite the generic type with our dynamically classified type
        structured_doc.document_type = doc_type
        
        return structured_doc
