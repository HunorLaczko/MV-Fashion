"""Statistics and counting helpers for the MV-Fashion dataset.

This module provides functions to compute statistics about the dataset,
including counts of subjects, outfits, layers, sequences, garments, etc.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from paths import (
    get_subjects,
    get_outfits,
    get_layers,
    get_sequences,
    iter_sequences,
    get_video_archives,
    get_cloth_images,
)
from metadata import (
    load_subject_info,
    load_intrinsics,
    load_bolt_extrinsics,
    get_dataset_summary,
)
from garments import (
    get_all_garments_in_outfit,
    count_garments_per_outfit,
    get_garment_fabric_types,
    get_garment_elasticity_values,
)


def count_subjects(root: Optional[Path] = None) -> int:
    return len(get_subjects(root))


def count_outfits(subject: str, root: Optional[Path] = None) -> int:
    return len(get_outfits(subject, root))


def count_layers(subject: str, outfit: str, root: Optional[Path] = None) -> int:
    return len(get_layers(subject, outfit, root))


def count_sequences(
    subject: str, outfit: str, layer: str, root: Optional[Path] = None
) -> int:
    return len(get_sequences(subject, outfit, layer, root))


def count_total_outfits(root: Optional[Path] = None) -> int:
    total = 0
    for subject in get_subjects(root):
        total += count_outfits(subject, root)
    return total


def count_total_layers(root: Optional[Path] = None) -> int:
    total = 0
    for subject in get_subjects(root):
        for outfit in get_outfits(subject, root):
            total += count_layers(subject, outfit, root)
    return total


def count_total_sequences(root: Optional[Path] = None) -> int:
    return sum(1 for _ in iter_sequences(root))


def count_total_garments(root: Optional[Path] = None) -> int:
    total = 0
    for subject in get_subjects(root):
        for outfit in get_outfits(subject, root):
            garments = get_all_garments_in_outfit(subject, outfit, root)
            total += len(garments)
    return total


def count_garments_by_type(root: Optional[Path] = None) -> dict[str, int]:
    type_counts = {}
    for subject in get_subjects(root):
        for outfit in get_outfits(subject, root):
            garments = get_all_garments_in_outfit(subject, outfit, root)
            for garment in garments:
                garment_type = garment.get("type", "unknown")
                type_counts[garment_type] = type_counts.get(garment_type, 0) + 1
    return type_counts


def count_garments_by_fabric(root: Optional[Path] = None) -> dict[str, int]:
    fabric_counts = {}
    for subject in get_subjects(root):
        for outfit in get_outfits(subject, root):
            garments = get_all_garments_in_outfit(subject, outfit, root)
            for garment in garments:
                fabric = garment.get("fabric", "unknown")
                fabric_counts[fabric] = fabric_counts.get(fabric, 0) + 1
    return fabric_counts


def count_garments_by_layer(root: Optional[Path] = None) -> dict[int, int]:
    layer_counts = {}
    for subject in get_subjects(root):
        for outfit in get_outfits(subject, root):
            garments = get_all_garments_in_outfit(subject, outfit, root)
            for garment in garments:
                layer = garment.get("layer")
                if layer is not None:
                    layer_counts[layer] = layer_counts.get(layer, 0) + 1
    return layer_counts


def count_garment_images(
    subject: str, outfit: str, root: Optional[Path] = None
) -> int:
    return len(get_cloth_images(subject, outfit, root))


def count_total_garment_images(root: Optional[Path] = None) -> int:
    total = 0
    for subject in get_subjects(root):
        for outfit in get_outfits(subject, root):
            total += count_garment_images(subject, outfit, root)
    return total


def count_video_archives(root: Optional[Path] = None) -> dict[str, int]:
    counts = {"bolt": 0, "rpi": 0}
    for subject, outfit, layer, sequence in iter_sequences(root):
        archives = get_video_archives(subject, outfit, layer, sequence, root)
        for archive_type in archives:
            if archive_type in counts:
                counts[archive_type] += 1
    return counts


def get_outfit_statistics(
    subject: str, outfit: str, root: Optional[Path] = None
) -> dict[str, Any]:
    layers = get_layers(subject, outfit, root)
    garments = get_all_garments_in_outfit(subject, outfit, root)
    
    layer_stats = {}
    for layer in layers:
        sequences = get_sequences(subject, outfit, layer, root)
        layer_stats[layer] = {
            "sequence_count": len(sequences),
        }
    
    garment_types = [g.get("type") for g in garments if g.get("type")]
    garment_fabrics = [g.get("fabric") for g in garments if g.get("fabric")]
    
    return {
        "layer_count": len(layers),
        "layers": layer_stats,
        "garment_count": len(garments),
        "garment_types": garment_types,
        "garment_fabrics": list(set(garment_fabrics)),
    }


def get_subject_statistics(
    subject: str, root: Optional[Path] = None
) -> dict[str, Any]:
    outfits = get_outfits(subject, root)
    
    outfit_stats = {}
    total_layers = 0
    total_sequences = 0
    total_garments = 0
    
    for outfit in outfits:
        layers = get_layers(subject, outfit, root)
        total_layers += len(layers)
        
        outfit_seq_count = 0
        for layer in layers:
            sequences = get_sequences(subject, outfit, layer, root)
            outfit_seq_count += len(sequences)
        total_sequences += outfit_seq_count
        
        garments = get_all_garments_in_outfit(subject, outfit, root)
        total_garments += len(garments)
        
        outfit_stats[outfit] = {
            "layer_count": len(layers),
            "sequence_count": outfit_seq_count,
            "garment_count": len(garments),
        }
    
    return {
        "outfit_count": len(outfits),
        "outfits": outfit_stats,
        "total_layers": total_layers,
        "total_sequences": total_sequences,
        "total_garments": total_garments,
    }


def get_full_dataset_statistics(root: Optional[Path] = None) -> dict[str, Any]:
    subjects = get_subjects(root)
    
    subject_stats = {}
    total_outfits = 0
    total_layers = 0
    total_sequences = 0
    total_garments = 0
    
    for subject in subjects:
        stats = get_subject_statistics(subject, root)
        subject_stats[subject] = stats
        total_outfits += stats["outfit_count"]
        total_layers += stats["total_layers"]
        total_sequences += stats["total_sequences"]
        total_garments += stats["total_garments"]
    
    garment_type_counts = count_garments_by_type(root)
    garment_fabric_counts = count_garments_by_fabric(root)
    garment_layer_counts = count_garments_by_layer(root)
    video_archive_counts = count_video_archives(root)
    
    return {
        "subject_count": len(subjects),
        "outfit_count": total_outfits,
        "layer_count": total_layers,
        "sequence_count": total_sequences,
        "garment_count": total_garments,
        "garment_type_distribution": garment_type_counts,
        "garment_fabric_distribution": garment_fabric_counts,
        "garment_layer_distribution": garment_layer_counts,
        "video_archive_counts": video_archive_counts,
        "subjects": subject_stats,
    }


def get_dataset_summary_report(root: Optional[Path] = None) -> str:
    stats = get_full_dataset_statistics(root)
    
    lines = [
        "=" * 60,
        "DATASET SUMMARY REPORT",
        "=" * 60,
        f"Total subjects: {stats['subject_count']}",
        f"Total outfits: {stats['outfit_count']}",
        f"Total layers: {stats['layer_count']}",
        f"Total sequences: {stats['sequence_count']}",
        f"Total garments: {stats['garment_count']}",
        "",
        "Garment types:",
    ]
    
    for garment_type, count in sorted(stats["garment_type_distribution"].items()):
        lines.append(f"  {garment_type}: {count}")
    
    lines.append("")
    lines.append("Garment fabrics:")
    for fabric, count in sorted(stats["garment_fabric_distribution"].items()):
        lines.append(f"  {fabric}: {count}")
    
    lines.append("")
    lines.append("Garment layers:")
    for layer, count in sorted(stats["garment_layer_distribution"].items()):
        lines.append(f"  Layer {layer}: {count}")
    
    lines.append("")
    lines.append("Video archives:")
    for archive_type, count in sorted(stats["video_archive_counts"].items()):
        lines.append(f"  {archive_type}: {count}")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)


def get_average_sequences_per_layer(root: Optional[Path] = None) -> float:
    total_sequences = 0
    total_layers = 0
    
    for subject in get_subjects(root):
        for outfit in get_outfits(subject, root):
            layers = get_layers(subject, outfit, root)
            total_layers += len(layers)
            for layer in layers:
                sequences = get_sequences(subject, outfit, layer, root)
                total_sequences += len(sequences)
    
    return total_sequences / total_layers if total_layers > 0 else 0.0


def get_average_garments_per_outfit(root: Optional[Path] = None) -> float:
    total_garments = 0
    total_outfits = 0
    
    for subject in get_subjects(root):
        for outfit in get_outfits(subject, root):
            total_outfits += 1
            garments = get_all_garments_in_outfit(subject, outfit, root)
            total_garments += len(garments)
    
    return total_garments / total_outfits if total_outfits > 0 else 0.0


def get_most_common_garment_type(root: Optional[Path] = None) -> Optional[str]:
    type_counts = count_garments_by_type(root)
    if not type_counts:
        return None
    return max(type_counts, key=type_counts.get)


def get_most_common_fabric(root: Optional[Path] = None) -> Optional[str]:
    fabric_counts = count_garments_by_fabric(root)
    if not fabric_counts:
        return None
    return max(fabric_counts, key=fabric_counts.get)
