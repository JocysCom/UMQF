#!/usr/bin/env python3
"""
Step 1: Search and Download Book (EPUB only)
Downloads a document (Gutenberg, Generic URL, or Local File) and saves it as an EPUB.

Outputs:
- analysis/{document}/source-document.epub
- analysis/{document}/manifest.json (initial)

Usage:
  python tools/{os.path.basename(__file__)} --id 68730 --document exploration-team
  python tools/{os.path.basename(__file__)} --url https://www.gutenberg.org/ebooks/68730 --document exploration-team
  python tools/{os.path.basename(__file__)} --file "/path/to/book.epub" --document exploration-team
  python tools/{os.path.basename(__file__)} --search "Exploration Team" --document exploration-team
"""

import argparse
import json
import os
import re
import sys
import time
import shutil
import requests
from datetime import datetime
import urllib.parse
import webbrowser
from typing import List, Tuple, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- Configuration & Constants ---
SCRIPT_NAME = os.path.basename(__file__)
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUTENBERG_SEARCH_URL = "https://www.gutenberg.org/ebooks/search/?query={}"
GUTENBERG_BASE_FILES = "https://www.gutenberg.org/files/{}"
GUTENBERG_CACHE_EPUB = "https://www.gutenberg.org/cache/epub/{}/pg{}.epub"
GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"
AMAZON_SEARCH_URL = "https://www.amazon.com/s?k={}&i=digital-text"

# Output Files
OUTPUT_EPUB = "source-document.epub"
OUTPUT_MANIFEST = "manifest.json"
NEXT_STEP_SCRIPT = "s02_extract_metadata.py"

