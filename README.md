# Minimal Catholic Saints Calendar — August 2025 (English)

A bare-bones Streamlit app prepared for GitHub → Streamlit deployment.

## Local run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud
- Push ALL files to a GitHub repo, preserving this structure:
  - app.py
  - data/calendar_2025_en.json
  - data/meditations_2025_en.json
  - notes/placeholder.txt
  - requirements.txt
  - README.md
- On Streamlit Cloud, set main file to `app.py` and deploy.
- If data changes, restart the app from the menu (⋮ → Restart).
