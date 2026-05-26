# Evidence-antitampering
Developed an image forensics and anti-tampering system using Python, OpenCV, Scikit-image, and PyExifTool to detect digital image manipulation through metadata extraction, Error Level Analysis (ELA), visual feature comparison, and binary stream analysis.

## Overview

The Evidence Anti-Tampering & Image Forensics System is a Python-based digital image forensic analysis framework designed to detect image manipulation, authenticity violations, and hidden anomalies through advanced forensic techniques. The system performs metadata extraction, visual feature computation, Error Level Analysis (ELA), binary stream comparison, and perceptual hashing to identify potential tampering in digital evidence. The project focuses on improving the reliability, traceability, and integrity verification of digital images for cybersecurity and forensic applications.

---

# Features

* EXIF metadata extraction and analysis
* Error Level Analysis (ELA) for manipulation detection
* Binary stream and hash comparison
* SHA-256 and perceptual hash (pHash) generation
* ORB feature extraction for visual similarity analysis
* Edge map generation using Sobel operator
* RGB color histogram analysis
* Timestamped forensic output directories
* Structured JSON and CSV report generation
* Automated evidence comparison workflows

---

# Tech Stack

### Language

* Python

### Libraries & Tools

* OpenCV (`cv2`)
* NumPy
* PIL / Pillow
* Scikit-image
* exifread
* imagehash
* hashlib
* argparse
* JSON & CSV handling

---

# System Architecture

The framework is divided into multiple forensic analysis modules:

```plaintext
Input Image
     │
     ▼
Metadata Extraction
     │
     ▼
Feature Extraction
     │
     ├── RGB Histogram Analysis
     ├── Sobel Edge Detection
     └── ORB Descriptor Extraction
     │
     ▼
Error Level Analysis (ELA)
     │
     ▼
Binary Stream Comparison
     │
     ├── SHA-256 Hashing
     ├── Perceptual Hashing (pHash)
     └── Pixel-wise Difference Detection
     │
     ▼
JSON & CSV Report Generation
     │
     ▼
Timestamped Forensic Outputs
```

---

# Core Functionalities

## 1. Metadata Extraction

Extracts EXIF metadata from image files to identify:

* camera information
* timestamps
* GPS coordinates
* device information
* image properties

### Output

```plaintext
image_metadata.json
```

### Libraries Used

* exifread
* json

---

# 2. Feature Extraction

## Color Histogram Analysis

Computes reduced 8-bin RGB histograms to analyze image color distributions and detect inconsistencies.

## Edge Detection

Uses the Sobel operator to generate edge maps and identify structural anomalies in manipulated regions.

## ORB Feature Detection

Extracts:

* Oriented FAST keypoints
* Rotated BRIEF descriptors

for feature matching and similarity comparison.

### Output

```plaintext
image_features.npz
feature_summary.json
```

### Libraries Used

* OpenCV
* NumPy

---

# 3. Error Level Analysis (ELA)

ELA identifies tampered regions by analyzing JPEG recompression artifacts.

## Workflow

1. Compress image at 90% quality
2. Compare compressed image with original
3. Amplify differences
4. Highlight suspicious regions

### Output

```plaintext
image_ela.jpg
```

### Purpose

Tampered regions often exhibit inconsistent compression levels compared to untouched regions.

---

# 4. Binary Stream Comparison

Performs low-level image integrity verification through:

* SHA-256 hashing
* Perceptual hashing (pHash)
* pixel-level difference analysis

## Functionalities

* Detects binary modifications
* Identifies visually similar manipulated images
* Compares image integrity

### Outputs

```plaintext
difference_image.png
hash_report.json
```

### Libraries Used

* hashlib
* imagehash
* PIL.ImageChops

---

# 5. Report Generation

Automatically consolidates forensic findings into structured reports.

## Reports Include

* Metadata summaries
* Feature statistics
* Hash values
* ELA findings
* Binary comparison results
* Suspicious anomaly indicators

### Output Formats

```plaintext
JSON
CSV
```

---

# Directory Structure

```plaintext
Evidence-AntiTampering/
│
├── images/
├── outputs/
│   ├── analysis_YYYYMMDD_HHMMSS/
│   │   ├── metadata/
│   │   ├── ela/
│   │   ├── hashes/
│   │   ├── features/
│   │   ├── reports/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── .venv/
└── __pycache__/
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/evidence-antitampering.git
cd evidence-antitampering
```

---

# Create Virtual Environment

## Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

## Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install opencv-python numpy pillow exifread imagehash scikit-image
```

---

# Running the Project

## Execute Main File

```bash
python main.py
```

## Example Command

```bash
python main.py --image images/image.jpeg
```

---

# Generated Outputs

The system automatically creates timestamped forensic directories:

```plaintext
outputs/analysis_20250525_143210/
```

Generated outputs include:

* metadata JSON files
* ELA images
* feature files
* difference images
* forensic reports

---

# Example Use Cases

* Digital Image Forensics
* Cybercrime Investigation
* Evidence Verification
* Media Integrity Validation
* Deepfake & Manipulation Detection
* Security Research
* Legal Evidence Analysis

---

# Challenges Addressed

One of the primary challenges was ensuring reliable tamper detection across multiple image formats and manipulation techniques. This was addressed by combining metadata analysis, visual feature extraction, ELA, perceptual hashing, and binary comparison instead of relying on a single forensic indicator.

---

# Future Enhancements

* AI-based tampering detection
* Deepfake detection support
* GUI dashboard integration
* Batch image forensic analysis
* Cloud-based evidence validation
* Blockchain-backed evidence integrity storage

---

# Key Learning Outcomes

* Digital Image Forensics
* Computer Vision
* Feature Extraction
* Hashing & Integrity Verification
* Metadata Analysis
* OpenCV-based Image Processing
* Cybersecurity Investigation Workflows
* Automated Forensic Reporting
