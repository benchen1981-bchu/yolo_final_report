# Detection Specifications | 偵測規格說明

This document details detection pipeline design: pre/post-process, thresholds, and evaluation. 本文件說明偵測流程的前後處理、門檻與評估方式。

---

1. Preprocessing | 前處理
- Resize: letterbox to imgsz (default 640) preserving aspect
- 調整尺寸：信封填充至 imgsz（預設 640），保留長寬比
- Padding color: 114 (gray) unless configured
- 內補顏色：114（灰）除非另設
- BGR→RGB and uint8→float with normalization if required
- BGR→RGB 與 uint8→float 正規化（若需）

2. Inference | 推論
- Device: cuda:0 if available else cpu
- 裝置：優先使用 cuda:0，否則使用 cpu
- Precision: fp16 on CUDA supported GPUs
- 精度：CUDA GPU 支援時使用 fp16
- Tiling (optional): for very large images, overlap=0.2
- 切片（可選）：超大圖採用，重疊 0.2

3. Postprocessing | 後處理
- Sigmoid/activation handled by model head (Ultralytics)
- 激活：由模型頭內部處理（Ultralytics）
- NMS: torchvision or Ultralytics NMS with configurable params
- 非極大抑制：可用 torchvision 或 Ultralytics NMS 並可設定
- Parameters | 參數：
  - conf_thres: 0.25 (range 0.1–0.5)
  - 置信門檻：0.25（範圍 0.1–0.5）
  - iou_thres: 0.45 (range 0.3–0.7)
  - IoU 門檻：0.45（範圍 0.3–0.7）
  - max_det: 300
  - 最大預測數：300
  - agnostic: false (class-aware NMS)
  - 類別無關：false（類別相關 NMS）
  - multi_label: true if overlaps by class are desired
  - 多標籤：若需分別輸出各類別重疊則 true

4. Output Schema | 輸出格式
- Each detection: [x1, y1, x2, y2, conf, cls_id]
- 每筆偵測：左上右下座標 + 置信 + 類別 ID
- Class mapping from dataset.yaml names
- 類別對應自 dataset.yaml 之 names

5. Evaluation Metrics | 評估指標
- mAP@0.5, mAP@0.5:0.95, Precision, Recall, F1
- mAP@0.5、mAP@0.5:0.95、精確率、召回率、F1
- Per-class metrics and confusion matrix
- 逐類別指標與混淆矩陣
- PR curve, P-R AUC
- PR 曲線與面積

6. Threshold Tuning | 門檻調校
- Sweep conf_thres in [0.1, 0.9], choose F1-max
- 掃描置信門檻於 [0.1, 0.9]，選擇 F1 最大
- Adjust iou_thres to balance duplicate suppression vs. recall
- 調整 IoU 門檻以平衡重複抑制與召回

7. Batch/Stream Inference | 批次/串流
- Batch: dataloader over images folder
- 批次：以資料夾建立 dataloader
- Stream: webcam/RTSP with buffer size and async decode
- 串流：網路攝影機/RTSP，設定緩衝與非同步解碼

8. Visualization | 視覺化
- Draw boxes, labels, confidences; color by cls_id
- 繪製框、標籤、置信；依類別上色
- Save: per-image annotated outputs under runs/detect/exp*
- 輸出：儲存於 runs/detect/exp* 目錄

9. Failure Modes | 失效情境
- Overlapping small objects missed: lower conf_thres or use higher-res
- 小物件重疊遺漏：降低置信或提高解析度
- Many duplicates: raise iou_thres or enable class-agnostic
- 太多重複：提高 IoU 門檻或啟用類別無關 NMS

10. Reproducible CLI | 可重現指令
- yolo detect predict model=weights.pt source=images/ conf=0.25 iou=0.45 imgsz=640
- 命令：yolo detect predict model=weights.pt source=images/ conf=0.25 iou=0.45 imgsz=640
