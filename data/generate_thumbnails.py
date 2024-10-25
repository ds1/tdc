import json
from PIL import Image, ImageDraw, ImageFont
import colorsys
import os

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

def generate_color(text):
    """Generate a color based on the text."""
    hue = sum(ord(c) for c in text) % 360 / 360.0
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(hue, 0.5, 0.95))

def create_thumbnail(domain, size=(200, 200)):
    """Create a thumbnail for a domain."""
    # Create a new image with a color based on the domain name
    color = generate_color(domain['domainName'])
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)

    # Use a default font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Split the domain name if it's too long
    text = domain['domainName']
    if len(text) > 10:
        parts = text.split('.')
        text = '\n'.join(parts)

    # Draw the text
    text_color = (0, 0, 0)  # Black text
    text_pos = (size[0]/2, size[1]/2)
    draw.text(text_pos, text, font=font, fill=text_color, anchor="mm", align="center")

    return img

# Construct the full path to domains.json
json_path = os.path.join(script_dir, 'domains.json')

# Load the JSON data
with open(json_path, 'r') as f:
    domains = json.load(f)

# Construct the full path to the thumbnails directory
thumbnails_dir = os.path.join(script_dir, '..', 'img', 'thumbnails')

# Create the thumbnails directory if it doesn't exist
os.makedirs(thumbnails_dir, exist_ok=True)

# Generate thumbnails for each domain
for domain in domains:
    img = create_thumbnail(domain)
    filename = os.path.join(thumbnails_dir, f"{domain['domainName'].split('.')[0]}.jpg")
    img.save(filename)
    print(f"Created thumbnail for {domain['domainName']}")

print("All thumbnails created successfully!")