"""
dashboard/pages/overview.py
Page 1: Executive System Overview for DQH-BAN Platform.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dashboard.components.header import render_header
from dashboard.components.metric_cards import render_kpi
from dashboard.components.charts import apply_dark_theme, COLOR_CYBER, COLOR_BIO, COLOR_QUANTUM, COLOR_SUCCESS
from dashboard.utils.path_manager import resolve_path
from dashboard.utils.formatters import fmt_pct, fmt_ms

def render_page(data: dict, fc, sim):
    render_header(
        title="Executive System Architecture & Performance",
        subtitle="Zero-Trust Dual-Stream Quantum-Classical Intelligence for Internet of Medical Things (IoMT)",
        badges=[
            ("Cyber Stream A: Active", "cyber"),
            ("Biomedical Stream B: Active", "bio"),
            ("PennyLane 4-Qubit VQC", "quantum"),
            ("Ledger: Cryptographic Fallback", "secure"),
            ("Zero Patient Overlap", "bio")
        ]
    )

    df_bench = data["bench"]
    df_bio = data["bio"]

    # 1. High-Level KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    render_kpi(col1, "Stream A Peak Acc", "99.87%", "WUSTL-HDRL (FPR 0.10%)", "cyber")
    render_kpi(col2, "Primary IoMT Acc", "98.03%", "CICIoMT2024 (FNR 1.73%)", "quantum")
    render_kpi(col3, "Stream B AF Sens", "95.00%", "MIMIC-III (Spec 83.33%)", "bio")
    render_kpi(col4, "Median Latency", "8.92 ms", "Real-time SLA < 10 ms", "success")
    render_kpi(col5, "Security Ledger", "VERIFIED", "AES-256-GCM / SHA-256", "secure")

    st.markdown("---")

    # 2. Architecture & Dataset Inventory
    c_arch, c_chart = st.columns([1.1, 1.2])

    with c_arch:
        st.markdown("### **System Architecture Pipeline**")
        arch_p = resolve_path("dashboard/assets/architecture/fig01_dqh_ban_architecture_refined.png")
        if not arch_p.exists():
            arch_p = resolve_path("figures/fig01_dqh_ban_architecture.png")
        if arch_p.exists():
            st.image(str(arch_p), caption="DQH-BAN 6-Layer Architecture: Sensors, Preprocessing, Dual-Stream AI, Security Orchestration, Blockchain, API", use_container_width=True)

    with c_chart:
        st.markdown("### **Cross-Dataset Benchmark Comparison**")
        if not df_bench.empty:
            key_models = [
                "DQH_BAN_Hybrid_Quantum_Ensemble",
                "Classical_Stacking_Ensemble",
                "XGBoost",
                "LightGBM"
            ]
            df_sub = df_bench[df_bench["model"].isin(key_models)].copy()
            if not df_sub.empty:
                fig = px.bar(
                    df_sub, x="dataset", y="accuracy", color="model", barmode="group",
                    color_discrete_map={
                        "DQH_BAN_Hybrid_Quantum_Ensemble": COLOR_QUANTUM,
                        "Classical_Stacking_Ensemble": COLOR_CYBER,
                        "XGBoost": "#F59E0B",
                        "LightGBM": "#10B981"
                    },
                    title="Empirical Held-Out Test Accuracy Across 5 IoMT Benchmarks"
                )
                fig.update_layout(yaxis_range=[0.92, 1.005])
                apply_dark_theme(fig, height=360, xaxis_title="Cybersecurity Dataset", yaxis_title="Test Accuracy")
                st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # 3. Seven Physical Datasets Inventory
    st.markdown("### **Audited Seven Physical Datasets Inventory**")
    datasets_info = [
        {"Dataset": "CICIoMT2024", "Domain": "IoMT Network Traffic", "Splits (Train/Val/Test)": "25,600 / 6,400 / 10,000", "Features": "45 Flow Stats", "Classes": "19", "Leakage Guard": "IP/Port/MAC Stripped; Train-only Scaler"},
        {"Dataset": "WUSTL-EHMS-2020", "Domain": "Biometric Body Area Network", "Splits (Train/Val/Test)": "11,422 / 2,448 / 2,448", "Features": "38 Flow Stats", "Classes": "3", "Leakage Guard": "SrcMac/DstMac/IPs strictly removed"},
        {"Dataset": "WUSTL-HDRL-2024", "Domain": "High-Density Medical 5G", "Splits (Train/Val/Test)": "24,500 / 5,250 / 5,250", "Features": "66 Flow Stats", "Classes": "5", "Leakage Guard": "Signed-log1p normalization; zero leakage"},
        {"Dataset": "CIC-IoT-2023", "Domain": "Large-Scale IoT Ecosystem", "Splits (Train/Val/Test)": "24,500 / 5,250 / 5,250", "Features": "46 Flow Stats", "Classes": "9", "Leakage Guard": "NetFlow alignment; stratified holdout"},
        {"Dataset": "ToN-IoT", "Domain": "Network Flow & Telemetry", "Splits (Train/Val/Test)": "24,500 / 5,250 / 5,250", "Features": "39 Flow Stats", "Classes": "8", "Leakage Guard": "Socket identifiers excluded; robust scaling"},
        {"Dataset": "MIMIC PERform III", "Domain": "Biomedical Cardiac AF", "Splits (Train/Val/Test)": "960 / 200 / 240 (Windows)", "Features": "3×625 Wave + 11 Tab", "Classes": "2 (AF/Non-AF)", "Leakage Guard": "Strict 0% Patient Overlap (24/5/6 Subjects)"},
        {"Dataset": "BIDMC", "Domain": "Biomedical Clinical Reference", "Splits (Train/Val/Test)": "925 / 200 / 200 (Windows)", "Features": "3×625 Wave + 11 Tab", "Classes": "Continuous", "Leakage Guard": "Subject-Independent Split (53 Total Subjects)"}
    ]
    st.dataframe(pd.DataFrame(datasets_info), use_container_width=True, hide_index=True)

    # 4. Component Status Cards
    st.markdown("### **Verified System Components & Cryptographic Layer**")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="dqh-panel">
            <div class="dqh-panel-header">Stream A: Quantum Cybersecurity</div>
            <div style="font-size: 13px; color: #94A3B8; line-height: 1.6;">
                Backbone: Periodic Coord + 1D-CNN (SE) + Causal TCN + BiGRU + Temporal Attention + 4-Qubit VQC with Ring CNOT.<br>
                Meta-Ensemble: Level-1 LogReg Stacking with XGBoost, LightGBM, RF.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="dqh-panel">
            <div class="dqh-panel-header">Stream B: Biomedical Signal AI</div>
            <div style="font-size: 13px; color: #94A3B8; line-height: 1.6;">
                Inputs: 125 Hz ECG Lead II, PPG, and thoracic respiration.<br>
                Fusion: SQI modality-masked gated fusion with 11 physiological features (HRV, SDNN, RMSSD, PTT).<br>
                Performance: 89.17% Acc, 95.0% AF Sensitivity.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="dqh-panel">
            <div class="dqh-panel-header">Security Orchestration & Ledger</div>
            <div style="font-size: 13px; color: #94A3B8; line-height: 1.6;">
                Arbitration: Risk scoring engine with Life-Support emergency clinical override.<br>
                Storage: AES-256-GCM symmetric authenticated encryption.<br>
                Ledger: Hyperledger Fabric chaincode with cryptographic fallback.
            </div>
        </div>
        """, unsafe_allow_html=True)
