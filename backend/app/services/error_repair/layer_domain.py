"""
Layer 1: Domain-Specific Correction
"""
import re
from .base import BaseRepairLayer

class DomainLayer(BaseRepairLayer):
    def __init__(self, pack: dict):
        self.pack = pack

    def repair(self, text: str) -> str:
        """
        Check if parts of the text closely match a domain keyword and replace them.
        """
        if not self.pack or not text:
            return text
            
        fixed_text = text
        
        # Exact/Substring match (case insensitive replace)
        # e.g., 'al &lot' -> 'AI & IoT'
        for error, fix in self.pack.items():
            fixed_text = re.sub(re.escape(error), fix, fixed_text, flags=re.IGNORECASE)
                
        return fixed_text
