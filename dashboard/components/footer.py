"""
dashboard/components/footer.py
Standardized research attribution and publication footer.
"""

import streamlit as st

def render_footer():
    st.markdown("""
    <div class="dqh-footer">
        <div style="font-weight: 600; color: #94A3B8; margin-bottom: 4px;">
            DQH-BAN: Dual-Stream Quantum Healthcare Intelligence Architecture for Secure Body Area Networks
        </div>
        <div>
            Experiment ID: <code>DQH-BAN-EXP-2026-V2</code> | MIT License | 
            <a href="https://github.com/kohlirupesh19/DQH-BAN" target="_blank">GitHub Repository</a>
        </div>
        <div style="margin-top: 6px; font-size: 11px; color: #64748B;">
            Validated offline on 7 physical datasets across 48 checkpoints • Purely for academic research and evaluation
        </div>
    </div>
    """, unsafe_allow_html=True)
