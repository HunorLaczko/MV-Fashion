#!/usr/bin/env python3
"""High-performance download script for MV-Fashion dataset with resumable downloads.

Features:
- Granular control: download specific subjects, camera types, annotations
- Resumable downloads with progress tracking
- Uses HF xet for faster downloads when available
- Parallel downloads with configurable workers
- Memory-efficient for large datasets
- Progress bars and detailed logging

Dataset: https://huggingface.co/datasets/MV-Fashion/MV-Fashion

Usage:
    python download_mv_fashion.py --help
    python download_mv_fashion.py --metadata-only
    python download_mv_fashion.py --subjects 1 2 3 --cameras rpi
    python download_mv_fashion.py --subjects 1 --annotations foreground garment
    python download_mv_fashion.py --all --resume
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

try:
    from huggingface_hub import hf_hub_download, HfApi
    from huggingface_hub.utils import GatedRepoError, RepositoryNotFoundError
except ImportError:
    print("Error: huggingface_hub is not installed.")
    print("Install with: pip install huggingface_hub")
    sys.exit(1)


REPO_ID = "MV-Fashion/MV-Fashion"
DEFAULT_OUTPUT_DIR = Path(os.environ.get("MV_FASHION_DATASET_ROOT", "./mv_fashion_dataset"))
PROGRESS_FILE = ".download_progress.json"


class DownloadProgress:
    """Track download progress for resumable downloads."""
    
    def __init__(self, progress_file: Path):
        self.progress_file = progress_file
        self.data = self._load()
    
    def _load(self) -> dict:
        if self.progress_file.exists():
            try:
                with open(self.progress_file, "r") as f:
                    return json.load(f)
            except Exception:
                return {"completed": [], "failed": [], "partial": []}
        return {"completed": [], "failed": [], "partial": []}
    
    def save(self):
        with open(self.progress_file, "w") as f:
            json.dump(self.data, f, indent=2)
    
    def is_completed(self, file_path: str) -> bool:
        return file_path in self.data["completed"]
    
    def mark_completed(self, file_path: str):
        if file_path not in self.data["completed"]:
            self.data["completed"].append(file_path)
            self.save()
    
    def mark_failed(self, file_path: str, error: str):
        self.data["failed"].append({"file": file_path, "error": error})
        self.save()
    
    def get_pending(self, all_files: list[str]) -> list[str]:
        return [f for f in all_files if not self.is_completed(f)]


def load_hf_token() -> Optional[str]:
    """Load HuggingFace token from environment or .env file."""
    token = os.environ.get("HF_TOKEN")
    if token:
        return token
    
    env_paths = [
        Path.home() / ".huggingface" / ".env",
        Path.cwd() / ".env",
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            with env_path.open("r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("HF_TOKEN="):
                        return line.split("=", 1)[1].strip()
    
    return None


def check_access(token: str) -> bool:
    """Check if the token has access to the gated dataset."""
    try:
        api = HfApi(token=token)
        api.dataset_info(REPO_ID)
        print("✓ Access granted to MV-Fashion dataset")
        return True
    except GatedRepoError:
        print("✗ Access denied. You need to request access first:")
        print("  1. Go to https://huggingface.co/datasets/MV-Fashion/MV-Fashion")
        print("  2. Click 'Request Access' and fill in the form")
        print("  3. Wait for approval (usually a few business days)")
        return False
    except RepositoryNotFoundError:
        print(f"✗ Repository {REPO_ID} not found")
        return False
    except Exception as e:
        print(f"✗ Error checking access: {e}")
        return False


def list_dataset_files(token: str, pattern: Optional[str] = None) -> list[str]:
    """List files in the dataset repository with optional filtering."""
    try:
        api = HfApi(token=token)
        files = api.list_repo_files(REPO_ID, repo_type="dataset")
        files = sorted(files)
        
        if pattern:
            import fnmatch
            files = [f for f in files if fnmatch.fnmatch(f, pattern)]
        
        return files
    except Exception as e:
        print(f"Error listing files: {e}")
        return []


def download_file(
    token: str,
    file_path: str,
    output_dir: Path,
    progress: DownloadProgress,
    use_xet: bool = True,
) -> bool:
    """Download a single file with progress tracking."""
    if progress.is_completed(file_path):
        return True
    
    try:
        downloaded_path = hf_hub_download(
            repo_id=REPO_ID,
            filename=file_path,
            repo_type="dataset",
            token=token,
            local_dir=output_dir,
            force_download=False,
        )
        progress.mark_completed(file_path)
        return True
    except Exception as e:
        progress.mark_failed(file_path, str(e))
        return False


def download_files_parallel(
    token: str,
    file_paths: list[str],
    output_dir: Path,
    max_workers: int = 8,
    use_xet: bool = True,
    resume: bool = True,
) -> dict:
    """Download multiple files in parallel with progress tracking."""
    progress_file = output_dir / PROGRESS_FILE
    progress = DownloadProgress(progress_file) if resume else DownloadProgress(Path("/dev/null"))
    
    pending_files = progress.get_pending(file_paths) if resume else file_paths
    
    if not pending_files:
        print("✓ All files already downloaded")
        return {"completed": len(file_paths), "failed": 0, "skipped": 0}
    
    print(f"\nDownloading {len(pending_files)} files ({len(file_paths) - len(pending_files)} already completed)...")
    
    stats = {"completed": 0, "failed": 0, "skipped": len(file_paths) - len(pending_files)}
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                download_file, token, file_path, output_dir, progress, use_xet
            ): file_path
            for file_path in pending_files
        }
        
        completed_count = 0
        for future in as_completed(futures):
            file_path = futures[future]
            try:
                success = future.result()
                if success:
                    stats["completed"] += 1
                else:
                    stats["failed"] += 1
            except Exception as e:
                stats["failed"] += 1
                progress.mark_failed(file_path, str(e))
            
            completed_count += 1
            if completed_count % 10 == 0 or completed_count == len(pending_files):
                elapsed = time.time() - start_time
                rate = completed_count / elapsed if elapsed > 0 else 0
                print(f"  Progress: {completed_count}/{len(pending_files)} ({rate:.1f} files/sec)")
    
    elapsed = time.time() - start_time
    print(f"\n✓ Download complete in {elapsed:.1f}s")
    print(f"  Completed: {stats['completed']}")
    print(f"  Failed: {stats['failed']}")
    print(f"  Skipped: {stats['skipped']}")
    
    return stats


def get_metadata_files() -> list[str]:
    """Get list of metadata files to download."""
    return [
        "info.csv",
        "cameras/intrinsics.json",
        "cameras/extrinsics_bolts.json",
    ]


def get_garment_metadata_files(all_files: list[str]) -> list[str]:
    """Get list of garment metadata files."""
    return [
        f for f in all_files
        if f.startswith("garments/") and (
            f.endswith(".json") or f.endswith(".csv")
        )
    ]


def get_annotation_files(
    all_files: list[str],
    annotation_types: Optional[list[str]] = None,
    subjects: Optional[list[int]] = None,
) -> list[str]:
    """Get list of annotation files with filtering."""
    files = [f for f in all_files if f.startswith("annotations/")]
    
    if annotation_types:
        filtered = []
        for ann_type in annotation_types:
            filtered.extend([f for f in files if f"/masks/{ann_type}/" in f])
        files = filtered
    
    if subjects:
        subject_patterns = [f"subject_{s:04d}" for s in subjects]
        files = [f for f in files if any(p in f for p in subject_patterns)]
    
    return files


def get_video_files(
    all_files: list[str],
    subjects: Optional[list[int]] = None,
    cameras: Optional[list[str]] = None,
) -> list[str]:
    """Get list of video files with filtering."""
    files = [f for f in all_files if f.startswith("videos/")]
    
    if subjects:
        subject_patterns = [f"subject_{s:04d}" for s in subjects]
        files = [f for f in files if any(p in f for p in subject_patterns)]
    
    if cameras:
        camera_patterns = []
        if "rpi" in cameras:
            camera_patterns.append("rpi.zip")
        if "bolt" in cameras:
            camera_patterns.append("bolt.zip")
        
        if camera_patterns:
            files = [f for f in files if any(p in f for p in camera_patterns)]
    
    return files


def main():
    parser = argparse.ArgumentParser(
        description="Download MV-Fashion dataset from HuggingFace with resumable downloads",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Download metadata only (fast, ~100 MB)
    python download_mv_fashion.py --metadata-only
    
    # Download videos for specific subjects, RPi cameras only
    python download_mv_fashion.py --subjects 1 2 3 --cameras rpi
    
    # Download videos for subjects 1-10, Bolt cameras only
    python download_mv_fashion.py --subject-range 1 10 --cameras bolt
    
    # Download annotations for specific subjects
    python download_mv_fashion.py --subjects 1 2 --annotations foreground garment
    
    # Download everything for subjects 1-5
    python download_mv_fashion.py --subjects 1 2 3 4 5 --cameras rpi bolt --annotations foreground garment
    
    # Resume interrupted download
    python download_mv_fashion.py --subjects 1 2 3 --resume
    
    # List all files
    python download_mv_fashion.py --list-files
    
    # Use custom output directory
    python download_mv_fashion.py --metadata-only --output-dir ./my_dataset
        """,
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    
    parser.add_argument(
        "--token",
        type=str,
        help="HuggingFace token (or set HF_TOKEN environment variable)",
    )
    
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of parallel download workers (default: 8)",
    )
    
    parser.add_argument(
        "--no-xet",
        action="store_true",
        help="Disable xet protocol (use standard HTTP)",
    )
    
    parser.add_argument(
        "--resume",
        action="store_true",
        default=True,
        help="Resume interrupted downloads (default: True)",
    )
    
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Do not resume, download everything fresh",
    )
    
    parser.add_argument(
        "--list-files",
        action="store_true",
        help="List all files in the dataset",
    )
    
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="Download only metadata (info.csv, cameras, garments)",
    )
    
    parser.add_argument(
        "--annotations",
        nargs="*",
        choices=["foreground", "garment"],
        help="Download annotations (foreground, garment, or both)",
    )
    
    parser.add_argument(
        "--subjects",
        type=int,
        nargs="+",
        help="Download for specific subjects (e.g., --subjects 1 2 3)",
    )
    
    parser.add_argument(
        "--subject-range",
        type=int,
        nargs=2,
        metavar=("START", "END"),
        help="Download for a range of subjects (e.g., --subject-range 1 10)",
    )
    
    parser.add_argument(
        "--cameras",
        nargs="*",
        choices=["rpi", "bolt"],
        help="Download specific camera types (rpi, bolt, or both)",
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Download entire dataset (WARNING: ~11.5 TB)",
    )

    parser.add_argument(
        "--include",
        nargs="*",
        metavar="PATTERN",
        help=(
            "Download only files whose path matches one of these glob-style "
            "patterns (e.g. 'videos/subject_0001/outfit_1/layer_1/sequence_1/**', "
            "'garments/images/subject_0001/outfit_1/**'). Combines with the other "
            "filters above."
        ),
    )

    args = parser.parse_args()
    
    resume = not args.no_resume
    
    token = args.token or load_hf_token()
    if not token:
        print("Error: HuggingFace token not found.")
        print("Please provide it via --token or set HF_TOKEN environment variable.")
        sys.exit(1)
    
    print(f"Output directory: {args.output_dir}")
    print(f"HuggingFace token: {token[:10]}...{token[-4:]}")
    print(f"Parallel workers: {args.workers}")
    print(f"Resume mode: {resume}")
    print(f"Use xet: {not args.no_xet}")
    
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    if not check_access(token):
        sys.exit(1)
    
    if args.list_files:
        print("\n=== Dataset Files ===")
        files = list_dataset_files(token)
        print(f"Total files: {len(files)}")
        for f in files[:50]:
            print(f"  {f}")
        if len(files) > 50:
            print(f"  ... and {len(files) - 50} more files")
        return
    
    all_files = list_dataset_files(token)
    files_to_download = []
    
    if args.metadata_only:
        print("\n=== Downloading Metadata ===")
        files_to_download.extend(get_metadata_files())
        files_to_download.extend(get_garment_metadata_files(all_files))
    
    if args.annotations is not None:
        print(f"\n=== Downloading Annotations ===")
        ann_files = get_annotation_files(all_files, args.annotations, args.subjects)
        print(f"Found {len(ann_files)} annotation files")
        files_to_download.extend(ann_files)
    
    if args.subjects or args.subject_range or args.cameras:
        subjects = args.subjects or []
        if args.subject_range:
            subjects.extend(range(args.subject_range[0], args.subject_range[1] + 1))
        
        if subjects or args.cameras:
            print(f"\n=== Downloading Videos ===")
            if subjects:
                print(f"Subjects: {subjects}")
            if args.cameras:
                print(f"Cameras: {args.cameras}")
            
            video_files = get_video_files(all_files, subjects, args.cameras)
            print(f"Found {len(video_files)} video files")
            files_to_download.extend(video_files)
    
    if args.all:
        response = input("\nThis will download ~11.5 TB. Continue? [y/N]: ")
        if response.lower() != "y":
            print("Aborted.")
            return
        files_to_download = all_files

    if args.include:
        import fnmatch as _fnmatch
        patterns = list(args.include)
        print(f"\n=== Applying include patterns ===")
        print(f"Patterns: {patterns}")
        # The pre-filter list only contains videos / annotations / metadata.
        # If the user's patterns also need top-level files (info.csv,
        # cameras/**, garments/**), make sure they're included.
        universe = list(set(files_to_download) | set(all_files))
        before = len(universe)
        files_to_download = [
            f for f in universe
            if any(_fnmatch.fnmatch(f, p) for p in patterns)
        ]
        print(f"  {before} -> {len(files_to_download)} files after filtering")

    if not files_to_download:
        print("\nNo files to download. Use --help for usage examples.")
        return
    
    print(f"\nTotal files to download: {len(files_to_download)}")
    
    stats = download_files_parallel(
        token=token,
        file_paths=files_to_download,
        output_dir=args.output_dir,
        max_workers=args.workers,
        use_xet=not args.no_xet,
        resume=resume,
    )
    
    if stats["failed"] > 0:
        print(f"\n⚠ {stats['failed']} files failed to download")
        print("You can retry with --resume to continue")
    
    print("\n✓ Download complete")


if __name__ == "__main__":
    main()
