import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def update_metadata(file_path, metadata):
    """Update metadata in an HTML file."""
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the head tag
    head_tag = soup.head
    
    if not head_tag:
        print(f"No head tag found in {file_path}")
        return
    
    # Remove existing metadata tags
    for tag in head_tag.find_all(['meta', 'title']):
        if tag.get('name') in ['description', 'keywords', 'author', 'robots', 'revisit-after'] or \
           tag.get('property', '').startswith('og:') or \
           tag.get('name', '').startswith('twitter:'):
            tag.decompose()
    
    # Set title
    title_tag = head_tag.find('title')
    if title_tag:
        title_tag.string = metadata['title']
    else:
        title_tag = soup.new_tag('title')
        title_tag.string = metadata['title']
        head_tag.append(title_tag)
    
    # Add new metadata tags
    for name, content in metadata.items():
        if name == 'title':
            continue  # Skip title, we've already handled it
        
        if name.startswith('og:'):
            tag = soup.new_tag('meta')
            tag['property'] = name
            tag['content'] = content
        elif name.startswith('twitter:'):
            tag = soup.new_tag('meta')
            tag['name'] = name
            tag['content'] = content
        elif name == 'canonical':
            tag = soup.new_tag('link')
            tag['rel'] = 'canonical'
            tag['href'] = content
        else:
            tag = soup.new_tag('meta')
            tag['name'] = name
            tag['content'] = content
        
        head_tag.append(tag)
    
    # Write the updated HTML
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Updated metadata in {file_path}")

def add_schema_to_index(file_path, schema_path):
    """Add JSON-LD schema to the index.html file."""
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Read the schema
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    
    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove any existing JSON-LD scripts
    for script in soup.find_all('script', {'type': 'application/ld+json'}):
        script.decompose()
    
    # Add the schema before the closing body tag
    script_tag = soup.new_tag('script')
    script_tag['type'] = 'application/ld+json'
    script_tag.string = schema
    
    if soup.body:
        soup.body.append(script_tag)
    else:
        print(f"No body tag found in {file_path}")
        return
    
    # Write the updated HTML
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Added schema to {file_path}")

