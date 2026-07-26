"""Path resolution and navigation helpers for the MV-Fashion dataset.

This module provides functions to navigate the dataset structure and resolve
paths to various data components (videos, masks, garments, cameras, etc.).

Dataset structure:
    <dataset_root>/
    ├── info.csv
    ├── annotations/masks/{foreground,garment}/subject_XXXX/...
    ├── cameras/{intrinsics.json,extrinsics_bolts.json}
    ├── garments/{images,masks,descriptions,measurements,styles}/...
    └── videos/subject_XXXX/outfit_X/layer_X/sequence_X/{bolt.zip,rpi.zip}
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Iterator, Optional


SUBJECT_PATTERN = re.compile(r"^subject_(\d{4})$")
OUTFIT_PATTERN = re.compile(r"^outfit_(\d+)$")
LAYER_PATTERN = re.compile(r"^layer_(\d+)$")
SEQUENCE_PATTERN = re.compile(r"^sequence_(\d+)$")
CLOTH_PATTERN = re.compile(r"^cloth_(\d+)_(front|back)_(\d+)$")


def get_dataset_root() -> Path:
    """Get the dataset root directory.
    
    Checks for MV_FASHION_DATASET_ROOT environment variable first,
    then falls back to ./mv_fashion_dataset in the current directory.
    """
    env_path = os.environ.get("MV_FASHION_DATASET_ROOT")
    if env_path:
        return Path(env_path)
    return Path("./mv_fashion_dataset")


def get_subjects(root: Optional[Path] = None) -> list[str]:
    root = root or get_dataset_root()
    videos_dir = root / "videos"
    if not videos_dir.is_dir():
        return []
    return sorted(
        d.name for d in videos_dir.iterdir()
        if d.is_dir() and SUBJECT_PATTERN.match(d.name)
    )


def get_subject_id(subject_name: str) -> int:
    match = SUBJECT_PATTERN.match(subject_name)
    if not match:
        raise ValueError(f"Invalid subject name: {subject_name}")
    return int(match.group(1))


def get_outfits(subject: str, root: Optional[Path] = None) -> list[str]:
    root = root or get_dataset_root()
    outfit_dir = root / "videos" / subject
    if not outfit_dir.is_dir():
        return []
    return sorted(
        d.name for d in outfit_dir.iterdir()
        if d.is_dir() and OUTFIT_PATTERN.match(d.name)
    )


def get_layers(subject: str, outfit: str, root: Optional[Path] = None) -> list[str]:
    root = root or get_dataset_root()
    layer_dir = root / "videos" / subject / outfit
    if not layer_dir.is_dir():
        return []
    return sorted(
        d.name for d in layer_dir.iterdir()
        if d.is_dir() and LAYER_PATTERN.match(d.name)
    )


def get_sequences(
    subject: str, outfit: str, layer: str, root: Optional[Path] = None
) -> list[str]:
    root = root or get_dataset_root()
    seq_dir = root / "videos" / subject / outfit / layer
    if not seq_dir.is_dir():
        return []
    return sorted(
        d.name for d in seq_dir.iterdir()
        if d.is_dir() and SEQUENCE_PATTERN.match(d.name)
    )


def iter_sequences(root: Optional[Path] = None) -> Iterator[tuple[str, str, str, str]]:
    root = root or get_dataset_root()
    for subject in get_subjects(root):
        for outfit in get_outfits(subject, root):
            for layer in get_layers(subject, outfit, root):
                for sequence in get_sequences(subject, outfit, layer, root):
                    yield subject, outfit, layer, sequence


def get_sequence_path(
    subject: str, outfit: str, layer: str, sequence: str, root: Optional[Path] = None
) -> Path:
    root = root or get_dataset_root()
    return root / "videos" / subject / outfit / layer / sequence


def get_video_archives(
    subject: str, outfit: str, layer: str, sequence: str, root: Optional[Path] = None
) -> dict[str, Path]:
    seq_path = get_sequence_path(subject, outfit, layer, sequence, root)
    archives = {}
    for name in ("bolt.zip", "rpi.zip"):
        archive_path = seq_path / name
        if archive_path.is_file():
            archives[name.replace(".zip", "")] = archive_path
    return archives


def get_info_csv(root: Optional[Path] = None) -> Path:
    root = root or get_dataset_root()
    return root / "info.csv"


def get_intrinsics_json(root: Optional[Path] = None) -> Path:
    root = root or get_dataset_root()
    return root / "cameras" / "intrinsics.json"


def get_extrinsics_json(root: Optional[Path] = None) -> Path:
    root = root or get_dataset_root()
    return root / "cameras" / "extrinsics_bolts.json"


def get_foreground_mask_dir(
    subject: str, outfit: str, root: Optional[Path] = None
) -> Path:
    root = root or get_dataset_root()
    return root / "annotations" / "masks" / "foreground" / subject / outfit


def get_garment_mask_dir(
    subject: str, outfit: str, root: Optional[Path] = None
) -> Path:
    root = root or get_dataset_root()
    return root / "annotations" / "masks" / "garment" / subject / outfit


def get_garment_image_dir(
    subject: str, outfit: str, root: Optional[Path] = None
) -> Path:
    root = root or get_dataset_root()
    return root / "garments" / "images" / subject / outfit


def get_garment_mask_image_dir(
    subject: str, outfit: str, root: Optional[Path] = None
) -> Path:
    root = root or get_dataset_root()
    return root / "garments" / "masks" / subject / outfit


def get_garment_descriptions_json(
    subject: str, root: Optional[Path] = None
) -> Path:
    root = root or get_dataset_root()
    return root / "garments" / "descriptions" / f"{subject}.json"


def get_garment_measurements_json(
    subject: str, outfit: str, root: Optional[Path] = None
) -> Path:
    root = root or get_dataset_root()
    subject_num = get_subject_id(subject)
    outfit_match = OUTFIT_PATTERN.match(outfit)
    outfit_num = int(outfit_match.group(1)) if outfit_match else 0
    return root / "garments" / "measurements" / f"{subject_num:04d}_{outfit}.json"


def get_styling_labels_json(
    subject: str, root: Optional[Path] = None
) -> Path:
    root = root or get_dataset_root()
    subject_num = get_subject_id(subject)
    return root / "garments" / "styles" / f"{subject_num:04d}_styling_labels.json"


def parse_cloth_filename(filename: str) -> Optional[dict]:
    match = CLOTH_PATTERN.match(Path(filename).stem)
    if not match:
        return None
    return {
        "cloth_number": int(match.group(1)),
        "view": match.group(2),
        "capture_index": int(match.group(3)),
    }


def get_cloth_images(
    subject: str, outfit: str, root: Optional[Path] = None
) -> list[dict]:
    img_dir = get_garment_image_dir(subject, outfit, root)
    if not img_dir.is_dir():
        return []
    results = []
    for f in sorted(img_dir.iterdir()):
        if f.is_file() and f.suffix.lower() in (".png", ".jpg", ".jpeg"):
            parsed = parse_cloth_filename(f.name)
            if parsed:
                results.append({**parsed, "path": f})
    return results


def get_cameras(root: Optional[Path] = None) -> dict:
    import json
    intrinsics_path = get_intrinsics_json(root)
    if not intrinsics_path.is_file():
        return {}
    with intrinsics_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_bolt_extrinsics(root: Optional[Path] = None) -> dict:
    import json
    extrinsics_path = get_extrinsics_json(root)
    if not extrinsics_path.is_file():
        return {}
    with extrinsics_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_sequence_path(path: Path) -> Optional[dict]:
    parts = path.parts
    subject = outfit = layer = sequence = None
    for part in parts:
        if SUBJECT_PATTERN.match(part):
            subject = part
        elif OUTFIT_PATTERN.match(part):
            outfit = part
        elif LAYER_PATTERN.match(part):
            layer = part
        elif SEQUENCE_PATTERN.match(part):
            sequence = part
    if all([subject, outfit, layer, sequence]):
        return {
            "subject": subject,
            "outfit": outfit,
            "layer": layer,
            "sequence": sequence,
        }
    return None
