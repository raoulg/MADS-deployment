import uvicorn
from calculator.api import app
from loguru import logger


def main():
    try:
        config = uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=True,  # Enable auto-reload during development
        )
        server = uvicorn.Server(config)
        logger.info("Check http://127.0.0.1:8000/docs for API documentation")
        logger.info("Starting FastAPI server")
        server.run()

    except Exception as e:
        logger.error(f"Error starting FastAPI server: {e}")
        raise
