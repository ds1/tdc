import os
import sys
import subprocess
import shutil
import re
from pathlib import Path

def run_pip_command(command):
    """Run a pip command and print output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error:", result.stderr)
        return False
    
    print("Success!")
    return True

def run_python_script(script_path):
    """Run a Python script and print output."""
    print(f"Running: python {script_path}")
    result = subprocess.run(f"python {script_path}", shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error:", result.stderr)
        return False
    
    print("Success!")
    return True

def copy_file(src, dest):
    """Copy a file using Python's shutil."""
    print(f"Copying file {src} to {dest}")
    try:
        shutil.copy2(src, dest)
        return True
    except Exception as e:
        print(f"Error copying file: {e}")
        return False

def copy_directory(src, dest):
    """Copy a directory using Python's shutil."""
    print(f"Copying directory {src} to {dest}")
    try:
        if os.path.exists(dest):
            shutil.rmtree(dest)
        
        shutil.copytree(src, dest)
        return True
    except Exception as e:
        print(f"Error copying directory: {e}")
        return False

def fix_html_links(directory, file_ext=".html"):
    """Add .html extension to internal links in HTML files."""
    print(f"Fixing HTML links in {directory}...")
    
    # Regular expression to find links that need fixing
    # This will match href attributes that:
    # 1. Don't already have a file extension
    # 2. Don't start with http://, https://, #, or /
    # 3. Don't have a trailing slash (which would indicate a directory)
    # 4. Are not empty
    link_pattern = re.compile(r'href=[\'"](?!(?:http|https)://|#|/|javascript:|mailto:)([^/\'".]+)[\'"]')
    
    for html_file in directory.glob('**/*.html'):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix links that need the .html extension
        modified = link_pattern.sub(r'href="\1.html"', content)
        
        # Also fix absolute links to pages
        absolute_pattern = re.compile(r'href=[\'"](/[^/\'".]+)[\'"]')
        modified = absolute_pattern.sub(r'href="\1.html"', modified)
        
        if content != modified:
            print(f"  Fixed links in {html_file}")
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(modified)
    
    print("HTML link fixing complete.")

def main():
    # Get script directory and project root
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    project_root = script_dir.parent if script_dir.name == 'scripts' else script_dir
    
    # Ensure required packages are installed
    print("Installing required packages...")
    if not run_pip_command("pip install beautifulsoup4"):
        sys.exit(1)
    
    # Run generate_llm_data.py
    print("\nGenerating LLM-friendly data files...")
    if not run_python_script(script_dir / "generate_llm_data.py"):
        sys.exit(1)
    
    # Run update_metadata.py
    print("\nUpdating HTML metadata...")
    if not run_python_script(script_dir / "update_metadata.py"):
        sys.exit(1)
    
    # Create output build directory for local testing
    build_dir = project_root / 'build'
    os.makedirs(build_dir, exist_ok=True)
    
    # Copy files as in GitHub workflow
    print("\nCopying files to build directory...")
    
    # Create necessary directories
    dirs_to_create = [
        'css', 'js', 'llm-data', 'categories', 
        os.path.join('data', 'output'), 'images'
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(build_dir / dir_path, exist_ok=True)
    
    # Copy main HTML files
    docs_dir = project_root / 'docs'
    for html_file in docs_dir.glob('*.html'):
        if not copy_file(html_file, build_dir):
            print(f"Warning: Error copying {html_file}")
    
    # Copy asset directories
    for asset_dir in ['css', 'js', 'images']:
        src_dir = docs_dir / asset_dir
        if src_dir.exists():
            if src_dir.is_dir():
                # Use copy_directory for full directories
                if not copy_directory(src_dir, build_dir / asset_dir):
                    print(f"Warning: Error copying directory {src_dir}")
            else:
                print(f"Warning: {src_dir} exists but is not a directory")
    
    # Copy LLM-friendly data
    llm_data_src = docs_dir / 'llm-data'
    if llm_data_src.exists():
        for item in llm_data_src.glob('*'):
            if item.is_file() and item.name != 'categories':
                if not copy_file(item, build_dir / 'llm-data'):
                    print(f"Warning: Error copying {item}")
    
    # Copy categories
    categories_src = docs_dir / 'llm-data' / 'categories'
    if categories_src.exists() and categories_src.is_dir():
        if not copy_directory(categories_src, build_dir / 'categories'):
            print(f"Warning: Error copying directory {categories_src}")
    
    # Copy directory HTML to root
    directory_src = docs_dir / 'llm-data' / 'directory.html'
    if directory_src.exists():
        if not copy_file(directory_src, build_dir):
            print(f"Warning: Error copying {directory_src}")
    
    # Copy data files with proper handling for directories
    data_src = project_root / 'data' / 'output'
    if data_src.exists():
        for item in data_src.glob('*'):
            dest_path = build_dir / 'data' / 'output' / item.name
            if item.is_file():
                if not copy_file(item, dest_path):
                    print(f"Warning: Error copying {item}")
            elif item.is_dir():
                if not copy_directory(item, dest_path):
                    print(f"Warning: Error copying directory {item}")
    
    # Copy robots.txt and sitemap.xml
    robots_src = docs_dir / 'llm-data' / 'robots.txt'
    if robots_src.exists():
        if not copy_file(robots_src, build_dir):
            print(f"Warning: Error copying {robots_src}")
    
    sitemap_src = docs_dir / 'llm-data' / 'sitemap.xml'
    if sitemap_src.exists():
        if not copy_file(sitemap_src, build_dir):
            print(f"Warning: Error copying {sitemap_src}")
    
    # Create required GitHub Pages files
    with open(build_dir / '.nojekyll', 'w') as f:
        pass
    
    with open(build_dir / 'CNAME', 'w') as f:
        f.write('topdomain.club')
    
    # Fix HTML links for local testing
    fix_html_links(build_dir)
    
    print("\nAll done! Local test build created in:", build_dir)
    print("To test locally, you can run: python -m http.server -d build 8000")
    print("Then open http://localhost:8000 in your browser")

if __name__ == "__main__":
    main()