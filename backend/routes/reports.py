from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.services.report_generator import generate_pdf
from backend.services.visualization import market_chart_image
from backend.services.database import get_session
from backend.models.db_models import Report, QueryLog, ResponseLog
from datetime import datetime

router = APIRouter()


class ReportRequest(BaseModel):
    query_id: int
    summary_text: str | None = None


@router.post("/reports/pdf")
async def create_report(payload: ReportRequest, db: Session = Depends(get_session)):
    try:
        if payload.query_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid query_id")
        
        latest_response = (
            db.query(ResponseLog)
            .filter(ResponseLog.query_id == payload.query_id)
            .order_by(ResponseLog.created_at.desc())
            .first()
        )
        
        # Get summary from payload or latest response
        if payload.summary_text:
            summary = {"text": payload.summary_text, "score": "N/A"}
        elif latest_response and latest_response.content.get("summary"):
            summary = latest_response.content.get("summary", {})
        else:
            # Fallback: get query text
            query = db.query(QueryLog).filter(QueryLog.id == payload.query_id).first()
            summary = {"text": query.query_text if query else "No summary available", "score": "N/A"}
        
        chart_png = None
        if latest_response and latest_response.content.get("market"):
            try:
                chart_png = market_chart_image(latest_response.content["market"])
            except Exception as e:
                # Chart generation is optional, continue without it
                pass
        
        pdf_bytes = generate_pdf(summary=summary, chart_png=chart_png)
        report_url = f"/api/reports/download/{payload.query_id}"
        
        # Save report record
        report = Report(query_id=payload.query_id, report_url=report_url, created_at=datetime.utcnow())
        db.add(report)
        db.commit()
        
        return {"status": "ok", "report_url": report_url}
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logging.exception("PDF generation error")
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")


@router.get("/reports/download/{query_id}")
async def download_report(query_id: int, db: Session = Depends(get_session)):
    try:
        q = db.query(QueryLog).filter(QueryLog.id == query_id).first()
        if not q:
            raise HTTPException(status_code=404, detail="Query not found")
        
        latest_response = (
            db.query(ResponseLog)
            .filter(ResponseLog.query_id == query_id)
            .order_by(ResponseLog.created_at.desc())
            .first()
        )
        
        chart_png = None
        if latest_response and latest_response.content.get("market"):
            try:
                chart_png = market_chart_image(latest_response.content["market"])
            except Exception:
                pass  # Chart is optional
        
        if latest_response and latest_response.content.get("summary"):
            summary = latest_response.content.get("summary", {})
        else:
            summary = {"text": q.query_text, "score": "N/A"}
        
        pdf_bytes = generate_pdf(summary=summary, chart_png=chart_png)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=pharma_report_{query_id}.pdf"}
        )
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logging.exception("PDF download error")
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")

