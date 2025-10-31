# language: zh-CN
# Feature: Vehicle Detection 車輛檢測
# 本功能展示 YOLOv8 在車輛檢測場景中的應用
# This feature demonstrates YOLOv8 application in vehicle detection scenarios

Feature: Vehicle Detection 車輛檢測
  As a traffic monitoring system user 作為交通監控系統使用者
  I want to detect different types of vehicles in images and videos 我想在圖片和影片中檢測不同類型的車輛
  So that I can analyze traffic patterns and vehicle counts 以便分析交通模式和車輛數量

  Background: 背景
    Given the YOLOv8 model is initialized 已初始化 YOLOv8 模型
    And the model is loaded with pretrained weights 且模型已載入預訓練權重
    And the confidence threshold is set to 0.5 且信心閾值設定為 0.5

  @basic @vehicle
  Scenario: Detect cars in a single image 在單張圖片中檢測汽車
    # 基礎場景：偵測靜態圖片中的車輛
    # Basic scenario: Detect vehicles in static image
    Given I have an image file "test_images/traffic_scene.jpg" containing multiple cars
          我有一個包含多輛汽車的圖片檔案 "test_images/traffic_scene.jpg"
    When I run vehicle detection on the image 當我對該圖片執行車輛檢測
    Then the system should detect at least 3 cars 系統應該檢測到至少 3 輛汽車
    And each detection should have a bounding box 每個檢測結果應該有邊界框
    And each detection should have a confidence score above 0.5 每個檢測結果的信心分數應該高於 0.5
    And the output should be saved to "output/detected_vehicles.jpg" 輸出應該儲存到 "output/detected_vehicles.jpg"

  @multi-class @vehicle
  Scenario: Detect multiple vehicle types 檢測多種車輛類型
    # 多類別場景：區分不同類型的車輛
    # Multi-class scenario: Distinguish different vehicle types
    Given I have an image file "test_images/mixed_traffic.jpg" containing cars, trucks, and buses
          我有一個包含汽車、卡車和公車的圖片檔案 "test_images/mixed_traffic.jpg"
    When I run vehicle detection with class filtering 當我執行帶類別篩選的車輛檢測
    Then the system should detect vehicles of class "car" 系統應該檢測到類別為 "car" 的車輛
    And the system should detect vehicles of class "truck" 系統應該檢測到類別為 "truck" 的車輛
    And the system should detect vehicles of class "bus" 系統應該檢測到類別為 "bus" 的車輛
    And each class should be labeled correctly in the output 輸出中每個類別應該正確標註
    And the detection results should be returned as a JSON object 檢測結果應該以 JSON 物件形式回傳

  @performance @vehicle
  Scenario: Process high-resolution traffic image 處理高解析度交通圖片
    # 效能場景：測試模型處理大圖的能力
    # Performance scenario: Test model capability with large images
    Given I have a high-resolution image "test_images/highway_4k.jpg" of size 3840x2160 pixels
          我有一張解析度為 3840x2160 像素的高解析度圖片 "test_images/highway_4k.jpg"
    When I run vehicle detection on the high-resolution image 當我對高解析度圖片執行車輛檢測
    Then the detection should complete within 5 seconds 檢測應該在 5 秒內完成
    And the system should detect all visible vehicles 系統應該檢測到所有可見的車輛
    And the memory usage should not exceed 4GB 記憶體使用量不應超過 4GB
    And the output image should maintain the original resolution 輸出圖片應保持原始解析度

  @batch @vehicle
  Scenario: Batch process multiple traffic images 批次處理多張交通圖片
    # 批次處理場景：同時處理多個檔案
    # Batch processing scenario: Process multiple files simultaneously
    Given I have a directory "test_images/batch/" containing 10 traffic images
          我有一個包含 10 張交通圖片的目錄 "test_images/batch/"
    When I run batch vehicle detection on all images 當我對所有圖片執行批次車輛檢測
    Then all 10 images should be processed successfully 所有 10 張圖片應該成功處理
    And the results should be saved to "output/batch_results/" 結果應該儲存到 "output/batch_results/"
    And a summary JSON file should be created with detection counts 應該建立一個包含檢測數量的摘要 JSON 檔案
    And the total processing time should be logged 總處理時間應該被記錄

  @accuracy @vehicle
  Scenario: Verify detection accuracy with ground truth 用真實標註驗證檢測準確度
    # 準確度驗證場景：與人工標註比對
    # Accuracy verification scenario: Compare with manual annotations
    Given I have an image "test_images/annotated_traffic.jpg" with ground truth annotations
          我有一張帶有真實標註的圖片 "test_images/annotated_traffic.jpg"
    And the ground truth file "test_images/annotated_traffic.json" contains 5 car annotations
          真實標註檔案 "test_images/annotated_traffic.json" 包含 5 個汽車標註
    When I run vehicle detection and compare with ground truth 當我執行車輛檢測並與真實標註比較
    Then the precision should be at least 0.85 精確率應該至少為 0.85
    And the recall should be at least 0.80 召回率應該至少為 0.80
    And the mAP (mean Average Precision) should be at least 0.82 平均精確率應該至少為 0.82
    And a confusion matrix should be generated 應該生成混淆矩陣

  @edge-case @vehicle
  Scenario: Handle images with no vehicles 處理沒有車輛的圖片
    # 邊界情況：空場景測試
    # Edge case: Empty scene test
    Given I have an image file "test_images/empty_road.jpg" containing no vehicles
          我有一個不包含車輛的圖片檔案 "test_images/empty_road.jpg"
    When I run vehicle detection on the image 當我對該圖片執行車輛檢測
    Then the system should return an empty detection list 系統應該回傳空的檢測列表
    And no bounding boxes should be drawn 不應該繪製任何邊界框
    And a message "No vehicles detected" should be logged 應該記錄訊息 "No vehicles detected"
    And the output image should be identical to the input 輸出圖片應該與輸入圖片相同

  @occlusion @vehicle
  Scenario: Detect partially occluded vehicles 檢測部分遮擋的車輛
    # 遮擋場景：測試模型對部分可見車輛的檢測能力
    # Occlusion scenario: Test model capability with partially visible vehicles
    Given I have an image "test_images/occluded_vehicles.jpg" with partially hidden cars
          我有一張包含部分遮擋汽車的圖片 "test_images/occluded_vehicles.jpg"
    And some vehicles are 50% occluded by other objects 某些車輛被其他物體遮擋 50%
    When I run vehicle detection with occlusion handling 當我執行帶遮擋處理的車輛檢測
    Then the system should detect at least 70% of the occluded vehicles 系統應該檢測到至少 70% 的遮擋車輛
    And each detection should have an occlusion flag if applicable 每個檢測結果應該在適用時標記遮擋旗標
    And the confidence scores may be lower for occluded vehicles 遮擋車輛的信心分數可能較低

  @night @vehicle
  Scenario: Detect vehicles in low-light conditions 在低光照條件下檢測車輛
    # 低光照場景：夜間或昏暗環境測試
    # Low-light scenario: Night or dim environment test
    Given I have a night-time image "test_images/night_traffic.jpg" with poor lighting
          我有一張光線不足的夜間圖片 "test_images/night_traffic.jpg"
    When I run vehicle detection with brightness enhancement 當我執行帶亮度增強的車輛檢測
    Then the system should apply image preprocessing for low-light conditions 系統應該為低光照條件應用圖片預處理
    And the system should detect vehicles with headlights on 系統應該檢測開啟頭燈的車輛
    And the detection accuracy should be at least 60% 檢測準確率應該至少為 60%
    And a preprocessing log should indicate "low-light mode activated" 預處理日誌應該顯示 "low-light mode activated"

  @real-time @vehicle
  Scenario Outline: Detect vehicles at different confidence thresholds 用不同信心閾值檢測車輛
    # 參數化場景：測試不同閾值的影響
    # Parameterized scenario: Test impact of different thresholds
    Given I have an image file "test_images/parking_lot.jpg" containing 20 vehicles
          我有一個包含 20 輛車的圖片檔案 "test_images/parking_lot.jpg"
    When I run vehicle detection with confidence threshold <threshold> 當我用信心閾值 <threshold> 執行車輛檢測
    Then the system should detect at least <min_detections> vehicles 系統應該檢測到至少 <min_detections> 輛車
    And the system should detect at most <max_detections> vehicles 系統應該檢測到最多 <max_detections> 輛車
    And all detected vehicles should have confidence above <threshold> 所有檢測到的車輛信心分數應高於 <threshold>

    Examples: 範例
      | threshold | min_detections | max_detections | description 說明          |
      | 0.3       | 18             | 20             | Low threshold 低閾值      |
      | 0.5       | 15             | 18             | Medium threshold 中閾值   |
      | 0.7       | 10             | 15             | High threshold 高閾值     |
      | 0.9       | 5              | 10             | Very high threshold 極高閾值 |
