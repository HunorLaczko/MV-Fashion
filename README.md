# MV-Fashion Dataset Tools

[![Paper](https://img.shields.io/badge/arXiv-2603.08147-b31b1b.svg)](https://arxiv.org/abs/2603.08147)
[![Project Page](https://img.shields.io/badge/Project-Page-blue.svg)](https://hunorlaczko.github.io/MV-Fashion/)
[![Dataset](https://img.shields.io/badge/Dataset-HuggingFace-yellow.svg)](https://huggingface.co/datasets/MV-Fashion/MV-Fashion)
[![License](https://img.shields.io/badge/License-Research_Use-lightgrey.svg)](#-license)

Complete toolkit for downloading, processing, and analyzing the MV-Fashion dataset.

## 🚀 Quick Start

```bash
# 1. Install dependencies (from the project root, where requirements.txt lives)
pip install -r requirements.txt

# 2. Switch to the utils/ directory that contains the scripts
cd utils

# 3. Download metadata (fast, ~100MB)
python download_mv_fashion.py --metadata-only

# 4. Download specific subjects with RPi cameras only
python download_mv_fashion.py --subjects 1 2 3 --cameras rpi

# 5. Unzip downloaded videos
python unzip_videos.py --subjects 1 2 3

# 6. Visualize the data
python visualize_dataset.py --sequence subject_0001/outfit_1/layer_1/sequence_1 --save viz.png
```

> All commands below assume you are inside `utils/`. Anywhere the README
> shows `cd /code/tools`, substitute the actual path to the `utils/` directory
> you cloned the repository into.

## 📦 Installation

All dependencies are listed in `requirements.txt` at the project root. We
recommend creating an isolated Python environment before installing them.

### Option A: `venv` (standard library, no extra tools)

```bash
# From the project root (the directory that contains requirements.txt)
python -m venv .venv

# Activate it
#    Linux / macOS:
source .venv/bin/activate
#    Windows (PowerShell):
.venv\Scripts\Activate.ps1
#    Windows (cmd.exe):
.venv\Scripts\activate.bat

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Option B: `conda` / `mamba`

```bash
# From the project root
conda create -y -n mv_fashion python=3.11
conda activate mv_fashion

# Install dependencies
pip install -r requirements.txt
```

### Option C: Install into the current environment

If you already have an environment you want to use:

```bash
# From the project root
pip install -r requirements.txt
```

> **Note:** `pillow-avif-plugin` (in `requirements.txt`) is required to read the
> `.avif` video frames used throughout the toolkit. If you skip it, frame-loading
> and undistortion examples will fail with an "cannot identify image file" error.
> `opencv-python` (already included) is needed for `cv2.undistort`.

### Verify the installation

```bash
# From the utils/ directory
cd utils
python visualize_dataset.py --help
```

## ⚙️ Configuration

### Dataset Location

Set the `MV_FASHION_DATASET_ROOT` environment variable to specify where the dataset is stored:

```bash
# Temporary (current session)
export MV_FASHION_DATASET_ROOT=/path/to/your/dataset

# Or use it inline
MV_FASHION_DATASET_ROOT=/path/to/dataset python download_mv_fashion.py --metadata-only
```

If not set, the default location is `./mv_fashion_dataset` in the current directory.

### HuggingFace Token

The dataset requires authentication. Set your HuggingFace token:

```bash
export HF_TOKEN=your_token_here
```

Or create a `.env` file. The download script looks for `.env` first in the
current working directory and then in `~/.huggingface/`:
```bash
HF_TOKEN=your_token_here
```

## 📥 Download Script

### Features
- **Granular control**: Download specific subjects, camera types, annotations
- **Resumable downloads**: Automatically resumes interrupted downloads
- **HF xet support**: Uses fast xet protocol when available
- **Parallel downloads**: Configurable number of workers
- **Progress tracking**: Real-time progress updates

### Usage Examples

```bash
# Download metadata only
python download_mv_fashion.py --metadata-only

# Download videos for subjects 1-5, RPi cameras only
python download_mv_fashion.py --subject-range 1 5 --cameras rpi

# Download videos for specific subjects, both camera types
python download_mv_fashion.py --subjects 1 2 3 --cameras rpi bolt

# Download annotations (foreground and garment masks)
python download_mv_fashion.py --subjects 1 2 --annotations foreground garment

# Download everything for subjects 1-3
python download_mv_fashion.py --subjects 1 2 3 --cameras rpi bolt --annotations foreground garment

# Resume interrupted download
python download_mv_fashion.py --subjects 1 2 3 --resume

# Use custom output directory
python download_mv_fashion.py --metadata-only --output-dir ./my_dataset

# List all available files
python download_mv_fashion.py --list-files
```

### Options

```
--output-dir PATH          Output directory (default: $MV_FASHION_DATASET_ROOT or ./mv_fashion_dataset)
--token TOKEN              HuggingFace token (or set HF_TOKEN env var)
--workers N                Number of parallel workers (default: 8)
--no-xet                   Disable xet protocol
--resume                   Resume interrupted downloads (default: True)
--no-resume                Download everything fresh
--list-files               List all files in dataset
--metadata-only            Download only metadata
--annotations [TYPE ...]   Download annotations (foreground, garment)
--subjects N [N ...]       Download specific subjects
--subject-range START END  Download range of subjects
--cameras [TYPE ...]       Download camera types (rpi, bolt)
--all                      Download entire dataset (~11.5 TB)
```

### Environment Variables

- `MV_FASHION_DATASET_ROOT`: Default dataset directory (default: `./mv_fashion_dataset`)
- `HF_TOKEN`: HuggingFace authentication token

Example:
```bash
export MV_FASHION_DATASET_ROOT=/path/to/your/dataset
python download_mv_fashion.py --metadata-only
```

## 📂 Unzip Script

### Features
- **Parallel extraction**: Multiple workers for fast extraction
- **Progress tracking**: Real-time progress updates
- **Skip existing**: Automatically skips already extracted files
- **Camera filtering**: Extract only RPi or Bolt cameras
- **Detailed statistics**: Comprehensive extraction reports

### Usage Examples

```bash
# Unzip all sequences
python unzip_videos.py --all

# Unzip specific subjects, RPi cameras only
python unzip_videos.py --subjects 1 2 3 --cameras rpi

# Unzip range of subjects, both camera types
python unzip_videos.py --subject-range 1 10 --cameras rpi bolt

# Unzip specific sequence
python unzip_videos.py --sequence subject_0001/outfit_1/layer_1/sequence_1

# Use more workers for faster extraction
python unzip_videos.py --subjects 1 --workers 8

# Extract to custom directory
python unzip_videos.py --subjects 1 --output-dir ./extracted

# Overwrite existing files
python unzip_videos.py --subjects 1 --overwrite
```

### Options

```
--output-dir PATH          Output directory (default: same as archives)
--overwrite                Overwrite existing files
--cameras [TYPE ...]       Camera types to extract (rpi, bolt)
--subjects N [N ...]       Unzip specific subjects
--subject-range START END  Unzip range of subjects
--sequence PATH            Unzip specific sequence
--all                      Unzip all sequences
--workers N                Number of parallel workers (default: 4)
```

## 🎨 Visualization Script

### Features
- **Multi-view frames**: Visualize frames from multiple cameras
- **Garment images**: Display front/back views of garments
- **Segmentation masks**: Visualize foreground and garment masks
- **Dataset statistics**: Generate statistical plots
- **Camera setup**: 3D visualization of camera positions
- **Headless support**: Works in non-interactive environments

### Usage Examples

```bash
# Visualize sequence frames
python visualize_dataset.py --sequence subject_0001/outfit_1/layer_1/sequence_1

# Visualize specific frame
python visualize_dataset.py --sequence subject_0001/outfit_1/layer_1/sequence_1 --frame-idx 10

# Visualize garment images
python visualize_dataset.py --garments subject_0001/outfit_1

# Visualize masks
python visualize_dataset.py --masks subject_0001/outfit_1

# Visualize dataset statistics
python visualize_dataset.py --stats

# Undistort a frame
python visualize_dataset.py --undistort subject_0001/outfit_1/layer_1/sequence_1 --camera rpi_01
```

### Options

```
--sequence PATH            Visualize sequence frames
--frame-idx N              Frame index (default: 0)
--garments PATH            Visualize garment images
--masks PATH               Visualize masks
--layer N                  Mask filter: only garments with layer <= N are drawn
--mask-sequence NAME       Sequence for --masks (default: first available)
--mask-camera NAME         Camera for --masks (default: rpi_01)
--stats                    Visualize dataset statistics
--undistort PATH           Undistort a single frame
--camera NAME              Camera for --undistort (default: rpi_01)
```

(All plots are rendered with Plotly and shown in the default browser.)

## 🐍 Python API

The toolkit ships as a set of small focused modules. You can call them
directly without any wrapper class — every example below is a complete,
self-contained snippet that runs as-is once the dataset is downloaded.

### Quick start

```python
from paths import get_subjects, get_outfits, get_sequences
from metadata import get_subject_info, get_camera_K
from garments import get_all_garments_in_outfit
from statistics import count_subjects, count_total_sequences, get_dataset_summary_report
from validation import validate_full_dataset

# Basic info
print(f"Subjects: {count_subjects()}")
print(f"Sequences: {count_total_sequences()}")

# Navigate the hierarchy
subjects = get_subjects()
outfits = get_outfits("subject_0001")
sequences = get_sequences("subject_0001", "outfit_1", "layer_1")

# Subject info
info = get_subject_info("subject_0001")
print(f"Gender: {info['gender']}, Height: {info['height']}cm")

# Garment data
garments = get_all_garments_in_outfit("subject_0001", "outfit_1")
for garment in garments:
    print(f"Cloth {garment['cloth_number']}: {garment['type']}")

# Camera data
K = get_camera_K("rpi_01")
print(f"Camera matrix:\n{K}")

# Validate
result = validate_full_dataset()
print(f"Valid: {result.is_valid}")

# Summary
print(get_dataset_summary_report())
```

### Helper Modules

#### paths.py
Path resolution and navigation:
```python
from paths import get_subjects, iter_sequences, get_sequence_path

subjects = get_subjects()
for subject, outfit, layer, sequence in iter_sequences():
    path = get_sequence_path(subject, outfit, layer, sequence)
```

#### metadata.py
Subject and camera metadata:
```python
from metadata import get_subject_info, get_camera_K, get_bolt_rotation

info = get_subject_info("subject_0001")
K = get_camera_K("rpi_01")
R = get_bolt_rotation("bolt_1")
```

#### garments.py
Garment data:
```python
from garments import get_all_garments_in_outfit, get_garment_description

garments = get_all_garments_in_outfit("subject_0001", "outfit_1")
desc = get_garment_description("subject_0001", "outfit_1", "cloth_1")
```

#### statistics.py
Statistics and counting:
```python
from statistics import count_garments_by_type, get_dataset_summary_report

type_counts = count_garments_by_type()
print(get_dataset_summary_report())
```

#### validation.py
Validation:
```python
from validation import validate_full_dataset

result = validate_full_dataset()
print(f"Valid: {result.is_valid}")
print(f"Errors: {len(result.errors)}")
```

## 📊 Dataset Overview

- **81 subjects** (41 male, 37 female, 3 non-binary)
- **332 outfits** with multiple garments
- **482 layers** across all outfits
- **2,357 sequences** of subjects wearing outfits
- **769 garments** across 35+ types
- **68 physical cameras** (60 RPi + 8 Bolt with RGB+depth) — listed as 76
  entries in `cameras/intrinsics.json` because each Bolt camera has separate
  RGB and depth intrinsics
- **52M+ frames** total (~11.5 TB)

Due to some GDPR limitations, some sequences are not yet released. Please check the Huggingface page for more details.

### Video Archive Structure

**rpi.zip** (60 RGB cameras):
```
rpi_01/00000.avif
rpi_01/00001.avif
...
rpi_60/00291.avif
```

**bolt.zip** (8 Bolt cameras, each with RGB + depth):
```
bolt_1/rgb/00000.avif
bolt_1/depth/00000.npz
...
bolt_8/rgb/00291.avif
bolt_8/depth/00291.npz
```

## 🔄 Resumable Downloads

The download script automatically tracks progress in `.download_progress.json`. If a download is interrupted:

```bash
# Resume automatically (default behavior)
python download_mv_fashion.py --subjects 1 2 3 --resume

# Start fresh (ignore progress)
python download_mv_fashion.py --subjects 1 2 3 --no-resume
```

## ⚡ Performance Tips

### Download
- Use `--workers 16` for faster downloads on high-bandwidth connections
- Use `--no-xet` if xet protocol causes issues
- Download metadata first to explore dataset structure

### Unzip
- Use `--workers 8` for faster extraction on multi-core systems
- Extract only needed cameras: `--cameras rpi` or `--cameras bolt`
- Use `--overwrite` carefully as it re-extracts everything

### Visualization
- Use `--dpi 150` for high-quality figures
- Save to file in headless environments: `--save output.png`
- Use lower DPI for quick previews: `--dpi 72`

## 📚 Jupyter Notebook

A complete tutorial is available in `utils/mv_fashion_tutorial.ipynb`:

```bash
cd utils
jupyter notebook mv_fashion_tutorial.ipynb
```

Topics covered:
1. Downloading the dataset
2. Unzipping video archives
3. Navigating dataset structure
4. Visualizing multi-view frames
5. Accessing garment metadata
6. Visualizing garment images
7. Visualizing segmentation masks (foreground + garment)
8. Working with camera calibration
9. Analyzing dataset statistics
10. Iterating through all sequences
11. Processing sequences end-to-end

## 🏗️ Repository Structure

```
MV-Fashion/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── LICENSE                   # Project license
├── .env.example              # Template for HF_TOKEN / dataset path
├── .gitignore                # Git ignore rules
└── utils/                    # All scripts and the tutorial notebook
    ├── download_mv_fashion.py    # Download script with resumable downloads
    ├── unzip_videos.py           # High-performance video extraction
    ├── visualize_dataset.py      # Visualization tools
    ├── paths.py                  # Path resolution utilities
    ├── metadata.py               # Subject and camera metadata
    ├── garments.py               # Garment data access
    ├── statistics.py             # Dataset statistics
    ├── validation.py             # Dataset validation
    ├── examples.py               # Standalone usage examples (10 demos)
    ├── mv_fashion_tutorial.ipynb # Jupyter tutorial (11 sections)
    └── test_smoke.py             # Import / smoke test
```

## 🔗 Resources

- **Dataset**: https://huggingface.co/datasets/MV-Fashion/MV-Fashion
- **Paper**: https://arxiv.org/abs/2603.08147
- **Project Page**: https://hunorlaczko.github.io/MV-Fashion/
- **GitHub**: https://github.com/HunorLaczko/MV-Fashion

## 📝 Citation

```bibtex
@InProceedings{Laczko_2026_CVPR,
    author    = {Laczk\'o, Hunor and Jia, Libang and Truong, Loc-Phat and Hern\'andez, Diego and Escalera, Sergio and Gonzalez, Jordi and Madadi, Meysam},
    title     = {MV-Fashion: Towards Enabling Virtual Try-On and Size Estimation with Multi-View Paired Data},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
    month     = {June},
    year      = {2026},
    pages     = {42810-42823}
}
```

## 📄 License

The dataset is available for non-commercial research purposes only under the [MV-Fashion Dataset Agreement](https://hunorlaczko.github.io/MV-Fashion/dataset_agreement.pdf).

## 🆘 Support

For questions or issues:
- GitHub: https://github.com/HunorLaczko/MV-Fashion
- Project Page: https://hunorlaczko.github.io/MV-Fashion/
