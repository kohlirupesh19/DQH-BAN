"""
dashboard/pages/simulator.py
Page 7: Real-Time Multi-Device Body Area Network (BAN) Simulator.
"""

import time
import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.components.header import render_header
from dashboard.components.metric_cards import render_kpi
from dashboard.components.charts import (
    apply_dark_theme, COLOR_CRITICAL, COLOR_WARNING, COLOR_SUCCESS, COLOR_CYBER, COLOR_BIO
)
from dashboard.utils.formatters import fmt_pct, fmt_hash

def render_page(sim):
    render_header(
        title="Real-Time Body Area Network (BAN) Telemetry Simulator",
        subtitle="Multi-Sensor Physiological Streaming, Synthetic Attack Scenarios, and Real-Time ML Inference",
        badges=[
            ("SYNTHETIC TELEMETRY", "warning"),
            ("Device Profiles: 5 Active", "cyber"),
            ("Dual-Head Classification", "quantum"),
            ("Controlled Cloud Probe", "secure")
        ]
    )

    st.markdown("""
    <div class="dqh-callout warning">
        <strong>⚠️ Simulation Transparency Notice:</strong> All telemetry frames generated on this page are <strong>CONTROLLED SYNTHETIC SIMULATIONS</strong>. Observations are fed dynamically into the offline-trained DQH-BAN preprocessor and calibrated models to verify real-time intrusion response.
    </div>
    """, unsafe_allow_html=True)

    # Simulator Controls Panel
    c_ctrl1, c_ctrl2, c_ctrl3, c_ctrl4 = st.columns([1.2, 1.2, 1, 1])

    devices = list(getattr(sim, "DEVICE_PROFILES", {}).keys()) or ["Smartwatch_Wearable", "Holter_Monitor_ECG", "Chest_Patch_Respiration"]
    scenarios = getattr(sim, "ATTACK_SCENARIOS", ["BENIGN_ROUTINE", "TCP_SYN_FLOOD", "SPOOFED_TELEMETRY", "MITM_REPLAY", "HIJACK_COMMAND"])

    with c_ctrl1:
        selected_dev = st.selectbox("Select IoMT Target Device:", devices)
    with c_ctrl2:
        selected_scen = st.selectbox("Injection Scenario:", scenarios)
    with c_ctrl3:
        sim_rate = st.slider("Sampling Rate (Hz):", 0.5, 5.0, 2.0, step=0.5)
    with c_ctrl4:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        btn_probe = st.button("🚀 Generate Probe Step", type="primary", use_container_width=True)

    # Execute simulation observation on click
    if btn_probe:
        try:
            obs = sim.generate_telemetry_observation(selected_dev, selected_scen)
            is_mal = obs.get("threat_prob", 0.0) >= obs.get("threshold_used", 0.5)
            badge_type = "critical" if is_mal else "success"
            
            st.markdown(f"""
            <div style="background: #172033; border: 1px solid {'#F87171' if is_mal else '#34D399'}; border-radius: 8px; padding: 14px 18px; margin: 16px 0;">
                <div style="font-weight: 700; color: {'#F87171' if is_mal else '#34D399'}; font-size: 14px;">
                    { '🚨 INTRUSION DETECTED' if is_mal else '✓ NORMAL BENIGN COMM' }: {selected_dev} [{selected_scen}]
                </div>
                <div style="font-size: 13px; color: #94A3B8; margin-top: 6px;">
                    • Threat Probability: <strong style="color: #F8FAFC;">{obs.get('threat_prob', 0.0):.4f}</strong> (Threshold: {obs.get('threshold_used', 0.0):.4f})<br>
                    • Arbitration Decision: <strong style="color: #38BDF8;">{obs.get('decision', 'N/A')}</strong> | Alert Level: <strong>{obs.get('alert_level', 'LOW')}</strong><br>
                    • SHA-256 On-Chain Commitment: <code>{fmt_hash(obs.get('sha256_commitment'), 24)}</code>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Simulation execution error: {e}")

    st.markdown("---")

    # Simulation Telemetry Log
    history = getattr(sim, "simulation_history", [])
    if history:
        st.markdown("### **Live Simulation Stream History (Last 15 Events)**")
        df_sim = pd.DataFrame(history[-15:])
        cols_sim = [c for c in ["step", "timestamp", "device_id", "scenario", "heart_rate", "threat_prob", "threshold_used", "attack_class", "decision", "alert_level", "sha256_commitment"] if c in df_sim.columns]
        
        # Display styled table
        st.dataframe(df_sim[cols_sim].sort_values("step", ascending=False).reset_index(drop=True), use_container_width=True, hide_index=True)

        # Plotly Threat Score Timeline
        if "step" in df_sim.columns and "threat_prob" in df_sim.columns:
            fig_stream = px.line(
                df_sim, x="step", y="threat_prob", color="device_id",
                markers=True, title="Simulated Device Threat Probability Trajectory"
            )
            fig_stream.add_hline(y=0.8893, line_dash="dash", line_color=COLOR_CRITICAL, annotation_text="Calibration Threshold (tau*)")
            apply_dark_theme(fig_stream, height=300, xaxis_title="Simulation Step", yaxis_title="Threat Probability")
            st.plotly_chart(fig_stream, use_container_width=True)
    else:
        st.info("Click 'Generate Probe Step' above to generate and inspect synthetic telemetry frames in real-time.")
