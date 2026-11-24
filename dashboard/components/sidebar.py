"""
dashboard/components/sidebar.py
Modern animated sidebar navigation and persistent system status for DQH-BAN.
"""

import os
import streamlit as st
from dashboard.utils.path_manager import resolve_path

PAGES = [
    "🌐 1. System Overview",
    "🛡️ 2. Cybersecurity Intelligence",
    "⚛️ 3. Quantum Intelligence",
    "💓 4. Biomedical Intelligence",
    "⚖️ 5. Security Orchestration",
    "⛓️ 6. Blockchain Security",
    "📡 7. Live BAN Simulator",
    "🔬 8. Benchmark Laboratory",
    "📑 9. Research Reports"
]

def render_sidebar(fc, sim) -> str:
    with st.sidebar:
        logo_path = resolve_path("dashboard/assets/logo.png")
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)

        st.markdown("""
        <div class="dqh-brand-container">
            <div class="dqh-brand-title">DQH-BAN PLATFORM</div>
            <div class="dqh-brand-tag">EXP-2026-V2 • QUANTUM HEALTHCARE LAB</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="dqh-nav-label">RESEARCH NAVIGATION</div>', unsafe_allow_html=True)
        selected = st.radio(
            "Select Page:",
            PAGES,
            label_visibility="collapsed"
        )

        st.markdown('<div class="dqh-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="dqh-nav-label">LIVE SYSTEM TELEMETRY</div>', unsafe_allow_html=True)

        is_sim_ledger = not getattr(fc, "is_live_fabric", False)

        st.markdown(f"""
        <div class="dqh-telemetry-box">
            <div class="dqh-telemetry-item">
                <span class="dqh-pulse-dot cyber"></span>
                <span class="dqh-tel-label">Stream A (Cyber):</span>
                <span class="dqh-tel-val cyber">v{sim.cyber_model_version}</span>
            </div>
            <div class="dqh-telemetry-item">
                <span class="dqh-pulse-dot bio"></span>
                <span class="dqh-tel-label">Stream B (Bio):</span>
                <span class="dqh-tel-val bio">v{sim.bio_model_version}</span>
            </div>
            <div class="dqh-telemetry-item">
                <span class="dqh-pulse-dot quantum"></span>
                <span class="dqh-tel-label">Ledger Engine:</span>
                <span class="dqh-tel-val quantum">{'Crypto Fallback' if is_sim_ledger else 'Live Peer'}</span>
            </div>
            <div class="dqh-telemetry-item">
                <span class="dqh-pulse-dot green"></span>
                <span class="dqh-tel-label">Encryption:</span>
                <span class="dqh-tel-val green">AES-256-GCM</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="dqh-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="dqh-sidebar-footer">
            DQH-BAN Architecture<br>
            <span>MIT License • Verified Offline</span>
        </div>
        """, unsafe_allow_html=True)

    return selected
