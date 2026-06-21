const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ExtractedFact {
  fact: string;
  source_sentence: string;
}

export interface EvaluatedMemory {
  fact: string;
  source_sentence: string;
  type: "episodic" | "semantic" | "procedural";
  importance: number;
  confidence: number;
  decision: "keep" | "drop";
  tier: "session" | "long_term";
  reason: string;
}

export interface TraceSpan {
  name: string;
  span_id: string;
  duration_ms: number | null;
  tokens_in: number;
  tokens_out: number;
  model: string;
  metadata: Record<string, unknown>;
  error: string | null;
}

export interface Trace {
  trace_id: string;
  total_duration_ms: number;
  total_tokens_in: number;
  total_tokens_out: number;
  spans: TraceSpan[];
}

export interface CaptureResponse {
  extraction: ExtractedFact[];
  evaluation: EvaluatedMemory[];
  stored: { session: string[]; long_term: string[] };
  trace: Trace;
}

export interface RetrievedMemory {
  id: string;
  fact: string;
  memory_type: "episodic" | "semantic" | "procedural";
  importance: number;
  confidence: number;
  tier: "session" | "long_term";
  similarity_score: number;
  signal: string;
}

export interface RetrieveResponse {
  retrieved_memories: RetrievedMemory[];
  answer: string;
  trace: Trace;
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let message = `Request failed: ${res.status}`;
    try {
      const body = await res.json();
      if (body.error) message = body.error;
    } catch {
      // ignore parse errors
    }
    throw new Error(message);
  }
  return res.json();
}

export async function captureMemories(text: string): Promise<CaptureResponse> {
  const res = await fetch(`${API_BASE}/api/capture`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  return handleResponse<CaptureResponse>(res);
}

export async function retrieveMemories(
  question: string
): Promise<RetrieveResponse> {
  const res = await fetch(`${API_BASE}/api/retrieve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  return handleResponse<RetrieveResponse>(res);
}
