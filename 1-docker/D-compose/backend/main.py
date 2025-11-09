import json
import sys
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel

LOG_FILE_PATH=Path("/var/log/app.log")
DATA_DIR = Path("/data")

logger.remove()
logger.add(sys.stderr, level="INFO", colorize=True)
logger.add(
    LOG_FILE_PATH,
    level="INFO",
    rotation="1 MB",
)

class Query(BaseModel):
    text: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for simplicity)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    """A simple root endpoint to check if the backend is running."""
    return {"message": "Backend is running!"}

@app.post("/save_query")
def save_query(query: Query):
    """
    Receives a query, adds a timestamp, and saves it to a JSON file.
    """
    try:
        if not DATA_DIR.exists():
            logger.info(f"Creating datadir at {DATA_DIR}")
            DATA_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now()
        data = {
            "timestamp": timestamp.isoformat(),
            "query": query.text
        }

        filename = f"{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.json"
        filepath = DATA_DIR / filename

        with filepath.open('w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Successfully saved query to {filepath}")
        return {"message": f"Query saved to {filename}"}

    except Exception as e:
        logger.error(f"Error saving query: {e}")
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail=f"an error: {e}"
        )