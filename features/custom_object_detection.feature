# language: zh-CN
# Feature: Custom Object Detection 自訂物件偵測
# 展示如何使用自製 dataset 與自訂類別在 YOLO 訓練與推論
# Demonstrate training/inference on custom classes with a self-made dataset in YOLO

Feature: Custom Object Detection 自訂物件偵測
  As a model developer 作為模型開發者
  I want to train and infer on a custom dataset with my own class schema 我想用自製數據集與自訂類別綱要進行訓練與推論
  So that I can detect domain-specific objects 以便偵測領域專屬物件

  Background: 背景
    Given a dataset YAML at "data/custom/data.yaml" defines classes: [helmet, vest, cone]
          已有數據集 YAML 檔於 "data/custom/data.yaml" 定義類別：[helmet, vest, cone]
    And images and labels follow YOLO format under data/custom/images, data/custom/labels
          且圖片與標註遵循 YOLO 格式，位於 data/custom/images 與 data/custom/labels
    And a pretrained YOLOv8m model checkpoint exists at "weights/yolov8m.pt"
          且存在預訓練模型檔於 "weights/yolov8m.pt"

  @schema @validation
  Scenario: Validate dataset structure 驗證數據集結構
    Given the dataset directories exist: images/train, images/val, labels/train, labels/val
          給定資料夾存在：images/train、images/val、labels/train、labels/val
    When I run the dataset validator 當我執行資料驗證器
    Then it should report zero missing image-label pairs 應報告 0 個遺失的影像-標註配對
    And all label files should only contain class ids in [0,1,2] 所有標註檔僅包含 [0,1,2] 類別索引
    And the YAML should be loadable without error YAML 應可無錯誤載入

  @train @custom
  Scenario: Train model on custom dataset 在自訂數據集上訓練模型
    Given I configure epochs=50, imgsz=640, batch=16 設定 epochs=50、imgsz=640、batch=16
    And I set project="runs/custom" and name="exp_custom" 設定 project 與 name
    When I start YOLO training 當我啟動 YOLO 訓練
    Then training should complete without error 訓練應無錯誤完成
    And best.pt and last.pt should be saved in runs/custom/exp_custom/ 應保存 best.pt 與 last.pt
    And metrics.yaml should include mAP50 and mAP50-95 指標檔包含 mAP50 與 mAP50-95

  @inference @custom
  Scenario: Run inference on sample images 對樣本圖片推論
    Given I have 5 test images in data/custom/test_images 我有 5 張測試圖片
    When I run YOLO detect on these images 當我執行 YOLO 偵測
    Then the outputs should be saved to runs/detect/custom_test 輸出應保存到 runs/detect/custom_test
    And predictions JSON should list class names helmet, vest, cone 預測 JSON 應列出類別名稱 helmet、vest、cone
    And each image should have at least one detection 每張圖至少 1 個偵測

  @confusion @evaluation
  Scenario: Evaluate confusion between similar classes 評估相似類別混淆
    Given I have a labeled validation set with helmets and vests 我有帶標註的驗證集
    When I compute the confusion matrix 當我計算混淆矩陣
    Then the off-diagonal values helmet-vs-vest should be under 0.2 交叉錯誤率應低於 0.2
    And per-class precision should exceed 0.8 每類精確率大於 0.8

  @export @deployment
  Scenario: Export trained model for deployment 匯出模型以便部署
    Given I have best.pt at runs/custom/exp_custom/best.pt 我有 best.pt
    When I export to ONNX and OpenVINO 當我匯出為 ONNX 與 OpenVINO
    Then onnx model should exist at runs/custom/exp_custom/weights/best.onnx 產生 onnx 檔
    And OpenVINO IR files should exist at runs/custom/exp_custom/weights/openvino/ 產生 IR 檔
    And a README deploy note should be generated 產生部署說明

  @robustness @aug
  Scenario Outline: Train with different augmentations 用不同增強策略訓練
    Given augmentation profile is <profile> 增強配置為 <profile>
    When I train for 10 epochs 當我訓練 10 個 epoch
    Then the validation mAP50 should be at least <map50> 驗證 mAP50 至少為 <map50>

    Examples: 範例
      | profile     | map50 |
      | light       | 0.80  |
      | medium      | 0.82  |
      | strong      | 0.85  |
