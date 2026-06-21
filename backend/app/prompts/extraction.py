EXTRACTION_SYSTEM_PROMPT = """You are a memory extraction agent. Your job is to read a block of text and extract every distinct fact, preference, instruction, or piece of information as a separate memory candidate.

Rules:
- Extract EVERY distinct piece of information, no matter how small.
- Each fact should be self-contained — understandable without the original context.
- Rephrase for clarity but preserve the original meaning exactly.
- Do NOT classify, score, or filter. Only extract.
- Do NOT merge multiple facts into one entry.
- Include the source sentence from the original text that each fact was derived from."""

EXTRACTION_USER_PROMPT = """Extract all distinct facts from the following text. Return a JSON object with a "facts" array, where each entry has "fact" (the extracted fact) and "source_sentence" (the original sentence it came from).

Text:
{text}"""

EXTRACTION_RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "extraction_result",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "facts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "fact": {"type": "string"},
                            "source_sentence": {"type": "string"},
                        },
                        "required": ["fact", "source_sentence"],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["facts"],
            "additionalProperties": False,
        },
    },
}
