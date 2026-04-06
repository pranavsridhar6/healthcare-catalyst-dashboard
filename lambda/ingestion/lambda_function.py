import os
import sys
import json

# Make the sibling `processing` package importable when this handler is executed
ROOT = os.path.dirname(os.path.dirname(__file__))  # points to the `lambda` folder
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

from processing import logic as proc


def handler(event, context):
	"""Basic lambda handler that accepts a list of records and runs processing logic.

	Expected input shape (flexible):
	  { "records": [ {"body": "..."}, ... ] }

	This function is intentionally minimal — it parses string bodies as JSON
	when possible and falls back to treating the body as raw text.
	"""
	records = event.get("records") or event.get("Records") or []
	results = []

	for rec in records:
		parsed = rec if isinstance(rec, dict) else {"body": rec}

		body = parsed.get("body") or parsed.get("text") or ""
		if isinstance(body, str):
			try:
				body_parsed = json.loads(body)
			except Exception:
				body_parsed = {"text": body}
		else:
			body_parsed = body

		res = proc.process_record(body_parsed if isinstance(body_parsed, dict) else {"text": str(body_parsed)})
		results.append(res)

	return {"statusCode": 200, "results": results}

