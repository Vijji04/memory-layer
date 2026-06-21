EVALUATION_SYSTEM_PROMPT = """You are a memory evaluation judge. For each candidate fact, you must classify it and decide whether it is worth remembering.

Classification rules:
- episodic: A specific event, occurrence, or time-bound fact (e.g., "I had coffee this morning", "We shipped v2 last Tuesday")
- semantic: A general truth, preference, belief, or enduring fact about the world or the person (e.g., "I prefer Python over Java", "The team uses PostgreSQL")
- procedural: A rule, process, instruction, or how-to (e.g., "Always use type hints in Python", "Deploy with docker compose up")

Scoring rules:
- importance (1-10): How useful is this fact for future interactions? 1 = trivial/throwaway, 10 = critical preference or instruction
- confidence (0-1): How confident are you in your classification and importance score?
- decision: "keep" if importance >= 4, "drop" if importance < 4. Trivial, ephemeral, or uninformative facts should be dropped.
- tier: "session" if the fact is specific to a current project, task, or temporary context. "long_term" if the fact is a durable preference, recurring instruction, or general truth.
- reason: One sentence explaining your decision."""

EVALUATION_USER_PROMPT = """Evaluate each of the following candidate memories. Return a JSON object with a "memories" array.

Candidates:
{candidates_json}"""

EVALUATION_RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "evaluation_result",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "memories": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "fact": {"type": "string"},
                            "source_sentence": {"type": "string"},
                            "type": {
                                "type": "string",
                                "enum": ["episodic", "semantic", "procedural"],
                            },
                            "importance": {"type": "integer"},
                            "confidence": {"type": "number"},
                            "decision": {
                                "type": "string",
                                "enum": ["keep", "drop"],
                            },
                            "tier": {
                                "type": "string",
                                "enum": ["session", "long_term"],
                            },
                            "reason": {"type": "string"},
                        },
                        "required": [
                            "fact",
                            "source_sentence",
                            "type",
                            "importance",
                            "confidence",
                            "decision",
                            "tier",
                            "reason",
                        ],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["memories"],
            "additionalProperties": False,
        },
    },
}
