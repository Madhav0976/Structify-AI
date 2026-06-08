from collections import Counter
import re


class DocumentAnalyzer:

    def analyze(self, text: str):

        if not text:
            return {
                "document_type": "unknown",
                "word_count": 0,
                "character_count": 0,
                "sentence_count": 0,
                "paragraph_count": 0,
                "estimated_read_time": "0 min",
                "keywords": [],
                "summary": ""
            }

        words = text.split()

        word_count = len(words)

        character_count = len(text)

        sentence_count = len(
            re.findall(r"[.!?]+", text)
        )

        paragraphs = [
            p.strip()
            for p in text.split("\n")
            if p.strip()
        ]

        paragraph_count = len(paragraphs)

        common_words = Counter(
            word.lower().strip(".,:;!?()[]{}")
            for word in words
            if len(word) > 3
        ).most_common(10)

        keywords = [
            word
            for word, _
            in common_words
        ]

        # Read Time
        read_time = max(
            1,
            round(word_count / 200)
        )

        # Simple Summary
        summary = ""

        if paragraphs:
            summary = paragraphs[0]

            if len(summary) > 250:
                summary = summary[:250] + "..."

        # Document Type Detection
        text_lower = text.lower()

        if any(
            keyword in text_lower
            for keyword in [
                "education",
                "experience",
                "skills",
                "certifications"
            ]
        ):
            document_type = "resume"

        elif any(
            keyword in text_lower
            for keyword in [
                "abstract",
                "methodology",
                "references",
                "conclusion"
            ]
        ):
            document_type = "academic"

        elif any(
            keyword in text_lower
            for keyword in [
                "problem statement",
                "objective",
                "project title",
                "scope"
            ]
        ):
            document_type = "report"

        else:
            document_type = "generic"

        return {
            "document_type": document_type,
            "word_count": word_count,
            "character_count": character_count,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "estimated_read_time": f"{read_time} min",
            "keywords": keywords,
            "summary": summary
        }