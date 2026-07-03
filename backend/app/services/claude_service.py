import json

from anthropic import AsyncAnthropic

from app.core.config import settings

_client: AsyncAnthropic | None = None


def _get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


FLAVOR_PARSE_SYSTEM_PROMPT = """You turn loose, informal coffee tasting notes into structured JSON.

Return ONLY a JSON object (no markdown fences, no preamble) with this shape:
{
  "flavor_tags": ["string", ...],   // 2-6 short flavor descriptors, e.g. "stone fruit", "dark chocolate"
  "acidity": "low" | "medium" | "high" | null,
  "body": "light" | "medium" | "heavy" | null,
  "sweetness": "low" | "medium" | "high" | null,
  "summary": "one sentence, plain language, under 20 words"
}

If the input doesn't give enough signal for a field, use null. Never invent specifics the input doesn't support.
"""


async def parse_flavor_notes(raw_notes: str) -> dict:
    """Call Claude to convert freeform tasting notes into structured flavor data.

    Falls back to an empty structure if no API key is configured or the call fails,
    so bean/tasting-entry creation never hard-fails on this enrichment step.
    """
    if not settings.anthropic_api_key:
        return {}

    try:
        client = _get_client()
        response = await client.messages.create(
            model="claude-sonnet-5",
            max_tokens=500,
            system=FLAVOR_PARSE_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": raw_notes}],
        )
        text_block = next((b for b in response.content if b.type == "text"), None)
        if not text_block:
            return {}
        return json.loads(text_block.text)
    except Exception:
        # Enrichment is a nice-to-have; never block the write path on it.
        return {}
