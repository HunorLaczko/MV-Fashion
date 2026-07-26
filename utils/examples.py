#!/usr/bin/env python3
"""Example usage of the MV-Fashion dataset helper scripts.

This script demonstrates how to use the various helper modules to navigate,
query, and analyze the dataset. Every example uses the helper modules
directly (paths, metadata, garments, statistics, validation) without any
unified loader class.
"""

from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

from paths import (
    iter_sequences,
    get_video_archives,
    get_foreground_mask_dir,
    get_garment_mask_dir,
    get_subjects,
    get_outfits,
    get_layers,
    get_sequences,
    get_sequence_path,
)
from metadata import (
    get_subjects_by_gender,
    get_subjects_by_height_range,
    get_subject_info,
    get_rpi_cameras,
    get_bolt_cameras,
    get_camera_K,
    get_camera_distortion,
    load_intrinsics,
)
from garments import (
    get_garment_description,
    get_garment_properties,
    get_all_garments_in_outfit,
)
from validation import validate_full_dataset, validate_subject_metadata
from statistics import (
    count_subjects,
    count_total_outfits,
    count_total_layers,
    count_total_sequences,
    count_total_garments,
    count_garments_by_type,
    count_garments_by_fabric,
    count_video_archives,
    get_dataset_summary_report,
)


def example_basic_navigation():
    """Example: Basic dataset navigation."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Dataset Navigation")
    print("=" * 60)

    subjects = get_subjects()
    print(f"\nTotal subjects: {len(subjects)}")
    print(f"First 5 subjects: {subjects[:5]}")

    if subjects:
        subject = subjects[0]
        outfits = get_outfits(subject)
        print(f"\nOutfits for {subject}: {outfits}")

        if outfits:
            outfit = outfits[0]
            layers = get_layers(subject, outfit)
            print(f"Layers for {subject}/{outfit}: {layers}")

            if layers:
                layer = layers[0]
                sequences = get_sequences(subject, outfit, layer)
                print(f"Sequences for {subject}/{outfit}/{layer}: {sequences}")
        else:
            print(f"  (no videos / outfits found for {subject} - download videos to navigate)")
    else:
        print("  (no videos found - download the dataset with download_mv_fashion.py first)")

    print(f"\nTotal sequences in dataset: {count_total_sequences()}")


def example_subject_info():
    """Example: Querying subject information."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Subject Information")
    print("=" * 60)

    subject = "subject_0001"
    info = get_subject_info(subject)
    print(f"\n{subject}:")
    print(f"  Gender: {info['gender']}")
    print(f"  Height: {info['height']} cm")
    print(f"  Weight: {info['weight']} kg")

    male_subjects = get_subjects_by_gender("Male")
    print(f"\nMale subjects: {len(male_subjects)}")
    print(f"First 5: {male_subjects[:5]}")

    tall_subjects = get_subjects_by_height_range(180, 190)
    print(f"\nSubjects 180-190cm tall: {len(tall_subjects)}")


def example_garment_data():
    """Example: Accessing garment data."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Garment Data")
    print("=" * 60)

    subject = "subject_0001"
    outfit = "outfit_1"

    garments = get_all_garments_in_outfit(subject, outfit)
    print(f"\nGarments in {subject}/{outfit}: {len(garments)}")

    for garment in garments:
        cloth_num = garment.get("cloth_number")
        garment_type = garment.get("type")
        fabric = garment.get("fabric")
        print(f"\n  Cloth {cloth_num}:")
        print(f"    Type: {garment_type}")
        print(f"    Fabric: {fabric}")
        print(f"    Layer: {garment.get('layer')}")

        measurements = garment.get("measurements", {})
        if measurements:
            print(f"    Measurements:")
            for key, value in list(measurements.items())[:5]:
                print(f"      {key}: {value}")

    description = get_garment_description(subject, outfit, "cloth_1")
    if description:
        print(f"\n  Cloth 1 description (first 100 chars):")
        print(f"    {description[:100]}...")


def example_camera_data():
    """Example: Accessing camera data."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Camera Data")
    print("=" * 60)

    rpi_cameras = get_rpi_cameras()
    bolt_cameras = get_bolt_cameras()

    print(f"\nRPI cameras: {len(rpi_cameras)}")
    print(f"First 5: {rpi_cameras[:5]}")

    print(f"\nBolt cameras: {len(bolt_cameras)}")
    print(f"First 5: {bolt_cameras[:5]}")

    camera = "rpi_01"
    intrinsics = load_intrinsics().get(camera)
    if intrinsics:
        print(f"\n{camera} intrinsics:")
        print(f"  Image shape: {intrinsics.get('image_shape')}")
        print(f"  Reprojection error: {intrinsics.get('reproj_error_rms'):.4f}")

    K = get_camera_K(camera, use_undistorted=True)
    if K is not None:
        print(f"\n{camera} K matrix (undistorted):")
        print(f"  {K}")


def example_video_archives():
    """Example: Accessing video archives."""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Video Archives")
    print("=" * 60)

    subject = "subject_0001"
    outfit = "outfit_1"
    layer = "layer_1"
    sequence = "sequence_1"

    archives = get_video_archives(subject, outfit, layer, sequence)
    print(f"\nVideo archives for {subject}/{outfit}/{layer}/{sequence}:")
    for archive_type, archive_path in archives.items():
        print(f"  {archive_type}: {archive_path}")
        if archive_path.exists():
            size_mb = archive_path.stat().st_size / (1024 * 1024)
            print(f"    Size: {size_mb:.2f} MB")

    print("\nIterating through sequences (first 5):")
    for i, (subj, outf, lay, seq) in enumerate(iter_sequences()):
        if i >= 5:
            break
        print(f"  {subj}/{outf}/{lay}/{seq}")


