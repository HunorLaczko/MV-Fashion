#!/usr/bin/env python3
"""Visualization tools for the MV-Fashion dataset (Plotly-based).

Every plot is rendered with Plotly and shown in the default browser via
``fig.show()`` rather than being saved to disk.

Usage:
    python visualize_dataset.py --help
    python visualize_dataset.py --sequence subject_0001/outfit_1/layer_1/sequence_1
    python visualize_dataset.py --garments subject_0001/outfit_1
    python visualize_dataset.py --stats
"""

import argparse
import sys
import zipfile
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from PIL import Image

# Register AVIF support if the optional plugin is installed.
try:
    import pillow_avif  # noqa: F401
except ImportError:
    pass

sys.path.insert(0, str(Path(__file__).parent))

from paths import (
    get_sequence_path,
    get_garment_image_dir,
    get_foreground_mask_dir,
    get_garment_mask_dir,
    get_cloth_images,
    get_dataset_root,
)
from metadata import (
    load_intrinsics,
    get_camera_K,
    get_camera_distortion,
    get_bolt_rotation,
    get_bolt_translation,
)
from garments import (
    get_all_garments_in_outfit,
    get_garment_description,
)
from statistics import (
    get_full_dataset_statistics,
    count_garments_by_type,
    count_garments_by_fabric,
)


# Use the browser as the default renderer. If no browser is available
# (e.g. on a headless server) Plotly will raise; the caller can override
# by setting the MV_FASHION_PLOTLY_RENDERER environment variable, e.g.
# "png" to write to a file or "json" to print the figure spec.
import os as _os
pio.renderers.default = _os.environ.get("MV_FASHION_PLOTLY_RENDERER", "browser")


def load_frame_from_zip(
    archive_path: Path,
    member_name: str,
) -> Optional[np.ndarray]:
    """Load a single frame from a zip archive efficiently."""
    try:
        with zipfile.ZipFile(archive_path, "r") as zf:
            with zf.open(member_name) as f:
                img = Image.open(f)
                img.load()
                return np.array(img)
    except Exception as e:
        print(f"Error loading {member_name} from {archive_path}: {e}")
        return None


def undistort_frame(
    frame: np.ndarray,
    camera: str,
    root: Optional[Path] = None,
) -> Optional[np.ndarray]:
    """Remove lens distortion from a single frame using camera intrinsics.

    Uses the original camera matrix ``K`` and distortion coefficients
    ``dist`` to undistort the frame. The dataset-provided ``K_new`` is the
    rectified intrinsics for the dataset's stereo / multi-view pipeline
    and is *not* appropriate as the new camera matrix for monocular
    undistortion in ``cv2.undistort`` - its principal point is typically
    off-centre, so feeding it in directly shifts the rectified image off
    the canvas. We instead call ``cv2.getOptimalNewCameraMatrix`` to
    derive a K_new that keeps the rectified principal point at the image
    centre, which produces a properly centred undistorted output.
    """
    K = get_camera_K(camera, root, use_undistorted=False)
    dist = get_camera_distortion(camera, root)
    if K is None or dist is None:
        print(f"Missing intrinsics for camera {camera}; cannot undistort.")
        return None
    h, w = frame.shape[:2]
    result = cv2.getOptimalNewCameraMatrix(K, dist, (w, h), 1, (w, h))
    K_new = result[0] if isinstance(result, tuple) else result
    return cv2.undistort(frame, K, dist, None, K_new)


def _image_subplot(fig, frame, row, col, title, rows=1, cols=1):
    """Add a frame (HxWx3 uint8) to a plotly figure as an image subplot."""
    fig.add_trace(
        go.Image(z=frame),
        row=row + 1,
        col=col + 1,
    )
    fig.update_xaxes(visible=False, row=row + 1, col=col + 1)
    fig.update_yaxes(visible=False, row=row + 1, col=col + 1)


