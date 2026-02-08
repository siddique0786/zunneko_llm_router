from fastapi import FastAPI
from src.queue.request_queue import request_queue
from src.queue.tasks import process_llm_request
from src.observability.metrics import metrics_collector

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import StreamingResponse
from src.router.intelligent_router import IntelligentRouter

from src.observability.metrics_exporter import export_metrics_snapshot
from fastapi.responses import FileResponse

router_instance = IntelligentRouter()


app = FastAPI(title="Zunneko Smart LLM Router")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate")
def generate(prompt: str):

    job = request_queue.enqueue(process_llm_request, prompt)

    return {
        "status": "queued",
        "job_id": job.id
    }

@app.get("/metrics")
def get_metrics():
    return metrics_collector.report()


@app.get("/stream")
def stream_llm(prompt: str):

    def generator():
        for token in router_instance.route_stream(prompt):
            yield token

    return StreamingResponse(generator(), media_type="text/plain")

@app.get("/metrics/snapshot")
def snapshot_metrics():
    return export_metrics_snapshot()

@app.get("/metrics/download")
def download_metrics():
    export_metrics_snapshot()
    return FileResponse("metrics_snapshot.json")