def example_undistort_images():
    """Example: Removing lens distortion using camera intrinsics."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Undistort Images")
    print("=" * 60)

    from visualize_dataset import undistort_frame, load_frame_from_zip, visualize_undistortion

    subject = "subject_0001"
    outfit = "outfit_1"
    layer = "layer_1"
    sequence = "sequence_1"
    camera = "rpi_01"
    frame_idx = 0

    K = get_camera_K(camera, use_undistorted=False)
    dist = get_camera_distortion(camera)
    K_new = get_camera_K(camera, use_undistorted=True)
    print(f"\nCamera {camera}:")
    print(f"  K (original):\n{K}")
    print(f"  K_new (dataset's rectified intrinsics):\n{K_new}")
    print(f"  Distortion coefficients: {dist}")
    print()
    print("  Note: K_new is the dataset's rectified intrinsics (used for")
    print("  stereo / multi-view workflows). For monocular undistortion we")
    print("  compute a centred K_new with cv2.getOptimalNewCameraMatrix - the")
    print("  raw K_new is *not* used directly because its principal point is")
    print("  off-centre and would shift the rectified image off the canvas.")

    if K is None or dist is None or K_new is None:
        print("  Intrinsics not available; skipping undistortion demo.")
        return

    seq_path = get_sequence_path(subject, outfit, layer, sequence)
    archive = seq_path / "rpi.zip"
    member_name = f"{camera}/{frame_idx:05d}.avif"

    if not archive.is_file():
        print(f"\nVideo archive not found: {archive}")
        print("  Download it (see the tutorial notebook) to run the live demo.")
        return

    frame = load_frame_from_zip(archive, member_name)
    if frame is None:
        print(f"\nCould not load {member_name} from {archive}")
        return

    undistorted = undistort_frame(frame, camera)
    if undistorted is None:
        return

    mean_abs_diff = float(np.abs(undistorted.astype(float) - frame.astype(float)).mean())
    valid_fraction = float((undistorted.sum(axis=2) > 0).mean())
    print(f"\nFrame loaded: {frame.shape}")
    print(f"Undistorted frame: {undistorted.shape}")
    print(f"Mean absolute pixel difference: {mean_abs_diff:.2f}")
    print(f"Valid (non-empty) pixel fraction: {valid_fraction:.3f}")

    # Show the side-by-side comparison in the browser via Plotly
    visualize_undistortion(
        subject, outfit, layer, sequence,
        camera=camera, frame_idx=frame_idx,
    )


def example_validation():
    """Example: Validating dataset structure."""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Dataset Validation")
    print("=" * 60)

    print("\nValidating subject_0001...")
    result = validate_subject_metadata("subject_0001")
    print(f"  Valid: {result.is_valid}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Warnings: {len(result.warnings)}")

    if result.errors:
        print("\n  Errors:")
        for err in result.errors[:3]:
            print(f"    - {err}")

    if result.warnings:
        print("\n  Warnings:")
        for warn in result.warnings[:3]:
            print(f"    - {warn}")


def example_statistics():
    """Example: Computing dataset statistics."""
    print("\n" + "=" * 60)
    print("EXAMPLE 8: Dataset Statistics")
    print("=" * 60)

    print(f"\nTotal subjects: {count_subjects()}")
    print(f"Total outfits: {count_total_outfits()}")
    print(f"Total layers: {count_total_layers()}")
    print(f"Total sequences: {count_total_sequences()}")
    print(f"Total garments: {count_total_garments()}")

    print("\nGarment types:")
    type_counts = count_garments_by_type()
    for garment_type, count in sorted(type_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {garment_type}: {count}")

    print("\nGarment fabrics:")
    fabric_counts = count_garments_by_fabric()
    for fabric, count in sorted(fabric_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {fabric}: {count}")

    print("\nVideo archives:")
    archive_counts = count_video_archives()
    for archive_type, count in archive_counts.items():
        print(f"  {archive_type}: {count}")


def example_segmentation_masks():
    """Example: Accessing segmentation masks."""
    print("\n" + "=" * 60)
    print("EXAMPLE 9: Segmentation Masks")
    print("=" * 60)

    subject = "subject_0001"
    outfit = "outfit_1"

    fg_mask_dir = get_foreground_mask_dir(subject, outfit)
    print(f"\nForeground mask directory: {fg_mask_dir}")
    print(f"  Exists: {fg_mask_dir.exists()}")

    garment_mask_dir = get_garment_mask_dir(subject, outfit)
    print(f"\nGarment mask directory: {garment_mask_dir}")
    print(f"  Exists: {garment_mask_dir.exists()}")

    if garment_mask_dir.exists():
        cloth_dirs = sorted([d for d in garment_mask_dir.iterdir()
                            if d.is_dir() and d.name.startswith("cloth_")])
        print(f"\n  Available garment masks: {[d.name for d in cloth_dirs]}")


def example_full_report():
    """Example: Generating a full dataset report."""
    print("\n" + "=" * 60)
    print("EXAMPLE 10: Full Dataset Report")
    print("=" * 60)

    report = get_dataset_summary_report()
    print("\n" + report)


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("MV-Fashion Dataset Helper Scripts - Examples")
    print("=" * 60)

    example_basic_navigation()
    example_subject_info()
    example_garment_data()
    example_camera_data()
    example_undistort_images()
    example_video_archives()
    example_validation()
    example_statistics()
    example_segmentation_masks()
    example_full_report()

    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
