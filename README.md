# YOLO Vehicle Detection Project

Ultralytics YOLO vehicle detection project with CRISP-DM, TDD, SDD, and BDD methodologies. Includes custom object detection, training features, and Streamlit demo.

## Project Overview

This project implements a comprehensive vehicle detection system using the latest Ultralytics YOLOv8/YOLO11 framework. The project follows industry-standard software development methodologies:

- **CRISP-DM**: Cross-Industry Standard Process for Data Mining
- **TDD**: Test-Driven Development
- **SDD**: Specification-Driven Development
- **BDD**: Behavior-Driven Development

## Project Structure

The repository is organized following software development best practices:

```
yolo_final_report/
├── notebooks/          # CRISP-DM methodology - Jupyter notebooks
│   └── .gitkeep       # Business Understanding, Data Understanding,
│                      # Data Preparation, Modeling, Evaluation, Deployment
│
├── tests/             # TDD methodology - Test-Driven Development
│   └── .gitkeep       # Unit tests: test_model_loading.py, test_detection.py,
│                      # test_custom_classes.py, test_video_processing.py
│
├── specs/             # SDD methodology - Specification-Driven Development
│   └── .gitkeep       # Specifications: model_specs.md, detection_specs.md,
│                      # custom_class_specs.md, api_specs.md
│
├── features/          # BDD methodology - Behavior-Driven Development
│   └── .gitkeep       # Gherkin features: vehicle_detection.feature,
│                      # custom_object_detection.feature, video_processing.feature,
│                      # model_training.feature
│
├── streamlit_app/     # Streamlit demo application
│   └── README.md      # TODO: app.py, requirements.txt, utils/, models/, config/
│
├── src/               # Source code (to be added)
├── data/              # Datasets (to be added)
├── models/            # Trained models (to be added)
└── docs/              # Documentation and reports (to be added)
```

### Methodology Directories

#### `notebooks/` - CRISP-DM
Contains Jupyter notebooks following the CRISP-DM process:
1. Business Understanding - Define project goals
2. Data Understanding - Explore and analyze video data
3. Data Preparation - Dataset preparation and annotation
4. Modeling - YOLO model training and fine-tuning
5. Evaluation - Performance metrics and validation
6. Deployment - Production deployment strategies

#### `tests/` - TDD (Test-Driven Development)
Unit and integration tests ensuring code quality:
- Model loading and initialization tests
- Detection algorithm tests
- Custom object class tests
- Video processing pipeline tests

#### `specs/` - SDD (Specification-Driven Development)
Detailed technical specifications:
- Model architecture specifications
- Detection requirements and criteria
- Custom object class definitions
- API interface specifications

#### `features/` - BDD (Behavior-Driven Development)
Gherkin-style feature files describing behaviors:
- Vehicle detection scenarios
- Custom object detection behaviors
- Video processing workflows
- Model training behaviors

#### `streamlit_app/` - Demo Application
Interactive web application for demonstration:
- Video upload and processing interface
- Real-time detection visualization
- Custom class configuration
- Model training interface
- Performance metrics dashboard

## Target Video

Vehicle detection analysis on: https://www.youtube.com/watch?v=Bbv5V3FQc0A

## Reference Repositories

This project utilizes code and concepts from the following open-source repositories:

### 1. Ultralytics YOLO - Official Repository
**Repository**: https://github.com/ultralytics/ultralytics  
**Purpose**: Core YOLO implementation, official models, and training framework  
**Key Features**:
- State-of-the-art YOLOv8 and YOLO11 models
- Comprehensive training, validation, and inference capabilities
- Support for detection, segmentation, classification, and pose estimation
- Well-documented API and CLI interface

### 2. YOLOv8 Custom Object Detection
**Repository**: https://github.com/mohammadamine99/YOLOv8-custom-object-detection  
**Purpose**: Guide for training custom object detection models  
**Key Features**:
- Custom dataset preparation and annotation
- Fine-tuning YOLO models for specific objects
- Training pipeline examples
- Model evaluation and optimization techniques

### 3. YOLOv8 Streamlit Detection and Tracking
**Repository**: https://github.com/aparsoft/yolov8-streamlit-detection-tracking  
**Purpose**: Streamlit web interface for object detection and tracking  
**Key Features**:
- Interactive web-based detection interface
- Real-time video processing
- Object tracking capabilities
- User-friendly visualization

### 4. YOLOv8 Streamlit App
**Repository**: https://github.com/ongaunjie1/YOLOv8-streamlit-app  
**Purpose**: Alternative Streamlit implementation for YOLO  
**Key Features**:
- Clean and simple UI design
- Image and video upload support
- Real-time inference display
- Configuration options for model parameters

### 5. YOLOv8 DeepSORT Streamlit
**Repository**: https://github.com/monemati/YOLOv8-DeepSORT-Streamlit  
**Purpose**: Advanced tracking with DeepSORT algorithm  
**Key Features**:
- YOLOv8 detection combined with DeepSORT tracking
- Multi-object tracking with ID persistence
- Streamlit interface for video analysis
- Performance metrics and visualization

### 6. Vehicle Detection and Counter using YOLO11
**Repository**: https://github.com/SrujanPR/Vehicle-Detection-and-Counter-using-Yolo11  
**Purpose**: Specific vehicle counting implementation with latest YOLO11  
**Key Features**:
- Vehicle detection and counting logic
- YOLO11 integration
- Traffic analysis capabilities
- Real-time counting metrics

## Features

- ✅ Vehicle detection using YOLOv8/YOLO11
- ✅ Custom object class training
- ✅ Multi-scale training capabilities
- ✅ Streamlit web interface for live demo
- ✅ Video processing and analysis
- ✅ Object tracking and counting
- ✅ Comprehensive testing framework
- ✅ Complete project documentation

## Installation

```bash
# Clone this repository
git clone https://github.com/benchen1981-bchu/yolo_final_report.git
cd yolo_final_report

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Train Custom Model
```bash
python src/train.py --data data/vehicle_dataset.yaml --epochs 100
```

### Run Detection
```bash
python src/detect.py --source data/videos/traffic.mp4 --weights models/best.pt
```

### Launch Streamlit Demo
```bash
streamlit run streamlit_app/app.py
```

## Methodology Implementation

### CRISP-DM Process
1. **Business Understanding**: Vehicle detection for traffic analysis
2. **Data Understanding**: Analyzing video data and annotation requirements
3. **Data Preparation**: Dataset collection, annotation, and preprocessing
4. **Modeling**: Training YOLOv8/YOLO11 models
5. **Evaluation**: Performance metrics and validation
6. **Deployment**: Streamlit application for demonstration

### TDD (Test-Driven Development)
- Unit tests for data loading and preprocessing
- Integration tests for model inference pipeline
- Performance tests for detection accuracy

### SDD (Specification-Driven Development)
- Detailed specifications for detection requirements
- Performance criteria and acceptance metrics
- API specifications for model interfaces

### BDD (Behavior-Driven Development)
- Feature scenarios for vehicle detection
- Given-When-Then test cases
- User story validation

## License

This project integrates multiple open-source repositories. Please refer to individual repository licenses:

- Ultralytics YOLO: AGPL-3.0 License
- Other reference repositories: Check individual repository licenses

## Acknowledgments

Special thanks to all the open-source contributors and repositories that made this project possible:

- Ultralytics team for the excellent YOLO implementation
- All reference repository authors for their valuable contributions
- The open-source community for continuous support and innovation

## Contact

Project maintained by: benchen1981@gmail.com  
Repository: https://github.com/benchen1981-bchu/yolo_final_report
