# Model Specifications | 模型規格說明

This document specifies the model design for YOLOv8/YOLOv11 variants used in this project. 本文件說明本專案所使用之 YOLOv8/YOLOv11 模型設計。

---

1. Model Family | 模型家族
- Options: YOLOv8n/s/m/l/x, YOLOv11n/s/m/l/x
- 選項：YOLOv8n/s/m/l/x、YOLOv11n/s/m/l/x
- Rationale: balance of speed/accuracy for edge vs. server. 理由：在邊緣與伺服器環境間平衡速度/準確度。

2. Input Specification | 輸入規格
- Input size: square letterboxed to 640 (train/test configurable: 416–1280)
- 輸入尺寸：方形信封填充至 640（可設定 416–1280）
- Color space: RGB uint8 [0–255] or float32 [0–1]
- 色彩空間：RGB uint8 [0–255] 或 float32 [0–1]
- Normalization: optional / Ultralytics default preprocessing
- 正規化：可選 / Ultralytics 內建前處理
- Augmentations (train): Mosaic, HSV, random flip/scale/rotate, MixUp (configurable)
- 訓練增強：Mosaic、HSV、隨機翻轉/縮放/旋轉、MixUp（可設定）

3. Output Specification | 輸出規格
- Detection heads: (B, N, (x, y, w, h, obj, C...)) where C = num_classes
- 偵測頭輸出：(批次, 預測數, (x, y, w, h, 物件性, 類別分數...))，類別數=C
- Coordinates: xywh in pixels relative to input, or normalized 0–1 (config)
- 座標：xywh 以像素或 0–1 正規化（依設定）
- NMS: class-agnostic or class-aware; IoU/score thresholds configurable
- 非極大抑制：可選類別無關或有關；IoU/分數門檻可設定

4. Backbone/Neck/Head | 主幹/頸部/頭部
- Backbone: CSP-like with C2f blocks (YOLOv8) or updated blocks (YOLOv11)
- 主幹：CSP 類與 C2f 區塊（YOLOv8）或 YOLOv11 更新結構
- Neck: PAN/FPN for multi-scale features
- 頸部：PAN/FPN 多尺度特徵融合
- Head: decoupled classification/regression with anchor-free pred
- 頭部：解耦分類/回歸，採無錨點預測

5. Loss Functions | 損失函數
- Box: CIoU/DIoU/GIoU (default: CIoU)
- 邊框：CIoU/DIoU/GIoU（預設 CIoU）
- Obj: BCE with logits
- 物件性：帶 logits 的 BCE
- Cls: BCE focal optional; label smoothing optional
- 類別：可選 Focal BCE；可選標籤平滑

6. Training Hyperparameters | 訓練超參數
- Epochs: 100–300 (default 100)
- 訓練輪數：100–300（預設 100）
- Batch size: 8–64 depending on GPU
- 批次大小：8–64 依 GPU 而定
- Optimizer: SGD/NAdam/AdamW (default: AdamW)
- 最佳化器：SGD/NAdam/AdamW（預設 AdamW）
- LR schedule: cosine or one-cycle; warmup 3–10 epochs
- 學習率排程：cosine 或 one-cycle；暖身 3–10 輪
- EMA: enabled for stable validation
- EMA：啟用以穩定驗證結果

7. Inference Settings | 推論設定
- Conf threshold: 0.25 (0.1–0.5 as task demands)
- 置信門檻：0.25（依任務 0.1–0.5）
- IoU threshold (NMS): 0.45 (0.3–0.7)
- IoU 門檻（NMS）：0.45（0.3–0.7）
- Max detections per image: 300
- 單圖最大偵測數：300
- Half precision: fp16 if device supports
- 半精度：若裝置支援則用 fp16

8. Model I/O Contracts | 模型 I/O 契約
- Input tensor shape: (B, 3, H, W) H=W in {416..1280}
- 輸入張量形狀：(批次, 3, 高, 寬)，H=W ∈ {416..1280}
- Output format (Ultralytics): List[Detections] or torch.Tensor
- 輸出格式（Ultralytics）：Detections 清單或 torch.Tensor
- Postprocess: scale coords back to original image size
- 後處理：將座標縮放回原圖尺寸

9. Checkpointing & Export | 權重與匯出
- Weights: .pt from Ultralytics trainer
- 權重：Ultralytics 訓練器輸出 .pt
- Export: onnx, torchscript, openvino, tflite (as needed)
- 匯出：onnx、torchscript、openvino、tflite（視需求）

10. Performance Targets | 效能目標
- mAP50: ≥ target set per dataset split
- mAP50：各資料集切分設定目標
- FPS: ≥ 30 on target device for n/s models
- FPS：在目標裝置 n/s 模型達 30 以上

11. Reproducibility | 可重現性
- Seed control, deterministic dataloader optional
- 隨機種子控制，資料載入可設為可重現
- Log: metrics.json, tensorboard/CSV, model.yaml snapshot
- 紀錄：metrics.json、tensorboard/CSV、model.yaml 快照

12. Safety & Bias Notes | 安全與偏誤
- Document dataset coverage; monitor false positives/negatives by class
- 紀錄資料覆蓋度；按類別監控誤檢/漏檢
- Add fail-safe thresholds for critical applications
- 關鍵應用加入失敗保護門檻

13. Versioning | 版本
- Model tag examples: yv8n_v1.0_dataA, yv11s_v1.1_augX
- 模型標籤範例：yv8n_v1.0_dataA、yv11s_v1.1_augX

Appendix A. Minimal Config | 最小設定範例
- model: yolov8n.pt | epochs: 100 | imgsz: 640 | batch: 16
- dataset.yaml: path/to/data, nc: K, names: [...]
- 推薦入門：yolov8n.pt、100 輪、640、批次 16、依據 dataset.yaml 設定 nc 與 names
