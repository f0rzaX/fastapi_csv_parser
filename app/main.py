import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.parser import save_file_to_storage
from celery_worker import process_file
from fastapi.responses import FileResponse
from app.database import init_db

app = FastAPI(title="CSV Uploader API")


@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def upload_page():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))

@app.post("/uploadFile")
def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    saved_file_path = save_file_to_storage(file)
    process_file.delay(saved_file_path)

    return {"message": "File uploaded successfully"}

