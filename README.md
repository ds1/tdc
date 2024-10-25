# TopDomain.Club

Repository for the TopDomain.Club website, a premium domain marketplace.

## Project Structure

```
tdc/
├── scripts/            # Data processing and setup scripts
├── data/              # Data files
│   ├── input/         # Source data files
│   └── output/        # Generated data and assets
├── src/               # Website source files
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
└── README.md
```

## Setup

1. Place your domain list in `data/input/domain_list.csv`
2. Run the conversion script:
   ```bash
   python scripts/convert_csv_to_json.py
   ```
3. Generate thumbnails:
   ```bash
   python scripts/generate_thumbnails.py
   ```

## Development

### Starting the Development Server

You can start the development server using either method:

1. Using the development server script (recommended):
   ```bash
   python scripts/dev_server.py
   ```

2. Or manually from the src directory:
   ```bash
   cd src && python -m http.server 8080
   ```

The website will be available at http://localhost:8080

### File Structure

The website files are in the `src` directory:
- `index.html` - Homepage
- `about.html` - About page
- `contact.html` - Contact page
- `search.html` - Domain search page
- `css/styles.min.css` - Minified styles
- `js/script.min.js` - Minified JavaScript

### Data Files

- Domain data is stored in `data/output/domains.json`
- Domain thumbnails are generated in `data/output/thumbnails/`
