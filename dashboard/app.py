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

# Ensure repository root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

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

# Lazy-load system components and cached research data
fc, vault, orch, sim = get_system_instances_lazy()
data = load_all_datasets_data()

# Render persistent sidebar navigation
selected_page = render_sidebar(fc, sim)

# Page routing
if selected_page == "1. System Overview":
    from dashboard.pages import overview
    overview.render_page(data, fc, sim)

elif selected_page == "2. Cybersecurity Intelligence":
    from dashboard.pages import cybersecurity
    cybersecurity.render_page(data)

elif selected_page == "3. Quantum Intelligence":
    from dashboard.pages import quantum
    quantum.render_page(data)

elif selected_page == "4. Biomedical Intelligence":
    from dashboard.pages import biomedical
    biomedical.render_page(data)

elif selected_page == "5. Security Orchestration":
    from dashboard.pages import orchestration
    orchestration.render_page(orch, fc)

elif selected_page == "6. Blockchain Security":
    from dashboard.pages import blockchain
    blockchain.render_page(fc, vault)

elif selected_page == "7. Live BAN Simulator":
    from dashboard.pages import simulator
    simulator.render_page(sim)

elif selected_page == "8. Benchmark Laboratory":
    from dashboard.pages import benchmark
    benchmark.render_page(data)

elif selected_page == "9. Research Reports":
    from dashboard.pages import reports
    reports.render_page()

# Render standardized footer
render_footer()
