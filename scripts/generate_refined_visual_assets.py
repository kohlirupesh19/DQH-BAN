#!/usr/bin/env python3
"""
scripts/generate_refined_visual_assets.py
Programmatically renders publication-grade, dark-themed scientific visual assets:
1. dashboard/assets/logo.png (Brand identity icon)
2. dashboard/assets/architecture/fig01_dqh_ban_architecture_refined.png (6-Layer System Architecture)
3. dashboard/assets/illustrations/fig15_quantum_circuit_refined.png (4-Qubit PennyLane VQC)
"""

import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "dashboard", "assets")
ARCH_DIR = os.path.join(ASSETS_DIR, "architecture")
ILLUST_DIR = os.path.join(ASSETS_DIR, "illustrations")

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(ARCH_DIR, exist_ok=True)
os.makedirs(ILLUST_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. RENDER BRAND LOGO (dashboard/assets/logo.png)
# ------------------------------------------------------------------------------
def generate_logo():
    width, height = 800, 800
    img = Image.new("RGBA", (width, height), (11, 16, 32, 255)) # #0B1020
    draw = ImageDraw.Draw(img)

    cx, cy = width // 2, height // 2 - 20
    radius = 280

    # Draw subtle background glow
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([cx - radius - 30, cy - radius - 30, cx + radius + 30, cy + radius + 30],
                      fill=(56, 189, 248, 25))
    glow_draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                      fill=(129, 140, 248, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(30))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # Outer Shield / Hexagonal Ring
    num_sides = 6
    hex_pts = []
    for i in range(num_sides):
        angle = math.radians(60 * i - 30)
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        hex_pts.append((px, py))
    draw.polygon(hex_pts, outline=(30, 41, 59, 255), width=6)
    draw.polygon([(x*0.96 + cx*0.04, y*0.96 + cy*0.04) for x, y in hex_pts],
                 outline=(56, 189, 248, 160), width=3)

    # 4 Qubit Nodes (Ring Entanglement)
    qubit_angles = [0, 90, 180, 270]
    q_coords = []
    q_radius = 175
    for a in qubit_angles:
        rad = math.radians(a)
        qx = cx + q_radius * math.cos(rad)
        qy = cy + q_radius * math.sin(rad)
        q_coords.append((qx, qy))

    # Ring connections
    for i in range(4):
        p1 = q_coords[i]
        p2 = q_coords[(i + 1) % 4]
        draw.line([p1, p2], fill=(129, 140, 248, 180), width=4)

    # Cross quantum entanglement lines
    draw.line([q_coords[0], q_coords[2]], fill=(129, 140, 248, 70), width=2)
    draw.line([q_coords[1], q_coords[3]], fill=(129, 140, 248, 70), width=2)

    # Draw Qubit Nodes
    for i, (qx, qy) in enumerate(q_coords):
        draw.ellipse([qx - 24, qy - 24, qx + 24, qy + 24], fill=(23, 32, 51, 255), outline=(129, 140, 248, 255), width=4)
        draw.ellipse([qx - 10, qy - 10, qx + 10, qy + 10], fill=(56, 189, 248, 255))

    # ECG Heartbeat Pulse across center
    ecg_y = cy
    ecg_points = [
        (cx - 210, ecg_y),
        (cx - 150, ecg_y),
        (cx - 130, ecg_y - 18),
        (cx - 110, ecg_y + 12),
        (cx - 80, ecg_y),
        (cx - 50, ecg_y - 8),
        (cx - 25, ecg_y + 25),
        (cx, ecg_y - 110),      # R-peak
        (cx + 25, ecg_y + 45),   # S-wave
        (cx + 50, ecg_y),
        (cx + 90, ecg_y - 35),   # T-wave
        (cx + 125, ecg_y),
        (cx + 210, ecg_y)
    ]
    # Draw ECG glow and main stroke
    for i in range(len(ecg_points) - 1):
        draw.line([ecg_points[i], ecg_points[i+1]], fill=(45, 212, 191, 240), width=6)

    # Brand Title Typography
    logo_path = os.path.join(ASSETS_DIR, "logo.png")
    img.save(logo_path, "PNG")
    print(f"Generated logo: {logo_path}")

# ------------------------------------------------------------------------------
# 2. RENDER REFINED ARCHITECTURE (fig01_dqh_ban_architecture_refined.png)
# ------------------------------------------------------------------------------
def generate_architecture_diagram():
    fig = plt.figure(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor("#0B1020")
    ax = fig.add_subplot(111)
    ax.set_facecolor("#0B1020")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # Header Title
    ax.text(8.0, 8.55, "DQH-BAN: Dual-Stream Quantum Healthcare Intelligence Architecture",
            ha="center", va="center", color="#F8FAFC", fontsize=15, fontweight="bold")
    ax.text(8.0, 8.25, "Zero-Trust IoMT Cybersecurity & Patient-Independent Multi-Modal Biomedical Intelligence",
            ha="center", va="center", color="#94A3B8", fontsize=10)

    # Define 6 layers as modular panels
    layers = [
        {"y": 7.0, "h": 0.85, "title": "Layer 1: Body Area Network (BAN) Multi-Modal Sensor Acquisition", "color": "#38BDF8",
         "boxes": [
             ("ECG Lead II Patch (125 Hz)", 0.6, 3.2),
             ("PPG Optical Oximeter (125 Hz)", 4.2, 3.2),
             ("Thoracic Impedance Respiration", 7.8, 3.2),
             ("IoMT Telemetry & NetFlow v2", 11.4, 4.0)
         ]},
        {"y": 5.8, "h": 0.85, "title": "Layer 2: Edge Preprocessing, SQI Gating & Leakage Prevention", "color": "#2DD4BF",
         "boxes": [
             ("Signal Quality Index (SQI) Filter", 0.6, 4.6),
             ("Zero Patient Overlap Windowing", 5.6, 4.6),
             ("Leakage Guards (MAC/IP Audit)", 10.6, 4.8)
         ]},
        {"y": 3.7, "h": 1.7, "title": "Layer 3: Dual-Stream Quantum-Classical Intelligence Engine", "color": "#818CF8",
         "sub": True},
        {"y": 2.2, "h": 1.1, "title": "Layer 4 & 5: Security Orchestration, Cryptography & Blockchain Ledger", "color": "#34D399",
         "boxes": [
             ("Multi-Factor Risk Arbitration Engine (Clinical Overrides)", 0.6, 5.0),
             ("AES-256-GCM Encryption + SHA-256 Commitments", 6.0, 4.8),
             ("Hyperledger Fabric Contract & Crypto Fallback", 11.2, 4.2)
         ]},
        {"y": 0.7, "h": 1.1, "title": "Layer 6: Clinical Inference Gateway & Research Laboratory", "color": "#FBBF24",
         "boxes": [
             ("FastAPI REST Microservice (:8000, 12 Production Endpoints)", 1.5, 6.0),
             ("Streamlit 9-Page Academic Research Lab (:8501)", 8.5, 6.0)
         ]}
    ]

    for layer in layers:
        # Layer border box
        rect = patches.FancyBboxPatch((0.4, layer["y"]), 15.2, layer["h"],
                                      boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor="#111827", edgecolor=layer["color"],
                                      linewidth=1.5, alpha=0.9)
        ax.add_patch(rect)
        ax.text(0.6, layer["y"] + layer["h"] - 0.22, layer["title"],
                color=layer["color"], fontsize=11, fontweight="bold")

        if "boxes" in layer:
            for text, bx, bw in layer["boxes"]:
                b_rect = patches.FancyBboxPatch((bx, layer["y"] + 0.12), bw, layer["h"] - 0.45,
                                                boxstyle="round,pad=0.08,rounding_size=0.1",
                                                facecolor="#172033", edgecolor="#334155", linewidth=1.0)
                ax.add_patch(b_rect)
                ax.text(bx + bw / 2.0, layer["y"] + 0.12 + (layer["h"] - 0.45) / 2.0, text,
                        ha="center", va="center", color="#F8FAFC", fontsize=9, fontweight="medium")

    # Layer 3 Dual-Stream Content
    y3 = 3.7
    # Stream B (Left)
    b_rect = patches.FancyBboxPatch((0.6, y3 + 0.12), 6.5, 1.2,
                                    boxstyle="round,pad=0.08,rounding_size=0.1",
                                    facecolor="#172033", edgecolor="#2DD4BF", linewidth=1.2)
    ax.add_patch(b_rect)
    ax.text(3.85, y3 + 1.12, "Stream B: Biomedical Signal Intelligence",
            ha="center", va="center", color="#2DD4BF", fontsize=10, fontweight="bold")
    ax.text(3.85, y3 + 0.72, "1D-CNN Encoders (ECG, PPG, Resp) + SQI Modality Gated Fusion",
            ha="center", va="center", color="#F8FAFC", fontsize=8.5)
    ax.text(3.85, y3 + 0.35, "Patient-Independent AF Classifier (Sensitivity 95.0%, AUC 0.9574)",
            ha="center", va="center", color="#94A3B8", fontsize=8)

    # Stream A (Right)
    a_rect = patches.FancyBboxPatch((7.5, y3 + 0.12), 7.9, 1.2,
                                    boxstyle="round,pad=0.08,rounding_size=0.1",
                                    facecolor="#172033", edgecolor="#818CF8", linewidth=1.2)
    ax.add_patch(a_rect)
    ax.text(11.45, y3 + 1.12, "Stream A: Hybrid Quantum-Classical Cybersecurity Ensemble",
            ha="center", va="center", color="#818CF8", fontsize=10, fontweight="bold")
    ax.text(11.45, y3 + 0.72, "1D-CNN (SE) + Causal TCN + BiGRU + Temporal Attn + 4-Qubit PennyLane VQC",
            ha="center", va="center", color="#F8FAFC", fontsize=8.5)
    ax.text(11.45, y3 + 0.35, "3-Fold Stacking: XGBoost, LightGBM, RF, LogReg (98.03% Acc, FPR 0.10-0.98%)",
            ha="center", va="center", color="#94A3B8", fontsize=8)

    # Inter-layer arrows
    arrow_props = dict(arrowstyle="->,head_width=0.3,head_length=0.4", color="#38BDF8", lw=1.8)
    ax.annotate("", xy=(8.0, 5.8), xytext=(8.0, 7.0), arrowprops=arrow_props)
    ax.annotate("", xy=(3.85, 4.9), xytext=(3.85, 5.8), arrowprops=dict(arrowstyle="->", color="#2DD4BF", lw=1.6))
    ax.annotate("", xy=(11.45, 4.9), xytext=(11.45, 5.8), arrowprops=dict(arrowstyle="->", color="#818CF8", lw=1.6))
    ax.annotate("", xy=(8.0, 3.3), xytext=(8.0, 3.7), arrowprops=dict(arrowstyle="->", color="#34D399", lw=1.6))
    ax.annotate("", xy=(8.0, 1.8), xytext=(8.0, 2.2), arrowprops=dict(arrowstyle="->", color="#FBBF24", lw=1.6))

    out_p = os.path.join(ARCH_DIR, "fig01_dqh_ban_architecture_refined.png")
    fig.savefig(out_p, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print(f"Generated architecture diagram: {out_p}")

# ------------------------------------------------------------------------------
# 3. RENDER REFINED QUANTUM CIRCUIT (fig15_quantum_circuit_refined.png)
# ------------------------------------------------------------------------------
def generate_quantum_circuit_diagram():
    fig = plt.figure(figsize=(14, 7), dpi=300)
    fig.patch.set_facecolor("#0B1020")
    ax = fig.add_subplot(111)
    ax.set_facecolor("#0B1020")
    ax.set_xlim(0, 14)
    ax.set_ylim(-0.5, 4.5)
    ax.axis("off")

    ax.text(7.0, 4.25, "PennyLane 4-Qubit Variational Quantum Circuit (VQC) with Ring CNOT Entanglement",
            ha="center", va="center", color="#F8FAFC", fontsize=13, fontweight="bold")
    ax.text(7.0, 3.95, "Data Re-Uploading RY Embeddings | 2 Layers | Pauli-Z Expectation Heads",
            ha="center", va="center", color="#818CF8", fontsize=9.5)

    qubit_y = [3.2, 2.2, 1.2, 0.2]
    qubit_labels = [r"$|q_0\rangle$", r"$|q_1\rangle$", r"$|q_2\rangle$", r"$|q_3\rangle$"]

    # Qubit lines
    for i, y in enumerate(qubit_y):
        ax.text(0.6, y, qubit_labels[i], ha="right", va="center", color="#38BDF8", fontsize=12, fontweight="bold")
        ax.plot([0.8, 12.8], [y, y], color="#334155", lw=2)

    # Stage 1: Hadamard Gates
    for y in qubit_y:
        h_box = patches.Rectangle((1.2, y - 0.25), 0.7, 0.5, facecolor="#1E293B", edgecolor="#38BDF8", lw=1.5)
        ax.add_patch(h_box)
        ax.text(1.55, y, "H", ha="center", va="center", color="#F8FAFC", fontsize=10, fontweight="bold")

    # Stage 2: Data Re-Uploading RY(x_i)
    for i, y in enumerate(qubit_y):
        ry_box = patches.Rectangle((2.3, y - 0.25), 1.1, 0.5, facecolor="#172033", edgecolor="#818CF8", lw=1.5)
        ax.add_patch(ry_box)
        ax.text(2.85, y, f"$R_Y(x_{i})$", ha="center", va="center", color="#818CF8", fontsize=9, fontweight="bold")

    # Stage 3: Layer 1 Variational Rotations R(alpha, beta, gamma)
    for i, y in enumerate(qubit_y):
        rot_box = patches.Rectangle((3.8, y - 0.28), 1.2, 0.56, facecolor="#1F2937", edgecolor="#A78BFA", lw=1.5)
        ax.add_patch(rot_box)
        ax.text(4.4, y, f"$U(\\theta^{(1)}_{i})$", ha="center", va="center", color="#F8FAFC", fontsize=9, fontweight="bold")

    # Stage 4: Ring CNOT Entanglement (Layer 1)
    # CNOT 0->1, 1->2, 2->3, 3->0 (Ring)
    cnots = [(0, 1, 5.4), (1, 2, 6.0), (2, 3, 6.6), (3, 0, 7.2)]
    for c, t, x in cnots:
        y_c = qubit_y[c]
        y_t = qubit_y[t]
        ax.plot([x, x], [y_c, y_t], color="#2DD4BF", lw=2)
        # Control dot
        ax.plot(x, y_c, marker="o", markersize=6, color="#2DD4BF")
        # Target circle with plus
        target_circle = patches.Circle((x, y_t), 0.18, facecolor="#0B1020", edgecolor="#2DD4BF", lw=1.8)
        ax.add_patch(target_circle)
        ax.plot([x - 0.12, x + 0.12], [y_t, y_t], color="#2DD4BF", lw=1.5)
        ax.plot([x, x], [y_t - 0.12, y_t + 0.12], color="#2DD4BF", lw=1.5)

    # Stage 5: Layer 2 Data Re-uploading & Variational Rotations
    for i, y in enumerate(qubit_y):
        ry_box = patches.Rectangle((8.0, y - 0.25), 1.1, 0.5, facecolor="#172033", edgecolor="#818CF8", lw=1.5)
        ax.add_patch(ry_box)
        ax.text(8.55, y, f"$R_Y(x_{i})$", ha="center", va="center", color="#818CF8", fontsize=9, fontweight="bold")

        rot_box = patches.Rectangle((9.4, y - 0.28), 1.2, 0.56, facecolor="#1F2937", edgecolor="#A78BFA", lw=1.5)
        ax.add_patch(rot_box)
        ax.text(10.0, y, f"$U(\\theta^{(2)}_{i})$", ha="center", va="center", color="#F8FAFC", fontsize=9, fontweight="bold")

    # Stage 6: Measurement Pauli-Z
    for i, y in enumerate(qubit_y):
        m_box = patches.Rectangle((11.1, y - 0.28), 1.2, 0.56, facecolor="#111827", edgecolor="#FBBF24", lw=1.5)
        ax.add_patch(m_box)
        ax.text(11.7, y, r"$\langle \sigma_z^{(%d)} \rangle$" % i, ha="center", va="center", color="#FBBF24", fontsize=10, fontweight="bold")

    # Annotations
    ax.text(1.55, -0.2, "Init (H)", ha="center", va="center", color="#94A3B8", fontsize=9)
    ax.text(2.85, -0.2, "Encoding", ha="center", va="center", color="#94A3B8", fontsize=9)
    ax.text(4.4, -0.2, "Var Layer 1", ha="center", va="center", color="#94A3B8", fontsize=9)
    ax.text(6.3, -0.2, "Ring CNOTs", ha="center", va="center", color="#2DD4BF", fontsize=9, fontweight="bold")
    ax.text(9.2, -0.2, "Re-Upload & Var 2", ha="center", va="center", color="#94A3B8", fontsize=9)
    ax.text(11.7, -0.2, "Pauli-Z ([-1, 1])", ha="center", va="center", color="#FBBF24", fontsize=9, fontweight="bold")

    out_p = os.path.join(ILLUST_DIR, "fig15_quantum_circuit_refined.png")
    fig.savefig(out_p, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print(f"Generated quantum circuit diagram: {out_p}")

if __name__ == "__main__":
    generate_logo()
    generate_architecture_diagram()
    generate_quantum_circuit_diagram()
