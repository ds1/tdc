import csv
import json
import os

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Define input and output paths relative to the script
csv_file = os.path.join(script_dir, 'source', 'domain_list.csv')
json_file = os.path.join(project_root, 'data', 'domains.json')

def calculate_length(domain_name):
    """Calculate the length of the domain name without the TLD."""
    return len(domain_name.split('.')[0])

def csv_to_json(csv_file, json_file):
    """Convert domain list CSV to JSON format."""
    domains = []
    
    with open(csv_file, 'r') as file:
        # Skip header row
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            domain = {
                "domainName": row['domainName'],
                "price": int(row['price']),  # Convert price to integer
                "category": row['category'],
                "tld": row['tld'],
                "imageUrl": f"/img/thumbnails/{row['domainName'].split('.')[0]}.jpg",
                "length": calculate_length(row['domainName'])
            }
            domains.append(domain)
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    
    # Write to JSON file with proper formatting
    with open(json_file, 'w') as file:
        json.dump(domains, file, indent=2)

    print(f"Successfully converted {len(domains)} domains to JSON format.")
    print(f"JSON file saved to: {json_file}")
    return domains

try:
    domains = csv_to_json(csv_file, json_file)
    print("\nFirst domain entry as example:")
    print(json.dumps(domains[0], indent=2))
except Exception as e:
    print(f"Error: {e}")