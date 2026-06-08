"""
Document Intelligence Classifier

Analyzes OCR text and uses keyword heuristics to determine
the most likely document type (resume, report, academic, assignment).
"""
import re
from typing import List
from app.schemas.ocr import OCRTextBlock

# Keywords that strongly indicate a document type
DOCUMENT_SIGNATURES = {
    "resume": ["experience", "education", "skills", "gpa", "university", "profile", "certifications"],
    "academic": ["abstract", "methodology", "introduction", "references", "ieee", "conclusion", "literature review"],
    "report": ["project title", "architecture", "system", "client", "overview", "executive summary"],
    "assignment": ["question", "answer", "roll number", "semester", "class", "assignment"]
}

class DocumentClassifier:
    def classify(self, blocks: List[OCRTextBlock]) -> str:
        """
        Combines block text and scores it against document signatures.
        Returns the document type with the highest score.
        If no score > 0, returns "generic".
        """
        if not blocks:
            return "generic"
            
        # Combine all text into a single lowercase string for analysis
        full_text = " ".join([b.text for b in blocks]).lower()
        
        scores = {doc_type: 0 for doc_type in DOCUMENT_SIGNATURES}
        
        for doc_type, keywords in DOCUMENT_SIGNATURES.items():
            for keyword in keywords:
                # Use regex to count occurrences of whole words/phrases
                matches = re.findall(rf"\b{keyword}\b", full_text)
                scores[doc_type] += len(matches)
                
        # Find the max score
        best_match = max(scores, key=scores.get)
        
        if scores[best_match] > 0:
            return best_match
            
        return "generic"
