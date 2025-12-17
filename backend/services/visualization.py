import plotly.graph_objects as go
from typing import Dict, Any, Tuple


def market_bar_chart(data: Dict[str, Any]) -> str:
    fig = go.Figure(
        data=[go.Bar(x=data.get("top_competitors", []), y=data.get("market_shares", [80, 65, 50]), marker_color="#0ea5e9")]
    )
    fig.update_layout(title="Competitor Market Share (mock)", template="plotly_white")
    return fig.to_json()


def market_chart_image(data: Dict[str, Any]) -> bytes:
    """
    Render the Plotly chart to PNG bytes for PDF embedding.
    """
    fig = go.Figure(
        data=[go.Bar(x=data.get("top_competitors", []), y=data.get("market_shares", [80, 65, 50]), marker_color="#0ea5e9")]
    )
    fig.update_layout(title="Competitor Market Share (mock)", template="plotly_white")
    return fig.to_image(format="png", width=800, height=500, scale=2)

