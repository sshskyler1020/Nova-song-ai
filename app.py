from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydub import AudioSegment
import tempfile
import os

app = FastAPI()

# CORS for Google Sites
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process")
async def process(vocals: list[UploadFile] = File(...), beat: UploadFile = File(...)):
    try:
        beat_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        with open(beat_path, "wb") as f:
            f.write(await beat.read())

        final = AudioSegment.from_file(beat_path)

        for v in vocals:
            vp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
            with open(vp, "wb") as f:
                f.write(await v.read())
            vocal_audio = AudioSegment.from_file(vp).normalize()
            final = final.overlay(vocal_audio)

        final = final.normalize()

        out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        final.export(out_path, format="wav")

        return FileResponse(out_path, filename="final_song.wav")

    except Exception as e:
        return {"error": str(e)}
