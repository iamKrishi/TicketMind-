# 🎧 SupportResolver AI — Autonomous Customer Support Ticket Resolver

A multi-agent AI system that classifies, researches, and **autonomously decides**
whether a customer support ticket can be auto-resolved or must be escalated to a
human — the core "agentic" behavior recruiters look for: agents making a real
decision, not just chaining prompts.

## How it works

1. **Classifier Agent** — categorizes the ticket (billing/technical/account),
   assesses urgency and sentiment
2. **Retrieval Agent** — searches a knowledge base for a matching solution,
   returns a confidence level
3. **Decision Agent** — autonomously decides: `auto_reply` or `escalate`, based on
   urgency, sentiment, and match confidence
4. **Response Agent** — drafts either a customer-facing reply (auto-reply case) or
   an internal handoff note for a human agent (escalation case)

This is genuinely agentic because the **Decision Agent branches based on its own
judgment** — the pipeline path is not fixed in code, it's determined by the model
reasoning over the ticket at runtime.

## Setup

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"      # Mac/Linux
# set OPENAI_API_KEY=your-key-here         # Windows

streamlit run app.py
```

Open the local URL Streamlit prints. Try the sample tickets in the dropdown —
one is designed to auto-reply, one is designed to escalate — to demo the
branching decision live.

## Tech Stack

- Python
- Streamlit (UI)
- OpenAI API (agent reasoning, JSON mode for structured outputs)
- Hardcoded knowledge base (`data/knowledge_base.py`) — swappable for a real DB/CSV

## Future Enhancements

- Replace hardcoded KB with a vector database (ChromaDB) for semantic search over
  hundreds/thousands of real support articles
- Add a **Learning Loop**: log escalated tickets + human resolutions, periodically
  auto-generate new KB articles from them
- Real ticketing system integration (Zendesk/Freshdesk API) instead of manual paste
- Multi-turn conversation support (follow-up questions from the customer)
- Analytics dashboard: auto-resolve rate, escalation reasons breakdown, response time

## Resume Description

> Built SupportResolver AI, a multi-agent customer support automation system where
> agents autonomously classify tickets, retrieve relevant knowledge base solutions,
> and decide in real time whether to auto-resolve or escalate to a human — reducing
> manual triage effort. Implemented with Python, OpenAI API (structured JSON
> outputs), and Streamlit.
