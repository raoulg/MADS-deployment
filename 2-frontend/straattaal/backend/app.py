import json
from contextlib import asynccontextmanager
from pathlib import Path

import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from pydantic import BaseModel
from slanggen import models
from tokenizers import Tokenizer
from utils import sample_n

logger.add("logs/app.log", rotation="5 MB")

FRONTEND_FOLDER = Path("frontend").resolve()
logger.info(f"Frontend folder set to {FRONTEND_FOLDER} and exists: {FRONTEND_FOLDER.exists()}")
ARTEFACTS = Path("artefacts").resolve()
model_state = {}

def load_model():
    logger.info(f"Loading model and tokenizer from {ARTEFACTS}")
    tokenizerfile = str(ARTEFACTS / "tokenizer.json")
    tokenizer = Tokenizer.from_file(tokenizerfile)
    with (ARTEFACTS / "config.json").open("r") as f:
        config = json.load(f)
    model = models.SlangRNN(config["model"])
    modelpath = str(ARTEFACTS / "model.pth")
    model.load_state_dict(torch.load(modelpath, weights_only=False))
    logger.success("Model and tokenizer loaded successfully")
    return model, tokenizer

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application startup and shutdown events.
    - Validates paths
    - Loads the ML model
    """

    # because ARTEFACTS is reassigned in the if block
    # we need to declare it as global to modify it
    global ARTEFACTS

    if not FRONTEND_FOLDER.exists():
        raise FileNotFoundError(f"Cant find the frontend folder at {FRONTEND_FOLDER}")
    else:
        logger.info(f"Found {FRONTEND_FOLDER}")

    if not ARTEFACTS.exists():
        logger.warning(f"Couldnt find artefacts at {ARTEFACTS}, trying parent")
        ARTEFACTS = Path("../artefacts").resolve()
        if not ARTEFACTS.exists():
            msg = f"Cant find the artefacts folder at {ARTEFACTS}"
            raise FileNotFoundError(msg)
        else:
            logger.info(f"Found {ARTEFACTS}")
    else:
        logger.info(f"Found {ARTEFACTS}")

    model, tokenizer = load_model()
    model_state["model"] = model
    model_state["tokenizer"] = tokenizer
    logger.info("Application startup complete")

    yield

    logger.info("Application shutdown...")
    model_state.clear()
    logger.success("Application shutdown complete")


app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory=str(FRONTEND_FOLDER)), name="static")

model, tokenizer = load_model()
starred_words = []


def new_words(n: int, temperature: float):
    output_words = sample_n(
        n=n,
        model=model,
        tokenizer=tokenizer,
        max_length=20,
        temperature=temperature,
    )
    return output_words


class Word(BaseModel):
    word: str


@app.get("/generate")
async def generate_words(num_words: int = 10, temperature: float = 1.0):
    try:
        words = new_words(num_words, temperature)
        return words
    except Exception as e:
        logger.exception(f"Error generating words: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/starred")
async def get_starred_words():
    return starred_words


@app.post("/starred")
async def add_starred_word(word: Word):
    if word.word not in starred_words:
        starred_words.append(word.word)
    return starred_words


@app.post("/unstarred")
async def remove_starred_word(word: Word):
    if word.word in starred_words:
        starred_words.remove(word.word)
    return starred_words


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def read_index():
    logger.info("serving index.html")
    return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
