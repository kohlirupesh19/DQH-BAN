# DQH-BAN Publication Figure Inventory & Visual Audit
**Experiment ID**: `DQH-BAN-EXP-2026-V2` | **Classification & Enhancement Register**

---

| Figure File | Category | Dim / DPI | Scientific Purpose | Visual Assessment | Enhancement / Companion Asset | Target Dashboard Page |
|---|---|---|---|---|---|---|
| `fig01_dqh_ban_architecture` | 1. System Architecture | 2501×1492 / 300 | 6-Layer End-to-End System Architecture | Light background; dense text blocks | Refined dark-theme vector diagram (`fig01_dqh_ban_architecture_refined.png`) | Page 1: System Overview |
| `fig02_dataset_workflow` | 3. Cybersecurity Pipeline | 2152×1048 / 300 | Leakage Audit, Scaler & Train/Val/Test Split Protocol | Clean workflow | Kept as verified artifact + interactive summary | Page 1: System Overview |
| `fig03_dataset_distribution` | 7. Experimental Results | 2322×1291 / 300 | Class distributions across 5 cyber datasets | Static bar chart | Replaced with interactive Plotly stacked bar in Streamlit | Page 2: Cybersecurity |
| `fig04_class_imbalance` | 7. Experimental Results | 2067×1102 / 300 | Attack vs Benign ratios per dataset | High-contrast static plot | Interactive metric cards + class filter | Page 2: Cybersecurity |
| `fig05_feature_correlation` | 6. Signal Processing | 2015×1753 / 300 | Pearson correlation across 45 flow features | Dense 45×45 static heatmap | Static high-res viewer with feature selector | Page 2: Cybersecurity |
| `fig06_feature_importance` | 7. Experimental Results | 2255×1282 / 300 | Top-15 Gini / Permutation importance features | Horizontal bar chart | Interactive Plotly horizontal bar chart | Page 2: Cybersecurity |
| `fig07_training_loss` | 7. Experimental Results | 2056×1166 / 300 | Epoch training loss for CNN, TCN, BiGRU, VQC | Multi-line static curve | Interactive Plotly multi-curve viewer | Page 2: Cybersecurity |
| `fig08_validation_loss` | 7. Experimental Results | 2056×1166 / 300 | Validation loss with early stopping | Multi-line static curve | Interactive Plotly multi-curve viewer | Page 2: Cybersecurity |
| `fig09_accuracy_curves` | 7. Experimental Results | 2079×1166 / 300 | Validation accuracy progression | Line chart | Interactive Plotly convergence curve | Page 2: Cybersecurity |
| `fig10_confusion_matrices` | 7. Experimental Results | 2584×1260 / 300 | Test confusion matrices on 5 cyber datasets | 5-subplot static heatmap | Interactive dynamic confusion matrix per model/dataset | Page 2: Cybersecurity |
| `fig11_roc_curves` | 7. Experimental Results | 2128×1351 / 300 | ROC curves across models & datasets | Static ROC curves | Interactive Plotly ROC curves with AUC hover | Page 2: Cybersecurity |
| `fig12_pr_curves` | 7. Experimental Results | 2148×1351 / 300 | Precision-Recall curves | Static PR curves | Interactive Plotly PR curves with AP hover | Page 2: Cybersecurity |
| `fig13_fpr_fnr_comparison` | 8. Performance Comparison | 2718×1436 / 300 | FPR vs FNR scatter/bar tradeoff | Static multi-panel plot | Interactive FPR/FNR trade-off comparison | Page 2: Cybersecurity |
| `fig14_threshold_optimization` | 7. Experimental Results | 2764×1378 / 300 | Validation threshold calibration ($\tau^*$) | Static dual-axis curve | Interactive threshold sensitivity slider & curve | Page 2: Cybersecurity |
| `fig15_quantum_circuit_diagram` | 2. Quantum Circuit | 2289×1049 / 300 | PennyLane 4-Qubit VQC with Ring CNOT | Light theme layout | Refined dark-theme vector circuit (`fig15_quantum_circuit_refined.png`) | Page 3: Quantum Intelligence |
| `fig16_qubit_comparison` | 8. Performance Comparison | 2168×1220 / 300 | 4 vs 6 vs 8 Qubit Macro-F1 & Latency | Static comparison | Interactive Plotly dual-axis comparison | Page 3: Quantum Intelligence |
| `fig17_quantum_noise_sensitivity`| 7. Experimental Results | 1957×1166 / 300 | Depolarizing noise probability ($p=0.0 \dots 0.1$) | Static decay curve | Interactive Plotly noise degradation curve | Page 3: Quantum Intelligence |
| `fig18_quantum_ablation` | 8. Performance Comparison | 2547×1512 / 300 | Standalone VQC vs No-Quantum vs Hybrid | Static grouped bar | Interactive ablation comparison with delta KPI cards | Page 3: Quantum Intelligence |
| `fig19_cross_dataset_generalization` | 8. Performance Comparison | 2067×1283 / 300 | Train on dataset A, test on dataset B | 5×5 transfer heatmap | Interactive Plotly heatmap with zero-shot transfer | Page 8: Benchmark Lab |
| `fig20_ecg_signal_plots` | 6. Signal Processing | 2046×1050 / 300 | ECG Lead II (125 Hz) filtered waveform | Static 3-panel wave | Interactive 125 Hz dynamic test window explorer | Page 4: Biomedical |
| `fig21_ppg_signal_plots` | 6. Signal Processing | 2046×1050 / 300 | PPG pulse oximeter waveform | Static 3-panel wave | Synchronized multi-channel waveform viewer | Page 4: Biomedical |
| `fig22_respiration_plots` | 6. Signal Processing | 2046×1050 / 300 | Thoracic impedance respiration wave | Static 3-panel wave | Synchronized multi-channel waveform viewer | Page 4: Biomedical |
| `fig23_biomedical_classification_results` | 4. Biomedical Architecture | 1959×1217 / 300 | AF vs Non-AF sensitivity & specificity | Static bar & ROC | Interactive AF classification metrics & confusion | Page 4: Biomedical |
| `fig24_blockchain_latency` | 5. Blockchain Security | 2310×1166 / 300 | Block commitment latency (ms) | Box plot | Interactive latency distribution chart | Page 6: Blockchain Security |
| `fig25_blockchain_throughput` | 5. Blockchain Security | 1895×1166 / 300 | Transaction throughput (TPS) vs Batch | Line chart | Interactive throughput curve with latency SLA | Page 6: Blockchain Security |
| `fig26_inference_latency` | 8. Performance Comparison | 2622×1441 / 300 | Per-sample inference latency across models | Multi-model box plot | Interactive latency SLA viewer (< 10 ms mark) | Page 1 & 8: Overview/Lab |
| `fig27_memory_cpu_consumption` | 8. Performance Comparison | 1956×1202 / 300 | RAM & CPU utilization during inference | Grouped bar chart | Interactive resource utilization gauge | Page 1 & 8: Overview/Lab |
