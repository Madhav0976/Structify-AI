from abc import ABC, abstractmethod

class BaseRepairLayer(ABC):
    """
    Abstract Base Class for an OCR Repair Layer.
    Every layer must implement the 'repair' method, taking a string
    and returning the (potentially) corrected string.
    """
    
    @abstractmethod
    def repair(self, text: str) -> str:
        """
        Takes raw/partially fixed OCR text and applies the layer's logic.
        """
        pass
