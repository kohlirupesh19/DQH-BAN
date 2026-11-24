"""
dashboard/pages/cybersecurity.py
Page 2: Stream A Quantum-Classical Cybersecurity Intelligence.
"""

import os
import ast
import torch
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dashboard.components.header import render_header
from dashboard.components.metric_cards import render_kpi
from dashboard.components.charts import (
    apply_dark_theme, COLOR_CYBER, COLOR_QUANTUM, COLOR_SUCCESS, COLOR_WARNING, COLOR_CRITICAL
)
from dashboard.utils.data_loader import load_threshold_artifact
from dashboard.utils.path_manager import resolve_path
from dashboard.utils.formatters import fmt_pct, fmt_ms, fmt_float

def render_page(data: dict):
    render_header(
        title="Stream A: Hybrid Quantum-Classical Cybersecurity Intelligence",
        subtitle="Periodic Coordinate & Quantile Encoder, 1D-CNN (SE), Causal TCN, BiGRU, Temporal Attention, 4-Qubit VQC, and 3-Fold Stacking Ensemble",
        badges=[
            ("5 Physical Datasets", "cyber"),
            ("3-Fold OOF Stacking", "quantum"),
            ("Real-Time SLA < 10ms", "secure")
        ]
    )

    df_bench = data["bench"]
    if df_bench.empty:
        st.warning("No benchmark results found.")
        return

    # Dataset & Model Selector Controls
    col_sel1, col_sel2 = st.columns([1, 1.2])
    with col_sel1:
        datasets = list(df_bench["dataset"].unique())
        selected_ds = st.selectbox("Select Target IoMT Dataset:", datasets, index=0)
    
    ds_sub = df_bench[df_bench["dataset"] == selected_ds].copy()
    with col_sel2:
        models = list(ds_sub["model"].unique())
        # Default to Hybrid Quantum Ensemble
        default_idx = next((i for i, m in enumerate(models) if "Hybrid_Quantum" in str(m)), 0)
        selected_mod = st.selectbox("Select Model Architecture to Inspect:", models, index=default_idx)

    selected_row = ds_sub[ds_sub["model"] == selected_mod].iloc[0]

    # Metrics KPI Strip
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    render_kpi(col1, "Test Accuracy", fmt_pct(selected_row.get("accuracy")), "Held-Out Split", "cyber")
    render_kpi(col2, "Precision", fmt_pct(selected_row.get("precision")), "Attack Detection", "cyber")
    render_kpi(col3, "Recall / Sens", fmt_pct(selected_row.get("recall")), "Intrusion Coverage", "quantum")
    render_kpi(col4, "Macro-F1", fmt_pct(selected_row.get("macro_f1")), "Balanced Metric", "quantum")
    render_kpi(col5, "False Pos Rate", fmt_pct(selected_row.get("fpr")), f"Target <= 1.0%", "warning" if float(selected_row.get("fpr", 0)) > 0.01 else "success")
    render_kpi(col6, "Mean Latency", fmt_ms(selected_row.get("mean_latency_ms")), "SLA < 10 ms", "success")

    st.markdown("---")

    # Confusion Matrix and Threshold Curve
    c_cm, c_th = st.columns(2)
    th_json = load_threshold_artifact(selected_ds)

    with c_cm:
        st.markdown("### **Held-Out Test Confusion Matrix**")
        ckpt_rel = str(selected_row.get("checkpoint_path", ""))
        ckpt_full = resolve_path(ckpt_rel) if ckpt_rel else None
        cm = None
        if ckpt_full and ckpt_full.suffix == ".pt" and ckpt_full.exists():
            try:
                ckpt_data = torch.load(ckpt_full, map_location="cpu", weights_only=False)
                cm = ckpt_data.get("test_metrics", {}).get("confusion_matrix")
            except Exception:
                pass
        
        if cm is None:
            cm = [
                [int(selected_row.get("tn_count", 0)), int(selected_row.get("fp_count", 0))],
                [int(selected_row.get("fn_count", 0)), int(selected_row.get("tp_count", 0))]
            ]
        
        fig_cm = px.imshow(
            cm, text_auto=True,
            x=["Benign", "Attack"], y=["Benign", "Attack"],
            color_continuous_scale=[[0, "#111827"], [0.5, "#1E3A8A"], [1, "#38BDF8"]],
            labels=dict(x="Predicted Label", y="True Label")
        )
        apply_dark_theme(fig_cm, title=f"Confusion Matrix: {selected_mod} [{selected_ds}]", height=320)
        st.plotly_chart(fig_cm, use_container_width=True)

    with c_th:
        st.markdown("### **Validation Threshold Calibration Curve**")
        if th_json and "threshold_curve" in th_json:
            tc = th_json["threshold_curve"]
            df_th = pd.DataFrame({
                "Threshold": tc["thresholds"],
                "FPR (%)": [v * 100 for v in tc["fpr"]],
                "FNR (%)": [v * 100 for v in tc["fnr"]]
            })
            opt_t = float(selected_row.get("threshold", th_json.get("optimal_threshold", 0.5)))
            fig_th = px.line(
                df_th, x="Threshold", y=["FPR (%)", "FNR (%)"],
                color_discrete_map={"FPR (%)": COLOR_WARNING, "FNR (%)": COLOR_CRITICAL}
            )
            fig_th.add_vline(x=opt_t, line_dash="dash", line_color=COLOR_QUANTUM,
                             annotation_text=f"tau*={opt_t:.4f}", annotation_position="top left")
            apply_dark_theme(fig_th, title=f"FPR vs FNR Operating Tradeoff (tau*={opt_t:.4f})", height=320,
                             xaxis_title="Classification Threshold (tau)", yaxis_title="Error Rate (%)")
            st.plotly_chart(fig_th, use_container_width=True)
        else:
            st.info("Validation threshold curve artifact is loaded from artifacts/thresholds/.")

    # Meta-Weights and Calibration Reliability Diagram
    c_w, c_cal = st.columns(2)
    with c_w:
        st.markdown("### **Stacking Meta-Classifier Weights (Model Contribution)**")
        meta_w_str = str(selected_row.get("meta_weights", ""))
        has_weights = False
        if meta_w_str and meta_w_str != "nan":
            try:
                mw = ast.literal_eval(meta_w_str) if isinstance(meta_w_str, str) else meta_w_str
                if isinstance(mw, dict):
                    has_weights = True
                    df_mw = pd.DataFrame({"Base Model": list(mw.keys()), "Weight": list(mw.values())}).sort_values("Weight", ascending=True)
                    fig_mw = px.bar(
                        df_mw, x="Weight", y="Base Model", orientation="h",
                        color="Weight", color_continuous_scale=[[0, "#1E1B4B"], [1, "#818CF8"]]
                    )
                    apply_dark_theme(fig_mw, title=f"Level-1 Logistic Regression Stacking Weights [{selected_mod}]",
                                     height=300, showlegend=False, xaxis_title="Stacking Weight", yaxis_title="Learner")
                    st.plotly_chart(fig_mw, use_container_width=True)
            except Exception:
                pass
        if not has_weights:
            st.markdown("""
            <div class="dqh-callout">
                <strong>Standalone Base Learner:</strong> This model operates as a standalone classifier (100% individual feature attribution without meta-level stacking).
            </div>
            """, unsafe_allow_html=True)

    with c_cal:
        st.markdown("### **Probability Calibration (Reliability Diagram)**")
        if th_json and "reliability_bins" in th_json:
            rb = th_json["reliability_bins"]
            if "bin_confs" in rb and "bin_accs" in rb:
                fig_cal = go.Figure()
                fig_cal.add_trace(go.Scatter(
                    x=rb["bin_confs"], y=rb["bin_accs"], mode="lines+markers",
                    name="Observed Empirical Frequency", marker=dict(color=COLOR_CYBER, size=7)
                ))
                fig_cal.add_trace(go.Scatter(
                    x=[0, 1], y=[0, 1], mode="lines", name="Perfect Calibration",
                    line=dict(dash="dash", color="#64748B")
                ))
                ece_v = th_json.get("expected_calibration_error", 0.0)
                brier_v = th_json.get("brier_score", 0.0)
                apply_dark_theme(fig_cal, title=f"Expected Calibration Error (ECE): {ece_v:.4f} | Brier: {brier_v:.4f}",
                                 height=300, xaxis_title="Mean Predicted Probability", yaxis_title="Empirical Positive Rate")
                st.plotly_chart(fig_cal, use_container_width=True)
        else:
            st.info("Probability calibration curves available in thresholds metadata.")

    # All Models Comparison Table for the Selected Dataset
    st.markdown(f"### **Comparative Cybersecurity Benchmark on {selected_ds}**")
    cols = ["model", "accuracy", "precision", "recall", "macro_f1", "roc_auc", "fpr", "fnr", "mean_latency_ms", "threshold"]
    valid_cols = [c for c in cols if c in ds_sub.columns]
    df_display = ds_sub[valid_cols].sort_values("macro_f1", ascending=False).reset_index(drop=True)
    st.dataframe(df_display, use_container_width=True, hide_index=True)
