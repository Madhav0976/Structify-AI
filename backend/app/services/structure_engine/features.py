"""
Geometric Feature Extraction

Extracts mathematical data from OCR bounding boxes.
bbox format: [[x1,y1], [x2,y1], [x2,y2], [x1,y2]] (Top-Left, Top-Right, Bottom-Right, Bottom-Left)
"""
from typing import List
from app.schemas.ocr import OCRTextBlock

def extract_geometric_features(blocks: List[OCRTextBlock]) -> List[dict]:
    """Calculate geometric features for all blocks."""
    features = []

    # First pass: collect raw metrics
    heights = []
    indents = []

    for block in blocks:
        # Bbox is a list of 4 [x, y] coordinates
        top_left = block.bbox[0]
        bottom_left = block.bbox[3]

        height = bottom_left[1] - top_left[1]
        indent = top_left[0]

        heights.append(height)
        indents.append(indent)

    # Calculate document-wide averages to establish baselines
    avg_height = sum(heights) / len(heights) if heights else 0
    avg_indent = sum(indents) / len(indents) if indents else 0
    max_height = max(heights) if heights else 0

    # Second pass: compute relative features
    for i, block in enumerate(blocks):
        text = block.text
        height = heights[i]
        indent = indents[i]

        # Font size proxy (is it bigger than average?)
        is_large = height > (avg_height * 1.2)
        is_largest = height >= (max_height * 0.9) # Within 10% of max

        # Formatting heuristics
        is_all_caps = text.isupper() and len([c for c in text if c.isalpha()]) > 3
        words = text.split()
        is_short = len(words) <= 5

        # Does it start with a number or bullet? (1., -, •)
        starts_with_bullet = any(text.startswith(char) for char in ["-", "*", "•"])
        starts_with_number = len(words) > 0 and (words[0].endswith(".") and words[0][:-1].isdigit())

        features.append({
            "height": height,
            "indent": indent,
            "is_large": is_large,
            "is_largest": is_largest,
            "is_all_caps": is_all_caps,
            "is_short": is_short,
            "starts_with_bullet": starts_with_bullet,
            "starts_with_number": starts_with_number
        })

    return features
