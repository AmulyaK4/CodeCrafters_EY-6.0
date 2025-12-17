from typing import Dict, Any, List
from backend.services.scraper import fetch_json
from backend.config import settings


class PatentsAgent:
    async def fetch_patents(self, query: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search mock USPTO/EPO endpoint for patents and expiry timelines.
        """
        params = {"q": query, "assignee": context.get("assignee")}
        try:
            data = await fetch_json(settings.mock_patent_url, params=params)
            patents = data.get("patents", [])
            if patents:
                return patents
        except Exception:
            pass

        return [
            {"title": "Inhalable formulation for COPD", "status": "Granted", "expiry": "2035-12-01", "assignee": "ACME"},
            {"title": "Novel delivery for asthma biologics", "status": "Pending", "expiry": "2040-05-20", "assignee": "HealthCorp"},
        ]

