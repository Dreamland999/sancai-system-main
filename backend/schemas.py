from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ─── Recommend ────────────────────────────────────────────

class UserStateRequest(BaseModel):
    scene: List[str] = Field(default_factory=list)
    body: List[str] = Field(default_factory=list)
    mood: List[str] = Field(default_factory=list)
    needs: List[str] = Field(default_factory=list)
    limits: List[str] = Field(default_factory=list)
    flavor_preference: List[str] = Field(default_factory=list)
    temperature_preference: List[str] = Field(default_factory=list)


class RecommendItem(BaseModel):
    recipe_id: str
    name: str
    type: str = ""
    score: float
    match_reason: str = ""
    polished_text: str = ""
    visual_prompt: str = ""
    visual_mapping: List[Dict[str, Any]] = Field(default_factory=list)
    image_url: Optional[str] = None
    health_notes: List[str] = Field(default_factory=list)
    description: str = ""
    sweetness: str = ""
    temperature: str = ""


class RecommendResponse(BaseModel):
    session_id: str
    status: Dict[str, Any] = Field(default_factory=dict)
    avoided_items: List[str] = Field(default_factory=list)
    pipeline: List[str] = Field(default_factory=list)
    model_mode: str = ""
    recommendations: List[RecommendItem] = Field(default_factory=list)


# ─── Feedback ─────────────────────────────────────────────

class FeedbackRequest(BaseModel):
    recommendation_id: str = ""
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    recipe_id: Optional[str] = None
    event_type: Optional[str] = None
    rating: Optional[float] = None
    state_feedback: Optional[str] = None
    taste_feedback: List[str] = Field(default_factory=list)
    visual_feedback: Optional[str] = None
    retry_intention: Optional[str] = None
    feedback_text: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None


class FeedbackResponse(BaseModel):
    feedback_id: Optional[str] = None
    status: str
    message: str = ""


# ─── Options ──────────────────────────────────────────────

class OptionsResponse(BaseModel):
    scene_options: List[str] = Field(default_factory=list)
    body_options: List[str] = Field(default_factory=list)
    mood_options: List[str] = Field(default_factory=list)
    need_options: List[str] = Field(default_factory=list)
    limit_options: List[str] = Field(default_factory=list)
    flavor_options: List[str] = Field(default_factory=list)
    temperature_options: List[str] = Field(default_factory=list)


# ─── Chat ─────────────────────────────────────────────────

class ChatRequest(BaseModel):
    user_id: Optional[str] = None
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    reply: str
    session_id: Optional[str] = None


# ─── Image ────────────────────────────────────────────────

class ImageGenerateRequest(BaseModel):
    recipe_id: str
    visual_prompt: str
    style: Optional[str] = None


class ImageGenerateResponse(BaseModel):
    status: str
    image_url: Optional[str] = None
    prompt: str
    task_id: Optional[str] = None


# ─── Intent Parse ─────────────────────────────────────────

class IntentParseRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None


class IntentParseResponse(BaseModel):
    scene: List[str] = Field(default_factory=list)
    body: List[str] = Field(default_factory=list)
    mood: List[str] = Field(default_factory=list)
    needs: List[str] = Field(default_factory=list)
    limits: List[str] = Field(default_factory=list)
    flavor_preference: List[str] = Field(default_factory=list)
    temperature_preference: List[str] = Field(default_factory=list)


# ─── Stores ───────────────────────────────────────────────

class StoreItem(BaseModel):
    store_id: str
    name: str
    address: str = ""
    distance: float = 0.0
    is_open: bool = True


class StoreListResponse(BaseModel):
    stores: List[StoreItem] = Field(default_factory=list)


# ─── State Infer ──────────────────────────────────────────

class EmotionResult(BaseModel):
    emotion: str = ""
    emotion_cn: str = ""
    confidence: float = 0.0

class UserProfile(BaseModel):
    flavor_preference: List[str] = Field(default_factory=list)
    temperature_preference: List[str] = Field(default_factory=list)
    limits: List[str] = Field(default_factory=list)

class InferContext(BaseModel):
    time_of_day: str = ""

class StateInferRequest(BaseModel):
    message: str
    emotion_result: Optional[EmotionResult] = None
    recommend_input: Optional[UserStateRequest] = None
    user_profile: Optional[UserProfile] = None
    context: Optional[InferContext] = None

class StateInferResponse(BaseModel):
    summary: str
    state_guess: UserStateRequest
    confidence: float = 0.0
    need_confirm: bool = True
