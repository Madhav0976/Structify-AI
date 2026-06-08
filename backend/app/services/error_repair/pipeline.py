"""
The Repair Pipeline.

Chains the Domain, Context, and Dictionary layers together.
"""
from typing import List

from .base import BaseRepairLayer
from .packs import get_pack
from .layer_domain import DomainLayer
from .layer_context import ContextLayer
from .layer_dictionary import DictionaryLayer

class RepairPipeline:
    def __init__(self, domain: str = "report"):
        """
        Initializes the pipeline with the specified domain.
        Layers are executed in the order they are added.
        """
        self.layers: List[BaseRepairLayer] = []
        
        # 1. Domain Layer (Highest Priority)
        pack = get_pack(domain)
        if pack:
            self.layers.append(DomainLayer(pack))
            
        # 2. Context Layer
        self.layers.append(ContextLayer())
        
        # 3. Dictionary Layer (Fallback)
        self.layers.append(DictionaryLayer())

    def fix_text(self, text: str) -> str:
        """
        Passes the text through all registered repair layers.
        """
        if not text:
            return text
            
        fixed_text = text
        for layer in self.layers:
            fixed_text = layer.repair(fixed_text)
            
        return fixed_text
