import sys
from pathlib import Path

import requests
import streamlit as st
from loguru import logger

BACKEND_URL = "http://backend:8000/save_query"
LOG_FILE_PATH=Path("/var/log/app.log")

logger.remove()
logger.add(sys.stderr, level="INFO", colorize=True)
logger.add(
    LOG_FILE_PATH,
    level="INFO",
    rotation="1 MB"
)


st.title("Submit a Query to the Backend")

query_text = st.text_input("Enter some text:", placeholder="Your query here...")

if st.button("Submit"):
    if not query_text:
        st.error("Please enter some text.")
        logger.warning("Empty query")
    else:
        try:
            payload = {"text": query_text}
            response = requests.post(BACKEND_URL, json=payload)

            response.raise_for_status()

            result = response.json()
            st.success(f"Success: {result.get('message', 'Query saved!')}")
            logger.success("sent payload to backend")

        except requests.exceptions.ConnectionError as e:
            logger.error(f"HTTP error from backend {e}")
            st.error("Error: Could not connect to the backend. Is it running?")
        except requests.exceptions.RequestException as e:
            logger.critical(f"An unexpected error {e}")
            st.error(f"An error occurred: {e}")