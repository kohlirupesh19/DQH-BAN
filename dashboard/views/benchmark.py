"""
dashboard/pages/benchmark.py
Page 8: Academic Benchmark Laboratory & Cross-Dataset Generalization.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.components.header import render_header
from dashboard.components.metric_cards import render_kpi
from dashboard.components.charts import apply_dark_theme, COLOR_CYBER, COLOR_QUANTUM

def render_page(data: dict):
    render_header(
        title="Academic Benchmark Laboratory & Model Registry",
        subtitle="Single Source of Truth: Verified Test Split Metrics Across 48 Models and 7 Physical Datasets",
        badges=[
            ("48 Model Checkpoints", "quantum"),
            ("Single Source of Truth", "secure"),
            ("Cross-Dataset Transfer", "cyber"),
            ("CSV Export Ready", "bio")
        ]
    )

    df_bench = data["bench"]
    df_cross = data["cross"]

    if df_bench.empty:
        st.warning("No benchmark results found in artifacts/results/.")
        return

    # Filter Controls
    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    with col_f1:
        all_ds = ["All Datasets"] + sorted(list(df_bench["dataset"].dropna().unique()))
        sel_ds = st.selectbox("Filter by Dataset:", all_ds, index=0)
    with col_f2:
        model_search = st.text_input("Filter by Model Name (Search):", placeholder="e.g., Quantum, XGBoost, Stacking")
    with col_f3:
        sort_col = st.selectbox("Sort Table By:", ["macro_f1", "accuracy", "roc_auc", "fpr", "mean_latency_ms"], index=0)

    # Apply filters
    filtered_df = df_bench.copy()
    if sel_ds != "All Datasets":
        filtered_df = filtered_df[filtered_df["dataset"] == sel_ds]
    if model_search:
        filtered_df = filtered_df[filtered_df["model"].str.contains(model_search, case=False, na=False)]

    if sort_col in filtered_df.columns:
        ascending = True if sort_col in ["fpr", "mean_latency_ms"] else False
        filtered_df = filtered_df.sort_values(sort_col, ascending=ascending).reset_index(drop=True)

    # Master Table Display
    st.markdown(f"### **Master Benchmark Results ({len(filtered_df)} Models Matching)**")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # Download Buttons
    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        st.download_button(
            label="📥 Export Filtered Table as CSV",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name="dqh_ban_filtered_benchmark.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_d2:
        st.download_button(
            label="📥 Export Full Master Benchmark CSV (48 Checkpoints)",
            data=df_bench.to_csv(index=False).encode("utf-8"),
            file_name="benchmark_results.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.markdown("---")

    # Cross-Dataset Generalization Section
    st.markdown("### **Cross-Dataset Generalization & Zero-Shot Transfer Matrix**")
    st.caption("Models trained strictly on source datasets and evaluated directly on target unseen network telemetry distributions.")

    if not df_cross.empty:
        st.dataframe(df_cross, use_container_width=True, hide_index=True)

        # Plot Cross-Dataset heatmap if suitable pivot
        try:
            pivot_cross = df_cross.pivot(index="train_dataset", columns="test_dataset", values="test_accuracy")
            fig_cross = px.imshow(
                pivot_cross, text_auto=".4f",
                color_continuous_scale=[[0, "#111827"], [0.5, "#1E3A8A"], [1, "#38BDF8"]],
                labels=dict(x="Held-Out Target Dataset", y="Training Source Dataset", color="Accuracy")
            )
            apply_dark_theme(fig_cross, title="Zero-Shot Cross-Dataset Generalization Matrix", height=380)
            st.plotly_chart(fig_cross, use_container_width=True)
        except Exception:
            pass
    else:
        st.info("Cross-dataset evaluation results available in artifacts/results/cross_dataset_generalization.csv.")
