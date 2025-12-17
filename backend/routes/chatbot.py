from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from backend.agents.master_agent import MasterAgent
from backend.services.database import get_session
from backend.models.db_models import QueryLog, ResponseLog, Citation
from sqlalchemy.orm import Session
import logging

router = APIRouter()
logger = logging.getLogger("pharma-platform")
master = MasterAgent()


class ChatRequest(BaseModel):
    user_id: str
    query: str
    context: Dict[str, Any] = {}


@router.post("/chat")
async def chat(payload: ChatRequest, db: Session = Depends(get_session)):
    try:
        qlog = QueryLog(user_id=payload.user_id, query_text=payload.query)
        db.add(qlog)
        db.commit()
        db.refresh(qlog)

        result = await master.run_query(payload.query, payload.context)

        rlog = ResponseLog(query_id=qlog.id, content=result)
        db.add(rlog)
        db.commit()
        db.refresh(rlog)

        for cite in result.get("summary", {}).get("citations", []):
            citation = Citation(response_id=rlog.id, source=cite.get("source", ""), link=cite.get("link", ""))
            db.add(citation)
        db.commit()

        return {"status": "ok", "data": result, "query_id": qlog.id, "response_id": rlog.id}
    except Exception as e:
        logger.exception("Chat error")
        raise HTTPException(status_code=500, detail=str(e))