def _frame_for_mask(mask_path: Path) -> Optional[Path]:
    """Resolve the RGB frame that corresponds to a given mask path.

    Mask paths are expected to be absolute (as produced by the dataset's
    helper modules which anchor them at ``get_dataset_root()``). The matching
    video path has the form::

        <dataset_root>/videos/<subject>/<outfit>/<layer>/<sequence>/<camera>/<frame>.avif

    The cloth_N segment only exists for garment masks, so we strip it.
    """
    parts = list(mask_path.parts)
    # Find the "annotations/masks/<kind>" anchor in the absolute path.
    try:
        anchor = parts.index("annotations")
    except ValueError:
        return None
    if anchor + 5 >= len(parts) or parts[anchor + 1] != "masks":
        return None
    kind = parts[anchor + 2]
    if kind not in ("foreground", "garment"):
        return None
    subject = parts[anchor + 3]
    outfit = parts[anchor + 4]
    layer = parts[anchor + 5]
    sequence = parts[anchor + 6]
    # After <sequence> we may have cloth_N (garment mask) or the camera name
    # (foreground mask) before the camera dir.
    tail = parts[anchor + 7:]
    if tail and tail[0].startswith("cloth_"):
        tail = tail[1:]  # drop cloth_N
    if not tail or len(tail) < 2:
        return None
    camera = tail[0]
    frame_stem = mask_path.stem
    from paths import get_dataset_root
    rel = Path("videos") / subject / outfit / layer / sequence / camera / f"{frame_stem}.avif"
    return get_dataset_root() / rel


def visualize_undistortion(
    subject: str,
    outfit: str,
    layer: str,
    sequence: str,
    camera: str = "rpi_01",
    frame_idx: int = 0,
) -> None:
    """Show the original and undistorted frame side by side in the browser."""
    seq_path = get_sequence_path(subject, outfit, layer, sequence)
    archive = seq_path / "rpi.zip"
    frame_str = f"{frame_idx:05d}"
    member_name = f"{camera}/{frame_str}.avif"

    if not archive.is_file():
        print(f"Video archive not found: {archive}")
        return

    frame = load_frame_from_zip(archive, member_name)
    if frame is None:
        print(f"Could not load {member_name} from {archive}")
        return

    undistorted = undistort_frame(frame, camera)
    if undistorted is None:
        return

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Original (distorted)", "Undistorted (centred)"),
    )
    _image_subplot(fig, frame, 0, 0, "Original")
    _image_subplot(fig, undistorted, 0, 1, "Undistorted")
    fig.update_layout(
        title_text=f"Undistortion: {subject}/{outfit}/{layer}/{sequence} - {camera} - Frame {frame_idx}",
        showlegend=False,
    )
    fig.show()


def visualize_sequence_frames(
    subject: str,
    outfit: str,
    layer: str,
    sequence: str,
    frame_idx: int = 0,
    cameras: Optional[list[str]] = None,
) -> None:
    """Show frames from the first 8 RPi cameras of a sequence in the browser."""
    seq_path = get_sequence_path(subject, outfit, layer, sequence)
    rpi_archive = seq_path / "rpi.zip"
    bolt_archive = seq_path / "bolt.zip"

    rpi_cameras = cameras or [f"rpi_{i:02d}" for i in range(1, 9)]
    fig = make_subplots(
        rows=2, cols=4,
        subplot_titles=rpi_cameras[:8],
    )
    fig.update_layout(
        title_text=f"{subject}/{outfit}/{layer}/{sequence} - Frame {frame_idx}",
        showlegend=False,
    )

    frame_str = f"{frame_idx:05d}"
    if rpi_archive.is_file():
        for idx, cam in enumerate(rpi_cameras[:8]):
            row, col = idx // 4, idx % 4
            member_name = f"{cam}/{frame_str}.avif"
            img = load_frame_from_zip(rpi_archive, member_name)
            if img is not None:
                _image_subplot(fig, img, row, col, cam)
            else:
                fig.add_annotation(
                    text="Not found", x=0.5, y=0.5, xref=f"x{idx+1}", yref=f"y{idx+1}",
                    showarrow=False, row=row + 1, col=col + 1,
                )
    fig.show()


