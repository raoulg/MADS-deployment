from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Option 1: Serve image directly
@app.get("/image")
async def get_image():
    image_path = Path("./img/clustering.png")  # Replace with your image path
    return FileResponse(image_path)


# Option 2: Serve HTML page with embedded image
@app.get("/show", response_class=HTMLResponse)
async def show_image():
    return """
    <html>
        <body style="text-align: center; background-color: #8FBC8F;">
            <h1>My Image</h1>
            <img src="/image" alt="Display Image">
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
