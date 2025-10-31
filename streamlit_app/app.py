# app.py - Streamlit Vehicle Detection Demo / 車輛偵測示範
# -----------------------------------------------------------
# EN: This is a minimal Streamlit app template for vehicle detection.
#     It supports: (1) video upload, (2) run YOLO detection, (3) show annotated video frames.
# ZH: 這是一個最基本的 Streamlit 車輛偵測範例樣板，
#     支援：(1) 影片上傳、(2) 執行 YOLO 偵測、(3) 顯示標註後影格。
#     程式內含中英雙語註解，指引每一步的邏輯。

import os
import tempfile
from typing import List, Optional

import streamlit as st
import cv2
import numpy as np

# Try to import ultralytics if available; otherwise show guidance.
# 嘗試匯入 ultralytics；若未安裝則提供提示訊息。
try:
    from ultralytics import YOLO  # YOLOv8/YOLOv11 unified API
    _ULTRALYTICS_OK = True
except Exception as e:
    YOLO = None
    _ULTRALYTICS_OK = False

# Local utilities for label mapping, color picking, etc.
# 本地工具函式：標籤對應、顏色生成等（會在 utils.py 中實作）。
try:
    from utils import load_class_names, get_color_for_id
except Exception:
    # Fallback stubs if utils.py is not present yet.
    def load_class_names(path: Optional[str]) -> List[str]:
        # EN: When no custom class file is provided, default to common vehicle classes
        # ZH: 若沒有提供自定義類別檔，使用常見車種作為預設
        return ["person", "bicycle", "car", "motorbike", "bus", "truck"]

    def get_color_for_id(idx: int) -> tuple:
        # EN: Deterministic color for class id
        # ZH: 依類別 id 產生固定顏色
        np.random.seed(idx)
        color = np.random.randint(0, 255, size=3).tolist()
        return int(color[0]), int(color[1]), int(color[2])


# EN: Sidebar configuration / ZH: 側邊欄設定
st.sidebar.title("Vehicle Detection / 車輛偵測")
st.sidebar.markdown(
    """
    - Upload a video then run YOLO detection
    - 上傳影片後執行 YOLO 偵測並顯示標註
    """
)

# EN: Model selection and class customization
# ZH: 模型選擇與自定義類別
model_name = st.sidebar.selectbox(
    "Model (YOLOv8/YOLOv11)",
    options=["yolov8n.pt", "yolov8s.pt", "yolov11n.pt", "yolov11s.pt"],
    index=0,
    help="Select a small model for quick demo / 選擇較小模型以便快速示範",
)

custom_classes_path = st.sidebar.text_input(
    "Custom classes file (optional) / 自定義類別檔(選填)",
    value="",
    help="Text file with one class name per line / 文字檔每行一個類別名稱",
)

conf_thres = st.sidebar.slider("Confidence / 置信度", 0.1, 0.9, 0.25, 0.05)
iou_thres = st.sidebar.slider("IOU Threshold / IOU 閾值", 0.1, 0.9, 0.45, 0.05)

st.title("Streamlit Vehicle Detection Template / 車輛偵測樣板")
st.write(
    "EN: Upload a video and click 'Run Detection' to see annotated results.\n"
    "ZH: 上傳影片並點選「Run Detection」以查看標註結果。"
)

# EN: File uploader for video
# ZH: 影片上傳元件
uploaded = st.file_uploader(
    "Upload video / 上傳影片", type=["mp4", "mov", "avi", "mkv"]
)

run_clicked = st.button("Run Detection / 執行偵測", type="primary")

# EN: Lazy-load model when needed
# ZH: 僅在需要時才載入模型
_model = None


def get_model(name: str):
    """Load YOLO model by name. 依名稱載入 YOLO 模型。"""
    global _model
    if _model is not None:
        return _model
    if not _ULTRALYTICS_OK:
        st.warning(
            "ultralytics is not installed. Please add 'ultralytics' to requirements.txt"
        )
        return None
    try:
        _model = YOLO(name)
        return _model
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None


def annotate_frame(frame: np.ndarray, boxes, class_names: List[str]):
    """
    EN: Draw bounding boxes and labels onto frame.
    ZH: 在影格上繪製邊界框與標籤文字。
    """
    if boxes is None or len(boxes) == 0:
        return frame

    for b in boxes:
        # Each box has xyxy, conf, cls
        # 每個框包含：xyxy 座標、置信度、類別 id
        x1, y1, x2, y2 = map(int, b.xyxy[0].tolist())
        conf = float(b.conf[0].item()) if hasattr(b.conf, "__len__") else float(b.conf)
        cls_id = int(b.cls[0].item()) if hasattr(b.cls, "__len__") else int(b.cls)

        label = class_names[cls_id] if 0 <= cls_id < len(class_names) else str(cls_id)
        color = get_color_for_id(cls_id)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        text = f"{label} {conf:.2f}"
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame, (x1, y1 - th - 6), (x1 + tw + 4, y1), color, -1)
        cv2.putText(
            frame,
            text,
            (x1 + 2, y1 - 4),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
    return frame


if run_clicked:
    if uploaded is None:
        st.info("Please upload a video first / 請先上傳影片")
        st.stop()

    # EN: Persist uploaded file to a temp file so OpenCV can read it
    # ZH: 將上傳的緩衝寫入暫存檔，方便 OpenCV 讀取
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded.name)[1]) as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name

    st.video(tmp_path)

    # EN: Load class names from custom file or fallback
    # ZH: 嘗試載入自定義類別，或使用預設類別
    class_names = load_class_names(custom_classes_path if custom_classes_path else None)

    # EN: Load model lazily
    # ZH: 延遲載入模型
    model = get_model(model_name)
    if model is None:
        st.stop()

    # EN: Open the video and iterate frames
    # ZH: 開啟影片並逐幀處理
    cap = cv2.VideoCapture(tmp_path)
    if not cap.isOpened():
        st.error("Cannot open video / 無法開啟影片")
        st.stop()

    # EN: Prepare a placeholder to stream annotated frames
    # ZH: 準備一個 placeholder 用於連續顯示標註影格
    placeholder = st.empty()

    frame_count = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame_count += 1

        # EN: Run inference. We pass a single frame array to model()
        # ZH: 執行推論，將單張影格傳入 model()
        try:
            results = model.predict(
                source=frame,
                conf=conf_thres,
                iou=iou_thres,
                verbose=False,
                imgsz=640,
            )
        except Exception as e:
            st.error(f"Inference failed at frame {frame_count}: {e}")
            break

        # EN: Extract boxes and draw
        # ZH: 取得偵測框並繪製
        boxes = []
        if results and len(results) > 0:
            r0 = results[0]
            if hasattr(r0, "boxes") and r0.boxes is not None:
                boxes = r0.boxes

        annotated = annotate_frame(frame.copy(), boxes, class_names)

        # EN: Show the annotated frame
        # ZH: 顯示標註影格
        placeholder.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), caption=f"Frame {frame_count}", use_column_width=True)

    cap.release()
    # EN: Clean temp file
    # ZH: 清理暫存檔案
    try:
        os.remove(tmp_path)
    except Exception:
        pass

    st.success("Done. End of video. / 完成，影片播放結束。")
