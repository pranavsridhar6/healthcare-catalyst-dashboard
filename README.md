# Healthcare Catalyst Dashboard

This project is a Streamlit dashboard with optional backend/Lambda helpers.

## Run Locally

1. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
2. Start the app:
	```bash
	streamlit run frontend/streamlit_app.py
	```

## Correct Way To Share The App

If you share a generic Streamlit link (or the Streamlit homepage), people will not land on your app.
You must deploy this repo and share the deployed app URL.

Recommended: Streamlit Community Cloud

1. Push this project to GitHub.
2. Go to https://share.streamlit.io and sign in.
3. Click **New app** and select:
	- Repository: your GitHub repo
	- Branch: your deployment branch (usually `main`)
	- Main file path: `frontend/streamlit_app.py`
4. Deploy.
5. Copy your app URL, which looks like:
	- `https://<your-app-name>.streamlit.app`

## Secrets / Environment Variables

In Streamlit Cloud app settings, add these secrets if needed:

```toml
APP_PUBLIC_URL = "https://<your-app-name>.streamlit.app"
NEWSAPI_KEY = "<your_newsapi_key>"
```

Why `APP_PUBLIC_URL` matters:
- The dashboard share popover uses this value for the copy link button.
- If it is missing or wrong, people may copy an incorrect URL.

## Common Deployment Mistake

- Wrong: sharing `streamlit.io` or a generic Streamlit page.
- Right: sharing your deployed app URL (`*.streamlit.app`).
