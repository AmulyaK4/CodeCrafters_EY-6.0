# Architecture

- Frontend: Tailwind static UI (NGINX) with chat, dashboard cards, Plotly market chart, WebSocket + REST to backend.
- Backend: FastAPI with async routes and WebSocket; orchestrates agents; LangChain/CrewAI-compatible synthesis; PDF and Plotly chart generation.
- Agents: Master agent orchestrates Trials, Patents, Market (IQVIA/EXIM), Papers, and Synthesis agents concurrently.
- DB: MySQL via SQLAlchemy. Tables: queries, response_logs, citations, user_sessions, reports.
- Reports: ReportLab PDF with embedded Plotly chart (via kaleido).

Data flow:
User -> Frontend (WS/HTTP) -> FastAPI -> Master Agent -> Worker Agents (mock APIs) -> Synthesis (LLM or heuristic) -> DB + PDF/Charts -> Frontend.

