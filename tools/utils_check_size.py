#!/usr/bin/env python3
"""
Utility: Check File Size
Returns line count and character count to help determine processing strategy.

Usage:
  python tools/utils_check_size.py analysis/bible/source-document.md
"""
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="Check file size statistics.")
    parser.add_argument("file", help="Path to file")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1)

    try:
        line_count = 0
        char_count = 0
        with open(args.file, 'r', encoding='utf-8') as f:
            for line in f:
                line_count += 1
                char_count += len(line)
        
        print(f"File: {args.file}")
        print(f"Lines: {line_count}")
        print(f"Chars: {char_count}")
        
        # Heuristic for "Large" (matches instruction threshold)
        # User indicates ~400k context capacity.
        # 10,000 lines * ~50 chars/line = ~500k chars = ~125k tokens.
        # This is a safe chunk size that utilizes large context while leaving room for reasoning.
        if line_count > 10000:
            print("Status: LARGE (Requires segmentation)")
        else:
            print("Status: SMALL (Process directly)")
            
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()