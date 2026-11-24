"""
dashboard/pages/blockchain.py
Page 6: Hyperledger Fabric Smart Contracts & Cryptographic Ledger Explorer.
"""

import json
import streamlit as st
import pandas as pd
from dashboard.components.header import render_header
from dashboard.components.metric_cards import render_kpi
from dashboard.utils.data_loader import load_json, load_ledger_blocks
from dashboard.utils.formatters import fmt_hash

def render_page(fc, vault):
    is_sim_ledger = not getattr(fc, "is_live_fabric", False)
    mode_text = "Cryptographic Fallback" if is_sim_ledger else "Live Fabric Peer"
    mode_badge = "warning" if is_sim_ledger else "secure"

    render_header(
        title="Hyperledger Fabric Permissioned Ledger & Off-Chain Vault",
        subtitle="Device Identity Management, Smart Contracts (Go Chaincode), AES-256-GCM Encryption, and SHA-256 State Anchoring",
        badges=[
            (f"Engine: {mode_text}", mode_badge),
            ("Chaincode: ban_security_contract", "cyber"),
            ("Off-Chain Vault: AES-256-GCM", "secure"),
            ("SHA-256 Commitments", "quantum")
        ]
    )

    if is_sim_ledger:
        st.markdown("""
        <div class="dqh-callout warning">
            <strong>🔒 Cryptographic Fallback Mode Notice:</strong> No live Hyperledger Fabric Docker peer was detected in the runtime environment. The system is operating seamlessly under <code>Fabric_Cryptographic_Ledger_Fallback</code>. All block hashes, device registrations, and SHA-256 tamper commitments are cryptographically calculated and saved locally in <code>artifacts/blockchain/ledger_state.json</code>.
        </div>
        """, unsafe_allow_html=True)

    state = getattr(fc, "state", {})
    blocks = state.get("blocks", [])
    devices = state.get("devices", {})
    events = state.get("security_events", [])

    # 1. Blockchain KPIs
    col1, col2, col3, col4 = st.columns(4)
    render_kpi(col1, "Total Blocks", str(len(blocks)), "Genesis to Tip", "quantum")
    render_kpi(col2, "Registered IoMT Nodes", str(len(devices)), "MSP Authorized", "cyber")
    render_kpi(col3, "Logged Security Events", str(len(events)), "Immutable Records", "warning")
    render_kpi(col4, "Ciphertext Vault", "AES-256-GCM", "96-bit Random IVs", "secure")

    st.markdown("---")

    # 2. Cryptographic Security Architecture Breakdown
    c_arch1, c_arch2 = st.columns(2)
    with c_arch1:
        st.markdown("""
        <div class="dqh-panel">
            <div class="dqh-panel-header">Off-Chain Vault & On-Chain Anchoring</div>
            <div style="font-size: 13px; color: #94A3B8; line-height: 1.8;">
                1. <strong>Payload Encryption:</strong> Patient telemetry is encrypted off-chain using AES-256-GCM with authenticated associated data (AAD).<br>
                2. <strong>Integrity Commitment:</strong> A cryptographic SHA-256 hash digest of the ciphertext is calculated.<br>
                3. <strong>On-Chain Ledger Anchor:</strong> Only the SHA-256 commitment, device ID, and timestamp are committed to the blockchain, eliminating HIPAA/GDPR PII exposure on the distributed ledger.<br>
                4. <strong>Tamper Verification:</strong> Any single-bit alteration in ciphertext invalidates the on-chain SHA-256 root and triggers rejection.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_arch2:
        st.markdown("""
        <div class="dqh-panel">
            <div class="dqh-panel-header">Smart Contract Specifications</div>
            <div style="font-size: 13px; color: #94A3B8; line-height: 1.8;">
                • <strong>Chaincode Source:</strong> <code>blockchain/smart_contracts/ban_security_contract.go</code><br>
                • <strong>Functions:</strong> <code>RegisterDevice()</code>, <code>VerifyDevice()</code>, <code>RecordSecurityEvent()</code>, <code>AnchorDataHash()</code>.<br>
                • <strong>Endorsement Policy:</strong> Requires endorsement by <code>Org1MSP</code> attending medical authority.<br>
                • <strong>Access Control:</strong> Attribute-based access control (ABAC) restricts medical data retrieval to authorized clinicians.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. Interactive Block Explorer
    st.markdown("### **Cryptographic Ledger Block Explorer (Last 10 Blocks)**")
    recent_blocks = blocks[-10:] if blocks else []

    if recent_blocks:
        table_rows = []
        for b in reversed(recent_blocks):
            table_rows.append({
                "Block #": b.get("block_number"),
                "Timestamp": b.get("timestamp"),
                "Tx Type": b.get("tx_type"),
                "Block Hash": fmt_hash(b.get("block_hash"), 16),
                "Previous Hash": fmt_hash(b.get("previous_hash"), 16),
                "Execution Engine": b.get("execution_engine")
            })
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

        with st.expander("🔍 View Raw JSON Block Payload (Latest Block)"):
            st.json(recent_blocks[-1])
    else:
        st.info("Ledger initialized. Blocks are committed as transactions occur.")
