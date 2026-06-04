# MV-Fashion: Towards Enabling Virtual Try-On and Size Estimation with Multi-View Paired Data

[![Website](https://img.shields.io/badge/Project-Website-blue)](https://hunorlaczko.github.io/MV-Fashion/)
[![arXiv](https://img.shields.io/badge/arXiv-2603.08147-b31b1b.svg)](https://arxiv.org/abs/2603.08147)
[![Venue](https://img.shields.io/badge/Venue-CVPR%202026-green)](https://cvpr.thecvf.com/)

Official website source code and repository for the CVPR 2026 paper:
**"MV-Fashion: Towards Enabling Virtual Try-On and Size Estimation with Multi-View Paired Data"**

[**Project Page**](https://hunorlaczko.github.io/MV-Fashion/) | [**arXiv**](https://arxiv.org/abs/2603.08147)

---

## Abstract

Existing 4D human datasets fall short for fashion-specific research, lacking either realistic garment dynamics or task-specific annotations. Synthetic datasets suffer from a realism gap, whereas real-world captures lack the detailed annotations and paired data required for virtual try-on (VTON) and size estimation tasks. To bridge this gap, we introduce **MV-Fashion**, a large-scale, multi-view video dataset engineered for domain-specific fashion analysis. MV-Fashion features **3,273 sequences (72.5 million frames)** from **80 diverse subjects** wearing 3-10 outfits each. 

Crucially for VTON applications, MV-Fashion provides **paired data**: multi-view synchronized captures of worn garments alongside their corresponding flat, catalogue images. We leverage this dataset to establish baselines for fashion-centric tasks, including virtual try-on, clothing size estimation, and novel view synthesis.

## Key Features

- 👕 **Large-scale Dataset**: 3,273 sequences, 72.5M frames, 80 subjects.
- 💃 **Real-world Dynamics**: Captures multi-layer garments and varied styling (tucked, rolled, etc.).
- 🏷️ **Rich Annotations**: Pixel-level semantics, material elasticity, and 3D point clouds.
- 🔄 **Paired Data**: Synchronized multi-view captures matched with flat catalogue images.

## Dataset Access

To request access to the **MV-Fashion** dataset, please visit our [official website](https://hunorlaczko.github.io/MV-Fashion/) and fill out the access request form.

## Citation

If you find our work useful, please cite:

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