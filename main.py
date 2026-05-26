from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from datetime import datetime

app = FastAPI()

class JobExecution(BaseModel):
    endpoint: str
    params: dict = {}
    job_id: str

@app.post("/execute")
async def execute_job(job: JobExecution):
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(job.endpoint, params=job.params)
            return {
                "job_id": job.job_id,
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "response_code": resp.status_code,
                "response": resp.json() if 'application/json' in resp.headers.get('content-type', '') else resp.text[:500]
            }
    except Exception as e:
        return {"job_id": job.job_id, "status": "error", "error": str(e)}

@app.get("/health")
def health():
    return {"status": "alive"}

@app.get("/")
def root():
    return {"service": "oracle-relay-bot"}
