#!/usr/bin/env python3
"""
Interactive Pipeline Runner
Allows selecting a document from 'analysis/' and running the ingestion pipeline.
"""

import os
import sys
import subprocess

# --- Configuration & Constants ---
SCRIPT_NAME = os.path.basename(__file__)
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANALYSIS_DIR = os.path.join(WORKSPACE_ROOT, "analysis")
TOOLS_DIR = os.path.join(WORKSPACE_ROOT, "tools")

# Pipeline Scripts
SCRIPT_S01 = "s01_search_and_download_book.py"
SCRIPT_S02 = "s02_extract_metadata.py"
SCRIPT_S03 = "s03_convert_to_markdown.py"

def run_step(script_name, args):
    print(f"\n{'='*60}")
    print(f"Running {script_name}...")
    print(f"{'='*60}")
    
    cmd = [sys.executable, os.path.join(TOOLS_DIR, script_name)] + args
    try:
        # Allow interactive input for s01 if needed
        result = subprocess.run(cmd, text=True)
        if result.returncode == 0:
            print(f"Success: {script_name}")
            return True
        else:
            print(f"[{SCRIPT_NAME}] Error: {script_name} failed with code {result.returncode}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"[{SCRIPT_NAME}] Error executing {script_name}: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n[{SCRIPT_NAME}] Interrupted.")
        return False

def list_documents():
    if not os.path.exists(ANALYSIS_DIR):
        print(f"Error: Analysis directory not found at {ANALYSIS_DIR}")
        return []
    
    docs = [d for d in os.listdir(ANALYSIS_DIR) if os.path.isdir(os.path.join(ANALYSIS_DIR, d)) and not d.startswith('.')]
    return sorted(docs)

def main():
    print(f"--- Document Pipeline Runner ---")
    
    docs = list_documents()
    if not docs:
        print("No document folders found in analysis/.")
        sys.exit(0)

    print("\nAvailable Documents:")
    for i, doc in enumerate(docs, 1):
        print(f"{i}. {doc}")
    
    print("\n0. Exit")

    try:
        choice = input("\nSelect a document (number): ").strip()
        if not choice.isdigit():
            print("Invalid input.")
            sys.exit(1)
        
        idx = int(choice)
        if idx == 0:
            sys.exit(0)
        
        if idx < 1 or idx > len(docs):
            print("Selection out of range.")
            sys.exit(1)
            
        selected_doc = docs[idx - 1]
        doc_path = os.path.join(ANALYSIS_DIR, selected_doc)
        epub_path = os.path.join(doc_path, "source-document.epub")
        
        print(f"\nSelected: {selected_doc}")
        
        # Check for EPUB
        if not os.path.exists(epub_path):
            print(f"\n'source-document.epub' not found in {selected_doc}.")
            run_download = input("Run search and download (s01)? (y/n): ").strip().lower()
            
            if run_download == 'y':
                # Run s01 interactively
                # We pass --document, but let the script handle the search/id input via its own arguments or interaction
                # However, s01 requires arguments. We'll ask the user for a search term or ID here to pass to it,
                # or we can run it with just --document and let it fail/ask? 
                # Looking at s01, it requires --id, --url, --file or --search.
                
                print("\nDownload Options:")
                print("1. Search by Title/Author")
                print("2. Enter Gutenberg ID")
                print("3. Enter URL")
                
                dl_choice = input("Select option: ").strip()
                
                s01_args = ["--document", selected_doc]
                
                if dl_choice == '1':
                    query = input("Enter search query: ").strip()
                    s01_args.extend(["--search", query])
                elif dl_choice == '2':
                    gid = input("Enter Gutenberg ID: ").strip()
                    s01_args.extend(["--id", gid])
                elif dl_choice == '3':
                    url = input("Enter URL: ").strip()
                    s01_args.extend(["--url", url])
                else:
                    print("Invalid option. Skipping download.")
                    sys.exit(1)

                if not run_step(SCRIPT_S01, s01_args):
                    print("Download failed. Aborting pipeline.")
                    sys.exit(1)
            else:
                print("Skipping download. Cannot proceed without EPUB.")
                sys.exit(1)
        else:
            print(f"\nFound existing EPUB: {epub_path}")
            
        # Proceed with pipeline
        print("\nProceeding with processing...")
        
        # Step 2: Extract Metadata
        if not run_step(SCRIPT_S02, ["--document", selected_doc]):
            print("Metadata extraction failed.")
            sys.exit(1)
            
        # Step 3: Convert to Markdown
        if not run_step(SCRIPT_S03, ["--document", selected_doc]):
            print("Markdown conversion failed.")
            sys.exit(1)

        print(f"\n{'='*60}")
        print("Pipeline Complete!")
        print(f"Output: {doc_path}")
        print(f"{'='*60}")

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()