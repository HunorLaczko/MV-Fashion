"""Metadata loading and querying helpers for the MV-Fashion dataset.

This module provides functions to load and query metadata from the dataset,
including subject info (info.csv), camera intrinsics, and extrinsics.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Optional

import numpy as np

from paths import (
    get_info_csv,
    get_intrinsics_json,
    get_extrinsics_json,
    get_subjects,
)


def load_subject_info(root: Optional[Path] = None) -> dict[str, dict]:
    info_path = get_info_csv(root)
    if not info_path.is_file():
        return {}
    result = {}
    with info_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            subject = row.get("subject", "").strip()
            if subject:
                result[subject] = {
                    "gender": row.get("gender", "").strip(),
                    "weight": float(row["weight"]) if row.get("weight") else None,
                    "height": float(row["height"]) if row.get("height") else None,
                }
    return result


def get_subject_info(
    subject: str, root: Optional[Path] = None
) -> Optional[dict]:
    info = load_subject_info(root)
    return info.get(subject)


def get_subjects_by_gender(
    gender: str, root: Optional[Path] = None
) -> list[str]:
    info = load_subject_info(root)
    gender_lower = gender.lower()
    return sorted(
        s for s, data in info.items()
        if data.get("gender", "").lower() == gender_lower
    )


def get_subjects_by_height_range(
    min_height: float, max_height: float, root: Optional[Path] = None
) -> list[str]:
    info = load_subject_info(root)
    return sorted(
        s for s, data in info.items()
        if data.get("height") is not None
        and min_height <= data["height"] <= max_height
    )


def get_subjects_by_weight_range(
    min_weight: float, max_weight: float, root: Optional[Path] = None
) -> list[str]:
    info = load_subject_info(root)
    return sorted(
        s for s, data in info.items()
        if data.get("weight") is not None
        and min_weight <= data["weight"] <= max_weight
    )


def load_intrinsics(root: Optional[Path] = None) -> dict[str, dict]:
    intrinsics_path = get_intrinsics_json(root)
    if not intrinsics_path.is_file():
        return {}
    with intrinsics_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_camera_intrinsics(
    camera: str, root: Optional[Path] = None
) -> Optional[dict]:
    intrinsics = load_intrinsics(root)
    return intrinsics.get(camera)


def get_camera_K(
    camera: str, root: Optional[Path] = None, use_undistorted: bool = True
) -> Optional[np.ndarray]:
    cam_data = get_camera_intrinsics(camera, root)
    if cam_data is None:
        return None
    key = "K_new" if use_undistorted else "K"
    K_data = cam_data.get(key)
    if K_data is None:
        return None
    return np.array(K_data, dtype=np.float64)


def get_camera_distortion(
    camera: str, root: Optional[Path] = None
) -> Optional[np.ndarray]:
    cam_data = get_camera_intrinsics(camera, root)
    if cam_data is None:
        return None
    dist_data = cam_data.get("dist")
    if dist_data is None:
        return None
    return np.array(dist_data, dtype=np.float64)


def get_camera_image_shape(
    camera: str, root: Optional[Path] = None
) -> Optional[tuple[int, int]]:
    cam_data = get_camera_intrinsics(camera, root)
    if cam_data is None:
        return None
    shape_data = cam_data.get("image_shape")
    if shape_data is None:
        return None
    return tuple(shape_data)


def get_rpi_cameras(root: Optional[Path] = None) -> list[str]:
    intrinsics = load_intrinsics(root)
    return sorted(k for k in intrinsics.keys() if k.startswith("rpi_"))


def get_bolt_cameras(root: Optional[Path] = None) -> list[str]:
    intrinsics = load_intrinsics(root)
    return sorted(k for k in intrinsics.keys() if k.startswith("bolt_"))


def load_bolt_extrinsics(root: Optional[Path] = None) -> dict[str, dict]:
    extrinsics_path = get_extrinsics_json(root)
    if not extrinsics_path.is_file():
        return {}
    with extrinsics_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_bolt_extrinsics(
    bolt: str, root: Optional[Path] = None
) -> Optional[dict]:
    extrinsics = load_bolt_extrinsics(root)
    return extrinsics.get(bolt)


def get_bolt_rotation(
    bolt: str, root: Optional[Path] = None
) -> Optional[np.ndarray]:
    ext_data = get_bolt_extrinsics(bolt, root)
    if ext_data is None:
        return None
    R_data = ext_data.get("R")
    if R_data is None:
        return None
    return np.array(R_data, dtype=np.float64)


def get_bolt_translation(
    bolt: str, root: Optional[Path] = None
) -> Optional[np.ndarray]:
    ext_data = get_bolt_extrinsics(bolt, root)
    if ext_data is None:
        return None
    t_data = ext_data.get("t")
    if t_data is None:
        return None
    return np.array(t_data, dtype=np.float64)


def get_all_cameras(root: Optional[Path] = None) -> list[str]:
    intrinsics = load_intrinsics(root)
    return sorted(intrinsics.keys())


def get_camera_count(root: Optional[Path] = None) -> int:
    return len(get_all_cameras(root))


def get_subject_count(root: Optional[Path] = None) -> int:
    return len(get_subjects(root))


def get_dataset_summary(root: Optional[Path] = None) -> dict[str, Any]:
    subject_info = load_subject_info(root)
    intrinsics = load_intrinsics(root)
    extrinsics = load_bolt_extrinsics(root)
    
    genders = {}
    heights = []
    weights = []
    for data in subject_info.values():
        gender = data.get("gender", "unknown")
        genders[gender] = genders.get(gender, 0) + 1
        if data.get("height") is not None:
            heights.append(data["height"])
        if data.get("weight") is not None:
            weights.append(data["weight"])
    
    return {
        "num_subjects": len(subject_info),
        "gender_distribution": genders,
        "height_stats": {
            "min": min(heights) if heights else None,
            "max": max(heights) if heights else None,
            "mean": sum(heights) / len(heights) if heights else None,
        },
        "weight_stats": {
            "min": min(weights) if weights else None,
            "max": max(weights) if weights else None,
            "mean": sum(weights) / len(weights) if weights else None,
        },
        "num_cameras": len(intrinsics),
        "num_rpi_cameras": len([k for k in intrinsics if k.startswith("rpi_")]),
        "num_bolt_cameras": len([k for k in intrinsics if k.startswith("bolt_")]),
        "num_bolt_extrinsics": len(extrinsics),
    }
