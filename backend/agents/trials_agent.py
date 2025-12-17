from typing import Dict, Any, List
from backend.services.scraper import fetch_json
from backend.config import settings


class TrialsAgent:
    async def fetch_trials(self, query: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch active clinical trials. Falls back to mock data if endpoint fails.
        """
        params = {"q": query, "region": context.get("region", "global")}
        try:
            data = await fetch_json(settings.mock_trials_url, params=params)
            trials = data.get("trials", [])
            if trials:
                return trials
        except Exception:
            pass

        # Fallback mock data
        return [
            {"condition": "COPD", "phase": "Phase III", "sponsor": "ACME Pharma", "status": "Recruiting"},
            {"condition": "Asthma", "phase": "Phase II", "sponsor": "HealthCorp", "status": "Active"},
        ]