def main():
    # Define paths
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    project_root = script_dir.parent if script_dir.name == 'scripts' else script_dir
    
    docs_dir = project_root / 'docs'
    schema_file = project_root / 'docs' / 'llm-data' / 'index-schema.json'
    
    # Define metadata for each page
    metadata = {
        'index.html': {
            'title': 'TopDomain.Club - Premium Domain Marketplace',
            'description': 'Browse our curated selection of premium domains including .ai, .bot, .si, and more at TopDomain.Club. Find your perfect domain name for your next project.',
            'keywords': 'premium domains, domain marketplace, .ai domains, .bot domains, domain names for sale',
            'canonical': 'https://www.topdomain.club/',
            'og:title': 'TopDomain.Club - Premium Domain Marketplace',
            'og:description': 'Browse our curated selection of premium domains including .ai, .bot, .si, and more.',
            'og:image': 'https://www.topdomain.club/images/tdc_hero_logo.png',
            'og:url': 'https://www.topdomain.club/',
            'og:type': 'website',
            'og:site_name': 'TopDomain.Club',
            'twitter:card': 'summary_large_image',
            'twitter:title': 'TopDomain.Club - Premium Domain Marketplace',
            'twitter:description': 'Browse our curated selection of premium domains including .ai, .bot, .si, and more.',
            'twitter:image': 'https://www.topdomain.club/images/tdc_hero_logo.png',
            'twitter:site': '@TopDomainClub',
            'robots': 'index, follow',
            'language': 'English',
            'revisit-after': '7 days',
            'author': 'TopDomain.Club'
        },
        'about.html': {
            'title': 'About TopDomain.Club | Premium Domain Marketplace',
            'description': 'Learn about TopDomain.Club, your trusted source for premium domain names. Discover our mission, values, and commitment to helping you secure the perfect domain.',
            'keywords': 'about us, domain marketplace, premium domains, domain expertise',
            'canonical': 'https://www.topdomain.club/about.html',
            'og:title': 'About TopDomain.Club | Premium Domain Marketplace',
            'og:description': 'Learn about TopDomain.Club, your trusted source for premium domain names.',
            'og:image': 'https://www.topdomain.club/images/tdc_hero_logo.png',
            'og:url': 'https://www.topdomain.club/about.html',
            'og:type': 'website',
            'og:site_name': 'TopDomain.Club',
            'twitter:card': 'summary_large_image',
            'twitter:title': 'About TopDomain.Club | Premium Domain Marketplace',
            'twitter:description': 'Learn about TopDomain.Club, your trusted source for premium domain names.',
            'twitter:image': 'https://www.topdomain.club/images/tdc_hero_logo.png',
            'twitter:site': '@TopDomainClub',
            'robots': 'index, follow',
            'language': 'English',
            'revisit-after': '30 days',
            'author': 'TopDomain.Club'
        },
        'contact.html': {
            'title': 'Contact TopDomain.Club | Get in Touch',
            'description': 'Have questions or need assistance? Contact TopDomain.Club for expert support with your domain purchase. We\'re here to help you find the perfect domain name.',
            'keywords': 'contact us, domain support, domain inquiry, premium domains, domain marketplace',
            'canonical': 'https://www.topdomain.club/contact.html',
            'og:title': 'Contact TopDomain.Club | Get in Touch',
            'og:description': 'Have questions or need assistance? Contact us for expert support with your domain purchase.',
            'og:image': 'https://www.topdomain.club/images/tdc_hero_logo.png',
            'og:url': 'https://www.topdomain.club/contact.html',
            'og:type': 'website',
            'og:site_name': 'TopDomain.Club',
            'twitter:card': 'summary_large_image',
            'twitter:title': 'Contact TopDomain.Club | Get in Touch',
            'twitter:description': 'Have questions or need assistance? Contact us for expert support with your domain purchase.',
            'twitter:image': 'https://www.topdomain.club/images/tdc_hero_logo.png',
            'twitter:site': '@TopDomainClub',
            'robots': 'index, follow',
            'language': 'English',
            'revisit-after': '30 days',
            'author': 'TopDomain.Club'
        },
        'updates.html': {
            'title': 'Updates - TopDomain.Club',
            'description': 'Get the latest updates from TopDomain.Club. Stay informed about new domain additions, promotions, and news from our premium domain marketplace.',
            'keywords': 'domain updates, domain news, premium domains, domain marketplace',
            'canonical': 'https://www.topdomain.club/updates.html',
            'og:title': 'Updates - TopDomain.Club',
            'og:description': 'Get the latest updates from TopDomain.Club.',
            'og:image': 'https://www.topdomain.club/images/tdc_hero_logo.png',
            'og:url': 'https://www.topdomain.club/updates.html',
            'og:type': 'website',
            'og:site_name': 'TopDomain.Club',
            'twitter:card': 'summary_large_image',
            'twitter:title': 'Updates - TopDomain.Club',
            'twitter:description': 'Get the latest updates from TopDomain.Club.',
            'twitter:image': 'https://www.topdomain.club/images/tdc_hero_logo.png',
            'twitter:site': '@TopDomainClub',
            'robots': 'index, follow',
            'language': 'English',
            'revisit-after': '7 days',
            'author': 'TopDomain.Club'
        }
    }
    
    # Update metadata for each page
    for file_name, meta in metadata.items():
        file_path = docs_dir / file_name
        if file_path.exists():
            update_metadata(file_path, meta)
        else:
            print(f"Warning: {file_path} does not exist")
    
    # Add schema to index.html
    if schema_file.exists():
        add_schema_to_index(docs_dir / 'index.html', schema_file)
    else:
        print(f"Warning: Schema file {schema_file} does not exist. Run generate_llm_data.py first.")
    
    print("All metadata updates complete!")

if __name__ == "__main__":
    main()