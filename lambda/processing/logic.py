import os
import sys
from typing import Dict

# Ensure project root is importable so `config` package can be imported
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

from config import keywords as kw


def extract_themes_and_stocks(text: str) -> Dict:
	"""Simple keyword-based extraction returning matched themes and stocks.

	This is intentionally small and deterministic — suitable for local testing
	and as a starting point for richer NLP later.
	"""
	found_themes = set()
	found_stocks = set()
	lower = (text or "").lower()

	# Match theme terms first (maps to theme->stocks)
	for theme, terms in kw.THEMES.items():
		for term in terms:
			if term in lower:
				found_themes.add(theme)
				for s in kw.THEME_TO_STOCKS.get(theme, []):
					found_stocks.add(s)
				break

	# Match company-specific keywords
	for ticker, terms in kw.KEYWORDS.items():
		for term in terms:
			if term in lower:
				found_stocks.add(ticker)
				for c in kw.COMPETITORS.get(ticker, []):
					found_stocks.add(c)
				break

	return {"themes": list(found_themes), "stocks": list(found_stocks)}


def process_record(record: dict) -> Dict:
	"""Process a single record (expects a dict with `text` or `body`)."""
	text = record.get("text") or record.get("body") or ""
	return extract_themes_and_stocks(text)

