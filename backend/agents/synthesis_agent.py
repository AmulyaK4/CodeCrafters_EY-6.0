from typing import Dict, Any, List
from backend.config import settings

try:
    from langchain_openai import ChatOpenAI  # langchain>=0.2
except Exception:  # pragma: no cover
    try:
        from langchain.chat_models import ChatOpenAI  # older langchain
    except Exception:
        ChatOpenAI = None

try:
    from langchain.prompts import ChatPromptTemplate
except Exception:  # pragma: no cover
    ChatPromptTemplate = None


class SynthesisAgent:
    def __init__(self):
        self.llm = (
            ChatOpenAI(
                temperature=0.2,
                model="gpt-3.5-turbo",
                api_key=settings.openai_api_key,
            )
            if settings.enable_llm and ChatOpenAI
            else None
        )

    async def summarize(self, query: str, trials: List[Dict[str, Any]], patents, market, papers) -> Dict[str, Any]:
        """
        Summarize evidence and compute a simple opportunity score.
        Uses LangChain LLM when configured, otherwise falls back to heuristic text.
        """
        if self.llm and ChatPromptTemplate:
            prompt = ChatPromptTemplate.from_template(
                """You are a pharma portfolio strategist.
Summarize the opportunity for: {query}
Trials: {trials}
Patents: {patents}
Market: {market}
Papers: {papers}
Return 4 bullets: Trials, Patents/IP, Market, Scientific evidence, plus an overall opportunity score 0-1."""
            )
            chain = prompt | self.llm
            llm_resp = await chain.ainvoke(
                {
                    "query": query,
                    "trials": trials,
                    "patents": patents,
                    "market": market,
                    "papers": papers,
                }
            )
            text = llm_resp.content if hasattr(llm_resp, "content") else str(llm_resp)
        else:
            text = (
                f"Query: {query}\n"
                f"- Trials: {len(trials)} active; key sponsor {trials[0]['sponsor'] if trials else 'n/a'}\n"
                f"- Patents: {len(patents)} found; earliest expiry {patents[0]['expiry'] if patents else 'n/a'}\n"
                f"- Market: est ${market.get('market_size_usd', 0)/1e9:.1f}B, CAGR {market.get('cagr', 0)}%\n"
                f"- Papers: {len(papers)} recent publications\n"
                "Opportunity: Moderate competition, strong growth, monitor IP expiries."
            )

        score = self._score(trials, patents, market, papers)
        citations = self._citations(trials, patents, papers)
        return {"text": text, "score": score, "citations": citations}

    def _score(self, trials, patents, market, papers) -> float:
        # Naive scoring: more trials and patents reduce score, higher CAGR increases it.
        trial_penalty = min(len(trials) * 0.05, 0.3)
        patent_penalty = min(len(patents) * 0.03, 0.25)
        cagr_bonus = min(max(market.get("cagr", 0), 0) * 0.02, 0.4)
        base = 0.5 + cagr_bonus - trial_penalty - patent_penalty
        return round(max(0.05, min(base, 0.95)), 2)

    def _citations(self, trials, patents, papers):
        cites = []
        for t in trials[:3]:
            cites.append({"source": "clinical_trial", "link": t.get("registry_url", "https://clinicaltrials.gov")})
        for p in patents[:3]:
            cites.append({"source": "patent", "link": p.get("link", "https://patents.example.com")})
        for pap in papers[:3]:
            cites.append({"source": "paper", "link": f"https://doi.org/{pap.get('doi', '')}"})
        return cites

