from fastapi import APIRouter

from app.schemas.text import TextRequest
from app.schemas.ocr import OCRTextBlock

from app.services.analyzer.document_analyzer import DocumentAnalyzer
from app.services.analyzer.summary_generator import SummaryGenerator
from app.services.analyzer.quality_scorer import QualityScorer
from app.services.error_repair.pipeline import RepairPipeline
from app.services.structure_engine.engine import StructureEngine

router = APIRouter(
    prefix="/api/v1/text",
    tags=["Text Analysis"]
)


@router.post("/analyze")
def analyze_text(request: TextRequest):

    raw_text = request.text

    structure_engine = StructureEngine()

    return {
        "step": "after_structure_init"
    }

    structure_engine = StructureEngine()
    # Convert lines into OCR-like blocks
    lines = [
        line.strip()
        for line in repaired_text.splitlines()
        if line.strip()
    ]

    ocr_blocks = []

    for line in lines:
        ocr_blocks.append(
            OCRTextBlock(
                text=line,
                confidence=1.0,
                bbox=[
                    [0, 0],
                    [100, 0],
                    [100, 20],
                    [0, 20]
                ]
            )
        )

    # Structure Analysis
    structure_engine = StructureEngine()

    result = structure_engine.process(
        blocks=ocr_blocks,
        doc_type="auto",
        enable_repair=False
    )

    analyzer = DocumentAnalyzer()

    analysis = analyzer.analyze(repaired_text)

    summary_generator = SummaryGenerator()
    smart_summary = summary_generator.generate(repaired_text)

    quality_scorer = QualityScorer()

    quality = quality_scorer.score(
        repaired_text
    )

    return {
        "raw_text": raw_text,
        "repaired_text": repaired_text,
        "structured_document": result,
        "analysis": analysis,
        "smart_summary": smart_summary,
        "quality": quality
    }