# Custom Class and Annotation Specifications | 自訂類別與標註規範

This document defines our dataset classes and labeling protocol to ensure consistency. 本文件定義本專案的資料集類別與標註流程，確保一致性。

---

1. Dataset Scope | 資料集範圍
- Domain: [Fill your domain, e.g., traffic signs, PCB defects]
- 領域：請填寫，例如交通號誌、PCB 瑕疵
- Environments: indoor/outdoor, day/night, weather variations
- 環境：室內/室外、晝/夜、天氣變化

2. Class List | 類別清單
- Example template | 範例樣板：
  - 0: person 人
  - 1: bicycle 腳踏車
  - 2: car 汽車
  - ...
- Ensure single, mutually exclusive primary label per object
- 每個物件應有單一且互斥的主要類別

3. Annotation Format | 標註格式
- YOLO txt per image, one object per line: cls cx cy w h (normalized 0–1)
- 每張圖一個 txt，逐行：類別 中心x 中心y 寬 高（0–1 正規化）
- Coordinate system uses pixel-to-normalized conversion based on image width/height
- 座標以影像寬高換算為 0–1

4. Bounding Box Rules | 邊框繪製規則
- Tight box around visible object; include entire object if partially occluded
- 框要緊貼可見區；遮擋時包含可推測之整體
- Exclude ambiguous shadows/reflections unless task-specific
- 除非任務特定，排除陰影/反射
- Minimum size: keep boxes with area ≥ 16x16 pixels (or project-defined)
- 最小尺寸：面積≥16x16像素（或依專案訂定）

5. Occlusion/Truncation | 遮擋/截斷
- If >50% occluded: still annotate if category recognizable
- 遮擋超過 50%：若仍可辨識，仍標註
- Truncated at image border: box can extend to edge but stay within image
- 影像邊界截斷：框可貼邊但不得超出圖外

6. Crowds and Overlaps | 群眾與重疊
- Overlapping same-class instances must receive separate boxes
- 相同類型重疊需各自標框
- Severe crowd regions may be tagged with group flag if tool supports
- 密集群眾可用群組旗標（若工具支援）

7. Difficult/Ignore Regions | 困難/忽略區
- Use ignore flag for tiny/blurred objects unlikely to train well
- 對極小/模糊物件以忽略標註，不納入訓練
- Keep a separate list of ignored instances for audit
- 保留忽略清單以供稽核

8. Quality Control | 品質控管
- Double annotation on 10% sample; resolve conflicts by senior reviewer
- 對 10% 抽樣雙人標註，由資深審核者裁決
- Inter-annotator agreement target: kappa ≥ 0.8
- 標註者一致性目標：Kappa ≥ 0.8

9. File/Folder Structure | 檔案/資料夾結構
- dataset/
  - images/{train,val,test}
  - labels/{train,val,test}
  - dataset.yaml (nc, names)
- 檔案結構同上，並保持檔名對應

10. Versioning & Changelog | 版本與變更
- Keep dataset version in dataset.yaml: version: v1.0
- 在 dataset.yaml 紀錄版本：version: v1.0
- Maintain CHANGELOG.md for classes/criteria updates
- 以 CHANGELOG.md 紀錄類別/規則更新

11. Labeling Tools | 標註工具
- Recommended: Label Studio, Roboflow, CVAT with YOLO export
- 推薦工具：Label Studio、Roboflow、CVAT（支援 YOLO 匯出）
- Validation: auto-check for bbox within image and class id range
- 驗證：自動檢查框在圖內與類別 ID 合法

12. Data Split Policy | 資料切分
- Split by instance or scene to avoid leakage: 70/20/10 train/val/test
- 以個體或場景切分避免洩漏：訓練/驗證/測試 70/20/10
- Keep class distribution balanced across splits
- 各切分類別比例需均衡

13. Ethics & Privacy | 倫理與隱私
- Blur personally identifiable info where applicable
- 視需求打碼個資資訊
- Respect licensing and obtain consents
- 遵守授權並取得同意

Appendix A. Template dataset.yaml | 範例
- path: data/
- train: images/train
- val: images/val
- test: images/test
- nc: K
- names: [class0, class1, ...]
- version: v1.0
