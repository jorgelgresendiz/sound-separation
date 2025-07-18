from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import shutil
import subprocess

app = FastAPI()

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")
DOWNLOAD_DIR = Path("downloads")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sound Separation GET"}

@app.post("/separate")
async def separate_audio(file: UploadFile = File(...)):
    upload_path = UPLOAD_DIR / file.filename

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run Spleeter
    command = [
        "spleeter", "separate",
        str(upload_path),
        "-p", "spleeter:2stems",
        "-o", str(OUTPUT_DIR)
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        return JSONResponse(
            status_code=500,
            content={"error": "Spleeter failed to process the audio file."}
        )

    track_folder = OUTPUT_DIR / upload_path.stem
    if not track_folder.exists():
        return JSONResponse(
            status_code=404,
            content={"error": "Separated files not found."}
        )

    separated_files = [f.name for f in track_folder.iterdir()]
    return {
        "original": file.filename,
        "separated_files": separated_files,
        "download_path": f"/output/{upload_path.stem}/"
    }

@app.get("/download/{folder_name}/{filename}")
async def download_audio(folder_name: str, track_name: str):
    file_path = OUTPUT_DIR/folder_name/track_name

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="track not found")
    return FileResponse(path=file_path, filename=track_name,media_type="audio/wav")
    