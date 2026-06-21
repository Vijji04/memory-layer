from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"


class MemoryTier(str, Enum):
    SESSION = "session"
    LONG_TERM = "long_term"


class Decision(str, Enum):
    KEEP = "keep"
    DROP = "drop"


# --- Extraction stage ---


class ExtractedFact(BaseModel):
    fact: str
    source_sentence: str


class ExtractionResult(BaseModel):
    facts: list[ExtractedFact]


# --- Evaluation stage ---


class EvaluatedMemory(BaseModel):
    fact: str
    source_sentence: str
    type: MemoryType
    importance: int = Field(ge=1, le=10)
    confidence: float = Field(ge=0.0, le=1.0)
    decision: Decision
    tier: MemoryTier
    reason: str


class EvaluationResult(BaseModel):
    memories: list[EvaluatedMemory]


# --- Stored memory ---


class StoredMemory(BaseModel):
    id: str
    fact: str
    memory_type: MemoryType
    importance: int
    confidence: float
    tier: MemoryTier
    reason: str
    created_at: datetime


# --- Retrieval ---


class RetrievedMemory(BaseModel):
    id: str
    fact: str
    memory_type: MemoryType
    importance: int
    confidence: float
    tier: MemoryTier
    similarity_score: float
    signal: str


# --- API request/response ---


class CaptureRequest(BaseModel):
    text: str


class CaptureResponse(BaseModel):
    extraction: list[ExtractedFact]
    evaluation: list[EvaluatedMemory]
    stored: dict[str, list[str]]  # {"session": [...facts], "long_term": [...facts]}
    trace: dict


class RetrieveRequest(BaseModel):
    question: str


class RetrieveResponse(BaseModel):
    retrieved_memories: list[RetrievedMemory]
    answer: str
    trace: dict
