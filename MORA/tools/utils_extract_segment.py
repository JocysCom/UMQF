#!/usr/bin/env python3
"""
Utility: Extract Segment
Extract a specific range of lines from a text file (TXT or Markdown).
Useful for splitting large books (like The Bible) into manageable parts.

Usage:
  python tools/utils_extract_segment.py --input analysis/exploration-team/source-document.md --start 100 --output analysis/exploration-team/part1.md
  python tools/utils_extract_segment.py --input big_file.txt --start 100 --end 500 --output small_part.txt
"""

import argparse
import sys
import os

# --- Configuration & Constants ---
SCRIPT_NAME = os.path.basename(__file__)

def main():
    parser = argparse.ArgumentParser(description=f"{SCRIPT_NAME}: Extract lines from a text file.")
    parser.add_argument("--input", required=True, help="Input text file path")
    parser.add_argument("--output", required=True, help="Output text file path")
    parser.add_argument("--start", type=int, required=True, help="Start line number (1-based)")
    parser.add_argument("--end", type=int, help="End line number (1-based, inclusive). Default: End of file")
    
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[{SCRIPT_NAME}] Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {args.input}...")
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"[{SCRIPT_NAME}] Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    total_lines = len(lines)
    start_idx = max(0, args.start - 1)
    end_idx = args.end if args.end else total_lines
    
    if start_idx >= total_lines:
        print(f"[{SCRIPT_NAME}] Error: Start line {args.start} is beyond file length ({total_lines} lines).", file=sys.stderr)
        sys.exit(1)

    extracted_lines = lines[start_idx:end_idx]
    
    print(f"Extracting lines {args.start} to {end_idx} ({len(extracted_lines)} lines)...")
    
    try:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.writelines(extracted_lines)
    except Exception as e:
        print(f"[{SCRIPT_NAME}] Error writing output: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Success! Saved to {args.output}")
    
    # Quick stat check
    char_count = sum(len(l) for l in extracted_lines)
    token_est = char_count // 4
    print(f"New File Size: {char_count:,} chars (~{token_est:,} tokens)")

if __name__ == "__main__":
    main()