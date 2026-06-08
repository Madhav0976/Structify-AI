"""
Structify AI - Structure Routes

Endpoint to convert raw OCR blocks into a Structured AST.
"""
import logging
from fastapi import APIRouter, HTTPException

from app.services.analyzer.document_analyzer import DocumentAnalyzer
from app.schemas.structure import StructuredDocument, StructureAnalyzeRequest
from app.services.structure_engine.engine import StructureEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Structure"])

# Instantiate the engine
engine = StructureEngine()

# Instantiate analyzer
analyzer = DocumentAnalyzer()

@router.post(
    "/structure/analyze",
    summary="Analyze OCR blocks to build a structured document tree.",
    description=(
        "Takes the raw output from the OCR extraction endpoint, "
        "runs error repair (optional), applies geometric and NLP analysis, "
        "and returns an AST mapping each block to a semantic type."
    ),
)
async def analyze_structure(request: StructureAnalyzeRequest):
    """
    1. Receive OCR blocks and config
    2. Pass to StructureEngine (Mediator)
    3. Return StructuredDocument
    """
    try:
        ocr_data = request.ocr_data
        if not ocr_data.success or not ocr_data.blocks:
            raise HTTPException(status_code=400, detail="Invalid or empty OCR data provided.")

        logger.info(f"Analyzing structure for {ocr_data.total_blocks} blocks...")
        
        # Pass the blocks and flags to the mediator
        structured_doc = engine.process(
            blocks=ocr_data.blocks, 
            doc_type=request.doc_type,
            enable_repair=request.enable_repair
        )
        
        logger.info(f"Structure analysis complete. Mapped {structured_doc.total_blocks} blocks.")

        full_text = "\n".join(
                block.text
            for block in structured_doc.blocks
        )

        analysis = analyzer.analyze(full_text)

        return {
            "document_type": structured_doc.document_type,
            "blocks": structured_doc.blocks,
            "total_blocks": structured_doc.total_blocks,
            "analysis": analysis,
        }
    except Exception as e:
        logger.error(f"Structure analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Structure analysis failed: {str(e)}",
        )
