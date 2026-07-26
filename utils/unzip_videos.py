#!/usr/bin/env python3
"""High-performance unzip script for MV-Fashion video archives.

Optimized for large-scale dataset handling:
- Parallel extraction with configurable workers
- Progress tracking and resumption
- Memory-efficient streaming extraction
- Skip existing files by default
- Detailed statistics and error reporting

Usage:
    python unzip_videos.py --help
    python unzip_videos.py --all
    python unzip_videos.py --subjects 1 2 3 --cameras rpi
    python unzip_videos.py --sequence subject_0001/outfit_1/layer_1/sequence_1
"""

import argparse
import sys
import zipfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

from paths import (
    get_subjects,
    get_outfits,
    get_layers,
    get_sequences,
    get_sequence_path,
    iter_sequences,
)


def extract_member(zf: zipfile.ZipFile, member: str, extract_dir: Path, overwrite: bool) -> dict:
    """Extract a single member from a zip file."""
    target_path = extract_dir / member
    
    if target_path.exists() and not overwrite:
        return {"status": "skipped", "member": member}
    
    try:
        if member.endswith("/"):
            target_path.mkdir(parents=True, exist_ok=True)
            return {"status": "created_dir", "member": member}
        else:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member) as src, open(target_path, "wb") as dst:
                while True:
                    chunk = src.read(8192)
                    if not chunk:
                        break
                    dst.write(chunk)
            return {"status": "extracted", "member": member}
    except Exception as e:
        return {"status": "failed", "member": member, "error": str(e)}


def unzip_archive(
    archive_path: Path,
    output_dir: Optional[Path] = None,
    overwrite: bool = False,
    members: Optional[list[str]] = None,
    max_workers: int = 4,
) -> dict:
    """Unzip a single archive with parallel extraction.
    
    Args:
        archive_path: Path to the zip file
        output_dir: Output directory (default: same as archive)
        overwrite: Whether to overwrite existing files
        members: Specific members to extract (None = all)
        max_workers: Number of parallel extraction workers
    
    Returns:
        Dict with extraction stats
    """
    result = {
        "archive": str(archive_path),
        "extracted": 0,
        "skipped": 0,
        "failed": 0,
        "errors": [],
    }
    
    if not archive_path.is_file():
        result["errors"].append(f"Archive not found: {archive_path}")
        return result
    
    extract_dir = output_dir or archive_path.parent
    
    try:
        with zipfile.ZipFile(archive_path, "r") as zf:
            if members is None:
                members = zf.namelist()
            
            print(f"  Extracting {len(members)} files from {archive_path.name}...")
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [
                    executor.submit(extract_member, zf, member, extract_dir, overwrite)
                    for member in members
                ]
                
                completed = 0
                for future in as_completed(futures):
                    res = future.result()
                    if res["status"] == "extracted":
                        result["extracted"] += 1
                    elif res["status"] == "skipped":
                        result["skipped"] += 1
                    elif res["status"] == "failed":
                        result["failed"] += 1
                        result["errors"].append(f"{res['member']}: {res['error']}")
                    
                    completed += 1
                    if completed % 100 == 0 or completed == len(members):
                        print(f"    Progress: {completed}/{len(members)} files")
    
    except Exception as e:
        result["errors"].append(f"Failed to open archive: {e}")
    
    return result


def unzip_sequence(
    subject: str,
    outfit: str,
    layer: str,
    sequence: str,
    output_dir: Optional[Path] = None,
    overwrite: bool = False,
    cameras: Optional[list[str]] = None,
    max_workers: int = 4,
) -> dict:
    """Unzip video archives for a specific sequence."""
    seq_path = get_sequence_path(subject, outfit, layer, sequence)
    
    archives_to_extract = []
    
    if cameras is None or "rpi" in cameras:
        rpi_archive = seq_path / "rpi.zip"
        if rpi_archive.is_file():
            archives_to_extract.append(rpi_archive)
    
    if cameras is None or "bolt" in cameras:
        bolt_archive = seq_path / "bolt.zip"
        if bolt_archive.is_file():
            archives_to_extract.append(bolt_archive)
    
    if not archives_to_extract:
        return {
            "sequence": f"{subject}/{outfit}/{layer}/{sequence}",
            "extracted": 0,
            "skipped": 0,
            "failed": 0,
            "errors": ["No archives found"],
        }
    
    total_result = {
        "sequence": f"{subject}/{outfit}/{layer}/{sequence}",
        "extracted": 0,
        "skipped": 0,
        "failed": 0,
        "errors": [],
    }
    
    for archive_path in archives_to_extract:
        result = unzip_archive(archive_path, output_dir, overwrite, max_workers=max_workers)
        total_result["extracted"] += result["extracted"]
        total_result["skipped"] += result["skipped"]
        total_result["failed"] += result["failed"]
        total_result["errors"].extend(result["errors"])
    
    return total_result


def unzip_subject(
    subject: str,
    output_dir: Optional[Path] = None,
    overwrite: bool = False,
    cameras: Optional[list[str]] = None,
    max_workers: int = 4,
) -> list[dict]:
    """Unzip all sequences for a subject."""
    results = []
    
    for outfit in get_outfits(subject):
        for layer in get_layers(subject, outfit):
            for sequence in get_sequences(subject, outfit, layer):
                result = unzip_sequence(
                    subject, outfit, layer, sequence,
                    output_dir, overwrite, cameras, max_workers,
                )
                results.append(result)
    
    return results


