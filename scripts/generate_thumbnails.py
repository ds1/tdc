import json
from PIL import Image, ImageDraw, ImageFont
import colorsys
import os

def generate_color(text):
    """Generate a color based on the text."""
    hue = sum(ord(c) for c in text) % 360 / 360.0
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(hue, 0.5, 0.95))

def get_safe_filename(domain_name):
    """
    Create a safe, unique filename for each domain including both SLD and TLD.
    Example: 'ai.prices' becomes 'ai_prices'
    """
    return domain_name.replace('.', '_')

def create_thumbnail(domain, size=(200, 200)):
    """Create a thumbnail for a domain."""
    color = generate_color(domain['domainName'])
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Display full domain name including TLD
    text = domain['domainName']
    if len(text) > 15:  # Increased threshold since we're showing full domain
        parts = text.split('.')
        text = '\n'.join(parts)

    text_color = (0, 0, 0)  # Black text
    text_pos = (size[0]/2, size[1]/2)
    draw.text(text_pos, text, font=font, fill=text_color, anchor="mm", align="center")

    return img

if __name__ == "__main__":
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Construct paths
    json_path = os.path.join(project_root, 'data', 'output', 'domains.json')
    thumbnails_dir = os.path.join(project_root, 'data', 'output', 'thumbnails')
    
    # Create thumbnails directory if it doesn't exist
    os.makedirs(thumbnails_dir, exist_ok=True)
    
    # Load the JSON data
    with open(json_path, 'r') as f:
        domains = json.load(f)
    
    # Generate thumbnails for each domain
    for domain in domains:
        img = create_thumbnail(domain)
        # Use full domain name for the filename to ensure uniqueness
        safe_filename = get_safe_filename(domain['domainName'])
        filename = os.path.join(thumbnails_dir, f"{safe_filename}.jpg")
        img.save(filename)
        print(f"Created thumbnail for {domain['domainName']} -> {filename}")
    
    print("\nAll thumbnails created successfully!")
    print(f"Total domains processed: {len(domains)}")