KEYWORDS = {
    "NVO": ["novo", "ozempic", "wegovy", "semaglutide"],
    "LLY": ["lilly", "eli lilly", "tirzepatide", "mounjaro", "zepbound"],
    "PFE": ["pfizer"],
    "MRK": ["merck", "keytruda"],
    "AMGN": ["amgen"],
    "REGN": ["regeneron", "eylea"],
    "BMY": ["bristol myers", "bms", "opdivo"],
    "GILD": ["gilead"],
    "VRTX": ["vertex"],
    "BIIB": ["biogen"]
}

COMPETITORS = {
    "NVO": ["LLY"],
    "LLY": ["NVO"],
    "MRK": ["BMY"],
    "BMY": ["MRK"]
}

THEMES = {
    "glp1_obesity": [
        "obesity", "weight loss", "glp-1", "glp1",
        "semaglutide", "tirzepatide", "wegovy",
        "ozempic", "mounjaro", "zepbound"
    ],
    "oncology": [
        "cancer", "oncology", "tumor", "keytruda", "opdivo"
    ],
    "fda_regulatory": [
        "fda", "approval", "reject", "rejection",
        "panel", "adcom", "clearance", "complete response letter"
    ]
}

THEME_TO_STOCKS = {
    "glp1_obesity": ["NVO", "LLY"],
    "oncology": ["MRK", "BMY", "REGN"],
    "fda_regulatory": []
}