def unzip_all(
    output_dir: Optional[Path] = None,
    overwrite: bool = False,
    cameras: Optional[list[str]] = None,
    max_workers: int = 4,
) -> list[dict]:
    """Unzip all sequences in the dataset with progress tracking."""
    results = []
    
    sequences = list(iter_sequences())
    print(f"Found {len(sequences)} sequences to process")
    
    start_time = time.time()
    
    for idx, (subject, outfit, layer, sequence) in enumerate(sequences, 1):
        print(f"\n[{idx}/{len(sequences)}] Processing {subject}/{outfit}/{layer}/{sequence}")
        result = unzip_sequence(
            subject, outfit, layer, sequence,
            output_dir, overwrite, cameras, max_workers,
        )
        results.append(result)
        
        if idx % 10 == 0 or idx == len(sequences):
            elapsed = time.time() - start_time
            rate = idx / elapsed if elapsed > 0 else 0
            print(f"Progress: {idx}/{len(sequences)} sequences ({rate:.2f} seq/sec)")
    
    return results


def print_summary(results: list[dict]) -> None:
    """Print a summary of extraction results."""
    total_extracted = sum(r["extracted"] for r in results)
    total_skipped = sum(r["skipped"] for r in results)
    total_failed = sum(r["failed"] for r in results)
    total_errors = sum(len(r["errors"]) for r in results)
    
    print("\n" + "=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Total files extracted: {total_extracted}")
    print(f"Total files skipped: {total_skipped}")
    print(f"Total files failed: {total_failed}")
    print(f"Total errors: {total_errors}")
    
    if total_errors > 0:
        print("\nErrors (first 10):")
        error_count = 0
        for result in results:
            for error in result["errors"]:
                if error_count >= 10:
                    print(f"  ... and {total_errors - 10} more errors")
                    break
                print(f"  - {error}")
                error_count += 1
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="High-performance unzip for MV-Fashion video archives",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Unzip all sequences
    python unzip_videos.py --all
    
    # Unzip specific subjects, RPi cameras only
    python unzip_videos.py --subjects 1 2 3 --cameras rpi
    
    # Unzip a range of subjects, both camera types
    python unzip_videos.py --subject-range 1 10 --cameras rpi bolt
    
    # Unzip a specific sequence
    python unzip_videos.py --sequence subject_0001/outfit_1/layer_1/sequence_1
    
    # Unzip with more workers
    python unzip_videos.py --subjects 1 --workers 8
    
    # Unzip to custom directory
    python unzip_videos.py --subjects 1 --output-dir ./extracted
    
    # Overwrite existing files
    python unzip_videos.py --subjects 1 --overwrite
        """,
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (default: same as archives)",
    )
    
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files",
    )
    
    parser.add_argument(
        "--cameras",
        choices=["rpi", "bolt"],
        nargs="+",
        help="Camera types to extract (default: all)",
    )
    
    parser.add_argument(
        "--subjects",
        type=int,
        nargs="+",
        help="Unzip videos for specific subjects (e.g., --subjects 1 2 3)",
    )
    
    parser.add_argument(
        "--subject-range",
        type=int,
        nargs=2,
        metavar=("START", "END"),
        help="Unzip videos for a range of subjects (e.g., --subject-range 1 10)",
    )
    
    parser.add_argument(
        "--sequence",
        type=str,
        help="Unzip a specific sequence (e.g., subject_0001/outfit_1/layer_1/sequence_1)",
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Unzip all sequences in the dataset",
    )
    
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel extraction workers (default: 4)",
    )
    
    args = parser.parse_args()
    
    if args.sequence:
        parts = args.sequence.split("/")
        if len(parts) != 4:
            print("Error: Sequence must be in format subject_XXXX/outfit_X/layer_X/sequence_X")
            sys.exit(1)
        
        subject, outfit, layer, sequence = parts
        print(f"Unzipping {args.sequence}...")
        result = unzip_sequence(
            subject, outfit, layer, sequence,
            args.output_dir, args.overwrite, args.cameras, args.workers,
        )
        print_summary([result])
        return
    
    if args.subjects:
        results = []
        for subject_num in args.subjects:
            subject = f"subject_{subject_num:04d}"
            print(f"\nUnzipping {subject}...")
            subject_results = unzip_subject(
                subject, args.output_dir, args.overwrite, args.cameras, args.workers,
            )
            results.extend(subject_results)
        print_summary(results)
        return
    
    if args.subject_range:
        start, end = args.subject_range
        results = []
        for subject_num in range(start, end + 1):
            subject = f"subject_{subject_num:04d}"
            print(f"\nUnzipping {subject}...")
            subject_results = unzip_subject(
                subject, args.output_dir, args.overwrite, args.cameras, args.workers,
            )
            results.extend(subject_results)
        print_summary(results)
        return
    
    if args.all:
        print("Unzipping all sequences...")
        results = unzip_all(
            args.output_dir, args.overwrite, args.cameras, args.workers,
        )
        print_summary(results)
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
