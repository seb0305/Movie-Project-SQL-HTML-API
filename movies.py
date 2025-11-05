import os
import statistics
import random
from fuzzywuzzy import process
from movie_storage import omdb_api, movie_storage_sql as moviestorage
from user import user_management

DATA_PATH = os.path.join("data", "movies.db")
TEMPLATE_PATH = os.path.join("_static", "index_template.html")
STYLE_PATH = os.path.join("_static", "style.css")
OUTPUT_PATH = "index.html"
APP_TITLE = "My Movie App"

active_user_id = None
active_username = None

def prompt_non_empty(prompt):
    """Prompt the user for input until a non-empty string is entered.

    Args:
        prompt (str): Message to display.

    Returns:
        str: A non-empty user input string.
    """
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("\033[31mInput cannot be empty.\033[0m")


def prompt_float(prompt, low=None, high=None):
    """Prompt the user for a float within optional bounds.

    Args:
        prompt (str): Message to display.
        low (float, optional): Minimum acceptable value.
        high (float, optional): Maximum acceptable value.

    Returns:
        float: The validated float input.
    """
    while True:
        try:
            val = float(input(prompt))
            if (low is not None and val < low) or (high is not None and val > high):
                print("\033[31mOut of allowed range.\033[0m")
                continue
            return val
        except ValueError:
            print("\033[31mPlease enter a number.\033[0m")


def prompt_int(prompt, low=None, high=None):
    """Prompt the user for an integer within optional bounds.

    Args:
        prompt (str): Message to display.
        low (int, optional): Minimum acceptable value.
        high (int, optional): Maximum acceptable value.

    Returns:
        int: The validated integer input.
    """
    while True:
        try:
            val = int(input(prompt))
            if (low is not None and val < low) or (high is not None and val > high):
                print("\033[31mOut of allowed range.\033[0m")
                continue
            return val
        except ValueError:
            print("\033[31mPlease enter an integer.\033[0m")


def print_menu():
    """Print the main menu."""
    print("\033[33mMy Movies Database\033[0m")
    print("\033[33mMenu\033[0m")
    print(" 0. Exit")
    print(" 1. List movies")
    print(" 2. Add movie")
    print(" 3. Delete movie")
    print(" 4. Update movie")
    print(" 5. Stats")
    print(" 6. Random movie")
    print(" 7. Search movie")
    print(" 8. Movies sorted by rating")
    print(" 9. Generate website")
    print("10. Switch User")


def list_movies(user_id):
    """List movies for active user."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster_url FROM movies WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3]} for row in movies}



def add_movie():
    """Add movie for active user using OMDb API with fallback."""
    movie_to_add = prompt_non_empty("\033[33mAdd which movie? \033[0m")
    movies = moviestorage.list_movies(active_user_id)
    if movie_to_add in movies:
        print("Movie exists already. Use the --Update Movie-- option.")
        return
    try:
        data = omdb_api.fetch_movie_data(title=movie_to_add)
        if data:
            title = data.get("Title")
            year = int(data.get("Year", "0").split("–")[0])
            rating_str = data.get("imdbRating", "0.0")
            rating = float(rating_str) if rating_str != "N/A" else 0.0
            poster_url = data.get("Poster")
            moviestorage.add_movie(title, year, rating, poster_url)
            print(f"Added '{title}' (Year: {year}, Rating: {rating}), poster URL saved.")
            return
        print("Movie not found in OMDb or API issue. Add manually.")
    except (ValueError, ConnectionError) as e:
        print(f"Error fetching from OMDb: {e}")
        print("Add movie manually.")
    rating = prompt_float("\033[33mRate 1-10 \033[0m", 1.0, 10.0)
    year = prompt_int("\033[33mYear \033[0m", 1888, 2100)
    moviestorage.add_movie(active_user_id, movie_to_add, year, rating)


def delete_movie():
    """Delete movie for active user."""
    movie_to_delete = prompt_non_empty("\033[33mDelete which movie? \033[0m")
    movies = moviestorage.list_movies()
    if movie_to_delete in movies:
        moviestorage.delete_movie(active_user_id, movie_to_delete)
    else:
        print("\033[31mError: Movie not found.\033[0m")


def update_movie():
    """Update movie rating for active user."""
    movie_to_update = prompt_non_empty("\033[33mUpdate rating of which movie? \033[0m")
    movies = moviestorage.list_movies(active_user_id)
    if movie_to_update in movies:
        rating = prompt_float("\033[33mNew rating 1-10 \033[0m", 1.0, 10.0)
        moviestorage.update_movie(active_user_id, movie_to_update, rating)
    else:
        print("\033[31mError: Movie not found.\033[0m")


def stats():
    """Show statistics for active user's movies."""
    movies = moviestorage.list_movies(active_user_id)
    if not movies:
        print("No movies available to compute statistics.")
        return
    ratings = [info['rating'] for info in movies.values()]
    avg = statistics.mean(ratings)
    median = statistics.median(ratings)
    max_rating = max(ratings)
    min_rating = min(ratings)
    best_movies = [movie for movie, info in movies.items() if info['rating'] == max_rating]
    worst_movies = [movie for movie, info in movies.items() if info['rating'] == min_rating]
    print(f"Average rating: {avg:.2f}")
    print(f"Median rating: {median:.2f}")
    print("Best movies:")
    for movie in best_movies:
        print(f"{movie} (Rating: {max_rating})")
    print("Worst movies:")
    for movie in worst_movies:
        print(f"{movie} (Rating: {min_rating})")


