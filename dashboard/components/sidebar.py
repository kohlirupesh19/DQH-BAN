"""
dashboard/components/sidebar.py
Modern sidebar navigation and persistent system status for DQH-BAN.
"""

import os
import streamlit as st
from dashboard.utils.path_manager import resolve_path

PAGES = [
    "1. System Overview",
    "2. Cybersecurity Intelligence",
    "3. Quantum Intelligence",
    "4. Biomedical Intelligence",
    "5. Security Orchestration",
    "6. Blockchain Security",
    "7. Live BAN Simulator",
    "8. Benchmark Laboratory",
    "9. Research Reports"
]

def render_sidebar(fc, sim) -> str:
    with st.sidebar:
        logo_path = resolve_path("dashboard/assets/logo.png")
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)

        st.markdown("""
        <div style="text-align: center; margin-bottom: 16px;">
            <div style="font-size: 16px; font-weight: 700; color: #F8FAFC; letter-spacing: -0.01em;">DQH-BAN PLATFORM</div>
            <div style="font-size: 11px; color: #94A3B8; font-family: monospace;">EXP-2026-V2 • RESEARCH LAB</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Navigation")
        selected = st.radio("Go to:", PAGES, label_visibility="collapsed")

        st.markdown("---")
        st.markdown("### System Telemetry")

        cyber_loaded = sim.cyber_model is not None or sim.cyber_model_version is not None
        bio_loaded = sim.biomedical_model is not None or sim.bio_model_version is not None
        is_sim_ledger = not getattr(fc, "is_live_fabric", False)

        st.markdown(f"""
        <div style="font-size: 12px; line-height: 1.8; color: #94A3B8;">
            <div>Stream A (Cyber): <span style="color: #38BDF8; font-family: monospace;">v{sim.cyber_model_version}</span></div>
            <div>Stream B (Bio): <span style="color: #2DD4BF; font-family: monospace;">v{sim.bio_model_version}</span></div>
            <div>Ledger Mode: <span style="color: #818CF8; font-family: monospace;">{'Crypto Fallback' if is_sim_ledger else 'Live Peer'}</span></div>
            <div>Encryption: <span style="color: #34D399; font-family: monospace;">AES-256-GCM</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.caption("DQH-BAN: Dual-Stream Quantum Healthcare Intelligence Architecture for Secure Body Area Networks • MIT License")

    return selected
