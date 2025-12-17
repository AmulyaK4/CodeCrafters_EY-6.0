from typing import Dict, Any, List
from backend.services.scraper import fetch_json
from backend.config import settings


class PapersAgent:
    async def fetch_papers(self, query: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Retrieve recent publications via mock web search proxy.
        """
        params = {"q": query, "limit": context.get("paper_limit", 5)}
        try:
            data = await fetch_json(settings.mock_patent_url.replace("patents", "papers"), params=params)
            papers = data.get("papers", [])
            if papers:
                return papers
        except Exception:
            pass

        return [
            {"title": "Real-world outcomes in COPD", "journal": "Respiratory Medicine", "year": 2023, "doi": "10.1000/resp.2023.01"},
            {"title": "Asthma biologics landscape", "journal": "J Asthma", "year": 2024, "doi": "10.1000/asthma.2024.02"},
        ]

