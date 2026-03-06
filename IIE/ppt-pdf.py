#!/usr/bin/env python3
"""
Convert .ppt/.pptx files in a folder to PDF.

Usage:
  python ppt-pdf.py
  python ppt-pdf.py --input . --output ./pdfs
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def find_presentations(input_dir: Path) -> list[Path]:
	return sorted(
		[
			p
			for p in input_dir.iterdir()
			if p.is_file() and p.suffix.lower() in {".ppt", ".pptx"}
		]
	)


def convert_with_soffice(soffice_cmd: str, file_path: Path, output_dir: Path) -> bool:
	cmd = [
		soffice_cmd,
		"--headless",
		"--convert-to",
		"pdf",
		"--outdir",
		str(output_dir),
		str(file_path),
	]

	result = subprocess.run(cmd, capture_output=True, text=True)
	if result.returncode != 0:
		print(f"✗ Failed: {file_path.name}")
		if result.stderr.strip():
			print(result.stderr.strip())
		return False

	expected_pdf = output_dir / f"{file_path.stem}.pdf"
	if expected_pdf.exists():
		print(f"✓ Converted: {file_path.name} -> {expected_pdf.name}")
		return True

	print(f"✗ Conversion command ran, but PDF not found for: {file_path.name}")
	return False


def main() -> int:
	parser = argparse.ArgumentParser(description="Convert PPT/PPTX files to PDF")
	parser.add_argument(
		"--input",
		"-i",
		type=Path,
		default=Path.cwd(),
		help="Folder containing .ppt/.pptx files (default: current directory)",
	)
	parser.add_argument(
		"--output",
		"-o",
		type=Path,
		default=None,
		help="Folder to save PDFs (default: same as input folder)",
	)
	args = parser.parse_args()

	input_dir = args.input.resolve()
	output_dir = args.output.resolve() if args.output else input_dir

	if not input_dir.exists() or not input_dir.is_dir():
		print(f"Input folder does not exist or is not a folder: {input_dir}")
		return 1

	output_dir.mkdir(parents=True, exist_ok=True)

	soffice = shutil.which("soffice") or shutil.which("libreoffice")
	if not soffice:
		print("LibreOffice is required but not found.")
		print("Install it, then ensure 'soffice' is available in PATH.")
		print("On macOS (Homebrew): brew install --cask libreoffice")
		return 1

	presentations = find_presentations(input_dir)
	if not presentations:
		print(f"No .ppt or .pptx files found in: {input_dir}")
		return 0

	print(f"Found {len(presentations)} file(s). Converting to PDF...")
	success_count = 0
	for file_path in presentations:
		if convert_with_soffice(soffice, file_path, output_dir):
			success_count += 1

	print(f"\nDone. {success_count}/{len(presentations)} file(s) converted.")
	return 0 if success_count == len(presentations) else 2


if __name__ == "__main__":
	sys.exit(main())