def visualize_garment_images(
    subject: str,
    outfit: str,
) -> None:
    """Show every cloth's front_1/front_2/back_1/back_2 catalogue images."""
    cloth_images = get_cloth_images(subject, outfit)

    if not cloth_images:
        print(f"No garment images found for {subject}/{outfit}")
        return

    garments = get_all_garments_in_outfit(subject, outfit)
    cloth_nums = sorted(set(img["cloth_number"] for img in cloth_images))
    num_cloths = len(cloth_nums)

    fig = make_subplots(
        rows=num_cloths, cols=4,
        subplot_titles=[
            f"Cloth {n} (front_1)" for n in cloth_nums
        ] + [
            f"Cloth {n} (front_2)" for n in cloth_nums
        ] + [
            f"Cloth {n} (back_1)" for n in cloth_nums
        ] + [
            f"Cloth {n} (back_2)" for n in cloth_nums
        ],
    )
    fig.update_layout(
        title_text=f"{subject}/{outfit} - Garment Images",
        showlegend=False,
        height=400 * num_cloths,
    )

    for row_idx, cloth_num in enumerate(cloth_nums):
        garment = next((g for g in garments if g.get("cloth_number") == cloth_num), None)
        garment_type = garment.get("type", "unknown") if garment else "unknown"
        for col_idx, key in enumerate([("front", 1), ("front", 2), ("back", 1), ("back", 2)]):
            view, cap = key
            match = next(
                (im for im in cloth_images
                 if im["cloth_number"] == cloth_num and im["view"] == view
                 and im["capture_index"] == cap),
                None,
            )
            if match and match["path"].exists():
                _image_subplot(fig, np.array(Image.open(match["path"])), row_idx, col_idx, "")
            else:
                fig.add_annotation(
                    text="Not found", x=0.5, y=0.5,
                    xref=f"x{row_idx*4+col_idx+1}",
                    yref=f"y{row_idx*4+col_idx+1}",
                    showarrow=False, row=row_idx + 1, col=col_idx + 1,
                )
    fig.show()


