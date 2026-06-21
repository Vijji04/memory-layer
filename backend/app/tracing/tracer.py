import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field


@dataclass
class Span:
    name: str
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    duration_ms: float | None = None
    tokens_in: int = 0
    tokens_out: int = 0
    model: str = ""
    metadata: dict = field(default_factory=dict)
    error: str | None = None

    def finish(self):
        self.end_time = time.time()
        self.duration_ms = round((self.end_time - self.start_time) * 1000, 2)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "span_id": self.span_id,
            "duration_ms": self.duration_ms,
            "tokens_in": self.tokens_in,
            "tokens_out": self.tokens_out,
            "model": self.model,
            "metadata": self.metadata,
            "error": self.error,
        }


class Trace:
    def __init__(self):
        self.trace_id = uuid.uuid4().hex[:12]
        self.spans: list[Span] = []
        self.start_time = time.time()

    @contextmanager
    def span(self, name: str):
        s = Span(name=name)
        self.spans.append(s)
        try:
            yield s
        except Exception as e:
            s.error = str(e)
            raise
        finally:
            s.finish()

    def to_dict(self) -> dict:
        total_ms = round((time.time() - self.start_time) * 1000, 2)
        total_tokens_in = sum(s.tokens_in for s in self.spans)
        total_tokens_out = sum(s.tokens_out for s in self.spans)
        return {
            "trace_id": self.trace_id,
            "total_duration_ms": total_ms,
            "total_tokens_in": total_tokens_in,
            "total_tokens_out": total_tokens_out,
            "spans": [s.to_dict() for s in self.spans],
        }
