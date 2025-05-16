import json
import csv
import os
import datetime
from pathlib import Path

def load_domains(json_file):
    """Load domains from JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_directory_html(domains, output_file):
    """Create a static HTML directory of domains."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    html_start = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TopDomain.Club - Premium Domain Directory</title>
    <meta name="description" content="Complete directory of premium domains available at TopDomain.Club. Browse our inventory of premium domain names categorized by TLD and price range.">
    <meta name="keywords" content="premium domains, domain marketplace, domain directory, domain list, domains for sale">
    <link rel="canonical" href="https://www.topdomain.club/directory.html">
    
    <!-- Open Graph Tags -->
    <meta property="og:title" content="TopDomain.Club - Premium Domain Directory">
    <meta property="og:description" content="Browse our complete directory of premium domains available for purchase.">
    <meta property="og:image" content="https://www.topdomain.club/images/tdc_hero_logo.png">
    <meta property="og:url" content="https://www.topdomain.club/directory.html">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="TopDomain.Club">
    
    <!-- Twitter Card Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="TopDomain.Club - Premium Domain Directory">
    <meta name="twitter:description" content="Browse our complete directory of premium domains available for purchase.">
    <meta name="twitter:image" content="https://www.topdomain.club/images/tdc_hero_logo.png">
    <meta name="twitter:site" content="@TopDomainClub">
    
    <!-- Other Meta Tags -->
    <meta name="robots" content="index, follow">
    <meta name="language" content="English">
    <meta name="revisit-after" content="7 days">
    <meta name="author" content="TopDomain.Club">
    <meta name="lastmod" content="{today}">
    
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f2f2f2; }}
        h1 {{ color: #333; }}
        .price {{ color: #2f855a; font-weight: bold; }}
        footer {{ margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px; }}
        header {{ margin-bottom: 30px; }}
        .back-home {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <header>
        <div class="back-home">
            <a href="/">← Back to Home</a>
        </div>
        <h1>TopDomain.Club Domain Directory</h1>
        <p>Complete list of our premium domains with prices and categories. Last updated: {today}</p>
    </header>
    
    <main>
        <table>
            <thead>
                <tr>
                    <th>Domain Name</th>
                    <th>Price</th>
                    <th>Category</th>
                    <th>TLD</th>
                    <th>Length</th>
                </tr>
            </thead>
            <tbody>
"""
    
    html_end = """            </tbody>
        </table>
    </main>
    
    <footer>
        <p>© 2025 TopDomain.Club. All rights reserved.</p>
        <p>
            <a href="/about.html">About Us</a> | 
            <a href="/contact.html">Contact</a> | 
            <a href="/updates.html">Updates</a> | 
            <a href="/categories/">Browse by Category</a>
        </p>
    </footer>

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Table",
      "about": "Premium Domain Listings",
      "description": "A comprehensive directory of premium domains available at TopDomain.Club"
    }
    </script>
</body>
</html>"""

    # Create the HTML rows for each domain
    html_rows = ""
    for domain in domains:
        price_formatted = "${:,}".format(domain['price'])
        html_rows += f"""                <tr>
                    <td><a href="https://{domain['domainName']}">{domain['domainName']}</a></td>
                    <td class="price">{price_formatted}</td>
                    <td>{domain['category']}</td>
                    <td>{domain['tld']}</td>
                    <td>{domain['length']}</td>
                </tr>
"""
    
    # Write the complete HTML file
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html_start + html_rows + html_end)
    
    print(f"Created HTML directory: {output_file}")

def create_csv_export(domains, output_file):
    """Create a CSV export of domains."""
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(['Domain Name', 'Price', 'Category', 'TLD', 'Length', 'URL'])
        
        # Write domain data
        for domain in domains:
            writer.writerow([
                domain['domainName'],
                domain['price'],
                domain['category'],
                domain['tld'],
                domain['length'],
                f"https://{domain['domainName']}"
            ])
    
    print(f"Created CSV export: {output_file}")

def create_json_ld(domains, output_file, full_file=False):
    """Create JSON-LD schema markup."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    json_ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "TopDomain.Club Premium Domains",
        "description": "A curated list of premium domain names available for purchase",
        "url": "https://www.topdomain.club",
        "numberOfItems": len(domains),
        "dateModified": today,
        "itemListElement": []
    }
    
    for i, domain in enumerate(domains, 1):
        item = {
            "@type": "ListItem",
            "position": i,
            "item": {
                "@type": "Product",
                "name": domain['domainName'],
                "description": f"Premium {domain['category']} domain name with {domain['length']} characters",
                "offers": {
                    "@type": "Offer",
                    "price": domain['price'],
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock",
                    "url": f"https://{domain['domainName']}"
                },
                "category": domain['category'],
                "productID": f"domain-{domain['domainName']}"
            }
        }
        json_ld["itemListElement"].append(item)
    
    # If creating full file, wrap in HTML
    if full_file:
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TopDomain.Club - Domain Schema Data</title>
    <meta name="robots" content="noindex">
</head>
<body>
    <h1>TopDomain.Club Structured Data</h1>
    <p>This page contains structured data for our domain listings. Last updated: {today}</p>
    
    <script type="application/ld+json">
{json.dumps(json_ld, indent=2)}
    </script>
</body>
</html>"""
        with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html_content)
    else:
        # Just write the JSON-LD
        with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(json_ld, f, indent=2)
    
    print(f"Created JSON-LD schema: {output_file}")

def get_categories_and_tlds(domains):
    """Extract unique categories and TLDs from domains."""
    categories = set()
    tlds = set()
    
    for domain in domains:
        categories.add(domain['category'])
        tlds.add(domain['tld'])
    
    return sorted(list(categories)), sorted(list(tlds))

def create_sitemap(domains, categories, tlds, output_file):
    """Create a sitemap.xml file with domain links."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    xml_start = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <!-- Main website URLs -->
    <url>
        <loc>https://www.topdomain.club/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://www.topdomain.club/about.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://www.topdomain.club/contact.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://www.topdomain.club/updates.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://www.topdomain.club/directory.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://www.topdomain.club/categories/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
"""
    
    # Add category pages
    for category in categories:
        xml_start += f"""    <url>
        <loc>https://www.topdomain.club/categories/category-{category}.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.7</priority>
    </url>
"""
    
    # Add TLD pages
    for tld in tlds:
        xml_start += f"""    <url>
        <loc>https://www.topdomain.club/categories/tld-{tld}.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.7</priority>
    </url>
"""
    
    xml_end = """</urlset>"""
    
    # Create entries for domains
    domain_entries = ""
    for domain in domains:
        domain_entries += f"""    <url>
        <loc>https://{domain['domainName']}</loc>
        <priority>0.6</priority>
    </url>
"""
    
    # Write the complete sitemap
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(xml_start + domain_entries + xml_end)
    
    print(f"Created sitemap: {output_file}")

def create_robots_txt(output_file):
    """Create a robots.txt file for the site."""
    content = """User-agent: *
Allow: /

# Explicitly allow crawling of important directories
Allow: /llm-data/
Allow: /categories/
Allow: /data/output/domains.json

# Sitemap location
Sitemap: https://www.topdomain.club/sitemap.xml
"""
    
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    
    print(f"Created robots.txt: {output_file}")

def create_markdown_list(domains, output_file):
    """Create a markdown list of domains."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    markdown = f"# TopDomain.Club Premium Domains\n\n"
    markdown += f"Last updated: {today}\n\n"
    markdown += "| Domain Name | Price | Category | TLD | Length |\n"
    markdown += "|-------------|-------|----------|-----|--------|\n"
    
    for domain in domains:
        price_formatted = "${:,}".format(domain['price'])
        markdown += f"| [{domain['domainName']}](https://{domain['domainName']}) | {price_formatted} | {domain['category']} | {domain['tld']} | {domain['length']} |\n"
    
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(markdown)
    
    print(f"Created markdown list: {output_file}")

def create_txt_list(domains, output_file):
    """Create a simple text list of domains."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(f"TopDomain.Club Premium Domains - {today}\n")
        f.write("==============================\n\n")
        
        for domain in domains:
            price_formatted = "${:,}".format(domain['price'])
            f.write(f"{domain['domainName']} - {price_formatted} - {domain['category']}\n")
    
    print(f"Created text list: {output_file}")

def create_category_page(category, domains, output_file):
    """Create an HTML page for a specific category."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    html_start = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category.capitalize()} Domains - TopDomain.Club</title>
    <meta name="description" content="Browse our selection of premium {category} domain names at TopDomain.Club.">
    <meta name="keywords" content="{category} domains, premium domains, domain marketplace, {category} domain names">
    <link rel="canonical" href="https://www.topdomain.club/categories/{os.path.basename(output_file)}">
    
    <!-- Open Graph Tags -->
    <meta property="og:title" content="{category.capitalize()} Domains - TopDomain.Club">
    <meta property="og:description" content="Browse our selection of premium {category} domain names.">
    <meta property="og:image" content="https://www.topdomain.club/images/tdc_hero_logo.png">
    <meta property="og:url" content="https://www.topdomain.club/categories/{os.path.basename(output_file)}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="TopDomain.Club">
    
    <!-- Twitter Card Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{category.capitalize()} Domains - TopDomain.Club">
    <meta name="twitter:description" content="Browse our selection of premium {category} domain names.">
    <meta name="twitter:image" content="https://www.topdomain.club/images/tdc_hero_logo.png">
    <meta name="twitter:site" content="@TopDomainClub">
    
    <!-- Other Meta Tags -->
    <meta name="robots" content="index, follow">
    <meta name="language" content="English">
    <meta name="revisit-after" content="7 days">
    <meta name="author" content="TopDomain.Club">
    <meta name="lastmod" content="{today}">
    
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f2f2f2; }}
        h1 {{ color: #333; }}
        .price {{ color: #2f855a; font-weight: bold; }}
        footer {{ margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px; }}
        header {{ margin-bottom: 30px; }}
        .navigation {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <header>
        <div class="navigation">
            <a href="index.html">← Back to Categories</a> | <a href="/">Home</a>
        </div>
        <h1>{category.capitalize()} Domains</h1>
        <p>Browse our premium selection of {category} domain names. Last updated: {today}</p>
    </header>
    
    <main>
        <table>
            <thead>
                <tr>
                    <th>Domain Name</th>
                    <th>Price</th>
                    <th>TLD</th>
                    <th>Length</th>
                </tr>
            </thead>
            <tbody>
"""
    
    html_end = """            </tbody>
        </table>
    </main>
    
    <footer>
        <p>© 2025 TopDomain.Club. All rights reserved.</p>
        <p>
            <a href="/about.html">About Us</a> | 
            <a href="/contact.html">Contact</a> | 
            <a href="/updates.html">Updates</a> | 
            <a href="/directory.html">Full Directory</a>
        </p>
    </footer>

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "Premium """ + category.capitalize() + """ Domains",
      "description": "A list of premium """ + category.capitalize() + """ domain names available at TopDomain.Club"
    }
    </script>
</body>
</html>"""

    # Create the HTML rows for each domain
    html_rows = ""
    for domain in domains:
        price_formatted = "${:,}".format(domain['price'])
        html_rows += f"""                <tr>
                    <td><a href="https://{domain['domainName']}">{domain['domainName']}</a></td>
                    <td class="price">{price_formatted}</td>
                    <td>{domain['tld']}</td>
                    <td>{domain['length']}</td>
                </tr>
"""
    
    # Write the complete HTML file
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html_start + html_rows + html_end)
    
    print(f"Created category page: {output_file}")

def create_tld_page(tld, domains, output_file):
    """Create an HTML page for a specific TLD."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    html_start = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>.{tld} Domains - TopDomain.Club</title>
    <meta name="description" content="Browse our selection of premium .{tld} domain names at TopDomain.Club.">
    <meta name="keywords" content=".{tld} domains, {tld} domain names, premium domains, domain marketplace">
    <link rel="canonical" href="https://www.topdomain.club/categories/{os.path.basename(output_file)}">
    
    <!-- Open Graph Tags -->
    <meta property="og:title" content=".{tld} Domains - TopDomain.Club">
    <meta property="og:description" content="Browse our selection of premium .{tld} domain names.">
    <meta property="og:image" content="https://www.topdomain.club/images/tdc_hero_logo.png">
    <meta property="og:url" content="https://www.topdomain.club/categories/{os.path.basename(output_file)}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="TopDomain.Club">
    
    <!-- Twitter Card Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content=".{tld} Domains - TopDomain.Club">
    <meta name="twitter:description" content="Browse our selection of premium .{tld} domain names.">
    <meta name="twitter:image" content="https://www.topdomain.club/images/tdc_hero_logo.png">
    <meta name="twitter:site" content="@TopDomainClub">
    
    <!-- Other Meta Tags -->
    <meta name="robots" content="index, follow">
    <meta name="language" content="English">
    <meta name="revisit-after" content="7 days">
    <meta name="author" content="TopDomain.Club">
    <meta name="lastmod" content="{today}">
    
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f2f2f2; }}
        h1 {{ color: #333; }}
        .price {{ color: #2f855a; font-weight: bold; }}
        footer {{ margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px; }}
        header {{ margin-bottom: 30px; }}
        .navigation {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <header>
        <div class="navigation">
            <a href="index.html">← Back to Categories</a> | <a href="/">Home</a>
        </div>
        <h1>.{tld} Domains</h1>
        <p>Browse our premium selection of .{tld} domain names. Last updated: {today}</p>
    </header>
    
    <main>
        <table>
            <thead>
                <tr>
                    <th>Domain Name</th>
                    <th>Price</th>
                    <th>Category</th>
                    <th>Length</th>
                </tr>
            </thead>
            <tbody>
"""
    
    html_end = """            </tbody>
        </table>
    </main>
    
    <footer>
        <p>© 2025 TopDomain.Club. All rights reserved.</p>
        <p>
            <a href="/about.html">About Us</a> | 
            <a href="/contact.html">Contact</a> | 
            <a href="/updates.html">Updates</a> | 
            <a href="/directory.html">Full Directory</a>
        </p>
    </footer>

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "Premium .""" + tld + """ Domains",
      "description": "A list of premium .""" + tld + """ domain names available at TopDomain.Club"
    }
    </script>
</body>
</html>"""

    # Create the HTML rows for each domain
    html_rows = ""
    for domain in domains:
        price_formatted = "${:,}".format(domain['price'])
        html_rows += f"""                <tr>
                    <td><a href="https://{domain['domainName']}">{domain['domainName']}</a></td>
                    <td class="price">{price_formatted}</td>
                    <td>{domain['category']}</td>
                    <td>{domain['length']}</td>
                </tr>
"""
    
    # Write the complete HTML file
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html_start + html_rows + html_end)
    
    print(f"Created TLD page: {output_file}")

def create_categories_index(categories, tlds, output_file):
    """Create an index page for categories and TLDs."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Domain Categories - TopDomain.Club</title>
    <meta name="description" content="Browse our premium domains by category or TLD at TopDomain.Club.">
    <meta name="keywords" content="domain categories, domain extensions, TLDs, premium domains, domain marketplace">
    <link rel="canonical" href="https://www.topdomain.club/categories/">
    
    <!-- Open Graph Tags -->
    <meta property="og:title" content="Domain Categories - TopDomain.Club">
    <meta property="og:description" content="Browse our premium domains by category or TLD.">
    <meta property="og:image" content="https://www.topdomain.club/images/tdc_hero_logo.png">
    <meta property="og:url" content="https://www.topdomain.club/categories/">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="TopDomain.Club">
    
    <!-- Twitter Card Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Domain Categories - TopDomain.Club">
    <meta name="twitter:description" content="Browse our premium domains by category or TLD.">
    <meta name="twitter:image" content="https://www.topdomain.club/images/tdc_hero_logo.png">
    <meta name="twitter:site" content="@TopDomainClub">
    
    <!-- Other Meta Tags -->
    <meta name="robots" content="index, follow">
    <meta name="language" content="English">
    <meta name="revisit-after" content="7 days">
    <meta name="author" content="TopDomain.Club">
    <meta name="lastmod" content="{today}">
    
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
        h1, h2 {{ color: #333; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin-bottom: 10px; }}
        a {{ color: #007bff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        section {{ margin-bottom: 30px; }}
        footer {{ margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px; }}
        .card-container {{ display: flex; flex-wrap: wrap; gap: 20px; }}
        .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 15px; min-width: 200px; }}
        header {{ margin-bottom: 30px; }}
        .navigation {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <header>
        <div class="navigation">
            <a href="/">← Back to Home</a>
        </div>
        <h1>Domain Categories & TLDs</h1>
        <p>Browse our premium domains by category or extension. Last updated: {today}</p>
    </header>
    
    <main>
        <section>
            <h2>Browse by Category</h2>
            <div class="card-container">
"""
    
    # Add category links
    for category in sorted(categories):
        html += f"""                <div class="card">
                    <h3>{category.capitalize()}</h3>
                    <p><a href="category-{category}.html">View {category} domains</a></p>
                </div>
"""
    
    html += """            </div>
        </section>
        
        <section>
            <h2>Browse by TLD</h2>
            <div class="card-container">
"""
    
    # Add TLD links
    for tld in sorted(tlds):
        html += f"""                <div class="card">
                    <h3>.{tld}</h3>
                    <p><a href="tld-{tld}.html">View .{tld} domains</a></p>
                </div>
"""
    
    html += """            </div>
        </section>
    </main>
    
    <footer>
        <p>© 2025 TopDomain.Club. All rights reserved.</p>
        <p>
            <a href="/about.html">About Us</a> | 
            <a href="/contact.html">Contact</a> | 
            <a href="/updates.html">Updates</a> | 
            <a href="/directory.html">Full Directory</a>
        </p>
    </footer>

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "Domain Categories",
      "description": "Browse domains by category or TLD at TopDomain.Club"
    }
    </script>
</body>
</html>"""
    
    # Write the index file
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    
    print(f"Created categories index: {output_file}")

def create_categories_html(domains, output_dir):
    """Create HTML pages for each category and TLD of domains."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Group domains by category
    categories = {}
    for domain in domains:
        category = domain['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(domain)
    
    # Group domains by TLD
    tlds = {}
    for domain in domains:
        tld = domain['tld']
        if tld not in tlds:
            tlds[tld] = []
        tlds[tld].append(domain)
    
    # Create category pages
    for category, category_domains in categories.items():
        output_file = os.path.join(output_dir, f"category-{category}.html")
        create_category_page(category, category_domains, output_file)
    
    # Create TLD pages
    for tld, tld_domains in tlds.items():
        output_file = os.path.join(output_dir, f"tld-{tld}.html")
        create_tld_page(tld, tld_domains, output_file)
    
    # Create an index page linking to all category and TLD pages
    create_categories_index(categories.keys(), tlds.keys(), os.path.join(output_dir, "index.html"))

def create_json_ld_for_index(domains, output_file):
    """Create JSON-LD schema markup for the index page."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    # Group domains by category for statistics
    categories = {}
    tlds = {}
    for domain in domains:
        cat = domain['category']
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
        
        tld = domain['tld']
        if tld not in tlds:
            tlds[tld] = 0
        tlds[tld] += 1
    
    # Create the organization markup
    organization = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "TopDomain.Club",
        "url": "https://www.topdomain.club",
        "logo": "https://www.topdomain.club/images/tdc_hero_logo.png",
        "description": "Premium domain marketplace offering domains in categories like AI, bot, tech and more.",
        "sameAs": [
            "https://twitter.com/TopDomainClub"
        ]
    }
    
    # Create the WebSite markup
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "TopDomain.Club",
        "url": "https://www.topdomain.club",
        "description": "Premium domain marketplace with curated domain names for sale.",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.topdomain.club/?search={search_term_string}",
            "query-input": "required name=search_term_string"
        }
    }
    
    # Create the ItemList markup (shortened version for the homepage)
    sample_domains = domains[:10]  # Just show first 10 domains
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Featured Premium Domains",
        "description": "A selection of premium domain names available for purchase",
        "url": "https://www.topdomain.club",
        "numberOfItems": len(sample_domains),
        "itemListElement": []
    }
    
    for i, domain in enumerate(sample_domains, 1):
        item = {
            "@type": "ListItem",
            "position": i,
            "item": {
                "@type": "Product",
                "name": domain['domainName'],
                "description": f"Premium {domain['category']} domain name with {domain['length']} characters",
                "url": f"https://{domain['domainName']}",
                "category": domain['category']
            }
        }
        item_list["itemListElement"].append(item)
    
    # Create the marketplace offer breadcrumb
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://www.topdomain.club/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Domain Directory",
                "item": "https://www.topdomain.club/directory.html"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": "Categories",
                "item": "https://www.topdomain.club/categories/"
            }
        ]
    }
    
    # Output all the JSON-LD objects
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps([organization, website, item_list, breadcrumb], indent=2))
    
    print(f"Created JSON-LD for index page: {output_file}")

