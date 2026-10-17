uv init --python 3.12
uv venv --python 3.12
uv add -r requirements.txt


Meridian AI

A small web app that does two jobs, using AI:

Ask questions about your documents. Upload PDFs (policies, contracts, reports), then ask in plain English. The app answers using only what is in your documents.
Check a purchase before paying. Paste a purchase request. Three AI "specialists" review it (risk, tax, accounting). A final "CFO" step writes one short memo with a decision.
It is built to learn from. The company in the examples, Aldermoor Industries, is fictional, and the sample documents contain made-up data.

The "checks" in the audit are done by the AI from its general knowledge (only the exchange-rate check uses a live data source). This is a demo of how such a system is built, not a real compliance tool.