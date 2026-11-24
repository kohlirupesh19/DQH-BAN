"""
dashboard/components/header.py
Modern header banner component for DQH-BAN research platform.
"""

import streamlit as st
import os
from dashboard.utils.path_manager import resolve_path

def render_header(title: str, subtitle: str, badges: list = None):
    """Renders a styled dark header with project identity and metadata badges."""
    badge_html = ""
    if badges:
        badge_html = '<div class="dqh-badge-row">'
        for text, btype in badges:
            badge_html += f'<span class="dqh-badge {btype}">{text}</span>'
        badge_html += '</div>'

    st.markdown(f"""
    <div class="dqh-header-container">
        <div class="dqh-title">
            <span class="dqh-title-accent">🛡️ DQH-BAN</span>
            <span style="color: #64748B;">|</span>
            <span>{title}</span>
        </div>
        <div class="dqh-subtitle">{subtitle}</div>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)
