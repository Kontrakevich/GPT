# Architectural Critic & Maximalist

Version 0.1.0

A supervisor-first multi-agent system for architectural project development.

The user communicates only with the **Architectural Critic & Maximalist**. The Critic delegates project creation to an internal **Architectural Project Creator**, audits both the project and the creator process, and returns the work for revision until the quality gate is passed.

## Architecture

```text
USER
  ↓
CRITIC & MAXIMALIST
  ↓
PROJECT CREATOR
  ↓
PROJECT PACKAGE + EXECUTION LOG
  ↓
CRITIC REVIEW
  ├─ REVISE → CREATOR
  └─ APPROVE → USER
```

## Included

- FastAPI service
- OpenRouter client
- critic/creator orchestration loop
- structured JSON contracts
- diagnostic logging
- n8n importable workflow
- immutable skill separation
- candidate skill update output
- project package persistence

## Quick start

1. Copy `.env.example` to `.env`.
2. Set `OPENROUTER_API_KEY`.
3. Install: `pip install -r requirements.txt`
4. Run: `uvicorn app.main:app --host 0.0.0.0 --port 8040`
5. Open: `http://127.0.0.1:8040/docs`

## Main endpoint

`POST /api/v1/projects/run`

The Critic does not automatically modify its own skill or the Creator skill. It may only produce a `candidate_skill_update` proposal for explicit human approval.
