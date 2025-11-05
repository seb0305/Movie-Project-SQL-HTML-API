# Movie Database Project

## About
This project is a Python-based Movie Database system that supports storing movie information locally with SQLite, integrating data from the OMDb API, and generating a dynamic website listing all stored movies.

## Features
- Add movies by fetching details from OMDb automatically or manual entry fallback.
- List, update, and delete movies stored in a SQLite database via SQLAlchemy.
- Generate a styled HTML website of movies based on a customizable template.
- Command-line interface with data validation and error handling.

## Project Structure
- `movies.py`: Main application CLI interface.
- `storage/`: Contains database and OMDb API modules.
- `_static/`: Static HTML template and CSS for website generation.
- `data/`: Stores the SQLite database file `movies.db`.

## Setup

### Prerequisites
- Python 3.7+
- Access to the OMDb API (get your API key: http://www.omdbapi.com/apikey.aspx)

### Installation

1. Clone the repository:
git clone https://github.com/seb0305/Movie-Project-SQL-HTML-API.git
cd Movie-Project-SQL-HTML-API
2. (Optional) Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
3. Install dependencies:
pip install -r requirements.txt
4. Add your OMDb API key in `storage/omdb_api.py` by replacing:
API_KEY = "YOUR_API_KEY" # Replace with your real key here

## Usage

Run the main program:
python movies.py

You will be presented with a menu to interact with your movie database. Options include adding movies, listing them, deleting, updating, generating a website, and more.

### Generating the Website
- A website can be generated reflecting your stored movies using the HTML template and CSS in the `_static` directory.
- The generated file is `index.html` in the root project directory.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.