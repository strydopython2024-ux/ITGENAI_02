from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.data_service import has_dataset
from app.services.generic_analysis_service import profile
from app.services.gemini_service import (
    GEMINI_MODEL,
    ask_gemini,
    create_ai_context,
    gemini_status,
)

router = APIRouter(prefix="/api/ai", tags=["AI"])


class ChatMessage(BaseModel):
    role: str
    content: str


class AIRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4000)
    history: list[ChatMessage] = Field(default_factory=list)


def _dataset_context() -> str:
    if not has_dataset():
        raise HTTPException(
            status_code=400,
            detail="No dataset is currently uploaded. Upload a CSV file first.",
        )

    dataset_profile = profile()
    if not dataset_profile.get("success"):
        raise HTTPException(
            status_code=400,
            detail=dataset_profile.get("message", "Unable to analyze the active dataset."),
        )

    return create_ai_context(dataset_profile)


@router.post("/chat")
def chat(request: AIRequest):
    try:
        context = _dataset_context()
        history = [item.model_dump() for item in request.history[-10:]]
        answer = ask_gemini(request.question, context, history)

        return {
            "success": True,
            "provider": "Google Gemini",
            "model": GEMINI_MODEL,
            "answer": answer,
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Gemini error: {exc}") from exc


# Keep the original endpoint available so existing clients do not break.
@router.post("/insights")
def generate_insights(request: AIRequest):
    try:
        context = _dataset_context()
        answer = ask_gemini(request.question, context)

        return {
            "success": True,
            "provider": "Google Gemini",
            "model": GEMINI_MODEL,
            "answer": answer,
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Gemini error: {exc}") from exc


@router.get("/status")
def status():
    return {"success": True, **gemini_status(), "dataset_available": has_dataset()}
