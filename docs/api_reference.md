# API Reference

GET /api/health
- 200 {"status":"ok"}

POST /api/chat
- body: { "user_id": "u1", "query": "COPD opportunities", "context": {} }
- resp: { status, query_id, response_id, data: { trials, patents, market, papers, summary, chart } }

POST /api/reports/pdf
- body: { "query_id": 1, "summary_text": "optional override" }
- resp: { status, report_url }

GET /api/reports/download/{query_id}
- returns PDF

WebSocket /ws/chat
- send: JSON { "query": "...", "context": {} }
- recv: { status, data }

