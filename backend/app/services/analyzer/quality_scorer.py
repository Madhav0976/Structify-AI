class QualityScorer:

    def score(self, text: str):

        text_lower = text.lower()

        score = 0

        checks = {
            "Title": "title" in text_lower,
            "Abstract": "abstract" in text_lower,
            "Problem Statement": "problem statement" in text_lower,
            "Objectives": (
                "objectives" in text_lower
                or "objective" in text_lower
            ),
            "Conclusion": "conclusion" in text_lower,
            "References": "references" in text_lower,
        }

        for value in checks.values():
            if value:
                score += 15

        score = min(score, 100)

        return {
            "score": score,
            "checks": checks
        }