from fastapi import FastAPI, HTTPException
from .models import ProjectRequest, ProjectRunResponse
from .orchestrator import ArchitecturalSupervisor

app = FastAPI(
    title="Architectural Critic & Maximalist",
    version="0.1.0",
    description="Supervisor-first architectural multi-agent system.",
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "architectural-critic-maximalist"}


@app.post("/api/v1/projects/run", response_model=ProjectRunResponse)
async def run_project(request: ProjectRequest) -> ProjectRunResponse:
    try:
        supervisor = ArchitecturalSupervisor()
        return await supervisor.run(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
