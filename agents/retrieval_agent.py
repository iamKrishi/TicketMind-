from utils.llm_client import call_llm_json
from data.knowledge_base import KNOWLEDGE_BASE

SYSTEM_PROMPT = """You are a Knowledge Retrieval Agent for a customer support system.
You will be given a customer ticket and a list of knowledge base articles (each with an id,
category, question, and answer).

Find the SINGLE best matching article for this ticket, if any exists.
Respond ONLY with a JSON object:

{
  "match_found": true | false,
  "matched_id": "kb00X" or null,
  "confidence": "high" | "medium" | "low",
  "reason": "short reason for the match or why nothing matched"
}

If nothing in the knowledge base reasonably answers the ticket, set match_found to false."""


def run(ticket_text: str, category: str) -> dict:
    # Narrow the knowledge base to the classified category (plus "other" fallback) to keep prompts small
    relevant_articles = [a for a in KNOWLEDGE_BASE if a["category"] == category] or KNOWLEDGE_BASE

    kb_text = "\n".join(
        f"- id: {a['id']} | category: {a['category']} | Q: {a['question']} | A: {a['answer']}"
        for a in relevant_articles
    )

    user_prompt = f"Ticket:\n{ticket_text}\n\nKnowledge Base Articles:\n{kb_text}"
    result = call_llm_json(SYSTEM_PROMPT, user_prompt)

    # Attach the full matched article (if any) so downstream agents have the actual answer text
    if result.get("match_found") and result.get("matched_id"):
        matched = next((a for a in KNOWLEDGE_BASE if a["id"] == result["matched_id"]), None)
        result["matched_article"] = matched
    else:
        result["matched_article"] = None

    return result
