import os
from sqlalchemy import create_engine, text

DB_PATH = os.path.join("data", "movies.db")
DB_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DB_URL, echo=False)

with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    """))
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT,
            UNIQUE(user_id, title),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """))
    connection.commit()

def list_movies():
    """Retrieve all movies from the database.

    Returns:
        dict: Mapping of movie titles to details (year, rating, poster_url).
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_url FROM movies"))
        movies = result.fetchall()
    return {
        row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3]}
        for row in movies
    }

def add_movie(title, year, rating, poster_url=None):
    """Add a new movie to the database.

    Args:
        title (str): Movie title.
        year (int): Release year.
        rating (float): Movie rating.
        poster_url (str, optional): URL to the movie poster.
    """
    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO movies (title, year, rating, poster_url) VALUES (:title, :year, :rating, :poster_url)"),
                {"title": title, "year": year, "rating": rating, "poster_url": poster_url}
            )
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

def delete_movie(title):
    """Delete a movie from the database by title.

    Args:
        title (str): Title of the movie to delete.
    """
    with engine.connect() as connection:
        result = connection.execute(text("DELETE FROM movies WHERE title = :title"), {"title": title})
        connection.commit()
        if result.rowcount > 0:
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")

def update_movie(title, rating):
    """Update the rating of a movie.

    Args:
        title (str): Title of the movie to update.
        rating (float): New rating value.
    """
    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating = :rating WHERE title = :title"),
            {"rating": rating, "title": title}
        )
        connection.commit()
        if result.rowcount > 0:
            print(f"Movie '{title}' updated successfully.")
        else:
            print(f"Movie '{title}' not found.")