def visualize_masks(
    subject: str,
    outfit: str,
    frame_idx: int = 0,
    layer: Optional[int] = None,
    sequence: Optional[str] = None,
    camera: str = "rpi_01",
) -> None:
    """Show segmentation masks in the browser.

    For per-garment masks we respect the dataset's layer hierarchy: if
    ``layer`` is given, only garments whose ``layer`` is <= ``layer`` are
    drawn (so a sequence stored in ``layer_1/sequence_X`` only shows
    layer-1 clothes, a ``layer_2`` sequence shows layers 1 and 2, etc.).
    If ``layer`` is not given we plot every garment in the outfit.

    The garment masks are drawn in two rows: the top row is the binary
    mask per cloth; the bottom row is the same mask painted in a distinct
    colour and overlaid on the corresponding frame (when a frame is
    available at the same path as the mask).
    """
    fg_mask_dir = get_foreground_mask_dir(subject, outfit)
    garment_mask_dir = get_garment_mask_dir(subject, outfit)

    if sequence is None:
        for layer_dir in sorted(p for p in garment_mask_dir.glob("layer_*") if p.is_dir()):
            for seq_dir in sorted(p for p in layer_dir.glob("sequence_*") if p.is_dir()):
                if any(seq_dir.glob("cloth_*")):
                    sequence = seq_dir.name
                    if layer is None:
                        layer = int(layer_dir.name.split("_")[-1])
                    break
            if sequence is not None:
                break
    if layer is None:
        layer = 1

    garments = get_all_garments_in_outfit(subject, outfit)
    eligible_garments = [g for g in garments if (g.get("layer") or 99) <= layer]
    eligible_cloth_nums = sorted(
        g.get("cloth_number") for g in eligible_garments
        if g.get("cloth_number") is not None
    )

    palette = [
        np.array([255,  80,  80], dtype=np.uint8),  # red
        np.array([ 80, 200,  80], dtype=np.uint8),  # green
        np.array([ 80, 130, 255], dtype=np.uint8),  # blue
        np.array([255, 200,  80], dtype=np.uint8),  # orange
        np.array([220,  80, 220], dtype=np.uint8),  # magenta
        np.array([ 80, 220, 220], dtype=np.uint8),  # cyan
        np.array([255, 130, 200], dtype=np.uint8),  # pink
    ]

    n_cols = max(len(eligible_cloth_nums), 1) + 1  # +1 for the foreground column
    fig = make_subplots(
        rows=2, cols=n_cols,
        subplot_titles=(
            [f"FG mask"] + [f"cloth_{c}" for c in eligible_cloth_nums]
            + [f"FG overlay"] + [f"cloth_{c} overlay" for c in eligible_cloth_nums]
        ),
    )
    fig.update_layout(
        title_text=(
            f"{subject}/{outfit} - Masks (layer<={layer}"
            f"{', ' + sequence if sequence else ''}, frame {frame_idx})"
        ),
        showlegend=False,
        height=600,
    )

    # Column 0: foreground mask + overlay
    fg_path = None
    if sequence is not None:
        candidate = fg_mask_dir / f"layer_{layer}" / sequence / camera
        if candidate.is_dir():
            fg_path = candidate
    if fg_path is None:
        fg_path = fg_mask_dir
    fg_mask_files = sorted(fg_path.glob("*.png")) if fg_path.is_dir() else sorted(fg_mask_dir.rglob("*.png"))
    if fg_mask_files:
        fg_mask_path = fg_mask_files[min(frame_idx, len(fg_mask_files) - 1)]
        fg_mask = np.array(Image.open(fg_mask_path))
        # Try to find a frame for overlay
        frame = None
        frame_candidate = _frame_for_mask(fg_mask_path)
        if frame_candidate is not None and frame_candidate.is_file():
            try:
                frame = np.array(Image.open(frame_candidate))
            except Exception:
                frame = None
        # Row 0: binary mask as a 3-channel image (so plotly shows it)
        mask_rgb = np.stack([fg_mask] * 3, axis=-1) if fg_mask.ndim == 2 else fg_mask
        _image_subplot(fig, mask_rgb, 0, 0, "FG mask")
        if frame is not None:
            # Resize mask to match frame if needed
            if fg_mask.shape[:2] != frame.shape[:2]:
                fg_mask = np.array(
                    Image.fromarray(fg_mask).resize(
                        (frame.shape[1], frame.shape[0]), Image.NEAREST
                    )
                )
            mask_bool = fg_mask > 127
            overlay = frame.copy()
            overlay[mask_bool] = (
                overlay[mask_bool] * 0.55 + np.array([0, 255, 0]) * 0.45
            ).astype(np.uint8)
            _image_subplot(fig, overlay, 1, 0, "FG overlay")
        else:
            fig.add_annotation(
                text="(no frame)", x=0.5, y=0.5, xref="x2", yref="y2",
                showarrow=False, row=2, col=1,
            )
    else:
        for col in (0, 0):
            fig.add_annotation(
                text="No foreground masks", x=0.5, y=0.5,
                xref="x1" if col == 0 else "x2",
                yref="y1" if col == 0 else "y2",
                showarrow=False, row=1 + col, col=1,
            )

    for col_idx, cloth_num in enumerate(eligible_cloth_nums, start=1):
        garment = next(
            (g for g in eligible_garments if g.get("cloth_number") == cloth_num), {}
        )
        garment_type = garment.get("type", "unknown")
        cloth_dir = None
        if sequence is not None:
            candidate = garment_mask_dir / f"layer_{layer}" / sequence / f"cloth_{cloth_num}" / camera
            if candidate.is_dir():
                cloth_dir = candidate
        if cloth_dir is None:
            candidates = sorted(garment_mask_dir.rglob(f"cloth_{cloth_num}/{camera}"))
            if candidates:
                cloth_dir = candidates[0]
        if cloth_dir is None or not cloth_dir.exists():
            fig.add_annotation(
                text="Not found", x=0.5, y=0.5,
                xref=f"x{col_idx+1}", yref=f"y{col_idx+1}",
                showarrow=False, row=1, col=col_idx + 1,
            )
            fig.add_annotation(
                text="Not found", x=0.5, y=0.5,
                xref=f"x{n_cols+col_idx+1}", yref=f"y{n_cols+col_idx+1}",
                showarrow=False, row=2, col=col_idx + 1,
            )
            continue
        mask_files = sorted(cloth_dir.glob("*.png"))
        if not mask_files:
            fig.add_annotation(
                text="Not found", x=0.5, y=0.5,
                xref=f"x{col_idx+1}", yref=f"y{col_idx+1}",
                showarrow=False, row=1, col=col_idx + 1,
            )
            continue
        mask_path = mask_files[min(frame_idx, len(mask_files) - 1)]
        mask = np.array(Image.open(mask_path))
        # Try to find a frame for overlay
        frame = None
        frame_candidate = _frame_for_mask(mask_path)
        if frame_candidate is not None and frame_candidate.is_file():
            try:
                frame = np.array(Image.open(frame_candidate))
            except Exception:
                frame = None
        # Top: binary mask
        mask_rgb = np.stack([mask] * 3, axis=-1) if mask.ndim == 2 else mask
        _image_subplot(fig, mask_rgb, 0, col_idx, f"cloth_{cloth_num} ({garment_type})")
        # Bottom: overlay
        if frame is not None:
            if mask.shape[:2] != frame.shape[:2]:
                mask = np.array(
                    Image.fromarray(mask).resize(
                        (frame.shape[1], frame.shape[0]), Image.NEAREST
                    )
                )
            color = palette[(col_idx - 1) % len(palette)]
            mask_bool = mask > 127
            overlay = frame.copy()
            overlay[mask_bool] = (
                overlay[mask_bool] * 0.55 + color * 0.45
            ).astype(np.uint8)
            _image_subplot(fig, overlay, 1, col_idx, f"cloth_{cloth_num} overlay")
        else:
            fig.add_annotation(
                text="(no frame)", x=0.5, y=0.5,
                xref=f"x{n_cols+col_idx+1}", yref=f"y{n_cols+col_idx+1}",
                showarrow=False, row=2, col=col_idx + 1,
            )

    fig.show()


