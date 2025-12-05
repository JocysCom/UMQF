#!/usr/bin/env python3
"""
Step 3: Convert to Markdown
Process a downloaded EPUB into Structured Markdown (SSOT).
Generates segments.jsonl and updates manifest.

Inputs:
- analysis/{document}/source-document.epub
- analysis/{document}/source-document-meta.json (optional)

Outputs:
- analysis/{document}/source-document.md
- analysis/{document}/segments.jsonl
- analysis/{document}/manifest.json (updated)
- analysis/{document}/citation.md

Usage:
  python tools/s03_convert_to_markdown.py --document exploration-team
"""

import argparse
import json
import os
import re
import sys
import zipfile
from datetime import datetime
from typing import List, Tuple, Optional

# --- Configuration & Constants ---
SCRIPT_NAME = os.path.basename(__file__)
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# File Names
INPUT_EPUB = "source-document.epub"
INPUT_META = "source-document-meta.json"
OUTPUT_MD = "source-document.md"
OUTPUT_SEGMENTS = "segments.jsonl"
OUTPUT_MANIFEST = "manifest.json"
OUTPUT_CITATION = "citation.md"
PREV_STEP_SCRIPT = "s01_search_and_download_book.py"

# --- Dependencies Check ---
try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:
    print(f"[{SCRIPT_NAME}] Missing dependencies. Please run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

try:
    import ebooklib
    from ebooklib import epub
except ImportError:
    ebooklib = None

# --- Helper Functions ---

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def write_text(path: str, content: str) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat() + "Z"

def parse_epub_structure(epub_path):
    """
    Parses an EPUB file to extract its structure and content.
    Returns a list of (title, content_html) tuples in reading order.
    """
    if not os.path.exists(epub_path):
        raise FileNotFoundError(f"EPUB file not found: {epub_path}")

    # Try using ebooklib first if available
    if ebooklib:
        try:
            book = epub.read_epub(epub_path)
            ordered_content = []
            
            # Use spine for correct reading order
            for item_id in book.spine:
                item = book.get_item_with_id(item_id[0])
                if item:
                    # Decode content, handling potential encoding issues
                    try:
                        content = item.get_content().decode('utf-8')
                    except UnicodeDecodeError:
                        content = item.get_content().decode('latin-1') # Fallback
                        
                    ordered_content.append({
                        'id': item.get_id(),
                        'href': item.get_name(),
                        'content': content
                    })
            return ordered_content
        except Exception as e:
            print(f"[{SCRIPT_NAME}] Warning: ebooklib failed ({e}), falling back to zipfile method.")

    # Fallback to manual zipfile parsing
    with zipfile.ZipFile(epub_path, 'r') as z:
        # 1. Find OPF file from META-INF/container.xml
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

        # 2. Parse OPF to get manifest and spine
        opf_content = z.read(opf_path).decode('utf-8')
        opf_soup = BeautifulSoup(opf_content, 'xml')
        
        # Manifest: id -> href
        manifest = {}
        for item in opf_soup.find_all('item'):
            manifest[item.get('id')] = item.get('href')
        
        # Spine: ordered list of itemrefs
        spine_ids = [itemref.get('idref') for itemref in opf_soup.find_all('itemref')]
        
        # Resolve paths relative to OPF location
        opf_dir = os.path.dirname(opf_path)
        
        ordered_content = []
        
        for item_id in spine_ids:
            if item_id not in manifest:
                continue
                
            href = manifest[item_id]
            full_path = os.path.join(opf_dir, href).replace('\\', '/')
            
            # Normalize path (handle ../)
            full_path = os.path.normpath(full_path).replace('\\', '/')
            
            try:
                html_content = z.read(full_path).decode('utf-8')
                ordered_content.append({
                    'id': item_id,
                    'href': href,
                    'content': html_content
                })
            except KeyError:
                print(f"[{SCRIPT_NAME}] Warning: Could not find file {full_path} in archive.")
                
        return ordered_content

def convert_html_to_markdown(html_content: str) -> str:
    """
    Converts HTML to Markdown, preserving structure and inserting page markers.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted tags
    for tag in soup(['script', 'style', 'meta', 'link', 'head', 'title', 'noscript']):
        tag.decompose()

    def process_text(text):
        return re.sub(r'\s+', ' ', text)

    def traverse(node):
        if isinstance(node, NavigableString):
            return process_text(str(node))
            
        if not isinstance(node, Tag):
            return ""
            
        # --- Page Break Detection ---
        page_marker = ""
        # Check epub:type, class, or id for page indicators
        is_page = False
        page_ref = ""
        
        if node.get('epub:type') == 'pagebreak':
            is_page = True
            page_ref = node.get('title') or node.get_text().strip()
        elif 'pagebreak' in node.get('class', []):
            is_page = True
            page_ref = node.get('title') or node.get_text().strip()
        
        # Check ID for patterns like page-1, pg1, p123
        node_id = node.get('id', '')
        if not is_page and node_id:
            # Regex for common page ID patterns
            match = re.search(r'^(?:page|pg|p)[-_]?(\d+)$', node_id, re.IGNORECASE)
            if match:
                is_page = True
                page_ref = match.group(1)
        
        if is_page:
            # Clean up page num
            page_num = re.sub(r'[^\d]', '', str(page_ref))
            if not page_num and node_id:
                 # Try extracting from ID if title/text failed
                 match = re.search(r'(\d+)', node_id)
                 if match: page_num = match.group(1)
            
            if page_num:
                page_marker = f"[[PAGE:{page_num}]]"

        # --- Recursion ---
        content = ""
        for child in node.children:
            content += traverse(child)
            
        # --- Element Handling ---
        
        # Heuristic: Promote <p class="phX"> to Headers (Common in Gutenberg)
        classes = node.get('class', [])
        if node.name == 'p':
            if 'ph1' in classes:
                return f"\n\n## {content.strip()}\n\n"
            elif 'ph2' in classes:
                return f"\n\n### {content.strip()}\n\n"
            elif 'ph3' in classes:
                return f"\n\n#### {content.strip()}\n\n"
            elif 'ph4' in classes:
                return f"\n\n##### {content.strip()}\n\n"
            elif 'title' in classes:
                return f"\n\n# {content.strip()}\n\n"
        
        # Standard Headers
        if node.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(node.name[1])
            return f"\n\n{'#' * level} {content.strip()}\n\n"
            
        elif node.name == 'p':
            # Paragraphs must be separated by blank lines
            return f"\n\n{page_marker}{content.strip()}\n\n"
            
        elif node.name == 'br':
            return "  \n"
            
        elif node.name == 'hr':
            return "\n\n---\n\n"
            
        elif node.name == 'blockquote':
            lines = content.strip().split('\n')
            quoted = '\n'.join(f'> {line.strip()}' for line in lines if line.strip())
            return f"\n\n{quoted}\n\n"
            
        elif node.name in ['ul', 'ol']:
            return f"\n\n{content.strip()}\n\n"
            
        elif node.name == 'li':
            return f"- {content.strip()}\n"
            
        elif node.name == 'div':
            # Check if div is acting as a header
            if 'title' in classes:
                 return f"\n\n# {content.strip()}\n\n"
            return f"{page_marker}{content}"
            
        elif node.name == 'pre':
            return f"\n\n```\n{content}\n```\n\n"

        # Inline elements
        elif node.name in ['i', 'em']:
            return f"*{content.strip()}*"
            
        elif node.name in ['b', 'strong']:
            return f"**{content.strip()}**"
            
        elif node.name == 'a':
            href = node.get('href')
            if href and content.strip():
                return f"[{content.strip()}]({href})"
            # If it's an anchor without href, it might be a target (handled by page detection above)
            return f"{page_marker}{content}"
            
        elif node.name == 'span':
             return f"{page_marker}{content}"

        # Default: just return content with page marker
        return f"{page_marker}{content}"

    root = soup.body if soup.body else soup
    markdown = traverse(root)
    
    # Post-processing cleanup
    # 1. Collapse multiple blank lines to max 2 (one empty line)
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    return markdown.strip()

def guess_chapter_headings_from_html(html: str) -> List[str]:
    """
    Scans HTML for likely chapter headings.
    Includes h1-h3 and p.ph1/ph2 classes common in Gutenberg.
    """
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "html.parser")

    headings = []
    
    # Standard Headers
    for tag in soup.find_all(["h1", "h2", "h3"]):
        txt = tag.get_text(separator=" ", strip=True)
        if txt: headings.append(txt)
            
    # Gutenberg Classes
    for tag in soup.find_all("p", class_=re.compile(r"ph[1-2]")):
        txt = tag.get_text(separator=" ", strip=True)
        if txt: headings.append(txt)

    # Filter and Normalize
    final_headings = []
    seen = set()
    
    for txt in headings:
        norm = re.sub(r"\s+", " ", txt).strip()
        if not norm: continue
        if norm.upper() in ["CONTENTS", "PREFACE", "INDEX"]: continue
        
        # Heuristics for valid chapter title
        is_chapter = False
        if re.search(r"\bCHAPTER\b", norm, re.I): is_chapter = True
        elif re.match(r"^[IVXLCDM]+$", norm): is_chapter = True # Roman numerals
        elif re.match(r"^\d+$", norm): is_chapter = True # Just numbers
        elif len(norm) > 3 and norm.upper() == norm: is_chapter = True # All caps
        
        if is_chapter and norm not in seen:
            final_headings.append(norm)
            seen.add(norm)
            
    return final_headings

def find_chapter_starts_in_text(lines: List[str], candidate_titles: List[str]) -> List[Tuple[str, int]]:
    """
    Identifies chapter starts based on Markdown headers.
    """
    starts: List[Tuple[str, int]] = []
    
    # 1. Trust the Markdown structure we just created
    for i, line in enumerate(lines, start=1):
        if line.startswith("#"):
            # Extract title, removing hashes
            title = line.lstrip("#").strip()
            
            # Skip non-structural headers (Gutenberg boilerplate, etc.)
            skip_keywords = [
                "Bibliographic Citation",
                "The Project Gutenberg eBook",
                "The Full Project Gutenberg License",
                "End of the Project Gutenberg EBook"
            ]
            if any(k.lower() in title.lower() for k in skip_keywords):
                continue
                
            starts.append((title, i))
            
    if starts:
        return starts

    # 2. Fallback: Use candidate titles if no Markdown headers found (unlikely)
    normalized_lines = [re.sub(r"\s+", " ", ln.strip()).lower() for ln in lines]
    
    for title in candidate_titles:
        norm_title = re.sub(r"\s+", " ", title.strip()).lower()
        idx = None
        try:
            idx = normalized_lines.index(norm_title)
        except ValueError:
            pass
            
        if idx is not None:
            starts.append((title, idx + 1))

    starts = sorted(starts, key=lambda x: x[1])
    uniq_by_line = []
    seen_lines = set()
    for t, li in starts:
        if li not in seen_lines:
            uniq_by_line.append((t, li))
            seen_lines.add(li)
    return uniq_by_line

def build_segments_jsonl(chapter_starts: List[Tuple[str, int]], total_lines: int) -> List[dict]:
    segments = []
    for idx, (title, start_line) in enumerate(chapter_starts, start=1):
        end_line = total_lines if idx == len(chapter_starts) else chapter_starts[idx][1] - 1
        seg = {
            "ssid": f"BK01-CH{idx:03d}",
            "level": "Chapter",
            "index": idx,
            "title": title,
            "line_start": start_line,
            "line_end": end_line
        }
        segments.append(seg)
    return segments

def write_manifest(document: str, title: str, source_type: str) -> None:
    manifest_path = os.path.join(WORKSPACE_ROOT, "analysis", document, OUTPUT_MANIFEST)
    
    # Load existing manifest if available to preserve source URL
    existing_manifest = {}
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                existing_manifest = json.load(f)
        except:
            pass
            
    source_url = existing_manifest.get("source", {}).get("url", "Unknown")
    
    manifest = {
        "document_id": document,
        "title": title,
        "authors": existing_manifest.get("authors", []),
        "source": {
            "type": source_type,
            "url": source_url,
            "citation": f"{title} - Processed from {source_type} ({datetime.now().date().isoformat()})"
        },
        "ssot_path": f"analysis/{document}/{OUTPUT_MD}",
        "segmentation_tokens": ["Series", "Book", "Part", "Chapter", "Section", "Paragraph"],
        "chunk_policy": "chapter-first",
        "ssid_format": "SE%02d-BK%02d-PT%02d-CH%03d-SC%03d-PG%04d",
        "created_at": existing_manifest.get("created_at", now_iso()),
        "updated_at": now_iso(),
        "notes": f"Generated by {SCRIPT_NAME}"
    }
    write_text(manifest_path, json.dumps(manifest, indent=2))

def write_citation(document: str, title: str, source_type: str) -> None:
    path = os.path.join(WORKSPACE_ROOT, "analysis", document, OUTPUT_CITATION)
    
    # Try to get URL from manifest
    manifest_path = os.path.join(WORKSPACE_ROOT, "analysis", document, OUTPUT_MANIFEST)
    url = "Unknown"
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                m = json.load(f)
                url = m.get("source", {}).get("url", "Unknown")
        except:
            pass

    md = f"""# Bibliographic Citation

**Title:** {title}

**Source Type:** {source_type}

**URL:** {url}

**Processed Date:** {datetime.now().date().isoformat()}
"""
    write_text(path, md)

def main():
    ap = argparse.ArgumentParser(description=f"{SCRIPT_NAME}: Convert EPUB to Structured Markdown.")
    ap.add_argument("--document", type=str, required=True, help="Short document slug")
    args = ap.parse_args()

    doc_dir = os.path.join(WORKSPACE_ROOT, "analysis", args.document)
    epub_path = os.path.join(doc_dir, INPUT_EPUB)
    meta_path = os.path.join(doc_dir, INPUT_META)

    if not os.path.exists(epub_path):
        print(f"Error: Source EPUB not found at {epub_path}", file=sys.stderr)
        print(f"Please run Step 1 ({PREV_STEP_SCRIPT}) first.", file=sys.stderr)
        sys.exit(1)

    # Load metadata if available
    title = args.document
    if os.path.exists(meta_path):
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
                title = meta.get('title', title)
        except:
            pass

    print(f"Processing EPUB: {epub_path}")
    
    # Let exceptions propagate or handle them explicitly
    try:
        chapters = parse_epub_structure(epub_path)
        full_markdown = ""
        full_html = ""
        total_page_markers = 0
        
        for chapter in chapters:
            full_html += chapter['content'] + "\n"
            md = convert_html_to_markdown(chapter['content'])
            
            # Count page markers in this chapter
            page_markers = re.findall(r'\[\[PAGE:\d+\]\]', md)
            total_page_markers += len(page_markers)
            
            if md:
                full_markdown += md + "\n\n---\n\n"
        
        if total_page_markers > 0:
            print(f"[{SCRIPT_NAME}] Found {total_page_markers} page markers.")
        else:
            print(f"[{SCRIPT_NAME}] No page markers found in this document.")

        txt_str = full_markdown
        html_str = full_html
        
    except Exception as e:
        print(f"[{SCRIPT_NAME}] Error processing EPUB: {e}", file=sys.stderr)
        sys.exit(1)

    if not txt_str:
        print(f"[{SCRIPT_NAME}] Error: Failed to extract text content.", file=sys.stderr)
        sys.exit(1)

    # Save SSOT
    txt_str = txt_str.replace("\r\n", "\n").replace("\r", "\n")
    ssot_path = os.path.join(doc_dir, OUTPUT_MD)
    write_text(ssot_path, txt_str)
    print(f"Generated SSOT: {ssot_path}")

    # Generate Segments
    lines = txt_str.split("\n")
    candidate_titles = []
    if html_str:
        candidate_titles = guess_chapter_headings_from_html(html_str)

    chapter_starts = find_chapter_starts_in_text(lines, candidate_titles)
    if not chapter_starts:
        print(f"[{SCRIPT_NAME}] Warning: No chapter headings detected; creating single segment.", file=sys.stderr)
        chapter_starts = [("FULL DOCUMENT", 1)]

    segments = build_segments_jsonl(chapter_starts, total_lines=len(lines))
    seg_path = os.path.join(doc_dir, OUTPUT_SEGMENTS)
    with open(seg_path, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(json.dumps(seg, ensure_ascii=False) + "\n")
    print(f"Generated Segments: {seg_path} ({len(segments)} segments)")

    # Generate Manifest & Citation
    write_manifest(args.document, title, "epub")
    write_citation(args.document, title, "epub")
    print("Updated Manifest and Citation.")

if __name__ == "__main__":
    main()