"""
Layer 2: Context-Aware Correction

This layer handles common merged words or split words.
Example: "Trattic" might not mean anything, but if the previous word is "Smart" and the next is "System", 
a context engine can fix it.
"""
import re
from .base import BaseRepairLayer

class ContextLayer(BaseRepairLayer):
    def __init__(self):
        # A basic dictionary of multi-word contextual fixes.
        # In a production AI system, this could use a HuggingFace Masked Language Model (e.g. BERT).
        self.context_fixes = {
            r"\bsmart trattic\b": "smart traffic",
            r"\btrattic systems?\b": "traffic system",
        }

    def repair(self, text: str) -> str:
        if not text:
            return text
            
        fixed_text = text
        for pattern, replacement in self.context_fixes.items():
            # Using regex substitution (case insensitive) to fix known contextual errors
            fixed_text = re.sub(pattern, replacement, fixed_text, flags=re.IGNORECASE)
            
        return fixed_text
