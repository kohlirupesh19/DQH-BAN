"""
dashboard/app.py
Professional Streamlit Research & Demonstration Platform for DQH-BAN Architecture.
Modular, publication-grade dark laboratory aesthetic, fully optimized for
Streamlit Community Cloud and local high-performance execution.
Dynamically reads artifacts/results/benchmark_results.csv with zero hardcoded metrics.
"""

import os
import sys
from pathlib import Path

# Ensure repository root and dashboard directory are in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(DASHBOARD_DIR) not in sys.path:
    sys.path.insert(0, str(DASHBOARD_DIR))

import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="DQH-BAN: Quantum Healthcare Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS design system
css_path = BASE_DIR / "dashboard" / "styles" / "theme.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Import modular components and utilities
from dashboard.components.sidebar import render_sidebar
from dashboard.components.footer import render_footer
from dashboard.utils.data_loader import load_all_datasets_data
from dashboard.utils.deployment import get_system_instances_lazy

# Import view modules
from dashboard.views import (
    overview,
    cybersecurity,
    quantum,
    biomedical,
    orchestration,
    blockchain,
    simulator,
    benchmark,
    reports
)

# Lazy-load system components and cached research data
fc, vault, orch, sim = get_system_instances_lazy()
data = load_all_datasets_data()

# Render persistent sidebar navigation
selected_page = render_sidebar(fc, sim)

# Page routing
if "1. System Overview" in selected_page:
    overview.render_page(data, fc, sim)

elif "2. Cybersecurity Intelligence" in selected_page:
    cybersecurity.render_page(data)

elif "3. Quantum Intelligence" in selected_page:
    quantum.render_page(data)

elif "4. Biomedical Intelligence" in selected_page:
    biomedical.render_page(data)

elif "5. Security Orchestration" in selected_page:
    orchestration.render_page(orch, fc)

elif "6. Blockchain Security" in selected_page:
    blockchain.render_page(fc, vault)

elif "7. Live BAN Simulator" in selected_page:
    simulator.render_page(sim)

elif "8. Benchmark Laboratory" in selected_page:
    benchmark.render_page(data)

elif "9. Research Reports" in selected_page:
    reports.render_page()

# Render standardized footer
render_footer()
