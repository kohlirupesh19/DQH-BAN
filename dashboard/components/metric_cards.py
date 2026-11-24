"""
dashboard/components/metric_cards.py
Responsive research KPI card renderer for DQH-BAN.
"""

import streamlit as st

def render_kpi(col, title: str, val: str, sub: str = "", status: str = "primary"):
    """
    Renders a styled KPI card into a streamlit column.
    status can be: primary, quantum, bio, success, warning, critical
    """
    with col:
        st.markdown(f"""
        <div class="dqh-kpi-card">
            <div class="dqh-kpi-title">{title}</div>
            <div class="dqh-kpi-val">{val}</div>
            <div class="dqh-kpi-sub {status}">{sub}</div>
        </div>
        """, unsafe_allow_html=True)
