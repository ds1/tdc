# repo_structure.py

# Generate a tree-like file structure of a directory and save it to a file.

# Dev Environment
    # Windows machine, Anaconda Powershell, Sublime Text

# Scripts
    # cd path\to\script
    # python repo_structure.py

import os
import sys
import argparse
from pathlib import Path

def generate_tree(startpath, exclude_dirs=None, exclude_files=None, output_file='repo_structure.txt'):
    """
    Generate a tree-like file structure of a directory and save it to a file.
    
    Args:
        startpath (str): Root directory to start the tree generation
        exclude_dirs (list): List of directory names to exclude (e.g., ['.git', 'node_modules'])
        exclude_files (list): List of file patterns to exclude (e.g., ['*.pyc', '.DS_Store'])
        output_file (str): Name of the output file
    """
    if exclude_dirs is None:
        exclude_dirs = ['.git', 'node_modules', '__pycache__', 'venv', 'env', '.pytest_cache']
    if exclude_files is None:
        exclude_files = ['*.pyc', '.DS_Store', '*.pyo', '*.pyd', '.env', 'Thumbs.db']
    
    # Convert startpath to Path object for better cross-platform compatibility
    startpath = Path(startpath)
    
    try:
        with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(f"Repository structure for: {startpath.absolute()}\n")
            f.write("=" * 50 + "\n\n")
            
            for root, dirs, files in os.walk(startpath):
                # Convert root to Path object
                root_path = Path(root)
                
                # Remove excluded directories
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                
                # Calculate current depth for indentation
                level = len(root_path.relative_to(startpath).parts)
                indent = '│   ' * level
                
                # Write directory name
                dir_name = root_path.name
                if level > 0:
                    f.write(f"{indent[:-4]}├── {dir_name}/\n")
                else:
                    f.write(f"{dir_name}/\n")
                
                # Write files
                file_indent = '│   ' * (level + 1)
                filtered_files = sorted([
                    file for file in files 
                    if not any(file.endswith(ext.replace('*', '')) for ext in exclude_files)
                ])
                
                for i, file in enumerate(filtered_files):
                    try:
                        if i == len(filtered_files) - 1:
                            f.write(f"{file_indent[:-4]}└── {file}\n")
                        else:
                            f.write(f"{file_indent[:-4]}├── {file}\n")
                    except UnicodeEncodeError:
                        # Handle files with special characters in their names
                        safe_name = file.encode('utf-8', errors='replace').decode('utf-8')
                        f.write(f"{file_indent[:-4]}├── {safe_name} (name contains special characters)\n")
                        
    except PermissionError:
        print(f"Error: Permission denied accessing {startpath}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate a file structure tree of a repository')
    parser.add_argument('path', nargs='?', default='.',
                      help='Path to the repository (default: current directory)')
    parser.add_argument('-o', '--output', default='repo_structure.txt',
                      help='Output file name (default: repo_structure.txt)')
    parser.add_argument('--exclude-dirs', nargs='*',
                      help='Additional directories to exclude')
    parser.add_argument('--exclude-files', nargs='*',
                      help='Additional file patterns to exclude')
    
    args = parser.parse_args()
    
    # Combine default exclusions with user-provided ones
    exclude_dirs = ['.git', 'node_modules', '__pycache__', 'venv', 'env', '.pytest_cache']
    exclude_files = ['*.pyc', '.DS_Store', '*.pyo', '*.pyd', '.env', 'Thumbs.db']
    
    if args.exclude_dirs:
        exclude_dirs.extend(args.exclude_dirs)
    if args.exclude_files:
        exclude_files.extend(args.exclude_files)
    
    # Convert relative path to absolute path
    try:
        input_path = Path(args.path).resolve()
        if not input_path.exists():
            print(f"Error: The path '{args.path}' does not exist.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: Invalid path '{args.path}': {str(e)}")
        sys.exit(1)
    
    try:
        generate_tree(input_path, exclude_dirs, exclude_files, args.output)
        print(f"File structure has been saved to {Path(args.output).absolute()}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)

if __name__ == '__main__':
    main()