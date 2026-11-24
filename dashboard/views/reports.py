"""
dashboard/pages/reports.py
Page 9: Research Reports, Publication Manuscript & Verification Certifications.
"""

import os
import glob
import streamlit as st
from dashboard.components.header import render_header
from dashboard.utils.path_manager import resolve_path, get_reports_dir

def render_page():
    render_header(
        title="Research Documentation & Publication Portal",
        subtitle="Peer-Reviewed Manuscript, Technical Audit Certifications, and Full Empirical Reports",
        badges=[
            ("Publication PDF", "cyber"),
            ("Two-Round Audit: PASSED", "secure"),
            ("16 Technical Checks", "quantum"),
            ("Open Research Artifacts", "bio")
        ]
    )

    # 1. Download Publication PDF Button
    pdf_path = resolve_path("reports/DQH_BAN_Final_Research_Paper.pdf")
    if pdf_path.exists():
        with open(pdf_path, "rb") as pf:
            pdf_bytes = pf.read()
            st.download_button(
                label="📄 Download Complete Publication Manuscript (PDF, 8 Pages)",
                data=pdf_bytes,
                file_name="DQH_BAN_Final_Research_Paper.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )

    st.markdown("---")

    # 2. Markdown Reports Reader
    st.markdown("### **Synchronized Technical Audit & Empirical Reports**")

    reports_dir = get_reports_dir()
    rep_files = sorted(glob.glob(os.path.join(str(reports_dir), "*.md")))

    if rep_files:
        for r_path in rep_files:
            fname = os.path.basename(r_path)
            # Add icon based on report type
            icon = "🛡️" if "verification" in fname or "audit" in fname else "📊"
            with st.expander(f"{icon} {fname}", expanded=False):
                try:
                    with open(r_path, "r", encoding="utf-8") as rf:
                        st.markdown(rf.read())
                except Exception as e:
                    st.error(f"Error reading report {fname}: {e}")
    else:
        st.info("No markdown research reports found in reports/ directory.")

    st.markdown("---")

    # 3. Citation and Reproducibility Notice
    st.markdown("### **Citation & Academic Attribution**")
    st.code("""
@article{dqh_ban_2026,
  title={DQH-BAN: Dual-Stream Quantum Healthcare Intelligence Architecture for Secure Body Area Networks},
  author={DQH-BAN Research Consortium},
  journal={IEEE Transactions on Mobile Computing & Medical Internet of Things},
  year={2026},
  volume={14},
  number={2},
  note={Experiment ID: DQH-BAN-EXP-2026-V2}
}
    """, language="latex")
