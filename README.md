#  TicketMind — Autonomous Customer Support Ticket Resolver

A multi-agent AI system that classifies, researches, and **autonomously decides**
whether a customer support ticket can be auto-resolved or must be escalated to a
human — the core "agentic" behavior: agents making a real decision, not just
chaining prompts together.

## How it works

1. **Classifier Agent** — categorizes the ticket (billing/technical/account),
   assesses urgency and sentiment
2. **Retrieval Agent** — searches a knowledge base for a matching solution,
   returns a confidence level
3. **Decision Agent** — autonomously decides: `auto_reply` or `escalate`, based on
   urgency, sentiment, and match confidence
4. **Response Agent** — drafts either a natural, human-sounding customer reply
   (auto-reply case) or an internal handoff note for a human agent (escalation case)

This is genuinely agentic because the **Decision Agent branches based on its own
judgment at runtime** — the pipeline path isn't hardcoded, it's determined by the
model reasoning over the ticket each time.

## Demo

Try the sample tickets in the dropdown — one is designed to auto-resolve, one is
designed to escalate — to see the branching decision live:

-  *"I forgot my password, how do I reset it?"* → auto-resolved instantly
-  *"I was charged twice and no one is responding!"* → escalated to a human, with a handoff note

## Tech Stack

- **Python**
- **Streamlit** — UI
- **Google Gemini API** (`google-genai` SDK) — agent reasoning with structured JSON outputs
- **python-dotenv** — secure API key management
- Hardcoded knowledge base (`data/knowledge_base.py`) — swappable for a real DB/CSV

## Setup

```bash
git clone https://github.com/iamKrishi/TicketMind-.git
cd TicketMind-
pip install -r requirements.txt
```

Create a `.env` file in the project root:
(Get a free key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey))

Run it:
```bash
streamlit run app.py
```

## Project Structure

TicketMind-/
├── agents/
│   ├── classifier_agent.py      # categorizes & assesses urgency
│   ├── retrieval_agent.py       # searches knowledge base
│   ├── decision_agent.py        # autonomous auto-reply vs escalate decision
│   └── response_agent.py        # drafts customer reply / handoff note
├── data/
│   └── knowledge_base.py        # FAQ articles the agent searches
├── utils/
│   └── llm_client.py            # shared Gemini API wrapper
├── app.py                       # Streamlit UI + orchestration
└── requirements.txt

## Future Enhancements

- Replace hardcoded KB with a vector database (ChromaDB) for semantic search over
  hundreds/thousands of real support articles
- Add a **Learning Loop**: log escalated tickets + human resolutions, periodically
  auto-generate new KB articles from them
- Real ticketing system integration (Zendesk/Freshdesk API) instead of manual paste
- Multi-turn conversation support (follow-up questions from the customer)
- Analytics dashboard: auto-resolve rate, escalation reasons breakdown, response time

## Resume Description

> Built TicketMind, a multi-agent customer support automation system where agents
> autonomously classify tickets, retrieve relevant knowledge base solutions, and
> decide in real time whether to auto-resolve or escalate to a human — reducing
> manual triage effort. Implemented with Python, the Gemini API (structured JSON
> outputs), and Streamlit.
