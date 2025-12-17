"""
Master agent that orchestrates worker agents and aggregates results.
Uses asyncio.gather to run workers concurrently and passes outputs to the synthesis agent.
"""
import asyncio
from typing import Dict, Any
from backend.agents.trials_agent import TrialsAgent
from backend.agents.patents_agent import PatentsAgent
from backend.agents.market_agent import MarketAgent
from backend.agents.papers_agent import PapersAgent
from backend.agents.synthesis_agent import SynthesisAgent
from backend.services.visualization import market_bar_chart


class MasterAgent:
    def __init__(self):
        self.trials = TrialsAgent()
        self.patents = PatentsAgent()
        self.market = MarketAgent()
        self.papers = PapersAgent()
        self.synthesis = SynthesisAgent()

    async def run_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decompose the query, run workers in parallel, and synthesize into a unified response.
        """
        trials_task = asyncio.create_task(self.trials.fetch_trials(query, context))
        patents_task = asyncio.create_task(self.patents.fetch_patents(query, context))
        market_task = asyncio.create_task(self.market.fetch_market(query, context))
        papers_task = asyncio.create_task(self.papers.fetch_papers(query, context))

        trials_res, patents_res, market_res, papers_res = await asyncio.gather(
            trials_task, patents_task, market_task, papers_task
        )

        summary = await self.synthesis.summarize(
            query=query,
            trials=trials_res,
            patents=patents_res,
            market=market_res,
            papers=papers_res,
        )

        chart_json = market_bar_chart(market_res)

        return {
            "query": query,
            "trials": trials_res,
            "patents": patents_res,
            "market": market_res,
            "papers": papers_res,
            "summary": summary,
            "chart": chart_json,
        }

