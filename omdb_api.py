import requests

API_KEY = "865834c6"


def fetch_movie_data(title=None, imdb_id=None):
    """Fetch movie data from OMDb API by title or IMDb ID.

    Args:
        title (str, optional): Movie title.
        imdb_id (str, optional): IMDb ID.

    Returns:
        dict or None: Movie data dictionary if successful, else None.
    """
    base_url = "http://www.omdbapi.com/"
    params = {"apikey": API_KEY}
    if title:
        params["t"] = title
    elif imdb_id:
        params["i"] = imdb_id
    else:
        raise ValueError("Either title or imdb_id must be provided.")

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            return data
        print(f"OMDb API error: {data.get('Error')}")
    except requests.RequestException as e:
        print(f"OMDb API request error: {e}")
    return None
