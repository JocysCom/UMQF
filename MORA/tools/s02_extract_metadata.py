#!/usr/bin/env python3
"""
Step 2: Extract Metadata
Extracts metadata from the EPUB file (OPF) and saves it to a JSON file.

Inputs:
- analysis/{document}/source-document.epub

Outputs:
- analysis/{document}/source-document-meta.json

Usage:
  python tools/s02_extract_metadata.py --document exploration-team
"""

import argparse
import json
import os
import sys
import zipfile
from datetime import datetime
from typing import Dict, Any

# --- Configuration & Constants ---
SCRIPT_NAME = os.path.basename(__file__)
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# File Names
INPUT_EPUB = "source-document.epub"
OUTPUT_META = "source-document-meta.json"
PREV_STEP_SCRIPT = "s01_search_and_download_book.py"
NEXT_STEP_SCRIPT = "s03_convert_to_markdown.py"

# --- Dependencies Check ---
try:
    from bs4 import BeautifulSoup
except ImportError:
    print(f"[{SCRIPT_NAME}] Missing dependencies. Please run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

# --- Helper Functions ---

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def write_json(path: str, content: Dict[str, Any]) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)

def extract_metadata_from_epub(epub_path: str) -> Dict[str, Any]:
    if not os.path.exists(epub_path):
        raise FileNotFoundError(f"EPUB file not found: {epub_path}")

    metadata = {}
    
    with zipfile.ZipFile(epub_path, 'r') as z:
        # 1. Find OPF file
        try:
            container_xml = z.read('META-INF/container.xml').decode('utf-8')
            soup = BeautifulSoup(container_xml, 'xml')
            rootfile = soup.find('rootfile')
            if not rootfile:
                raise ValueError("No rootfile found in container.xml")
            opf_path = rootfile['full-path']
        except Exception:
            # Fallback: look for .opf file
            opf_files = [f for f in z.namelist() if f.endswith('.opf')]
            if not opf_files:
                raise ValueError("Could not locate OPF file.")
            opf_path = opf_files[0]

        # 2. Parse OPF
        opf_content = z.read(opf_path).decode('utf-8')
        soup = BeautifulSoup(opf_content, 'xml')
        
        # Extract Dublin Core metadata
        dc_metadata = soup.find('metadata')
        if dc_metadata:
            # Title
            titles = dc_metadata.find_all('dc:title')
            if titles:
                metadata['title'] = titles[0].get_text()
            
            # Creator (Author)
            creators = dc_metadata.find_all('dc:creator')
            if creators:
                metadata['authors'] = [c.get_text() for c in creators]
            
            # Language
            langs = dc_metadata.find_all('dc:language')
            if langs:
                metadata['language'] = langs[0].get_text()
            
            # Identifier
            ids = dc_metadata.find_all('dc:identifier')
            if ids:
                metadata['identifiers'] = [i.get_text() for i in ids]
            
            # Date
            dates = dc_metadata.find_all('dc:date')
            if dates:
                metadata['date'] = dates[0].get_text()
            
            # Publisher
            publishers = dc_metadata.find_all('dc:publisher')
            if publishers:
                metadata['publisher'] = publishers[0].get_text()
            
            # Description
            descriptions = dc_metadata.find_all('dc:description')
            if descriptions:
                metadata['description'] = descriptions[0].get_text()
            
            # Rights
            rights = dc_metadata.find_all('dc:rights')
            if rights:
                metadata['rights'] = rights[0].get_text()

    return metadata

def main():
    ap = argparse.ArgumentParser(description=f"{SCRIPT_NAME}: Extract Metadata from EPUB.")
    ap.add_argument("--document", type=str, required=True, help="Short document slug")
    args = ap.parse_args()

    doc_dir = os.path.join(WORKSPACE_ROOT, "analysis", args.document)
    epub_path = os.path.join(doc_dir, INPUT_EPUB)
    
    if not os.path.exists(epub_path):
        print(f"Error: Source EPUB not found at {epub_path}", file=sys.stderr)
        print(f"Please run Step 1 ({PREV_STEP_SCRIPT}) first.", file=sys.stderr)
        sys.exit(1)

    print(f"Extracting metadata from: {epub_path}")
    
    # Let exceptions propagate to top level or handle them here without masking
    try:
        metadata = extract_metadata_from_epub(epub_path)
        
        # Add extraction timestamp
        metadata['extracted_at'] = datetime.now().replace(microsecond=0).isoformat() + "Z"
        
        output_path = os.path.join(doc_dir, OUTPUT_META)
        write_json(output_path, metadata)
        
        print(f"Success! Metadata saved to: {output_path}")
        print(json.dumps(metadata, indent=2))
        
        print(f"\nNext Step: Convert to Markdown:")
        print(f"  python tools/{NEXT_STEP_SCRIPT} --document {args.document}")
        
    except Exception as e:
        print(f"[{SCRIPT_NAME}] Failed to extract metadata: {e}", file=sys.stderr)
        # Re-raise if debugging is needed, or exit with error code
        sys.exit(1)

if __name__ == "__main__":
    main()