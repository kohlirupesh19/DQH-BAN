"""
dashboard/pages/biomedical.py
Page 4: Stream B Multi-Modal Biomedical Signal Intelligence & Cardiac Arrhythmia Detection.
"""

import os
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dashboard.components.header import render_header
from dashboard.components.metric_cards import render_kpi
from dashboard.components.charts import (
    apply_dark_theme, COLOR_BIO, COLOR_CYBER, COLOR_SUCCESS, COLOR_WARNING, COLOR_CRITICAL
)
from dashboard.utils.data_loader import load_biomedical_test_waveforms
from dashboard.utils.formatters import fmt_pct, fmt_float, fmt_ms

def render_page(data: dict):
    render_header(
        title="Stream B: Multi-Modal Biomedical Signal Intelligence",
        subtitle="1D-CNN Waveform Encoders, SQI Modality-Masked Gated Fusion, and Patient-Independent Atrial Fibrillation (AF) Detection",
        badges=[
            ("MIMIC PERform III", "bio"),
            ("BIDMC Clinical Reference", "bio"),
            ("0% Patient Overlap", "secure"),
            ("125 Hz Waveforms", "cyber")
        ]
    )

    st.markdown("""
    <div class="dqh-callout bio">
        <strong>⚠️ Investigational Research Notice:</strong> DQH-BAN Stream B is a scientific research architecture engineered for zero-trust physiological signal processing and arrhythmia classification under patient-independent cross-validation. It is not an FDA-cleared or CE-marked medical diagnostic device.
    </div>
    """, unsafe_allow_html=True)

    df_bio = data["bio"]
    if df_bio.empty:
        st.warning("No biomedical benchmark data found.")
        return

    # Extract MIMIC Benchmark Metrics
    mimic_rows = df_bio[df_bio["dataset"].str.contains("MIMIC", case=False, na=False)]
    if not mimic_rows.empty:
        m_row = mimic_rows.iloc[0]
        col1, col2, col3, col4, col5 = st.columns(5)
        render_kpi(col1, "Held-Out Accuracy", fmt_pct(m_row.get("accuracy")), "Zero Patient Overlap", "bio")
        render_kpi(col2, "AF Sensitivity (Recall)", fmt_pct(m_row.get("af_sensitivity_recall")), "24/5/6 Subject Split", "bio")
        render_kpi(col3, "AF Specificity", fmt_pct(m_row.get("af_specificity")), "Normal Sinus Rhythm", "cyber")
        render_kpi(col4, "Macro-F1 Score", fmt_pct(m_row.get("macro_f1")), "Balanced Detection", "quantum")
        render_kpi(col5, "ROC-AUC Score", fmt_float(m_row.get("roc_auc")), "Discrimination Power", "success")

    st.markdown("---")

    # 1. Biomedical Benchmark Table (MIMIC PERform III & BIDMC)
    st.markdown("### **Biomedical Benchmark Results (MIMIC PERform III & BIDMC Clinical Reference)**")
    st.dataframe(df_bio, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 2. Synchronized Multi-Channel Waveform Explorer
    st.markdown("### **Synchronized Patient Waveform Windows (125 Hz Sampling, 5-Second Windows)**")
    st.caption("Inspect authentic held-out test windows from MIMIC PERform III without patient overlap. Waveforms are preprocessed with bandpass filters and normalized.")

    bio_test_data = load_biomedical_test_waveforms()
    if bio_test_data and bio_test_data["waveforms"] is not None:
        w_test = bio_test_data["waveforms"]
        y_test = bio_test_data["labels"]
        n_windows = len(w_test)

        col_ctrl1, col_ctrl2 = st.columns([2, 1])
        with col_ctrl1:
            win_idx = st.slider("Select Held-Out Test Window Index:", 0, n_windows - 1, 0)
        with col_ctrl2:
            lbl_val = int(y_test[win_idx]) if y_test is not None else 0
            lbl_str = "Atrial Fibrillation (AF)" if lbl_val == 1 else "Normal Sinus Rhythm (Non-AF)"
            chip_color = "#F87171" if lbl_val == 1 else "#34D399"
            st.markdown(f"""
            <div style="padding: 12px; background: #111827; border: 1px solid #1E293B; border-radius: 8px; margin-top: 10px;">
                <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase;">Ground Truth Label</div>
                <div style="font-size: 16px; font-weight: 700; color: {chip_color};">{lbl_str}</div>
            </div>
            """, unsafe_allow_html=True)

        t = np.linspace(0, 5, 625)
        c_w1, c_w2, c_w3 = st.columns(3)

        with c_w1:
            fig_ecg = px.line(x=t, y=w_test[win_idx, 0], labels={"x": "Time (seconds)", "y": "Normalized Amplitude"})
            fig_ecg.update_traces(line=dict(color="#F87171", width=1.8))
            apply_dark_theme(fig_ecg, title="ECG Lead II Waveform (125 Hz)", height=260, showlegend=False)
            st.plotly_chart(fig_ecg, use_container_width=True)

        with c_w2:
            fig_ppg = px.line(x=t, y=w_test[win_idx, 1], labels={"x": "Time (seconds)", "y": "Normalized Amplitude"})
            fig_ppg.update_traces(line=dict(color="#38BDF8", width=1.8))
            apply_dark_theme(fig_ppg, title="PPG Photoplethysmogram (125 Hz)", height=260, showlegend=False)
            st.plotly_chart(fig_ppg, use_container_width=True)

        with c_w3:
            fig_resp = px.line(x=t, y=w_test[win_idx, 2], labels={"x": "Time (seconds)", "y": "Normalized Amplitude"})
            fig_resp.update_traces(line=dict(color="#2DD4BF", width=1.8))
            apply_dark_theme(fig_resp, title="Thoracic Impedance Respiration (125 Hz)", height=260, showlegend=False)
            st.plotly_chart(fig_resp, use_container_width=True)
    else:
        st.info("Biomedical splits artifact is loaded from artifacts/preprocessing/biomedical/mimic_perform_splits.pkl.")

    # 3. BIDMC Physiological Rate Agreement Analysis
    st.markdown("---")
    st.markdown("### **BIDMC Clinical Rate Estimation & SQI Gating**")
    c_rate1, c_rate2 = st.columns(2)
    with c_rate1:
        st.markdown("""
        <div class="dqh-panel">
            <div class="dqh-panel-header">BIDMC Multi-Rate Estimation Performance</div>
            <div style="font-size: 13px; color: #94A3B8; line-height: 1.8;">
                • <strong>Heart Rate (ECG) MAE:</strong> <span style="color: #F8FAFC;">2.20 bpm</span><br>
                • <strong>Pulse Rate (PPG) MAE:</strong> <span style="color: #F8FAFC;">3.05 bpm</span><br>
                • <strong>Respiration Rate MAE:</strong> <span style="color: #F8FAFC;">1.62 brpm</span><br>
                • <strong>ECG–PPG Rate Agreement:</strong> <span style="color: #2DD4BF; font-weight: 600;">90.50% within +/- 5 bpm</span><br>
                • <strong>Mean Signal Quality Index (SQI):</strong> <span style="color: #38BDF8;">0.4032</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_rate2:
        st.markdown("""
        <div class="dqh-panel">
            <div class="dqh-panel-header">SQI Modality-Masked Gated Fusion Logic</div>
            <div style="font-size: 13px; color: #94A3B8; line-height: 1.8;">
                • <strong>Lead II ECG SQI:</strong> Skewness, Kurtosis, and QRS energy ratio.<br>
                • <strong>PPG SQI:</strong> Perfusion index, waveform trough-peak ratio, template matching.<br>
                • <strong>Gating Mechanism:</strong> If SQI &lt; 0.20, waveform representation is zero-masked and the fusion layer dynamically shifts weight to remaining valid channels.<br>
                • <strong>Fail-Safe:</strong> Alerts security orchestration if 2+ channels fail SQI simultaneously.
            </div>
        </div>
        """, unsafe_allow_html=True)
