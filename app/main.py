from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from app.texttoimg.routes import image as text_to_image

import requests

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",  # Adjust this depending on where your frontend is hosted
    "http://localhost:3000",
    "http://127.0.0.1:8000"
]
#CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow all origins (adjust in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routes
app.include_router(text_to_image.router,prefix="/text_to_image", tags=["Text to Image"])


# Serve the common selection page
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("frontend/index.html") as f:
        return HTMLResponse(f.read())

# Serve the Text to Image HTML page
@app.get("/text_to_image", response_class=HTMLResponse)
def text_to_image_page():
    with open("frontend/text2img.html") as f:
        return HTMLResponse(f.read())

# # Serve the Image to Image HTML page
# @app.get("/image_to_image", response_class=HTMLResponse)
# def image_to_image_page():
#     with open("frontend/imgtoimg.html") as f:
#         return HTMLResponse(f.read())



app.mount("/", StaticFiles(directory="frontend"), name="frontend")