def random_movie():
    """Select and display a random movie.

    Chooses a movie from storage and prints its details.
    Handles the case of an empty database.
    """
    movies = moviestorage.list_movies()
    if not movies:
        print("No movies available.")
        return
    pick_title = random.choice(list(movies.keys()))
    info = movies[pick_title]
    print(f"Random movie {pick_title} with rating {info['rating']} and year {info['year']}")


def search_movie():
    """Search movies by partial or fuzzy matching.

    Prompts user for part of the movie name.
    Prints direct matches or fuzzy suggestions with similarity scores.
    """
    movies = moviestorage.list_movies()
    search_part = prompt_non_empty("\033[33mEnter part of movie name \033[0m").lower()
    found = False
    for movie in movies:
        if search_part in movie.lower():
            info = movies[movie]
            print(f"{movie} with rating {info['rating']} and year {info['year']}")
            found = True
    if not found:
        matches = process.extract(search_part, movies.keys(), limit=5)
        close_matches = [match for match in matches if match[1] > 70]
        if close_matches:
            print("\033[31mThe movie does not exist. Did you mean:\033[0m")
            for match in close_matches:
                print(match[0])
        else:
            print("\033[31mNo movies found matching search.\033[0m")


def sort_movies_by_rating():
    """Display movies sorted by rating in descending order.

    Retrieves all movies and prints them sorted from highest to lowest rating.
    """
    movies = moviestorage.list_movies()
    sorted_by_value_desc = dict(sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=True))
    print(f"{len(sorted_by_value_desc)} movies in total")
    for title, info in sorted_by_value_desc.items():
        print(f"{title} Rating {info['rating']} Year {info['year']}")


def generate_website():
    """Generate website for active user's movies."""
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template_html = f.read()

    movies = moviestorage.list_movies(active_user_id)
    grid_items = []
    for movie, data in movies.items():
        poster = data.get('poster_url') or ""
        year = data.get('year') or ""
        grid_items.append(f'''
        <li>
            <div class="movie">
                <img class="movie-poster" src="{poster}">
                <div class="movie-title">{movie}</div>
                <div class="movie-year">{year}</div>
            </div>
        </li>
        ''')

    full_grid_html = '<ol class="movie-grid">\n' + "\n".join(grid_items) + '\n</ol>'
    rendered_content = template_html.replace("__TEMPLATE_TITLE__", f"{active_username}'s Movie Collection")
    rendered_content = rendered_content.replace("__TEMPLATE_MOVIE_GRID__", full_grid_html)

    # Wrap in full HTML structure to keep the template unchanged
    final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    f'<title>{active_username} Movies</title>
    <link rel="stylesheet" href="{STYLE_PATH}">
</head>
<body>
    {rendered_content}
</body>
</html>
"""
    with open(f"{active_username}.html", "w", encoding="utf-8") as out_f:
        out_f.write(final_html)

    print(f"Website {active_username}.html generated successfully.")


def switch_user():
    """Switch active user."""
    global active_user_id, active_username
    active_user_id, active_username = user_management.select_user()


def main():
    """Main loop to select commands."""
    global active_user_id, active_username
    active_user_id, active_username = user_management.select_user()

    dispatch = {
        '1': list_movies,
        '2': add_movie,
        '3': delete_movie,
        '4': update_movie,
        '5': stats,
        '6': random_movie,
        '7': search_movie,
        '8': sort_movies_by_rating,
        '9': generate_website,
        '10': switch_user
    }

    while True:
        print_menu()
        choice = input("\033[33mEnter choice 0-12 \033[0m").strip()
        if choice == '0':
            print("Bye!")
            break
        func = dispatch.get(choice)
        if func:
            func()
        else:
            print("\033[31mInvalid choice.\033[0m")


if __name__ == "__main__":
    main()
