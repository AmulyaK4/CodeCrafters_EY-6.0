"""
Scraper service stub. Replace with real HTTP clients to mock APIs or live sources.
"""
import httpx
from typing import Dict, Any
import logging

logger = logging.getLogger("pharma-platform")


async def fetch_json(url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        logger.debug("Fetched %s with params %s", url, params)
        return resp.json()

