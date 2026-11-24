"""
dashboard/pages/quantum.py
Page 3: Quantum Intelligence, PennyLane VQC & Component Ablations.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dashboard.components.header import render_header
from dashboard.components.metric_cards import render_kpi
from dashboard.components.charts import (
    apply_dark_theme, COLOR_QUANTUM, COLOR_CYBER, COLOR_BIO, COLOR_WARNING, COLOR_CRITICAL
)
from dashboard.utils.path_manager import resolve_path
from dashboard.utils.formatters import fmt_pct, fmt_ms

def render_page(data: dict):
    render_header(
        title="Variational Quantum Circuit (VQC) & Ablation Laboratory",
        subtitle="PennyLane Data Re-Uploading VQC, Ring CNOT Entanglement, Multi-Scale Classical Fusion, and Controlled Noise Sensitivity",
        badges=[
            ("PennyLane 0.45.1", "quantum"),
            ("4-Qubit Ring CNOT", "quantum"),
            ("Hardware Noise Simulation", "warning"),
            ("Empirical Artifacts", "secure")
        ]
    )

    df_bench = data["bench"]
    df_dl = data["dl"]
    df_q = data["q"]
    df_noise = data["noise"]

    # 1. Quantum Architecture KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    render_kpi(col1, "Encoding Protocol", "Data Re-Uploading", "Periodic Coord + Soft-RY", "quantum")
    render_kpi(col2, "Active Qubits", "4 Qubits", "2-Layer Ring CNOT", "quantum")
    render_kpi(col3, "VQC Latency", "3.92 ms", "CICIoMT2024 (Mean)", "cyber")
    render_kpi(col4, "Standalone VQC", "90.69%", "CICIoMT2024 Accuracy", "quantum")
    render_kpi(col5, "Hybrid Ensemble", "98.03%", "+7.34% Boost via Stacking", "secure")

    st.markdown("---")

    # 2. Quantum Circuit Architecture Visualization
    st.markdown("### **Variational Quantum Circuit (VQC) Circuit Architecture**")
    st.caption("Conceptual Architecture Diagram: 4 Qubits, Hadamard initialization, Data Re-Uploading RY rotations, Ring CNOT entanglement topology, and Pauli-Z expectation value readouts.")
    
    q_fig = resolve_path("dashboard/assets/illustrations/fig15_quantum_circuit_refined.png")
    if not q_fig.exists():
        q_fig = resolve_path("figures/fig15_quantum_circuit_diagram.png")
    if q_fig.exists():
        st.image(str(q_fig), caption="Figure 15: PennyLane 4-Qubit Variational Quantum Circuit Architecture with Ring CNOT Entanglement", use_container_width=True)

    st.markdown("---")

    # 3. Macro-F1 Ablation: Quantum vs No-Quantum vs Classical Ensemble
    st.markdown("### **Quantum Value-Add: Stacking Ensemble Ablation Study**")
    st.markdown("""
    <div class="dqh-callout">
        <strong>Empirical Ablation Protocol:</strong> Evaluates identical held-out test splits comparing:
        (1) <code>DQH_BAN_Hybrid_Quantum_Ensemble</code> (Full quantum-classical stacking),
        (2) <code>DQH_BAN_Hybrid_NoQuantum_Ensemble</code> (Deep learning backbone with classical matched head replacing VQC),
        (3) <code>Classical_Stacking_Ensemble</code> (XGBoost, LightGBM, Random Forest, Logistic Regression), and
        (4) Standalone <code>classical_matched</code> VQC proxy.
    </div>
    """, unsafe_allow_html=True)

    if not df_bench.empty:
        ablation_models = [
            "DQH_BAN_Hybrid_Quantum_Ensemble",
            "DQH_BAN_Hybrid_NoQuantum_Ensemble",
            "Classical_Stacking_Ensemble",
            "classical_matched"
        ]
        df_ab = df_bench[df_bench["model"].isin(ablation_models) | df_bench["model"].str.contains("Quantum_4q", case=False, na=False)].copy()
        if not df_ab.empty:
            fig_ab = px.bar(
                df_ab, x="dataset", y="macro_f1", color="model", barmode="group",
                color_discrete_map={
                    "DQH_BAN_Hybrid_Quantum_Ensemble": COLOR_QUANTUM,
                    "DQH_BAN_Hybrid_NoQuantum_Ensemble": COLOR_CYBER,
                    "Classical_Stacking_Ensemble": "#10B981",
                    "classical_matched": "#F59E0B"
                },
                title="Measured Test Macro-F1 Across Cybersecurity Datasets"
            )
            fig_ab.update_layout(yaxis_range=[0.80, 1.005])
            apply_dark_theme(fig_ab, height=360, xaxis_title="Benchmark Dataset", yaxis_title="Test Macro-F1")
            st.plotly_chart(fig_ab, use_container_width=True)

            # Ablation Data Table
            cols_show = [c for c in ["dataset", "model", "accuracy", "precision", "recall", "macro_f1", "fpr", "fnr", "mean_latency_ms"] if c in df_ab.columns]
            st.dataframe(df_ab[cols_show].sort_values(["dataset", "macro_f1"], ascending=[True, False]).reset_index(drop=True), use_container_width=True, hide_index=True)

    st.markdown("---")

    # 4. Deep Learning Backbone Ablation & Depolarizing Noise Sensitivity
    c_dl, c_noise = st.columns(2)

    with c_dl:
        st.markdown("### **Deep Learning Backbone Ablation (CICIoMT2024)**")
        if not df_dl.empty or not df_q.empty:
            comb = pd.concat([
                df_dl[df_dl["dataset"] == "CICIoMT2024"] if not df_dl.empty else pd.DataFrame(),
                df_q[df_q["dataset"] == "CICIoMT2024"] if not df_q.empty else pd.DataFrame()
            ], ignore_index=True)
            if not comb.empty:
                cols_dl = [c for c in ["model", "accuracy", "macro_f1", "roc_auc", "fpr", "fnr", "mean_latency_ms"] if c in comb.columns]
                st.dataframe(comb[cols_dl].sort_values("macro_f1", ascending=False).reset_index(drop=True), use_container_width=True, hide_index=True)

    with c_noise:
        st.markdown("### **Quantum Hardware Noise Sensitivity**")
        if not df_noise.empty:
            fig_noise = px.line(
                df_noise, x="noise_probability", y="macro_f1",
                markers=True, color_discrete_sequence=[COLOR_QUANTUM],
                title="Depolarizing Noise Impact on Test Macro-F1"
            )
            apply_dark_theme(fig_noise, height=300, xaxis_title="Depolarizing Error Probability (p)", yaxis_title="Macro-F1 Score")
            st.plotly_chart(fig_noise, use_container_width=True)
        else:
            st.info("Quantum noise sensitivity results available in artifacts/results/quantum_noise_sensitivity.csv.")
