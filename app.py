from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
from jobs import create_job, add_job, JOBS
from worker import process_job
from users import get_user, authenticate_user
import tempfile

app = FastAPI()

# Allow Google Sites
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Signup/Login (simple JWT-based)
@app.post("/signup")
def signup(email: str = Form(...), password: str = Form(...)):
    from users import create_user
    return create_user(email, password)

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    from users import login_user
    token = login_user(email, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": token}

# Start Job
@app.post("/start-job")
async def start_job(token: str = Form(...), vocals: list[UploadFile] = File(...), beat: UploadFile = File(...), preset: str = Form(...)):
    user = get_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check length for free users
    beat_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    with open(beat_path, "wb") as f:
        f.write(await beat.read())

    from pydub import AudioSegment
    audio = AudioSegment.from_file(beat_path)
    if not user["is_premium"] and len(audio) > 3*60*1000:
        raise HTTPException(status_code=400, detail="Free users max 3 minutes")

    # Save vocals
    vocal_paths = []
    for v in vocals:
        vp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        with open(vp, "wb") as f:
            f.write(await v.read())
        vocal_paths.append(vp)

    # Create job and add to queue
    job_id = create_job()
    add_job(job_id, user["is_premium"])

    Thread(target=process_job, args=(job_id, vocal_paths, beat_path, user["is_premium"], preset)).start()
    return {"job_id": job_id}

# Progress Polling
@app.get("/progress/{job_id}")
def progress(job_id: str):
    return JOBS.get(job_id, {"status": "not_found"})

# Download Result
@app.get("/download/{job_id}")
def download(job_id: str):
    job = JOBS.get(job_id)
    if job and job["status"] == "done":
        return FileResponse(job["file"], filename="final_song.wav")
    else:
        raise HTTPException(status_code=404, detail="File not ready")        final.export(out_path, format="wav")

        return FileResponse(out_path, filename="final_song.wav")

    except Exception as e:
        return {"error": str(e)}
