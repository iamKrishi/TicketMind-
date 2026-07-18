"""
knowledge_base.py
A small hardcoded FAQ knowledge base for a fictional SaaS product ("CloudNest").
Swap this out later with a CSV/database if you want to extend the project.
"""

KNOWLEDGE_BASE = [
    {
        "id": "kb001",
        "category": "billing",
        "question": "How do I update my payment method?",
        "answer": "Go to Account Settings > Billing > Payment Methods, then click 'Add New Card' "
                   "and set it as default. Your old card will be removed automatically."
    },
    {
        "id": "kb002",
        "category": "billing",
        "question": "How do I get a refund?",
        "answer": "Refunds are available within 14 days of purchase. Go to Account Settings > "
                   "Billing > Order History, select the transaction, and click 'Request Refund'."
    },
    {
        "id": "kb003",
        "category": "technical",
        "question": "The app is not loading / stuck on loading screen.",
        "answer": "Try clearing your browser cache and cookies, then reload. If the issue persists, "
                   "check status.cloudnest.com for ongoing outages, or try a different browser."
    },
    {
        "id": "kb004",
        "category": "technical",
        "question": "How do I reset my password?",
        "answer": "Click 'Forgot Password' on the login page, enter your registered email, and "
                   "follow the reset link sent to your inbox. The link expires in 30 minutes."
    },
    {
        "id": "kb005",
        "category": "account",
        "question": "How do I delete my account?",
        "answer": "Go to Account Settings > Privacy > Delete Account. Note: this is irreversible "
                   "and all your data will be permanently removed after 30 days."
    },
    {
        "id": "kb006",
        "category": "account",
        "question": "How do I invite team members?",
        "answer": "Go to Team Settings > Members > Invite, enter their email, and choose a role "
                   "(Admin, Editor, Viewer). They'll receive an invite link valid for 7 days."
    },
    {
        "id": "kb007",
        "category": "technical",
        "question": "I'm getting a 'Sync failed' error.",
        "answer": "This usually means your internet connection dropped mid-sync. Reconnect and "
                   "click 'Retry Sync' in the top bar. If it keeps failing, log out and back in."
    },
]
