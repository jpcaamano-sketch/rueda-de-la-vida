import os


def _get(key: str, default: str = "") -> str:
    """Lee primero de st.secrets (Streamlit Cloud), luego de os.environ (local)."""
    try:
        import streamlit as st
        return st.secrets[key]
    except Exception:
        return os.environ.get(key, default)


SUPABASE_URL   = _get("SUPABASE_URL")
SUPABASE_KEY   = _get("SUPABASE_KEY")
GOOGLE_API_KEY = _get("GOOGLE_API_KEY")
SMTP_PASSWORD  = _get("SMTP_PASSWORD")
BASE_URL       = _get("BASE_URL", "http://localhost:8532")
ADMIN_PASSWORD = _get("ADMIN_PASSWORD", "rueda2024")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587
SMTP_USER   = "jpcaamano@gmail.com"
