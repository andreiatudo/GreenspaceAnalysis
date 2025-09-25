# 🌿 GreenSpace Analysis Pipeline

> A comprehensive computer vision pipeline for detecting and analyzing green spaces in satellite/aerial imagery using YOLOv8 segmentation models.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange)](https://github.com/ultralytics/ultralytics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Pipeline Components](#-pipeline-components)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Output Formats](#-output-formats)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

The Green-Space Analysis Pipeline is a complete end-to-end solution for automated detection, segmentation, and analysis of green spaces in aerial imagery. Built during the **RAAI Summer School**, this project combines state-of-the-art computer vision techniques with practical urban planning applications.

### Key Capabilities
- **Automated Dataset Management** - Extract and organize Roboflow datasets
- **Model Training** - Train custom YOLOv8 segmentation models
- **Inference & Analysis** - Run predictions and analyze mask quality
- **Comprehensive Reporting** - Generate detailed analysis reports with visualizations
- **Image Processing** - Split large images into patches and reconstruct results

## ✨ Features

### 🤖 Machine Learning
- YOLOv8 segmentation model training and inference
- Configurable confidence thresholds and area filters
- Multi-class green space detection (trees, grass, parks, etc.)
- GPU acceleration support

### 📊 Analysis & Reporting
- Automated mask quality analysis with area calculations
- Interactive HTML reports with charts and metrics
- CSV export for further analysis
- Coverage statistics per class

### 🖼️ Image Processing
- Large image splitting into manageable patches
- Seamless reconstruction from processed patches
- Support for multiple image formats (PNG, JPG, TIFF, BMP)
- Batch processing capabilities

### 📈 Visualization
- matplotlib-based coverage charts
- Per-class statistics and distributions
- Model performance metrics integration
- Professional report generation

## 🚀 Installation

### Prerequisites
```bash
Python 3.8+
CUDA-compatible GPU (recommended)
```

### Dependencies
```bash
pip install ultralytics torch torchvision
pip install matplotlib pillow pathlib
pip install argparse json csv datetime base64
```

### Clone Repository
```bash
git clone https://github.com/yourusername/green-space-pipeline.git
cd green-space-pipeline
```

## 🏃‍♂️ Quick Start

### 1. Setup Your Dataset
```powershell
python .\src\setup_roboflow.py --zip .\data\MainDataSet.v2i.yolov8.zip --outdir . --force
```

### 2. Train the Model
```powershell
python .\src\train_seg.py --data .\data.yaml --model yolov8n-seg.pt --epochs 50 --imgsz 640 --batch -1 --device 0
```

### 3. Run Analysis
```powershell
python .\src\analyze_masks.py --weights .\runs\seg_n_640\weights\best.pt --source .\test\images --conf 0.6 --min-area-frac 0.02
```

### 4. Generate Report
```powershell
python .\src\generate_report.py --indir .\reports\YYYY-MM-DD_HH-MM-SS\json --model-name "YOLOv8-seg (best.pt)"
```

## 🔧 Pipeline Components

### 1. `setup_roboflow.py` - Dataset Manager
Extracts and organizes dataset ZIP files with automatic validation.

**Key Features:**
- Automatic dataset structure detection
- Image counting per split (train/val/test)
- Force extraction with cleanup options

```powershell
python .\src\setup_roboflow.py --zip <ZIP_PATH> --outdir <EXTRACT_DIR> [--force]
```

### 2. `train_seg.py` - Model Training
Trains YOLOv8 segmentation models with comprehensive configuration options.

**Key Features:**
- Automatic corrupted weights detection and cleanup
- Configurable training parameters
- Multi-GPU support
- Early stopping with patience

```powershell
python .\src\train_seg.py --data <DATA_YAML> [OPTIONS]
```

**Training Options:**
- `--model`: Pre-trained weights (default: `yolov8n-seg.pt`)
- `--epochs`: Training epochs (default: 50)
- `--imgsz`: Image size (default: 640)
- `--batch`: Batch size (default: 8, use -1 for auto)
- `--device`: GPU device (default: auto-detect)
- `--patience`: Early stopping patience (default: 50)

### 3. `infer_seg.py` - Visual Inference
Runs segmentation inference with visual output generation.

**Key Features:**
- Batch processing of images/directories
- Visual overlay generation
- Configurable output organization
- Multi-format support

```powershell
python .\src\infer_seg.py --weights <WEIGHTS_PT> --source <IMG_OR_DIR> [OPTIONS]
```

### 4. `analyze_masks.py` - Quantitative Analysis
Performs detailed mask analysis with filtering and JSON export.

**Key Features:**
- Confidence-based filtering
- Minimum area threshold filtering
- Per-image JSON export with metadata
- Class-wise statistics

```powershell
python .\src\analyze_masks.py --weights <WEIGHTS_PT> --source <IMG_DIR_OR_FILE> [OPTIONS]
```

**Analysis Parameters:**
- `--conf`: Confidence threshold (default: 0.5)
- `--min-area-frac`: Minimum area fraction (default: 0.01)
- `--imgsz`: Inference image size (default: 1280)

### 5. `generate_report.py` - Report Generation
Creates comprehensive analysis reports in multiple formats.

**Key Features:**
- HTML reports with interactive charts
- Markdown documentation
- CSV data export
- Model metrics integration

```powershell
python .\src\generate_report.py --indir <REPORT_JSON_DIR> [OPTIONS]
```

**Report Components:**
- Coverage summary with bar charts
- Per-class statistics table
- Model performance metrics (if available)
- Interpretation and recommendations

### 6. Image Processing Utilities

#### `CreatingPatches.py` - Image Splitting
Splits large images into fixed-size patches for processing.

```powershell
python CreatingPatches.py --input <IMAGE_OR_FOLDER> --patch-width <W> --patch-height <H> --output-dir <OUT_DIR>
```

**Features:**
- Configurable patch dimensions
- Batch processing support
- Multiple output formats
- Automatic padding for edge patches

#### `CreatingBigImage.py` - Image Reconstruction
Reconstructs original images from processed patches.

```powershell
python CreatingBigImage.py --patch-dir <PATCH_FOLDER> --output <OUT_IMAGE>
```

**Features:**
- Automatic coordinate detection from filenames
- Size inference from patch metadata
- Seamless reconstruction
- Error handling for missing patches

## 💡 Usage Examples

### Complete Workflow Example
```powershell
# 1. Setup dataset
python .\src\setup_roboflow.py --zip .\data\GreenSpaces.zip --outdir .\data --force

# 2. Train model
python .\src\train_seg.py --data .\data\data.yaml --model yolov8s-seg.pt --epochs 100 --imgsz 640 --batch 16 --device 0 --name greenspace_v1

# 3. Process large images (if needed)
python CreatingPatches.py --input .\test\large_image.tif --patch-width 1280 --patch-height 1280 --output-dir .\test\patches

# 4. Run analysis
python .\src\analyze_masks.py --weights .\runs\greenspace_v1\weights\best.pt --source .\test\patches --conf 0.7 --min-area-frac 0.005 --imgsz 1280

# 5. Generate comprehensive report
python .\src\generate_report.py --indir .\reports\2024-08-15_14-30-22\json --model-name "YOLOv8s-seg Custom Model" --metrics .\runs\greenspace_v1\results.json

# 6. Reconstruct results (if using patches)
python CreatingBigImage.py --patch-dir .\runs_local\predict_20240815_143022 --output .\results\reconstructed_analysis.png
```

### Advanced Configuration Example
```powershell
# High-precision analysis for research
python .\src\analyze_masks.py \
  --weights .\models\best_research.pt \
  --source .\data\validation \
  --conf 0.8 \
  --min-area-frac 0.001 \
  --imgsz 1920 \
  --outdir .\research_results
```

## ⚙️ Configuration

### Model Training Configuration
Create a `config.yaml` file for consistent training:

```yaml
# Training parameters
epochs: 100
imgsz: 640
batch: 16
device: 0

# Model parameters
model: yolov8s-seg.pt
patience: 30

# Data augmentation
hsv_h: 0.015
hsv_s: 0.7
hsv_v: 0.4
degrees: 0.0
translate: 0.1
scale: 0.5
shear: 0.0
perspective: 0.0
flipud: 0.0
fliplr: 0.5
mosaic: 1.0
mixup: 0.0
```

### Analysis Thresholds
Recommended settings for different use cases:

| Use Case | Confidence | Min Area Frac | Image Size |
|----------|------------|---------------|------------|
| **Urban Planning** | 0.7 | 0.01 | 1280 |
| **Research** | 0.8 | 0.005 | 1920 |
| **Quick Survey** | 0.5 | 0.02 | 640 |
| **High Precision** | 0.9 | 0.001 | 1920 |

## 📄 Output Formats

### JSON Analysis Files
Each processed image generates a detailed JSON file:

```json
{
  "image": "/path/to/image.jpg",
  "height": 1080,
  "width": 1920,
  "segments_kept": [
    {
      "class_id": 0,
      "class_name": "tree",
      "conf": 0.85,
      "area_pixels": 15420,
      "area_frac": 0.0074
    }
  ],
  "params": {
    "conf_threshold": 0.6,
    "min_area_frac": 0.02
  }
}
```

### HTML Report Features
- **Interactive Charts**: matplotlib-generated coverage charts
- **Responsive Design**: Works on desktop and mobile
- **Professional Styling**: Clean, print-friendly layout
- **Comprehensive Tables**: Sortable data with metrics

### CSV Export Schema
```csv
class,mean_area_percent,instances
tree,12.45,156
grass,8.23,89
building,15.67,234
water,3.12,45
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/yourusername/green-space-pipeline.git
cd green-space-pipeline
pip install -r requirements.txt
pip install -e .
```

## 🏆 Acknowledgments

- **RAAI Summer School** - For providing the learning environment and inspiration
- **Ultralytics Team** - For the excellent YOLOv8 framework
- **Open Source Community** - For the amazing tools and libraries
