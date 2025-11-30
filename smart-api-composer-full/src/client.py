# src/client.py

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_PLANNER = "gemini-2.5-flash-lite"   # or another model you have access to
MODEL_REPORTER = "gemini-2.5-flash-lite"


def get_client() -> genai.Client:
    """
    Returns a configured Google Generative AI client.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:

        raise RuntimeError("GOOGLE_API_KEY environment variable is not set.")
    return genai.Client(api_key=api_key)
