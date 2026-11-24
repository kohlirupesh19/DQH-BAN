"""
dashboard/utils/data_loader.py
Cached, lightweight, scientific artifact loader for DQH-BAN research dashboard.
Ensures zero retraining on startup and graceful fallbacks.
"""

import os
import json
import pickle
import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, Any, Optional
from dashboard.utils.path_manager import get_repo_root, resolve_path

@st.cache_data(ttl=60, show_spinner=False)
def load_csv(rel_path: str) -> pd.DataFrame:
    p = resolve_path(rel_path)
    if p.exists():
        try:
            return pd.read_csv(p)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

@st.cache_data(ttl=60, show_spinner=False)
def load_json(rel_path: str) -> Dict[str, Any]:
    p = resolve_path(rel_path)
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

@st.cache_data(ttl=60, show_spinner=False)
def get_master_benchmark_df() -> pd.DataFrame:
    """Loads and unifies master benchmark and hybrid ensemble tables."""
    df_bench = load_csv("artifacts/results/benchmark_results.csv")
    df_ens = load_csv("artifacts/results/hybrid_ensemble_results.csv")
    if not df_ens.empty:
        if df_bench.empty:
            df_bench = df_ens.copy()
        else:
            df_bench = pd.concat([df_bench, df_ens], ignore_index=True)
            df_bench = df_bench.drop_duplicates(subset=["dataset", "model"], keep="last").reset_index(drop=True)
    return df_bench

@st.cache_data(ttl=60, show_spinner=False)
def load_all_datasets_data() -> Dict[str, pd.DataFrame]:
    """Loads all core empirical CSV artifacts in a single cached call."""
    return {
        "bench": get_master_benchmark_df(),
        "ens": load_csv("artifacts/results/hybrid_ensemble_results.csv"),
        "dl": load_csv("artifacts/results/cyber_deep_learning_results.csv"),
        "q": load_csv("artifacts/results/quantum_model_results.csv"),
        "bio": load_csv("artifacts/results/biomedical_results.csv"),
        "noise": load_csv("artifacts/results/quantum_noise_sensitivity.csv"),
        "cross": load_csv("artifacts/results/cross_dataset_generalization.csv"),
        "baselines": load_csv("artifacts/results/baseline_results.csv")
    }

@st.cache_data(ttl=60, show_spinner=False)
def load_threshold_artifact(dataset_name: str) -> Dict[str, Any]:
    ds_key_map = {
        "CICIoMT2024": "ciciomt2024",
        "WUSTL-EHMS-2020": "wustl_ehms",
        "WUSTL-HDRL-2024": "wustl_hdrl",
        "CIC-IoT-2023": "cic_iot2023",
        "ToN-IoT": "ton_iot"
    }
    key = ds_key_map.get(dataset_name, dataset_name.lower().replace("-", "_"))
    return load_json(f"artifacts/thresholds/{key}_threshold.json")

@st.cache_data(ttl=300, show_spinner=False)
def load_biomedical_test_waveforms() -> Optional[Dict[str, Any]]:
    """Loads test waveforms from MIMIC PERform III splits for interactive visual inspection."""
    p = resolve_path("artifacts/preprocessing/biomedical/mimic_perform_splits.pkl")
    if p.exists():
        try:
            with open(p, "rb") as f:
                data = pickle.load(f)
            return {
                "waveforms": data.get("X_test_waveforms"),
                "labels": data.get("y_test"),
                "subjects": data.get("af_test_subjects", []) + data.get("non_af_test_subjects", [])
            }
        except Exception:
            return None
    return None

@st.cache_data(ttl=30, show_spinner=False)
def load_ledger_blocks(limit: int = 20) -> list:
    """Loads blockchain blocks from ledger_state.json."""
    st_json = load_json("artifacts/blockchain/ledger_state.json")
    blocks = st_json.get("blocks", [])
    return blocks[-limit:] if blocks else []
