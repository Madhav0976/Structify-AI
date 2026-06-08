"""
Layer 3: Standard Dictionary Fallback
"""
import spacy
from spellchecker import SpellChecker

from .base import BaseRepairLayer


class DictionaryLayer(BaseRepairLayer):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.spell = SpellChecker()

    def repair(self, text: str) -> str:
        if not text:
            return text

        doc = self.nlp(text)
        corrected_words = []

        for token in doc:
            word = token.text

            # Skip punctuation/numbers
            if not token.is_alpha:
                corrected_words.append(word)
                continue

            # Skip tiny words
            if len(word) <= 2:
                corrected_words.append(word)
                continue

            # Skip acronyms
            if word.isupper():
                corrected_words.append(word)
                continue

            # Skip proper nouns
            if word.istitle():
                corrected_words.append(word)
                continue

            # Skip mixed-case words
            if (
                not word.islower()
                and not word.isupper()
                and not word.istitle()
            ):
                corrected_words.append(word)
                continue

            # Simple spell correction only
            if word not in self.spell:
                correction = self.spell.correction(word)

                if correction:
                    corrected_words.append(correction)
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)

        result = "".join(
            word + token.whitespace_
            for word, token in zip(corrected_words, doc)
        )

        return result