class SummaryGenerator:

    def generate(self, text: str) -> str:

        if not text:
            return ""

        paragraphs = [
            p.strip()
            for p in text.split("\n")
            if p.strip()
        ]

        if len(paragraphs) >= 3:
            return " ".join(paragraphs[:3])

        if len(paragraphs) == 2:
            return f"{paragraphs[0]} {paragraphs[1]}"

        return paragraphs[0]