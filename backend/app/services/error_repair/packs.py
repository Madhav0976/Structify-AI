"""
Domain-Specific Correction Packs.
These act as ground-truth dictionaries for specific document types.
"""

# OCR mistakes frequently seen in technical reports
TECH_REPORT_PACK = {
    # AI & IoT variants
    "al &lot": "AI & IoT",
    "ai & iot": "AI & IoT",
    "ai & lot": "AI & IoT",

    # Headings
    "project tite": "Project Title",
    "problem statment": "Problem Statement",

    # OCR word errors
    "overvlew": "Overview",
    "trattic": "Traffic",
    "curenturban": "Current urban",
    "systemsale": "systems are",
    "computng": "Computing",
    "inetticient": "inefficient",
    "in tticient": "inefficient",

    # Protect brand/domain words
    "nextgen": "Nextgen",

    # Full phrase corrections
    "smart trattic system": "Smart Traffic System",
    "project overvlew structure": "Project Overview Structure"
}

# Resume headers
RESUME_PACK = {
    "educatn": "Education",
    "expeience": "Experience",
    "skils": "Skills",
    "certitications": "Certifications",
    "profle": "Profile"
}

# Academic paper headers
ACADEMIC_PACK = {
    "abstrat": "Abstract",
    "introducton": "Introduction",
    "methodolgy": "Methodology",
    "concluson": "Conclusion",
    "refernces": "References"
}


def get_pack(domain: str) -> dict:
    if domain == "report":
        return TECH_REPORT_PACK
    elif domain == "resume":
        return RESUME_PACK
    elif domain == "academic":
        return ACADEMIC_PACK

    return {}