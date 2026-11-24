"""
dashboard/components/charts.py
Plotly visualization styling engine with consistent dark laboratory aesthetic.
"""

import plotly.graph_objects as go
from typing import Optional

# Palette definition
COLOR_CYBER = "#38BDF8"       # Cyan / Sky
COLOR_QUANTUM = "#818CF8"     # Purple / Violet
COLOR_BIO = "#2DD4BF"         # Teal / Mint
COLOR_SUCCESS = "#34D399"     # Emerald
COLOR_WARNING = "#FBBF24"     # Amber
COLOR_CRITICAL = "#F87171"    # Rose / Coral
COLOR_MUTED = "#94A3B8"       # Slate
BG_PAPER = "#0B1020"
BG_PLOT = "#111827"
BORDER_COLOR = "#1E293B"

def apply_dark_theme(fig: go.Figure,
                     title: Optional[str] = None,
                     height: int = 340,
                     xaxis_title: Optional[str] = None,
                     yaxis_title: Optional[str] = None,
                     showlegend: bool = True) -> go.Figure:
    """Applies unified dark publication styling to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor=BG_PAPER,
        plot_bgcolor=BG_PLOT,
        font=dict(family="Inter, sans-serif", color="#F8FAFC", size=11),
        title=dict(
            text=f"<b>{title}</b>" if title else None,
            font=dict(size=13, color="#F8FAFC"),
            x=0.01,
            y=0.96
        ) if title else None,
        height=height,
        margin=dict(l=40, r=20, t=50 if title else 20, b=40),
        xaxis=dict(
            title=xaxis_title,
            gridcolor=BORDER_COLOR,
            zerolinecolor=BORDER_COLOR,
            linecolor=BORDER_COLOR,
            tickfont=dict(size=10, color=COLOR_MUTED)
        ),
        yaxis=dict(
            title=yaxis_title,
            gridcolor=BORDER_COLOR,
            zerolinecolor=BORDER_COLOR,
            linecolor=BORDER_COLOR,
            tickfont=dict(size=10, color=COLOR_MUTED)
        ),
        legend=dict(
            font=dict(size=10, color="#F8FAFC"),
            bgcolor="rgba(17, 24, 39, 0.7)",
            bordercolor=BORDER_COLOR,
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ) if showlegend else None,
        hoverlabel=dict(
            bgcolor="#172033",
            font_size=11,
            font_family="JetBrains Mono, monospace"
        )
    )
    return fig
