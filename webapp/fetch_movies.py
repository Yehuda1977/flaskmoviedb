import requests     # "Module not found" --> pip install requests

url = "https://api.themoviedb.org/3/search/movie"
token = "9f48abce2dfcb47468c659a152b248a4"

def get_movies(query, page):
    params = {
        "api_key": token,
        "query": query,
        "page": page,
        "include_adult": False
    }

    movies = requests.get(url, params=params)
    print(movies.json())
    return movies.json()