def visualize_dataset_statistics() -> None:
    """Show dataset statistics charts in the browser."""
    stats = get_full_dataset_statistics()

    garment_types = count_garments_by_type()
    top_types = dict(sorted(garment_types.items(), key=lambda x: -x[1])[:10])

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Top 10 Garment Types",
            "Top 10 Garment Fabrics",
            "Dataset Overview",
            "Garments by Layer",
        ),
    )
    fig.update_layout(
        title_text="MV-Fashion Dataset Statistics",
        showlegend=False,
        height=800,
    )

    # Top 10 garment types
    fig.add_trace(
        go.Bar(
            x=list(top_types.values()),
            y=list(top_types.keys()),
            orientation="h",
        ),
        row=1, col=1,
    )

    # Top 10 garment fabrics
    garment_fabrics = count_garments_by_fabric()
    top_fabrics = dict(sorted(garment_fabrics.items(), key=lambda x: -x[1])[:10])
    fig.add_trace(
        go.Bar(
            x=list(top_fabrics.values()),
            y=list(top_fabrics.keys()),
            orientation="h",
            marker_color="orange",
        ),
        row=1, col=2,
    )

    # Dataset overview
    summary_data = [
        stats["subject_count"],
        stats["outfit_count"],
        stats["layer_count"],
        stats["sequence_count"],
        stats["garment_count"],
    ]
    summary_labels = ["Subjects", "Outfits", "Layers", "Sequences", "Garments"]
    fig.add_trace(
        go.Bar(
            x=summary_labels,
            y=summary_data,
            marker_color="green",
            text=[str(v) for v in summary_data],
            textposition="auto",
        ),
        row=2, col=1,
    )

    # Garments by layer
    layer_dist = stats["garment_layer_distribution"]
    layers = sorted(layer_dist.keys())
    counts = [layer_dist[l] for l in layers]
    fig.add_trace(
        go.Bar(
            x=[f"Layer {l}" for l in layers],
            y=counts,
            marker_color="purple",
        ),
        row=2, col=2,
    )

    fig.show()


