from datetime import datetime, timezone
from pathlib import Path
import json

from .config import settings
from .models import ProjectRequest, ProjectRunResponse, CriticDecision
from .openrouter import OpenRouterClient

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "data" / "projects"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_knowledge(paths: list[str]) -> str:
    chunks: list[str] = []
    for item in paths:
        path = ROOT / item
        if path.exists() and path.is_file():
            chunks.append(f"\n--- SOURCE: {item} ---\n{_read(path)}")
    return "\n".join(chunks)


def _save(project_id: str, name: str, data: dict) -> None:
    folder = PROJECTS / project_id
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class ArchitecturalSupervisor:
    def __init__(self) -> None:
        self.client = OpenRouterClient()
        self.creator_skill = _read(ROOT / "skills/project_creator/SKILL.md")
        self.critic_skill = _read(ROOT / "skills/critic_maximalist/SKILL.md")

    async def run(self, request: ProjectRequest) -> ProjectRunResponse:
        max_iterations = request.max_iterations or settings.max_iterations
        knowledge = _load_knowledge(request.knowledge_context)
        execution_log: list[dict] = []
        correction_directive: list[str] = []
        project: dict = {}
        final_review: dict = {}

        for iteration in range(1, max_iterations + 1):
            creator_input = {
                "brief": request.brief,
                "knowledge": knowledge,
                "iteration": iteration,
                "correction_directive": correction_directive,
                "required_output": "Complete project package plus evidence and self-QC."
            }
            project = await self.client.complete_json(
                model=settings.openrouter_creator_model,
                system_prompt=self.creator_skill,
                user_prompt=json.dumps(creator_input, ensure_ascii=False),
                temperature=0.35,
            )
            _save(request.project_id, f"iteration_{iteration:02d}_creator.json", project)

            critic_input = {
                "brief": request.brief,
                "knowledge": knowledge,
                "iteration": iteration,
                "creator_output": project,
                "quality_gate": settings.quality_gate,
            }
            final_review = await self.client.complete_json(
                model=settings.openrouter_critic_model,
                system_prompt=self.critic_skill,
                user_prompt=json.dumps(critic_input, ensure_ascii=False),
                temperature=0.1,
            )
            _save(request.project_id, f"iteration_{iteration:02d}_critic.json", final_review)

            decision = CriticDecision.model_validate(final_review)
            execution_log.append({
                "iteration": iteration,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "decision": decision.decision,
                "overall_confidence": decision.scorecard.overall_confidence,
                "critical_failures": decision.critical_failures,
            })

            if decision.decision in {"approved", "rejected"}:
                result = ProjectRunResponse(
                    project_id=request.project_id,
                    status=decision.decision,
                    iterations=iteration,
                    final_project=project,
                    final_review=decision,
                    execution_log=execution_log,
                )
                _save(request.project_id, "final_result.json", result.model_dump())
                return result

            correction_directive = decision.correction_directive

        decision = CriticDecision.model_validate(final_review)
        result = ProjectRunResponse(
            project_id=request.project_id,
            status="iteration_limit",
            iterations=max_iterations,
            final_project=project,
            final_review=decision,
            execution_log=execution_log,
        )
        _save(request.project_id, "final_result.json", result.model_dump())
        return result
