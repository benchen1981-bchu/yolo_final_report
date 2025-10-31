#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO Training Script with CRISP-DM Methodology
YOLO 訓練腳本：CRISP-DM 方法論

This script implements the complete YOLO training pipeline following CRISP-DM methodology.
本腳本實現完整的 YOLO 訓練流程，遵循 CRISP-DM 方法論。

Author: Ben Chen
Date: 2025-10-31
Version: 1.0
"""

import os
import sys
from pathlib import Path
import argparse
import yaml
import json
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime

# Data processing / 數據處理
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import cv2

# Deep Learning / 深度學習
import torch
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

# Configure logging / 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class YOLOTrainer:
    """
    YOLO Trainer class implementing CRISP-DM methodology
    YOLO 訓練器類別，實現 CRISP-DM 方法論
    
    English: This class handles the complete training pipeline from data preparation
    to model deployment, following the CRISP-DM (Cross-Industry Standard Process for 
    Data Mining) methodology.
    
    中文：此類別處理從數據準備到模型部署的完整訓練流程，遵循 CRISP-DM
    （跨行業數據挖掘標準流程）方法論。
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize YOLO Trainer / 初始化 YOLO 訓練器
        
        Args:
            config_path (str): Path to configuration file / 配置文件路徑
        """
        self.config = self._load_config(config_path)
        self.project_root = Path(self.config.get('project_root', '.'))
        self.data_dir = self.project_root / 'data'
        self.models_dir = self.project_root / 'models'
        self.results_dir = self.project_root / 'results'
        
        # Create directories / 創建目錄
        for dir_path in [self.data_dir, self.models_dir, self.results_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.model = None
        self.results = None
        
        logger.info("YOLOTrainer initialized successfully / YOLO訓練器初始化成功")
    
    def _load_config(self, config_path: str) -> Dict:
        """
        Load configuration from file / 從文件加載配置
        
        Args:
            config_path (str): Path to config file / 配置文件路徑
            
        Returns:
            Dict: Configuration dictionary / 配置字典
        """
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    return yaml.safe_load(f)
                elif config_path.endswith('.json'):
                    return json.load(f)
        
        # Default configuration / 默認配置
        return {
            'project_root': '.',
            'model_version': 'yolov8n.pt',  # Options: yolov8n/s/m/l/x, yolov11n/s/m/l/x
            'img_size': 640,
            'batch_size': 16,
            'epochs': 100,
            'device': 'cuda' if torch.cuda.is_available() else 'cpu',
            'workers': 8,
            'classes': ['car', 'motorcycle', 'pedestrian']
        }
    
    # ============================================================
    # CRISP-DM Phase 1: Business Understanding / 業務理解
    # ============================================================
    
    def define_objectives(self):
        """
        Define business objectives / 定義業務目標
        
        English: In this phase, we define the project objectives and requirements
        from a business perspective. For object detection, this typically involves
        identifying what objects need to be detected and why.
        
        中文：在此階段，我們從業務角度定義專案目標和需求。對於物件偵測，
        這通常涉及確定需要檢測哪些物件以及原因。
        """
        objectives = {
            'goal': 'Detect vehicles and pedestrians in traffic scenes',
            'target_classes': self.config['classes'],
            'performance_metric': 'mAP50-95',
            'deployment_target': 'Real-time inference'
        }
        
        logger.info(f"Business Objectives / 業務目標: {objectives}")
        return objectives
    
    # ============================================================
    # CRISP-DM Phase 2: Data Understanding / 數據理解  
    # ============================================================
    
    def explore_dataset(self, annotations_dir: str) -> Dict:
        """
        Explore and analyze dataset / 探索和分析數據集
        
        English: This function analyzes the dataset to understand its characteristics,
        including class distribution, image sizes, and annotation quality.
        
        中文：此函數分析數據集以了解其特徵，包括類別分佈、圖像大小和標註質量。
        
        Args:
            annotations_dir (str): Directory containing annotations / 包含標註的目錄
            
        Returns:
            Dict: Dataset statistics / 數據集統計信息
        """
        annotations_path = Path(annotations_dir)
        
        if not annotations_path.exists():
            logger.warning(f"Annotations directory not found: {annotations_dir}")
            return {}
        
        # Read class names / 讀取類別名稱
        classes_file = annotations_path / 'classes.txt'
        if classes_file.exists():
            with open(classes_file, 'r') as f:
                classes = [line.strip() for line in f.readlines()]
        else:
            classes = self.config['classes']
        
        # Analyze annotations / 分析標註
        stats = {
            'num_classes': len(classes),
            'classes': classes,
            'class_distribution': {}
        }
        
        # Count objects per class / 統計每個類別的物件數量
        for ann_file in annotations_path.glob('*.txt'):
            if ann_file.name == 'classes.txt':
                continue
            
            with open(ann_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        class_id = int(parts[0])
                        class_name = classes[class_id] if class_id < len(classes) else f'class_{class_id}'
                        stats['class_distribution'][class_name] = stats['class_distribution'].get(class_name, 0) + 1
        
        logger.info(f"Dataset Statistics / 數據集統計: {stats}")
        return stats