def main():
    parser = argparse.ArgumentParser(
        description="Visualization for the MV-Fashion dataset (Plotly)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Visualize sequence frames
    python visualize_dataset.py --sequence subject_0001/outfit_1/layer_1/sequence_1

    # Visualize garment images
    python visualize_dataset.py --garments subject_0001/outfit_1

    # Visualize masks
    python visualize_dataset.py --masks subject_0001/outfit_1

    # Visualize dataset statistics
    python visualize_dataset.py --stats

    # Undistort frames and compare to originals
    python visualize_dataset.py --undistort subject_0001/outfit_1/layer_1/sequence_1 --camera rpi_01
        """,
    )

    parser.add_argument(
        "--sequence",
        type=str,
        help="Visualize sequence frames (e.g., subject_0001/outfit_1/layer_1/sequence_1)",
    )
    parser.add_argument(
        "--frame-idx",
        type=int,
        default=0,
        help="Frame index to visualize (default: 0)",
    )
    parser.add_argument(
        "--garments",
        type=str,
        help="Visualize garment images (e.g., subject_0001/outfit_1)",
    )
    parser.add_argument(
        "--masks",
        type=str,
        help="Visualize masks (e.g., subject_0001/outfit_1)",
    )
    parser.add_argument(
        "--layer",
        type=int,
        help="Layer index for mask filtering (only garments with layer <= this are drawn)",
    )
    parser.add_argument(
        "--mask-sequence",
        type=str,
        dest="mask_sequence",
        help="Sequence for mask visualization (e.g., sequence_1). Defaults to the first available.",
    )
    parser.add_argument(
        "--mask-camera",
        type=str,
        default="rpi_01",
        help="Camera to read masks from for --masks (default: rpi_01)",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Visualize dataset statistics",
    )
    parser.add_argument(
        "--undistort",
        type=str,
        help="Undistort frames (e.g., subject_0001/outfit_1/layer_1/sequence_1)",
    )
    parser.add_argument(
        "--camera",
        type=str,
        default="rpi_01",
        help="Camera to undistort (default: rpi_01)",
    )

    args = parser.parse_args()

    if args.sequence:
        parts = args.sequence.split("/")
        if len(parts) != 4:
            print("Error: Sequence must be in format subject_XXXX/outfit_X/layer_X/sequence_X")
            sys.exit(1)
        subject, outfit, layer, sequence = parts
        visualize_sequence_frames(subject, outfit, layer, sequence, args.frame_idx)
        return

    if args.garments:
        parts = args.garments.split("/")
        if len(parts) != 2:
            print("Error: Garments must be in format subject_XXXX/outfit_X")
            sys.exit(1)
        subject, outfit = parts
        visualize_garment_images(subject, outfit)
        return

    if args.masks:
        parts = args.masks.split("/")
        if len(parts) != 2:
            print("Error: Masks must be in format subject_XXXX/outfit_X")
            sys.exit(1)
        subject, outfit = parts
        visualize_masks(
            subject, outfit, args.frame_idx,
            layer=args.layer, sequence=args.mask_sequence,
            camera=args.mask_camera,
        )
        return

    if args.stats:
        visualize_dataset_statistics()
        return

    if args.undistort:
        parts = args.undistort.split("/")
        if len(parts) != 4:
            print("Error: Undistort must be in format subject_XXXX/outfit_X/layer_X/sequence_X")
            sys.exit(1)
        subject, outfit, layer, sequence = parts
        visualize_undistortion(
            subject, outfit, layer, sequence,
            camera=args.camera, frame_idx=args.frame_idx,
        )
        return

    parser.print_help()


if __name__ == "__main__":
    main()