# --- Dependencies Check ---
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    print(f"[{SCRIPT_NAME}] Missing dependencies. Please run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

# --- Helper Functions ---

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def write_text(path: str, content: str) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat() + "Z"

def guess_id_from_url(url: str) -> Optional[int]:
    m = re.search(r"/ebooks/(\d+)", url)
    if m:
        return int(m.group(1))
    return None

def resolve_gutenberg_epub_url(book_id: int) -> str:
    return GUTENBERG_CACHE_EPUB.format(book_id, book_id)

def download_file_with_resume(url: str, dest_path: str, retries: int = 5) -> bool:
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    for attempt in range(retries):
        file_mode = 'wb'
        resume_header = {}
        downloaded_bytes = 0
        
        if os.path.exists(dest_path):
            downloaded_bytes = os.path.getsize(dest_path)
            if downloaded_bytes > 0:
                resume_header = {'Range': f'bytes={downloaded_bytes}-'}
                file_mode = 'ab'
                if attempt > 0:
                    print(f"Resuming download from byte {downloaded_bytes}...", file=sys.stderr)

        try:
            if attempt == 0:
                print(f"Connecting to {url}...", file=sys.stderr)
            
            response = session.get(url, stream=True, timeout=30, headers=resume_header)
            
            if response.status_code == 416:
                print("Range not satisfiable (file likely complete).", file=sys.stderr)
                return True
                
            if response.status_code not in [200, 206]:
                print(f"Failed to connect: Status {response.status_code}", file=sys.stderr)
                if response.status_code == 404:
                    return False
                time.sleep(2)
                continue

            total_size = int(response.headers.get('content-length', 0))
            if response.status_code == 206:
                total_size += downloaded_bytes
            elif response.status_code == 200:
                if downloaded_bytes > 0:
                    print("Server does not support resume. Restarting download.", file=sys.stderr)
                    file_mode = 'wb'
                    downloaded_bytes = 0
            
            if attempt == 0:
                print(f"Downloading {total_size/1024/1024:.2f} MB...", file=sys.stderr)

            with open(dest_path, file_mode) as f:
                for chunk in response.iter_content(chunk_size=32768):
                    if chunk:
                        f.write(chunk)
                        downloaded_bytes += len(chunk)
                        if total_size > 0:
                            percent = (downloaded_bytes / total_size) * 100
                            sys.stderr.write(f"\rDownloading: {percent:.1f}%")
            
            sys.stderr.write("\nDownload complete.\n")
            return True

        except Exception as e:
            sys.stderr.write(f"\nDownload interrupted: {e}\n")
            time.sleep(2)
            continue
            
    return False

def download_gutenberg(book_id: int, out_dir: str) -> Tuple[str, str]:
    url = resolve_gutenberg_epub_url(book_id)
    epub_path = os.path.join(out_dir, OUTPUT_EPUB)
    print(f"Attempting EPUB download...", file=sys.stderr)
    if download_file_with_resume(url, epub_path):
        return "epub", url
    return None, None

def download_generic(url: str, out_dir: str) -> Tuple[str, str]:
    # Let requests raise exceptions naturally if connection fails
    r = requests.get(url, timeout=30, stream=True)
    r.raise_for_status()
    
    content_type = r.headers.get("Content-Type", "").lower()
    
    if "epub" not in content_type and not url.endswith(".epub"):
            print(f"Warning: URL does not appear to be an EPUB. Downloading anyway as {OUTPUT_EPUB}...", file=sys.stderr)
        
    dest_path = os.path.join(out_dir, OUTPUT_EPUB)
    
    with open(dest_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
            
    return "epub", url

def ingest_local_file(filepath: str, out_dir: str) -> Tuple[str, str]:
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}", file=sys.stderr)
        return None, None
        
    ext = os.path.splitext(filepath)[1].lower()
    if ext != ".epub":
        print(f"Error: Local file must be an EPUB (got {ext})", file=sys.stderr)
        return None, None
    
    dest_path = os.path.join(out_dir, OUTPUT_EPUB)
    
    # Avoid SameFileError if source and dest are the same
    if os.path.abspath(filepath) != os.path.abspath(dest_path):
        shutil.copy2(filepath, dest_path)
    
    return "epub", f"file://{os.path.abspath(filepath)}"

def write_initial_manifest(document: str, title: str, url: str, source_type: str) -> None:
    manifest_path = os.path.join(WORKSPACE_ROOT, "analysis", document, OUTPUT_MANIFEST)
    manifest = {
        "document_id": document,
        "title": title or document,
        "source": {
            "type": source_type,
            "url": url,
            "downloaded_at": now_iso()
        },
        "created_at": now_iso(),
        "status": "downloaded"
    }
    write_text(manifest_path, json.dumps(manifest, indent=2))

# --- Search Functions ---

def search_gutenberg(query: str) -> List[Tuple[int, str]]:
    url = GUTENBERG_SEARCH_URL.format(urllib.parse.quote(query))
    results = []
    
    r = requests.get(url, timeout=15)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        for li in soup.find_all("li", class_="booklink"):
            link = li.find("a", class_="link")
            if link:
                href = link.get("href")
                title_span = link.find("span", class_="title")
                title_text = title_span.get_text(strip=True) if title_span else "Unknown Title"
                m = re.search(r"/ebooks/(\d+)", href)
                if m:
                    results.append((int(m.group(1)), title_text))
    return results

def search_google_books(query: str, max_results: int = 5) -> List[dict]:
    params = {"q": query, "maxResults": max_results, "printType": "books"}
    results = []
    
    r = requests.get(GOOGLE_BOOKS_API, params=params, timeout=10)
    if r.status_code == 200:
        items = r.json().get("items", [])
        for item in items:
            info = item.get("volumeInfo", {})
            results.append({
                "title": info.get("title", "Unknown"),
                "authors": ", ".join(info.get("authors", [])),
                "isbn": next((i.get("identifier") for i in info.get("industryIdentifiers", []) if i.get("type") == "ISBN_13"), None)
            })
    return results

def search_amazon_kindle(query: str, max_results: int = 5) -> List[dict]:
    clean_query = urllib.parse.quote(query)
    return [{
        "title": f"Browse Amazon Kindle Results for '{query}'",
        "authors": "Amazon Store",
        "isbn": None,
        "url": AMAZON_SEARCH_URL.format(clean_query)
    }]

def connect_browser_and_navigate(url: str, port: int = 9222) -> None:
    if not sync_playwright:
        print("Error: Playwright is not installed.", file=sys.stderr)
        webbrowser.open(url)
        return
    print(f"Connecting to browser at localhost:{port}...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(f"http://localhost:{port}")
            page = browser.contexts[0].new_page()
            page.goto(url)
            print(f"Navigated to: {url}")
            print("\n=== MANUAL ACTION REQUIRED ===")
            print("1. Purchase the book.")
            print("2. Download the book file (often .acsm).")
            print("3. If .acsm, open with Adobe Digital Editions to download the .epub.")
            print("   (Check %USERPROFILE%\\Documents\\My Digital Editions\\)")
            print("4. Use Calibre to DeDRM if necessary and save as standard EPUB.")
            print("5. Run this script again with --file 'path/to/book.epub'")
    except Exception as e:
        print(f"Failed to connect: {e}")
        webbrowser.open(url)

def main():
    ap = argparse.ArgumentParser(description=f"{SCRIPT_NAME}: Search and Download Book (EPUB only).")
    ap.add_argument("--id", type=int, help="Project Gutenberg ID")
    ap.add_argument("--url", type=str, help="Source URL")
    ap.add_argument("--file", type=str, help="Local file path")
    ap.add_argument("--search", type=str, help="Search query")
    ap.add_argument("--document", type=str, required=True, help="Short document slug")
    ap.add_argument("--debug-port", type=int, default=9222)
    args = ap.parse_args()

    if not any([args.id, args.url, args.search, args.file]):
        print("Error: Must provide --id, --url, --file, or --search", file=sys.stderr)
        sys.exit(2)

    out_dir = os.path.join(WORKSPACE_ROOT, "analysis", args.document)
    ensure_dir(out_dir)

    # Handle Search
    if args.search:
        print(f"Searching for: '{args.search}'...")
        gutenberg = search_gutenberg(args.search)[:5]
        google = search_google_books(args.search, max_results=5)
        amazon = search_amazon_kindle(args.search, max_results=5)
        
        all_options = []
        print("\n--- Project Gutenberg ---")
        for bid, title in gutenberg:
            all_options.append({"type": "gutenberg", "id": bid, "title": title, "display": f"{title} (ID: {bid})"})
            print(f"[{len(all_options)}] {all_options[-1]['display']}")
            
        print("\n--- Commercial ---")
        for b in google + amazon:
            all_options.append({"type": "commercial", "url": b.get('url'), "title": b['title'], "display": b['title']})
            print(f"[{len(all_options)}] {all_options[-1]['display']}")

        if not all_options:
            print("No results found.")
            sys.exit(0)

        try:
            sel = int(input("\nSelect a book number (0 to exit): "))
            if sel == 0: sys.exit(0)
            selection = all_options[sel-1]
            
            if selection["type"] == "gutenberg":
                args.id = selection["id"]
            elif selection["type"] == "commercial":
                if "url" in selection and selection["url"]:
                    connect_browser_and_navigate(selection["url"], args.debug_port)
                else:
                    print("No direct URL available.")
                sys.exit(0)
        except (ValueError, IndexError):
            print("Invalid selection.")
            sys.exit(1)

    # Download Logic
    final_type = None
    final_url = None

    if args.id:
        print(f"Downloading Gutenberg ID {args.id}...")
        final_type, final_url = download_gutenberg(args.id, out_dir)
    elif args.url:
        gid = guess_id_from_url(args.url)
        if gid:
            print(f"Detected Gutenberg URL. Downloading ID {gid}...")
            final_type, final_url = download_gutenberg(gid, out_dir)
        else:
            print(f"Downloading Generic URL {args.url}...")
            final_type, final_url = download_generic(args.url, out_dir)
    elif args.file:
        print(f"Ingesting local file {args.file}...")
        final_type, final_url = ingest_local_file(args.file, out_dir)

    if not final_type:
        print("Download failed. Ensure you are downloading an EPUB file.", file=sys.stderr)
        sys.exit(1)

    print(f"\nSuccess! Document saved to analysis/{args.document}/{OUTPUT_EPUB}")
    
    # Create initial manifest
    write_initial_manifest(args.document, args.document, final_url, "book" if args.id else "web")
    
    print(f"\nNext Step: Extract metadata:")
    print(f"  python tools/{NEXT_STEP_SCRIPT} --document {args.document}")

if __name__ == "__main__":
    main()