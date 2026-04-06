"""Predefined healthcare categories mapped to tickers.

This file centralizes grouping definitions used by the dashboard for quick
filtering and focus. Update categories and tickers here as the project grows.
"""

CATEGORIES = {
    "All": [],
    "GLP-1 (Obesity/Diabetes)": ["NVO", "LLY"],
    "Oncology": ["MRK", "BMY", "REGN"],
    "Epilepsy / Neurology": ["BIIB", "GILD"],
    "MedTech / Devices": ["MDT", "ISRG", "SYK"]
}

CATEGORY_DESCRIPTIONS = {
    "GLP-1 (Obesity/Diabetes)": "Companies involved in GLP-1 therapeutics and obesity/diabetes treatments.",
    "Oncology": "Major oncology drugmakers and immuno-oncology players.",
    "Epilepsy / Neurology": "Companies with neurology and epilepsy-focused pipelines.",
    "MedTech / Devices": "Surgical, diagnostic, and device manufacturers."
}
