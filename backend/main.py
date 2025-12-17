from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import health, chatbot, reports
from backend.services.database import init_db
from backend.agents.master_agent import MasterAgent
from backend.config import settings
import json
import logging

logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
logger = logging.getLogger("pharma-platform")
master_agent = MasterAgent()


def create_app() -> FastAPI:
    app = FastAPI(title="Pharma Agentic Platform", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    app.include_router(health.router, prefix="/api")
    app.include_router(chatbot.router, prefix="/api")
    app.include_router(reports.router, prefix="/api")
    return app


app = create_app()


@app.on_event("startup")
async def on_startup():
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized")


@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async for message in websocket.iter_text():
            try:
                payload = json.loads(message)
                query = payload.get("query", "")
                context = payload.get("context", {})
            except Exception:
                query = message
                context = {}
            result = await master_agent.run_query(query, context)
            await websocket.send_text(json.dumps({"status": "ok", "data": result}))
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as exc:  # noqa: BLE001
        await websocket.send_text(json.dumps({"status": "error", "detail": str(exc)}))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=False)

