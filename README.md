# MovieWebApp
**Command‑line Movie Database with OMDb API & Static Website Export**

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-yellow)](https://www.sqlite.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.x-green)](https://www.sqlalchemy.org/)
[![OMDb API](https://img.shields.io/badge/OMDb_API-v1-orange)](http://www.omdbapi.com/)

## 🎯 Features

| Feature | Description |
|---------|-------------|
| **Add Movies** | Fetch details from OMDb by title or fall back to manual entry |
| **CRUD Operations** | List, update, and delete movies stored in a SQLite database |
| **Website Export** | Generate a styled HTML website listing all movies from a customizable template |
| **CLI Interface** | Menu‑driven console app with input validation and error handling |
| **Local Storage** | Persistent movie data via SQLite + SQLAlchemy ORM |

## 🏗️ Tech Stack

CLI & Backend: Python + SQLAlchemy + SQLite  
API: OMDb API (movie metadata)  
Frontend: Static HTML/CSS website generated from template  
Build: Pure Python, no heavy frameworks

## 🚀 Quick Start

```bash
# Clone & install
git clone https://github.com/seb0305/Movie-Project-SQL-HTML-API.git
cd Movie-Project-SQL-HTML-API

# Optional: create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set OMDb API key
# Edit storage/omdb_api.py and replace:
API_KEY = "YOUR_API_KEY"  # Replace with your real key here

# Run the app
python movies.py
```

## 🎬 How to Use

### Add Movies
- Choose "Add movie" from the menu.
- Enter a title; the app will try to fetch details from OMDb.
- If no result, fall back to manual entry (title, year, director, etc.).

### Browse & Edit
- Use "List movies" to see all stored entries.
- Select "Update movie" to edit title, year, director, or notes.
- Use "Delete movie" to remove entries by ID.

### Generate Website
- Select "Generate website" from the menu.
- The app reads the HTML template and CSS from `_static/`.
- Outputs a fresh `index.html` in the project root showing all movies.

### View Output
- Open `index.html` in any browser.
- The page lists movies with metadata and a clean, responsive layout.

## 🧠 Data Flow
- User input → Python CLI → SQLAlchemy ORM → SQLite (`data/movies.db`)  
- On "Generate website": ORM query → Jinja‑style template fill → `index.html`  
- OMDb API is called only when adding or refreshing a movie by title.

## 📊 Database Schema (simplified)

```text
movies
  id          INTEGER PRIMARY KEY
  title       TEXT NOT NULL
  year        TEXT
  director    TEXT
  genre       TEXT
  plot        TEXT
  poster_url  TEXT
  rating      REAL
  notes       TEXT

```

## 🔮 Future Roadmap
- Web UI (Flask/Dash) instead of CLI  
- Movie search & filters on the generated website  
- Star‑rating & watch‑status fields  
- Export to JSON or CSV  
- Batch import from CSV/JSON

## 🐛 Known Issues (Fixed)
✅ Manual‑entry fallback when OMDb returns no result  
✅ SQLite connection handling via SQLAlchemy  
✅ Proper escaping of HTML‑unsafe fields in template  
✅ CLI input validation (empty titles, invalid years)

## 📝 Development

```bash
# Add dev tools (optional)
pip install python-dotenv

# Run in debug mode (if you extend with a web layer)
python -m debugpy --listen 5678 movies.py
```

## 🙌 Contributing
- Fork the repo and open a PR with:

  - New CLI commands (e.g., search, filter, export).

  - Improved OMDb error handling or caching.

  - Better templates or responsive CSS.

- Bonus: add unit tests for storage/ modules.

## 📄 License
MIT – Free for personal and educational use.
