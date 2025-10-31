# API Specifications | API 介面規格

This document defines the Streamlit app and Python module APIs for training, evaluation, and inference. 本文件定義 Streamlit 應用與 Python 模組在訓練/評估/推論之 API。

---

1. Python Module APIs | Python 模組介面
- Module: src/api/train.py
  - train_yolo(model, data_yaml, epochs=100, imgsz=640, batch=16, device="auto", seed=42, optimizer="AdamW", lr0=0.01, lrf=0.01, cos_lr=True, workers=8) -> dict
  - 說明：訓練指定 YOLO 模型。回傳 metrics 字典（mAP、loss 等）。
  - Args：
    - model: str | Path — 權重或模型名（例："yolov8n.pt"）
    - data_yaml: str | Path — 資料集設定檔（含 nc 與 names）
    - epochs: int — 訓練輪數
    - imgsz: int — 輸入尺寸
    - batch: int — 批次
    - device: str — "auto" | "cpu" | "cuda:0"
    - seed: int — 隨機種子
    - optimizer: str — 優化器（SGD/NAdam/AdamW）
    - lr0: float — 初始學習率
    - lrf: float — 最終學習率比例
    - cos_lr: bool — 是否使用 cosine
    - workers: int — dataloader 執行緒數
  - Returns：dict — 指標與權重路徑

- Module: src/api/predict.py
  - predict_yolo(weights, source, conf=0.25, iou=0.45, imgsz=640, device="auto", save=True, project="runs/detect", name="exp", stream=False) -> list
  - 說明：進行影像或資料夾/串流之偵測。回傳每張圖片之偵測結果清單。
  - Args：weights: 權重路徑；source: 來源（檔案/資料夾/URL/RTSP/0）... 其餘同名參數同 Ultralytics。
  - Returns：list — 每張輸出之路徑與偵測陣列

- Module: src/api/eval.py
  - evaluate(weights, data_yaml, imgsz=640, batch=16, device="auto") -> dict
  - 說明：對驗證集計算 mAP 與各指標。

2. Streamlit App APIs | Streamlit 前端互動
- Pages:
  - Home: 專案說明與資料上傳
  - Train: 選擇模型/資料，開始訓練，顯示即時曲線
  - Predict: 上傳圖片/影片，顯示偵測結果與匯出
  - Metrics: 顯示混淆矩陣、PR 曲線、mAP
- Widgets/Params | 控制項參數：
  - model_name: selectbox [yolov8n, yolov8s, yolov11s, ...]
  - data_yaml: file_uploader or text_input
  - epochs/imgsz/batch/device/optimizer/lr/conf/iou 等
  - Callbacks: on_train_start/on_epoch_end/on_train_end

3. REST-like Local Endpoints (optional) | 本機端點（可選）
- If FastAPI enabled at src/api/server.py:
  - POST /train — body: {model, data_yaml, epochs, imgsz, ...} -> {run_id, metrics}
  - POST /predict — body: {weights, source, conf, iou, imgsz} -> {outputs}
  - GET /metrics/{run_id} — 取得訓練結果
  - 中英參數與錯誤碼請對照 Ultralytics 預設

4. Error Handling | 錯誤處理
- Validate file paths, class counts (nc) matching names length
- 檢查路徑與 nc 與 names 長度一致
- Try/except around model.load/validate to return user-friendly messages
- 於載入/驗證周圍加上例外處理，回傳易懂錯誤

5. I/O Schemas | 輸入輸出結構
- Train return: {metrics: {...}, weights: "runs/train/exp/weights/best.pt"}
- 推論回傳：[{image: path, boxes: [[x1,y1,x2,y2,conf,cls], ...]}]

6. Example Usage | 使用範例
- Python:
  - from src.api.train import train_yolo
  - metrics = train_yolo("yolov8n.pt", "data/dataset.yaml", epochs=100)
- CLI (Ultralytics):
  - yolo detect train model=yolov8n.pt data=data/dataset.yaml imgsz=640 epochs=100
