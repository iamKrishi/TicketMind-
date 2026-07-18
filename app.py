"""
SupportResolver AI - Autonomous Customer Support Ticket Resolver
Run with: streamlit run app.py
"""

import streamlit as st
from agents import classifier_agent, retrieval_agent, decision_agent, response_agent
from data.knowledge_base import KNOWLEDGE_BASE

st.set_page_config(page_title="TicketMind", page_icon="🎫", layout="wide")

# ---------------------------------------------------------------------------
# Custom styling — ops-desk / ticket-stub visual identity
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
code, .mono { font-family: 'IBM Plex Mono', monospace; }

.brand-row { display: flex; align-items: baseline; gap: 14px; margin-bottom: 2px; }
.brand-title { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 2.3rem;
                letter-spacing: -0.02em; color: #F1EEE6; margin: 0; }
.brand-tag { font-family: 'IBM Plex Mono', monospace; font-size: 0.78rem; color: #8C93A0;
             letter-spacing: 0.04em; text-transform: uppercase; }
.brand-sub { color: #9AA3AF; font-size: 0.98rem; margin-top: 4px; margin-bottom: 22px; }

.kb-card { background: #1B212B; border: 1px solid #2A3140; border-radius: 10px;
           padding: 14px 18px; margin-bottom: 8px; }
.kb-cat { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: #E8A33D;
          text-transform: uppercase; letter-spacing: 0.06em; }
.kb-q { color: #F1EEE6; font-weight: 600; margin: 3px 0; }
.kb-a { color: #9AA3AF; font-size: 0.92rem; }

/* Ticket stub styling for the classification/retrieval readout */
.stub { background: #1B212B; border: 1px dashed #3A4152; border-radius: 12px;
        padding: 18px 20px; position: relative; }
.stub-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: #6C7484;
              text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px; }
.stub-row { display: flex; justify-content: space-between; padding: 6px 0;
            border-bottom: 1px solid #262D3A; font-size: 0.92rem; }
.stub-row:last-child { border-bottom: none; }
.stub-key { color: #7C8494; font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; }
.stub-val { color: #F1EEE6; font-weight: 500; text-align: right; }

/* Rubber-stamp decision badge */
.stamp { display: inline-block; font-family: 'IBM Plex Mono', monospace; font-weight: 600;
         font-size: 1.05rem; letter-spacing: 0.06em; padding: 10px 22px; border-radius: 6px;
         border: 2.5px solid; transform: rotate(-2deg); text-transform: uppercase; }
.stamp-auto { color: #4FAE8B; border-color: #4FAE8B; background: rgba(79,174,139,0.08); }
.stamp-escalate { color: #E2574C; border-color: #E2574C; background: rgba(226,87,76,0.08); }
.stamp-reason { color: #9AA3AF; font-size: 0.88rem; margin-top: 10px; font-style: italic; }

.output-card { background: #1B212B; border: 1px solid #2A3140; border-radius: 12px;
               padding: 20px 22px; margin-top: 10px; color: #F1EEE6; line-height: 1.55; }
.output-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: #E8A33D;
                text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("""
<div class="brand-row">
  <p class="brand-title"># TicketMind</p>
  <span class="brand-tag">Multi-Agent Triage Desk</span>
</div>
<p class="brand-sub">Classifies, researches, and autonomously decides — auto-resolve or hand off to a human.</p>
""", unsafe_allow_html=True)

with st.expander("# Knowledge base this agent can search"):
    for article in KNOWLEDGE_BASE:
        st.markdown(f"""
        <div class="kb-card">
            <div class="kb-cat">{article['category']}</div>
            <div class="kb-q">{article['question']}</div>
            <div class="kb-a">{article['answer']}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

sample_tickets = {
    "-- pick a sample or write your own --": "",
    "Easy (should auto-reply)": "Hi, I forgot my password and can't log in. How do I reset it?",
    "Medium (should auto-reply)": "My sync keeps failing with an error, it's annoying but not urgent.",
    "Hard/Angry (should escalate)": "I was charged TWICE this month and nobody is responding to my emails! "
                                     "I want a refund NOW or I'm cancelling everything.",
    "Ambiguous (should escalate)": "Something weird happened with my account, not sure what, "
                                    "can someone look into it?",
}

choice = st.selectbox("Try a sample ticket, or write your own below:", list(sample_tickets.keys()))
ticket_text = st.text_area(
    "Customer ticket text",
    value=sample_tickets[choice],
    height=100,
    placeholder="Paste or type a customer support ticket here..."
)

run_button = st.button("Resolve Ticket", type="primary")

if run_button and ticket_text.strip():
    with st.status("Agents processing ticket...", expanded=True) as status:

        status.write("# Classifier Agent analyzing ticket...")
        classification = classifier_agent.run(ticket_text)

        status.write("# Retrieval Agent searching knowledge base...")
        retrieval = retrieval_agent.run(ticket_text, classification.get("category", "other"))

        status.write("# Decision Agent deciding: auto-reply or escalate...")
        decision = decision_agent.run(ticket_text, classification, retrieval)

        if decision["action"] == "auto_reply" and retrieval.get("matched_article"):
            status.write("# Response Agent drafting customer reply...")
            final_output = response_agent.run_auto_reply(ticket_text, retrieval["matched_article"])
        else:
            status.write("# Response Agent drafting escalation note for human agent...")
            final_output = response_agent.run_escalation_note(
                ticket_text, classification, decision["reasoning"]
            )

        status.update(label="☑️ Ticket processed!", state="complete")

    col1, col2 = st.columns(2)

    with col1:
        rows = [
            ("Category", classification.get("category", "-")),
            ("Urgency", classification.get("urgency", "-")),
            ("Sentiment", classification.get("sentiment", "-")),
            ("Summary", classification.get("summary", "-")),
            ("KB Match", "Yes" if retrieval.get("match_found") else "No"),
            ("Confidence", retrieval.get("confidence", "-")),
        ]
        rows_html = "".join(
            f'<div class="stub-row"><span class="stub-key">{key}</span>'
            f'<span class="stub-val">{val}</span></div>'
            for key, val in rows
        )
        st.markdown(
            f'<div class="stub"><div class="stub-label">Ticket Readout</div>{rows_html}</div>',
            unsafe_allow_html=True
        )

    with col2:
        stamp_class = "stamp-auto" if decision["action"] == "auto_reply" else "stamp-escalate"
        stamp_text = "Auto-Resolved" if decision["action"] == "auto_reply" else "Escalated"
        st.markdown(f'<div class="stamp {stamp_class}">{stamp_text}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stamp-reason">{decision["reasoning"]}</div>', unsafe_allow_html=True)

        label = "Customer Reply" if decision["action"] == "auto_reply" else "Handoff Note"
        st.markdown(f"""
        <div class="output-card">
            <div class="output-label">{label}</div>
            {final_output.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)

elif run_button:
    st.warning("Please enter a ticket first.")
