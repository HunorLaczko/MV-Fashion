"""Dataset structure validation helpers for the MV-Fashion dataset.

This module provides functions to validate the dataset structure,
check for missing files, and verify data integrity.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from paths import (
    get_dataset_root,
    get_subjects,
    get_outfits,
    get_layers,
    get_sequences,
    get_sequence_path,
    get_video_archives,
    get_info_csv,
    get_intrinsics_json,
    get_extrinsics_json,
    get_foreground_mask_dir,
    get_garment_mask_dir,
    get_garment_image_dir,
    get_garment_mask_image_dir,
    get_garment_descriptions_json,
    get_garment_measurements_json,
    get_styling_labels_json,
)
from metadata import load_subject_info, load_intrinsics, load_bolt_extrinsics
from garments import (
    load_garment_descriptions,
    load_garment_measurements,
    load_styling_labels,
)


class ValidationResult:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)

    def add_info(self, msg: str) -> None:
        self.info.append(msg)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def summary(self) -> str:
        lines = []
        if self.errors:
            lines.append(f"ERRORS ({len(self.errors)}):")
            for err in self.errors[:10]:
                lines.append(f"  - {err}")
            if len(self.errors) > 10:
                lines.append(f"  ... and {len(self.errors) - 10} more errors")
        if self.warnings:
            lines.append(f"WARNINGS ({len(self.warnings)}):")
            for warn in self.warnings[:10]:
                lines.append(f"  - {warn}")
            if len(self.warnings) > 10:
                lines.append(f"  ... and {len(self.warnings) - 10} more warnings")
        if self.info:
            lines.append(f"INFO ({len(self.info)}):")
            for info in self.info[:5]:
                lines.append(f"  - {info}")
        if not self.errors and not self.warnings:
            lines.append("Validation passed with no issues.")
        return "\n".join(lines)


def validate_dataset_root(root: Optional[Path] = None) -> ValidationResult:
    result = ValidationResult()
    root = root or get_dataset_root()

    if not root.is_dir():
        result.add_error(f"Dataset root does not exist: {root}")
        return result

    required_dirs = ["videos", "annotations", "cameras", "garments"]
    for dir_name in required_dirs:
        dir_path = root / dir_name
        if not dir_path.is_dir():
            result.add_error(f"Missing required directory: {dir_name}")
        else:
            result.add_info(f"Found directory: {dir_name}")

    required_files = ["info.csv"]
    for file_name in required_files:
        file_path = root / file_name
        if not file_path.is_file():
            result.add_error(f"Missing required file: {file_name}")
        else:
            result.add_info(f"Found file: {file_name}")

    return result


def validate_camera_files(root: Optional[Path] = None) -> ValidationResult:
    result = ValidationResult()
    root = root or get_dataset_root()

    intrinsics_path = get_intrinsics_json(root)
    if not intrinsics_path.is_file():
        result.add_error(f"Missing intrinsics file: {intrinsics_path}")
    else:
        try:
            with intrinsics_path.open("r", encoding="utf-8") as f:
                intrinsics = json.load(f)
            result.add_info(f"Loaded {len(intrinsics)} camera intrinsics")
            
            for cam_name, cam_data in intrinsics.items():
                if "K" not in cam_data:
                    result.add_warning(f"Camera {cam_name} missing K matrix")
                if "dist" not in cam_data:
                    result.add_warning(f"Camera {cam_name} missing distortion coefficients")
        except json.JSONDecodeError as e:
            result.add_error(f"Invalid JSON in intrinsics file: {e}")

    extrinsics_path = get_extrinsics_json(root)
    if not extrinsics_path.is_file():
        result.add_warning(f"Missing extrinsics file: {extrinsics_path}")
    else:
        try:
            with extrinsics_path.open("r", encoding="utf-8") as f:
                extrinsics = json.load(f)
            result.add_info(f"Loaded {len(extrinsics)} bolt extrinsics")
        except json.JSONDecodeError as e:
            result.add_error(f"Invalid JSON in extrinsics file: {e}")

    return result


def validate_subject_metadata(
    subject: str, root: Optional[Path] = None
) -> ValidationResult:
    result = ValidationResult()
    root = root or get_dataset_root()

    subject_info = load_subject_info(root)
    if subject not in subject_info:
        result.add_warning(f"Subject {subject} not found in info.csv")
    else:
        info = subject_info[subject]
        if not info.get("gender"):
            result.add_warning(f"Subject {subject} missing gender")
        if info.get("height") is None:
            result.add_warning(f"Subject {subject} missing height")
        if info.get("weight") is None:
            result.add_warning(f"Subject {subject} missing weight")

    desc_path = get_garment_descriptions_json(subject, root)
    if not desc_path.is_file():
        result.add_warning(f"Missing garment descriptions for {subject}")
    else:
        try:
            descriptions = load_garment_descriptions(subject, root)
            if "outfits" not in descriptions:
                result.add_warning(f"Garment descriptions for {subject} missing 'outfits' key")
        except json.JSONDecodeError as e:
            result.add_error(f"Invalid JSON in garment descriptions for {subject}: {e}")

    styles_path = get_styling_labels_json(subject, root)
    if not styles_path.is_file():
        result.add_warning(f"Missing styling labels for {subject}")
    else:
        try:
            styles = load_styling_labels(subject, root)
            if "outfits" not in styles:
                result.add_warning(f"Styling labels for {subject} missing 'outfits' key")
        except json.JSONDecodeError as e:
            result.add_error(f"Invalid JSON in styling labels for {subject}: {e}")

    return result


def validate_outfit_metadata(
    subject: str, outfit: str, root: Optional[Path] = None
) -> ValidationResult:
    result = ValidationResult()
    root = root or get_dataset_root()

    meas_path = get_garment_measurements_json(subject, outfit, root)
    if not meas_path.is_file():
        result.add_warning(f"Missing garment measurements for {subject}/{outfit}")
    else:
        try:
            measurements = load_garment_measurements(subject, outfit, root)
            if "garments" not in measurements:
                result.add_warning(f"Measurements for {subject}/{outfit} missing 'garments' key")
            elif not measurements["garments"]:
                result.add_warning(f"No garments found in measurements for {subject}/{outfit}")
            else:
                for i, garment in enumerate(measurements["garments"]):
                    if "cloth_number" not in garment:
                        result.add_warning(f"Garment {i} in {subject}/{outfit} missing cloth_number")
                    if "measurements" not in garment:
                        result.add_warning(f"Garment {i} in {subject}/{outfit} missing measurements")
        except json.JSONDecodeError as e:
            result.add_error(f"Invalid JSON in measurements for {subject}/{outfit}: {e}")

    return result


def validate_sequence_structure(
    subject: str, outfit: str, layer: str, sequence: str, root: Optional[Path] = None
) -> ValidationResult:
    result = ValidationResult()
    root = root or get_dataset_root()

    seq_path = get_sequence_path(subject, outfit, layer, sequence, root)
    if not seq_path.is_dir():
        result.add_error(f"Sequence directory does not exist: {seq_path}")
        return result

    archives = get_video_archives(subject, outfit, layer, sequence, root)
    if not archives:
        result.add_warning(f"No video archives found in {seq_path}")
    else:
        for archive_type, archive_path in archives.items():
            if not archive_path.is_file():
                result.add_error(f"Video archive missing: {archive_path}")
            else:
                result.add_info(f"Found {archive_type} archive: {archive_path.name}")

    fg_mask_dir = get_foreground_mask_dir(subject, outfit, root)
    if not fg_mask_dir.is_dir():
        result.add_warning(f"Foreground mask directory missing: {fg_mask_dir}")

    garment_mask_dir = get_garment_mask_dir(subject, outfit, root)
    if not garment_mask_dir.is_dir():
        result.add_warning(f"Garment mask directory missing: {garment_mask_dir}")

    return result


def validate_full_dataset(root: Optional[Path] = None) -> ValidationResult:
    result = ValidationResult()
    root = root or get_dataset_root()

    root_result = validate_dataset_root(root)
    result.errors.extend(root_result.errors)
    result.warnings.extend(root_result.warnings)
    result.info.extend(root_result.info)

    if not root_result.is_valid:
        return result

    camera_result = validate_camera_files(root)
    result.errors.extend(camera_result.errors)
    result.warnings.extend(camera_result.warnings)
    result.info.extend(camera_result.info)

    subjects = get_subjects(root)
    result.add_info(f"Found {len(subjects)} subjects")

    for subject in subjects:
        subject_result = validate_subject_metadata(subject, root)
        result.errors.extend(subject_result.errors)
        result.warnings.extend(subject_result.warnings)

        outfits = get_outfits(subject, root)
        for outfit in outfits:
            outfit_result = validate_outfit_metadata(subject, outfit, root)
            result.errors.extend(outfit_result.errors)
            result.warnings.extend(outfit_result.warnings)

            layers = get_layers(subject, outfit, root)
            for layer in layers:
                sequences = get_sequences(subject, outfit, layer, root)
                for sequence in sequences:
                    seq_result = validate_sequence_structure(
                        subject, outfit, layer, sequence, root
                    )
                    result.errors.extend(seq_result.errors)
                    result.warnings.extend(seq_result.warnings)

    return result


def find_missing_files(
    subject: str, outfit: str, layer: str, sequence: str, root: Optional[Path] = None
) -> dict[str, list[str]]:
    root = root or get_dataset_root()
    missing = {
        "video_archives": [],
        "foreground_masks": [],
        "garment_masks": [],
        "garment_images": [],
    }

    archives = get_video_archives(subject, outfit, layer, sequence, root)
    expected_archives = ["bolt.zip", "rpi.zip"]
    for archive_name in expected_archives:
        archive_type = archive_name.replace(".zip", "")
        if archive_type not in archives:
            missing["video_archives"].append(archive_name)

    fg_mask_dir = get_foreground_mask_dir(subject, outfit, root)
    if not fg_mask_dir.is_dir():
        missing["foreground_masks"].append(f"Directory missing: {fg_mask_dir}")

    garment_mask_dir = get_garment_mask_dir(subject, outfit, root)
    if not garment_mask_dir.is_dir():
        missing["garment_masks"].append(f"Directory missing: {garment_mask_dir}")

    garment_img_dir = get_garment_image_dir(subject, outfit, root)
    if not garment_img_dir.is_dir():
        missing["garment_images"].append(f"Directory missing: {garment_img_dir}")

    return missing


def check_data_consistency(root: Optional[Path] = None) -> dict[str, Any]:
    root = root or get_dataset_root()
    consistency = {
        "subjects_in_info_csv": 0,
        "subjects_in_videos": 0,
        "subjects_with_descriptions": 0,
        "subjects_with_styles": 0,
        "mismatched_subjects": [],
    }

    subject_info = load_subject_info(root)
    consistency["subjects_in_info_csv"] = len(subject_info)

    video_subjects = get_subjects(root)
    consistency["subjects_in_videos"] = len(video_subjects)

    garments_dir = root / "garments"
    desc_dir = garments_dir / "descriptions"
    if desc_dir.is_dir():
        desc_subjects = [f.stem for f in desc_dir.iterdir() if f.is_file() and f.suffix == ".json"]
        consistency["subjects_with_descriptions"] = len(desc_subjects)

    styles_dir = garments_dir / "styles"
    if styles_dir.is_dir():
        style_subjects = [
            f.stem.replace("_styling_labels", "")
            for f in styles_dir.iterdir()
            if f.is_file() and f.name.endswith("_styling_labels.json")
        ]
        consistency["subjects_with_styles"] = len(style_subjects)

    info_subjects = set(subject_info.keys())
    video_subjects_set = set(video_subjects)
    if info_subjects != video_subjects_set:
        consistency["mismatched_subjects"] = list(info_subjects.symmetric_difference(video_subjects_set))

    return consistency
