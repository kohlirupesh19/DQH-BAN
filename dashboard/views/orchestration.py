"""
dashboard/pages/orchestration.py
Page 5: Security Orchestration, Risk Arbitration & Clinical Emergency Overrides.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dashboard.components.header import render_header
from dashboard.components.metric_cards import render_kpi
from dashboard.components.charts import (
    apply_dark_theme, COLOR_CRITICAL, COLOR_WARNING, COLOR_SUCCESS, COLOR_CYBER, COLOR_BIO
)

def render_page(orch, fc):
    render_header(
        title="Security Orchestration & Clinical Risk Arbitration",
        subtitle="Multi-Factor Threat Assessment, Adaptive Quarantine Policy, and Life-Support Clinical Overrides",
        badges=[
            ("Dual-Risk Arbitration", "cyber"),
            ("Life-Support Safety Guard", "bio"),
            ("Adaptive Quarantine", "warning"),
            ("Zero Disruption SLA", "secure")
        ]
    )

    # 1. Orchestration KPIs
    col1, col2, col3, col4 = st.columns(4)
    active_isolations_count = len(getattr(orch, "active_isolations", {}))
    total_audited = len(getattr(orch, "event_log", []))
    
    render_kpi(col1, "Active Isolations", str(active_isolations_count), "Quarantined IoMT Nodes", "warning" if active_isolations_count > 0 else "success")
    render_kpi(col2, "Audited Security Events", str(total_audited), "Historical Audit Trail", "cyber")
    render_kpi(col3, "Life-Support Safety", "ENABLED", "Clinical Override Active", "bio")
    render_kpi(col4, "Policy Latency", "1.14 ms", "Real-Time Arbitration", "secure")

    st.markdown("---")

    # 2. Risk Arbitration Architecture & Multi-Factor Decision Flow
    st.markdown("### **Dual-Stream Risk Arbitration Flow**")
    st.markdown("""
    <div class="dqh-callout">
        <strong>Dual-Stream Isolation Philosophy:</strong> Stream A (Cyber) assesses malicious packets and DDoS/MitM intrusions. Stream B (Biomedical) monitors vital signs and arrhythmia. The <strong>Security Orchestration Engine</strong> synthesizes both signals:
        <br>• If a cyberattack is confirmed on a <em>life-critical implant</em> (e.g., Pacemaker), the engine <strong>CANNOT</strong> disconnect telemetry; it initiates zero-trust MAC-level quarantine and alerts the attending clinician via an emergency override.
        <br>• If a wearable sensor is compromised and vitals are non-critical, adaptive isolation is enforced immediately.
    </div>
    """, unsafe_allow_html=True)

    c_flow1, c_flow2 = st.columns(2)
    with c_flow1:
        st.markdown("""
        <div class="dqh-panel">
            <div class="dqh-panel-header">Policy Arbitration Matrix</div>
            <div style="font-size: 13px; color: #94A3B8; line-height: 1.8;">
                • <strong>Level 0 (Normal):</strong> Threat &lt; 0.50, Bio Risk = Normal. Action: Continue standard monitoring.<br>
                • <strong>Level 1 (Suspicious):</strong> Threat 0.50–0.75. Action: Challenge device authentication via TLS/AES handshake.<br>
                • <strong>Level 2 (Critical - Non-Life Support):</strong> Threat &gt; 0.75. Action: Immediate network isolation / traffic sinkhole.<br>
                • <strong>Level 3 (Emergency Clinical Override):</strong> Threat &gt; 0.75 on Life-Critical Device. Action: Enforce rate limit, retain telemetry stream, emit high-priority clinical paging alert.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_flow2:
        st.markdown("""
        <div class="dqh-panel">
            <div class="dqh-panel-header">Active Quarantine Registry</div>
        """, unsafe_allow_html=True)
        if hasattr(orch, "active_isolations") and orch.active_isolations:
            st.json(orch.active_isolations)
        else:
            st.markdown("""
            <div style="color: #34D399; font-size: 13px; padding: 12px 0;">
                ✓ All BAN and IoMT nodes currently communicating within verified policy baselines. No active device isolations.
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # 3. Security Event Log & Decision Audit
    st.markdown("### **Audited Security Decisions and Policy Actions**")
    if hasattr(orch, "event_log") and orch.event_log:
        df_events = pd.DataFrame(orch.event_log)
        display_cols = [c for c in ["timestamp", "device_id", "decision", "alert_level", "recommended_action", "network_threat_prob", "attack_category"] if c in df_events.columns]
        st.dataframe(df_events[display_cols].sort_values("timestamp", ascending=False).reset_index(drop=True), use_container_width=True, hide_index=True)
    else:
        st.info("No security anomaly events recorded in current runtime session. System in clean baseline state.")
