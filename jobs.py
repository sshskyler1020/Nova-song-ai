import uuid

JOBS = {}

FREE_QUEUE = []
PRO_QUEUE = []

def create_job():
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"progress":0, "status":"queued", "file":None}
    return job_id

def add_job(job_id, is_pro=False):
    if is_pro:
        PRO_QUEUE.append(job_id)
    else:
        FREE_QUEUE.append(job_id)