def main():
    # Define paths
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    project_root = script_dir.parent if script_dir.name == 'scripts' else script_dir
    
    # Input and output paths
    domains_json = project_root / 'data' / 'output' / 'domains.json'
    output_dir = project_root / 'docs' / 'llm-data'
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load domains
    domains = load_domains(domains_json)
    print(f"Loaded {len(domains)} domains from {domains_json}")
    
    # Get unique categories and TLDs
    categories, tlds = get_categories_and_tlds(domains)
    
    # Create various exports
    create_directory_html(domains, output_dir / 'directory.html')
    create_csv_export(domains, output_dir / 'domains.csv')
    create_json_ld(domains, output_dir / 'domains-schema.json')
    create_json_ld(domains, output_dir / 'domains-schema.html', full_file=True)
    create_json_ld_for_index(domains, output_dir / 'index-schema.json')
    create_sitemap(domains, categories, tlds, output_dir / 'sitemap.xml')
    create_robots_txt(output_dir / 'robots.txt')
    create_markdown_list(domains, output_dir / 'domains.md')
    create_txt_list(domains, output_dir / 'domains.txt')
    
    # Create category-based HTML files
    categories_dir = output_dir / 'categories'
    create_categories_html(domains, categories_dir)
    
    print(f"All files created successfully in {output_dir}")

if __name__ == "__main__":
    main()