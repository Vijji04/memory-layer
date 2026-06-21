import json
import uuid
from datetime import datetime, timezone

import numpy as np
from sqlalchemy import Column, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings
from app.models.memory import (
    EvaluatedMemory,
    MemoryTier,
    RetrievedMemory,
)

Base = declarative_base()


class MemoryRecord(Base):
    __tablename__ = "memories"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex[:12])
    fact = Column(Text, nullable=False)
    memory_type = Column(String, nullable=False)
    importance = Column(Integer, nullable=False)
    confidence = Column(Float, nullable=False)
    tier = Column(String, nullable=False)
    reason = Column(Text, nullable=False)
    embedding = Column(Text, nullable=False)  # JSON-serialized float array
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,    # reconnect on stale connections (Neon serverless)
    pool_recycle=300,       # recycle connections every 5 min
)
SessionLocal = sessionmaker(bind=engine)

# In-memory session store
_session_memories: dict[str, list[dict]] = {"default": []}


async def init_db():
    Base.metadata.create_all(engine)


def store_long_term_memory(
    memory: EvaluatedMemory, embedding: list[float]
) -> str:
    record_id = uuid.uuid4().hex[:12]
    with SessionLocal() as db:
        record = MemoryRecord(
            id=record_id,
            fact=memory.fact,
            memory_type=memory.type.value,
            importance=memory.importance,
            confidence=memory.confidence,
            tier=memory.tier.value,
            reason=memory.reason,
            embedding=json.dumps(embedding),
        )
        db.add(record)
        db.commit()
    return record_id


def store_session_memory(
    memory: EvaluatedMemory, embedding: list[float], session_id: str = "default"
) -> str:
    memory_id = uuid.uuid4().hex[:12]
    if session_id not in _session_memories:
        _session_memories[session_id] = []
    _session_memories[session_id].append(
        {
            "id": memory_id,
            "fact": memory.fact,
            "memory_type": memory.type.value,
            "importance": memory.importance,
            "confidence": memory.confidence,
            "tier": memory.tier.value,
            "reason": memory.reason,
            "embedding": embedding,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    return memory_id


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    a_arr = np.array(a)
    b_arr = np.array(b)
    dot = np.dot(a_arr, b_arr)
    norm = np.linalg.norm(a_arr) * np.linalg.norm(b_arr)
    if norm == 0:
        return 0.0
    return float(dot / norm)


def search_long_term(
    query_embedding: list[float], top_k: int = 5
) -> list[RetrievedMemory]:
    with SessionLocal() as db:
        records = db.query(MemoryRecord).all()

    scored = []
    for r in records:
        emb = json.loads(r.embedding)
        sim = _cosine_similarity(query_embedding, emb)
        scored.append((r, sim))

    scored.sort(key=lambda x: x[1], reverse=True)
    results = []
    for r, sim in scored[:top_k]:
        signal_parts = [f"semantic similarity: {sim:.3f}"]
        if r.importance >= 7:
            signal_parts.append(f"high importance ({r.importance}/10)")
        elif r.importance >= 4:
            signal_parts.append(f"moderate importance ({r.importance}/10)")
        results.append(
            RetrievedMemory(
                id=r.id,
                fact=r.fact,
                memory_type=r.memory_type,
                importance=r.importance,
                confidence=r.confidence,
                tier=r.tier,
                similarity_score=round(sim, 4),
                signal=" | ".join(signal_parts),
            )
        )
    return results


def search_session(
    query_embedding: list[float],
    session_id: str = "default",
    top_k: int = 5,
) -> list[RetrievedMemory]:
    memories = _session_memories.get(session_id, [])
    scored = []
    for m in memories:
        sim = _cosine_similarity(query_embedding, m["embedding"])
        scored.append((m, sim))

    scored.sort(key=lambda x: x[1], reverse=True)
    results = []
    for m, sim in scored[:top_k]:
        signal_parts = [f"semantic similarity: {sim:.3f}"]
        if m["importance"] >= 7:
            signal_parts.append(f"high importance ({m['importance']}/10)")
        elif m["importance"] >= 4:
            signal_parts.append(f"moderate importance ({m['importance']}/10)")
        results.append(
            RetrievedMemory(
                id=m["id"],
                fact=m["fact"],
                memory_type=m["memory_type"],
                importance=m["importance"],
                confidence=m["confidence"],
                tier=m["tier"],
                similarity_score=round(sim, 4),
                signal=" | ".join(signal_parts),
            )
        )
    return results
