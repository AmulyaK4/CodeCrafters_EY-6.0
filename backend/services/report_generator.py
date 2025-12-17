import io
from datetime import datetime
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def generate_pdf(summary: Dict[str, Any], chart_png: Optional[bytes] = None) -> bytes:
    """
    Generate PDF with summary text and optional chart image.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 750, "Pharma Agentic Research Report")
    c.setFont("Helvetica", 10)
    c.drawString(50, 730, f"Generated: {datetime.utcnow().isoformat()} UTC")
    c.drawString(50, 716, f"Opportunity score: {summary.get('score', 'n/a')}")
    y = 690
    c.setFont("Helvetica", 11)
    for line in summary.get("text", "").split("\n"):
        c.drawString(50, y, line[:95])
        y -= 16
        if y < 120:
            c.showPage()
            y = 750
    if chart_png:
        try:
            c.drawImage(ImageReader(io.BytesIO(chart_png)), 50, y - 260, width=500, height=240, preserveAspectRatio=True)
        except Exception:
            pass
    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

