import os
import sys
import subprocess
from pathlib import Path

def run_command(command):
    """Run a command and print output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error:", result.stderr)
        return False
    
    print("Success!")
    return True

def main():
    # Get script directory and project root
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    project_root = script_dir.parent if script_dir.name == 'scripts' else script_dir
    
    # Step 1: Run convert_csv_to_json.py
    print("\n1. Updating domains.json from CSV...")
    if not run_command(f"python {script_dir}/convert_csv_to_json.py"):
        print("Failed to convert CSV to JSON. Aborting.")
        sys.exit(1)
    
    # Step 2: Generate LLM-friendly data
    print("\n2. Generating LLM-friendly data files...")
    if not run_command(f"python {script_dir}/generate_llm_data.py"):
        print("Failed to generate LLM data. Aborting.")
        sys.exit(1)
    
    # Step 3: Update HTML metadata
    print("\n3. Updating HTML metadata...")
    if not run_command(f"python {script_dir}/update_metadata.py"):
        print("Failed to update metadata. Aborting.")
        sys.exit(1)
    
    # Step 4: Offer to launch dev server
    print("\n4. All updates complete!")
    choice = input("\nWould you like to:\n1. Start the dev server\n2. Build local test version\n3. Exit\nEnter choice (1-3): ")
    
    if choice == "1":
        print("\nStarting dev_server.py...")
        run_command(f"python {script_dir}/dev_server.py")
    elif choice == "2":
        print("\nBuilding local test version...")
        run_command(f"python {script_dir}/test_local.py")
        
        port = input("\nEnter port for test server (default: 8000): ") or "8000"
        print(f"\nStarting HTTP server on port {port}...")
        run_command(f"python -m http.server -d build {port}")
    else:
        print("\nExiting. All files have been updated.")
    
    # Step 5: Offer to commit changes
    commit = input("\nWould you like to commit and push changes to GitHub? (y/n): ")
    if commit.lower() == 'y':
        message = input("Enter commit message (default: 'Update domain list'): ") or "Update domain list"
        
        print("\nCommitting changes...")
        commands = [
            f"git add data/output/domains.json",
            f"git add domain_list.csv",
            f"git add docs/llm-data",
            f'git commit -m "{message}"',
            f"git push"
        ]
        
        for cmd in commands:
            if not run_command(cmd):
                print("Git operation failed. You may need to complete it manually.")
                break
        
        print("\nChanges pushed to GitHub. GitHub Actions will handle deployment.")

if __name__ == "__main__":
    main()