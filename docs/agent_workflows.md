# Agent Workflows (ASCII)

[User Query]
    |
    v
[Master Agent] --decompose--> [Trials Agent] (ClinicalTrials mock)
        |                    [Patents Agent] (USPTO mock)
        |                    [Market Agent] (IQVIA/EXIM mock)
        |                    [Papers Agent] (web/papers mock)
        v
    asyncio.gather (parallel)
        v
    [Synthesis Agent] --LLM/heuristic--> summary + score + citations
        |
        v
   DB log (queries/responses/citations) -> PDF + Plotly chart -> Frontend

