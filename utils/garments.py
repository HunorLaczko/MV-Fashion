"""Garment data helpers for the MV-Fashion dataset.

This module provides functions to load and query garment-related data,
including descriptions, measurements, and styling labels.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from paths import (
    get_garment_descriptions_json,
    get_garment_measurements_json,
    get_styling_labels_json,
    get_subject_id,
    get_outfits,
    get_layers,
    get_sequences,
)


def load_garment_descriptions(
    subject: str, root: Optional[Path] = None
) -> dict[str, Any]:
    desc_path = get_garment_descriptions_json(subject, root)
    if not desc_path.is_file():
        return {}
    with desc_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_garment_description(
    subject: str, outfit: str, cloth: str, root: Optional[Path] = None
) -> Optional[str]:
    descriptions = load_garment_descriptions(subject, root)
    outfits = descriptions.get("outfits", {})
    outfit_data = outfits.get(outfit, {})
    cloth_data = outfit_data.get(cloth, {})
    return cloth_data.get("description")


def get_all_garment_descriptions(
    subject: str, root: Optional[Path] = None
) -> dict[str, dict[str, str]]:
    descriptions = load_garment_descriptions(subject, root)
    result = {}
    outfits = descriptions.get("outfits", {})
    for outfit_name, outfit_data in outfits.items():
        result[outfit_name] = {}
        for cloth_name, cloth_data in outfit_data.items():
            if isinstance(cloth_data, dict) and "description" in cloth_data:
                result[outfit_name][cloth_name] = cloth_data["description"]
    return result


def load_garment_measurements(
    subject: str, outfit: str, root: Optional[Path] = None
) -> dict[str, Any]:
    meas_path = get_garment_measurements_json(subject, outfit, root)
    if not meas_path.is_file():
        return {}
    with meas_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_garment_measurements(
    subject: str, outfit: str, cloth_number: int, root: Optional[Path] = None
) -> Optional[dict]:
    measurements = load_garment_measurements(subject, outfit, root)
    garments = measurements.get("garments", [])
    for garment in garments:
        if garment.get("cloth_number") == cloth_number:
            return garment.get("measurements")
    return None


def get_garment_properties(
    subject: str, outfit: str, cloth_number: int, root: Optional[Path] = None
) -> Optional[dict]:
    measurements = load_garment_measurements(subject, outfit, root)
    garments = measurements.get("garments", [])
    for garment in garments:
        if garment.get("cloth_number") == cloth_number:
            return {
                "type": garment.get("type"),
                "group": garment.get("group"),
                "fabric": garment.get("fabric"),
                "elasticity": garment.get("elasticity"),
                "layer": garment.get("layer"),
                "fit": garment.get("fit"),
            }
    return None


def get_all_garments_in_outfit(
    subject: str, outfit: str, root: Optional[Path] = None
) -> list[dict]:
    measurements = load_garment_measurements(subject, outfit, root)
    return measurements.get("garments", [])


def load_styling_labels(
    subject: str, root: Optional[Path] = None
) -> dict[str, Any]:
    styles_path = get_styling_labels_json(subject, root)
    if not styles_path.is_file():
        return {}
    with styles_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_styling_label(
    subject: str, outfit: str, layer: str, sequence: str, root: Optional[Path] = None
) -> Optional[dict]:
    styles = load_styling_labels(subject, root)
    outfits = styles.get("outfits", {})
    outfit_data = outfits.get(outfit, {})
    layers = outfit_data.get(layer, {})
    sequences = layers.get(sequence, {})
    return sequences.get("style")


def get_layer_styles(
    subject: str, outfit: str, layer: str, sequence: str, root: Optional[Path] = None
) -> Optional[dict]:
    style = get_styling_label(subject, outfit, layer, sequence, root)
    if style is None:
        return None
    return style.get(layer)


def get_all_styling_labels_for_sequence(
    subject: str, outfit: str, layer: str, sequence: str, root: Optional[Path] = None
) -> dict[str, dict]:
    style = get_styling_label(subject, outfit, layer, sequence, root)
    if style is None:
        return {}
    return style


def get_cloth_type_mapping(root: Optional[Path] = None) -> dict[str, str]:
    return {
        "shirt-blouse": "top",
        "t-shirt": "top",
        "sweater": "top",
        "jacket": "outerwear",
        "coat": "outerwear",
        "vest": "outerwear",
        "pants": "bottom",
        "shorts": "bottom",
        "jeans": "bottom",
        "skirt": "bottom",
        "dress": "full_body",
    }


def get_garment_layer_info(
    subject: str, outfit: str, root: Optional[Path] = None
) -> dict[str, list[int]]:
    outfits = get_outfits(subject, root)
    if outfit not in outfits:
        return {}
    
    layer_garments = {}
    garments = get_all_garments_in_outfit(subject, outfit, root)
    for garment in garments:
        layer = garment.get("layer")
        cloth_num = garment.get("cloth_number")
        if layer is not None and cloth_num is not None:
            layer_key = f"layer_{layer}"
            if layer_key not in layer_garments:
                layer_garments[layer_key] = []
            layer_garments[layer_key].append(cloth_num)
    
    return layer_garments


def get_garment_fabric_types(
    subject: str, outfit: str, root: Optional[Path] = None
) -> list[str]:
    garments = get_all_garments_in_outfit(subject, outfit, root)
    fabrics = set()
    for garment in garments:
        fabric = garment.get("fabric")
        if fabric:
            fabrics.add(fabric)
    return sorted(fabrics)


def get_garment_elasticity_values(
    subject: str, outfit: str, root: Optional[Path] = None
) -> list[int]:
    garments = get_all_garments_in_outfit(subject, outfit, root)
    elasticities = []
    for garment in garments:
        elasticity = garment.get("elasticity")
        if elasticity is not None:
            elasticities.append(elasticity)
    return sorted(set(elasticities))


def count_garments_per_outfit(
    subject: str, root: Optional[Path] = None
) -> dict[str, int]:
    outfits = get_outfits(subject, root)
    result = {}
    for outfit in outfits:
        garments = get_all_garments_in_outfit(subject, outfit, root)
        result[outfit] = len(garments)
    return result


def get_garment_measurements_summary(
    subject: str, outfit: str, root: Optional[Path] = None
) -> dict[str, dict]:
    garments = get_all_garments_in_outfit(subject, outfit, root)
    result = {}
    for garment in garments:
        cloth_num = garment.get("cloth_number")
        if cloth_num is not None:
            result[f"cloth_{cloth_num}"] = {
                "type": garment.get("type"),
                "measurements": garment.get("measurements", {}),
            }
    return result
