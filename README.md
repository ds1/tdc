# TopDomain.Club

Repository for the TopDomain.Club website, a premium domain marketplace.

## Project Structure

```
topdomain.club/             # Root directory
├── .github/                # GitHub configuration
│   └── workflows/          # GitHub Actions workflows
│       └── deploy.yml      # Deployment configuration
├── scripts/                # Python scripts
│   ├── convert_csv_to_json.py    # Data processing script
│   └── dev_server.py            # Local development server
├── data/                   # Data files
│   ├── input/             # Source data files
│   │   └── domain_list.csv     # Raw domain data
│   └── output/            # Generated data and assets
│       ├── custom_previews/    # Custom domain preview images (1600x800)
│       │   ├── .gitkeep
│       │   └── domain_name.jpg  # Example preview
│       └── domains.json        # Processed domain data
├── src/                    # Website source files
│   ├── css/               # Stylesheets
│   │   └── styles.min.css      # Minified CSS
│   ├── js/                # JavaScript files
│   │   └── script.min.js       # Minified JS
│   ├── domains/           # Domain detail pages
│   │   └── template.html       # Detail page template
│   ├── about.html         # About page
│   ├── contact.html       # Contact page
│   └── index.html         # Homepage
├── build/                 # Generated site (gitignored)
├── .gitignore            # Git ignore configuration
├── CNAME                 # GitHub Pages custom domain config
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```
Each directory serves a specific purpose:
- `.github/`: Contains GitHub-specific configurations and workflows
- `scripts/`: Python utilities for data processing and local development
- `data/`: Raw and processed data files
  - `input/`: Source CSV files
  - `output/`: Generated JSON and custom preview images
- `src/`: Website source files that get deployed
- `build/`: Generated site (created during deployment, not committed)

## Development

## Development (Windows with Anaconda)

### Setup
1. Install Anaconda from https://www.anaconda.com/
2. Open Anaconda PowerShell Prompt
3. Create and activate environment:
   ```powershell
   conda create -n topdomain python=3.11
   conda activate topdomain
   ```
4. Install dependencies:
`pip install -r requirements.txt`

Local Development

1. Activate environment:
`conda activate topdomain`

2. Process domain data:
`python .\scripts\convert_csv_to_json.py`

3. Start development server:
`python .\scripts\dev_server.py`

4. Visit http://localhost:8080

## Adding Custom Domain Previews

1. Prepare your image (1600x800 pixels, JPG format)
2. Convert domain name to lowercase and replace dots with underscores
- Example: `SpaceRace.ai` → `spacerace_ai.jpg`
3. Place image in `data\output\custom_previews\`

## Deployment

1. Ensure all changes are committed:
`git add .
git commit -m "Your update message"`

2. Push to GitHub:
`git push origin main`

3. GitHub Actions will automatically deploy to `topdomain.club`

