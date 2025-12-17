from typing import Dict, Any
from backend.services.scraper import fetch_json
from backend.config import settings


class MarketAgent:
    async def fetch_market(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pull market size, CAGR, and trade insights from mock IQVIA/EXIM endpoints.
        """
        params = {"therapy": query, "country": context.get("country", "US")}
        market_data = {}
        try:
            iqvia = await fetch_json(settings.mock_iqvia_url, params=params)
            market_data.update(iqvia)
        except Exception:
            market_data.update(
                {
                    "market_size_usd": 2.5e9,
                    "cagr": 8.2,
                    "top_competitors": ["ACME Pharma", "HealthCorp", "Generico"],
                }
            )

        try:
            exim = await fetch_json(settings.mock_exim_url, params=params)
            market_data["trade"] = exim.get("trade", [])
        except Exception:
            market_data["trade"] = [
                {"country": "IN", "imports": 120, "exports": 45, "unit": "MT"},
                {"country": "US", "imports": 80, "exports": 90, "unit": "MT"},
            ]

        return market_data

