# Streamlit YOLO Vehicle Detection / 車輛偵測動態展示

This Streamlit app provides a minimal, interactive demo for vehicle detection using YOLOv8/YOLOv11. 上述應用提供最基本的互動式車輛偵測：影片上傳、YOLO 偵測、顯示標註。

## Quick Start / 快速開始

Prerequisites / 先決條件
- Python 3.9–3.11
- macOS/Linux/Windows supported

Install / 安裝
```
cd streamlit_app
pip install -r requirements.txt
```

Run / 啟動
```
streamlit run app.py
```
Then open the printed local URL in your browser. 開啟終端機輸出之本機網址。

## Usage / 使用方式
1) Upload a video file (mp4/mov/avi/mkv)
2) Select a YOLO model (yolov8n/s or yolov11n/s)
3) Optionally provide a custom classes file (one class per line)
4) Click “Run Detection” to see annotated frames streamed

1) 上傳影片檔
2) 選擇 YOLO 模型
3) 可選：提供自定義類別檔（每行一個類別）
4) 點「Run Detection」開始推論並即時顯示標註

## Custom Classes / 自定義類別
- Prepare a UTF-8 text file with one class name per line. 以 UTF-8 編碼，每行一個類別名稱。
- In the sidebar, paste the file path into “Custom classes file”. 在側邊欄輸入該檔路徑。
- If omitted, defaults to common classes: person, bicycle, car, motorbike, bus, truck.

## Models / 模型
- The app loads small pre-trained checkpoints by default: yolov8n/s or yolov11n/s.
- For speed on CPU, prefer n models. Use GPU if available for better FPS.

## File Overview / 專案檔案說明
- app.py: Streamlit UI, video upload, YOLO inference, drawing boxes. 介面、上傳、推論與標註顯示。
- utils.py: Helpers for class names and colors. 類別載入與顏色工具。
- requirements.txt: Dependencies 相依套件清單。

## Notes / 注意事項
- This is a minimal template. For production, consider batching frames, async I/O, and caching the model.
- 若要改為僅偵測特定類別，可在推論後依 cls_id 過濾，或載入僅含該類別的模型權重。

## Troubleshooting / 疑難排解
- ImportError ultralytics: ensure ultralytics is installed from requirements.txt.
- No GPU: the demo runs on CPU; performance may be lower.
- OpenCV cannot open video: make sure the file format/codec is supported by your OS build of OpenCV.
