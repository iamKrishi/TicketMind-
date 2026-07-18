from utils.llm_client import call_llm_json

SYSTEM_PROMPT = """You are a Ticket Classifier Agent for a customer support system.
Given a customer support ticket, classify it and respond ONLY with a JSON object:

{
  "category": "billing" | "technical" | "account" | "other",
  "urgency": "low" | "medium" | "high",
  "summary": "one-sentence summary of what the customer wants",
  "sentiment": "neutral" | "frustrated" | "angry" | "happy"
}

Rules:
- "high" urgency: account access lost, payment charged incorrectly, data loss, angry/urgent tone
- "medium" urgency: feature not working, billing question
- "low" urgency: general how-to questions"""


def run(ticket_text: str) -> dict:
    return call_llm_json(SYSTEM_PROMPT, f"Ticket:\n{ticket_text}")
