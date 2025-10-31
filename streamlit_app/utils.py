# utils.py - Helper functions for Streamlit demo / Streamlit 輔助工具
# -------------------------------------------------------------------
# EN: Utility helpers for class names, colors, etc.
# ZH: 提供類別名稱載入、顏色生成等輔助功能。

from typing import List, Optional
import hashlib


def load_class_names(path: Optional[str]) -> List[str]:
    """
    EN: Load class names from a text file, one per line. If path is None or
        file missing, fall back to common vehicle classes.
    ZH: 從文字檔載入類別名稱（每行一個）。若 path 為 None 或檔案不存在，
        則回退到常見車輛類別清單。
    """
    default = ["person", "bicycle", "car", "motorbike", "bus", "truck"]
    if path is None or str(path).strip() == "":
        return default
    try:
        names = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                if name:
                    names.append(name)
        return names if names else default
    except Exception:
        return default


def get_color_for_id(idx: int) -> tuple:
    """
    EN: Generate a deterministic BGR color for given class id.
    ZH: 根據類別 id 生成可重現的 BGR 顏色。
    """
    # Use a quick hash to get stable color
    h = hashlib.md5(str(idx).encode()).hexdigest()
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    return (b, g, r)
