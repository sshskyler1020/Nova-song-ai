from pydub import AudioSegment
from jobs import JOBS
import time
import os
from audio import stems, beat, master
from presets import PRESETS

def process_job(job_id, vocal_paths, beat_path, is_premium, preset_name):
    job = JOBS[job_id]
    try:
        job["status"] = "processing"
        job["progress"] = 10

        # Load beat
        beat_audio = AudioSegment.from_file(beat_path)
        job["progress"] = 20

        # Stem separation for premium
        if is_premium:
            beat_audio, vocal_audio = stems.separate_stems_premium(beat_path, vocal_paths)
        else:
            vocal_audio = [AudioSegment.from_file(v).normalize() for v in vocal_paths]

        job["progress"] = 50

        # Overlay vocals + beat snapping
        final = beat.snap_beat(beat_audio, vocal_audio, PRESETS[preset_name]["snap"])
        job["progress"] = 70

        # Mastering
        if is_premium:
            final = master.master_advanced(final, PRESETS[preset_name])
        else:
            final = master.master_basic(final)
        job["progress"] = 90

        # Export
        out_path = f"/tmp/{job_id}.wav"
        final.export(out_path, format="wav")
        job["file"] = out_path
        job["progress"] = 100
        job["status"] = "done"

    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)
