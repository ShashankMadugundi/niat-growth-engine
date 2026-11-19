
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_secret(key, default=None):
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default


GEMINI_API_KEY = (
    get_secret("GEMINI_API_KEY")
    or os.getenv("GEMINI_API_KEY")
)

GOOGLE_SHEET_ID = (
    get_secret("GOOGLE_SHEET_ID")
    or os.getenv("GOOGLE_SHEET_ID")
)

GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv(
    "GOOGLE_SERVICE_ACCOUNT_FILE",
    "service_account.json"
)

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing")

if not GOOGLE_SHEET_ID:
    raise ValueError("GOOGLE_SHEET_ID is missing")
