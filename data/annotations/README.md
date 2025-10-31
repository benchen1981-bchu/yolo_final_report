# YOLO Annotation Format Examples
# YOLO 標註格式範例

## Overview / 概述

This directory contains custom annotation examples for YOLO object detection.
本目錄包含 YOLO 物件偵測的自訂標註範例。

## Class Definitions / 類別定義

See `classes.txt` for the class mapping:
參見 `classes.txt` 查看類別對應：

- 0: car (汽車)
- 1: motorcycle (摩托車)
- 2: pedestrian (行人)

## Annotation Format / 標註格式

YOLO format: `<class_id> <x_center> <y_center> <width> <height>`

All coordinates are normalized (0-1 range):
所有座標都已正規化（0-1 範圍）：

- `x_center`: Center X coordinate / 中心 X 座標
- `y_center`: Center Y coordinate / 中心 Y 座標
- `width`: Bounding box width / 邊界框寬度
- `height`: Bounding box height / 邊界框高度

## Example / 範例

`sample_001.txt` contains three objects:
`sample_001.txt` 包含三個物件：

```
0 0.45 0.35 0.15 0.25  # car
1 0.62 0.48 0.08 0.12  # motorcycle
2 0.78 0.52 0.05 0.18  # pedestrian
```
