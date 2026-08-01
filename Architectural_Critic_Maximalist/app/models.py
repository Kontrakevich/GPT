from typing import Any, Literal
from pydantic import BaseModel, Field


class ProjectRequest(BaseModel):
    project_id: str = Field(min_length=3)
    brief: str = Field(min_length=20)
    knowledge_context: list[str] = []
    max_iterations: int | None = Field(default=None, ge=1, le=10)


class Scorecard(BaseModel):
    architecture: int = 0
    urban_design: int = 0
    landscape: int = 0
    engineering: int = 0
    buildability: int = 0
    regulatory_compliance: int = 0
    composition: int = 0
    visualization: int = 0
    editorial_quality: int = 0
    investment_credibility: int = 0
    consistency: int = 0
    source_reliability: int = 0
    overall_confidence: int = 0


class CriticDecision(BaseModel):
    decision: Literal["approved", "revise", "rejected"]
    scorecard: Scorecard
    critical_failures: list[str] = []
    major_weaknesses: list[str] = []
    missed_opportunities: list[str] = []
    unsupported_claims: list[str] = []
    correction_directive: list[str] = []
    candidate_skill_update: dict[str, Any] | None = None


class ProjectRunResponse(BaseModel):
    project_id: str
    status: Literal["approved", "rejected", "iteration_limit"]
    iterations: int
    final_project: dict[str, Any]
    final_review: CriticDecision
    execution_log: list[dict[str, Any]]
