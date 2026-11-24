"""
dashboard/utils/formatters.py
Scientific and UI formatting utilities for DQH-BAN research metrics.
"""

from typing import Union, Optional

def fmt_pct(val: Union[float, int, None], decimals: int = 2) -> str:
    if val is None or val == "" or str(val).lower() == "nan":
        return "N/A"
    try:
        fval = float(val)
        if fval <= 1.0 and fval > 0.0:
            fval = fval * 100.0
        return f"{fval:.{decimals}f}%"
    except Exception:
        return str(val)

def fmt_float(val: Union[float, int, None], decimals: int = 4) -> str:
    if val is None or val == "" or str(val).lower() == "nan":
        return "N/A"
    try:
        return f"{float(val):.{decimals}f}"
    except Exception:
        return str(val)

def fmt_ms(val: Union[float, int, None], decimals: int = 2) -> str:
    if val is None or val == "" or str(val).lower() == "nan":
        return "N/A"
    try:
        return f"{float(val):.{decimals}f} ms"
    except Exception:
        return str(val)

def fmt_hash(h_str: Optional[str], length: int = 12) -> str:
    if not h_str:
        return "0" * length
    s = str(h_str)
    if len(s) <= length:
        return s
    return f"{s[:length // 2]}...{s[-length // 2:]}"

def get_status_color(val: Union[float, str], metric_type: str = "accuracy") -> str:
    try:
        fval = float(val)
        if metric_type in ["accuracy", "precision", "recall", "macro_f1", "roc_auc"]:
            if fval >= 0.95: return "success"
            if fval >= 0.90: return "quantum"
            return "warning"
        elif metric_type in ["fpr", "fnr"]:
            if fval <= 0.02: return "success"
            if fval <= 0.05: return "warning"
            return "critical"
    except Exception:
        pass
    return "primary"
