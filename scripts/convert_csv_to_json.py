import csv
import json
import os

def calculate_length(domain_name):
    """Calculate the length of the domain name without the TLD."""
    return len(domain_name.split('.')[0])

def get_safe_filename(domain_name):
    """
    Create a safe, unique filename for each domain including both SLD and TLD.
    Example: 'ai.prices' becomes 'ai_prices'
    """
    return domain_name.replace('.', '_')

def csv_to_json(csv_file, json_file):
    """Convert domain list CSV to JSON format."""
    domains = []
    
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            domain_name = row['domainName']
            safe_filename = get_safe_filename(domain_name)
            
            # Handle empty price values by setting a default or converting only if not empty
            price_value = 0  # Default value
            if row['price'] and row['price'].strip():  # Check if price exists and is not just whitespace
                try:
                    price_value = int(row['price'])
                except ValueError:
                    print(f"Warning: Invalid price for domain {domain_name}. Using default value 0.")
            
            domain = {
                "domainName": domain_name,
                "price": price_value,
                "category": row['category'],
                "tld": row['tld'],
                # Use the safe filename that includes both SLD and TLD
                "imageUrl": f"/data/output/thumbnails/{safe_filename}.jpg",
                "length": calculate_length(domain_name)
            }
            domains.append(domain)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    
    # Write to JSON file with proper formatting
    with open(json_file, 'w') as file:
        json.dump(domains, file, indent=2)

    print(f"Successfully converted {len(domains)} domains to JSON format.")
    print(f"JSON file saved to: {json_file}")
    
    # Print some validation information
    tlds = {}
    for domain in domains:
        name = domain['domainName']
        tld = domain['tld']
        if name.split('.')[0] in tlds:
            tlds[name.split('.')[0]].append(tld)
        else:
            tlds[name.split('.')[0]] = [tld]
    
    # Print domains that have multiple TLDs
    print("\nDomains with multiple TLDs:")
    for sld, tld_list in tlds.items():
        if len(tld_list) > 1:
            print(f"{sld}: {', '.join(tld_list)}")
    
    return domains

if __name__ == "__main__":
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Define input and output paths relative to project root
    csv_file = os.path.join(project_root, 'data', 'input', 'domain_list.csv')
    json_file = os.path.join(project_root, 'data', 'output', 'domains.json')
    
    try:
        domains = csv_to_json(csv_file, json_file)
        print("\nFirst domain entry as example:")
        print(json.dumps(domains[0], indent=2))
    except Exception as e:
        print(f"Error: {e}")