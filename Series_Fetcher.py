import requests
import json

with open("/home/frost/Projects/To-Do-Automation/config.json", "r") as file:
    config = json.load(file)

API_KEY = config["API_KEY"]

def fetch_series_episodes(series_name):
    try:
        # TMDb API search URL for TV shows (including web series & anime)
        search_url = f"https://api.themoviedb.org/3/search/tv?api_key={API_KEY}&query={series_name}"
        search_response = requests.get(search_url)
        search_data = search_response.json()

        # Check if the series was found
        if not search_data.get("results"):
            print("Series not found. Please check the name and try again.")
            return None, []

        # Get the first search result
        series = search_data["results"][0]
        series_id = series["id"]
        series_title = series["name"]
        print(f"Fetching episodes for: {series_title}\n")

        # Fetch the number of seasons
        details_url = f"https://api.themoviedb.org/3/tv/{series_id}?api_key={API_KEY}"
        details_response = requests.get(details_url)
        details_data = details_response.json()
        total_seasons = details_data.get("number_of_seasons", 1)

        episode_list = []
        for season in range(1, total_seasons + 1):
            season_url = f"https://api.themoviedb.org/3/tv/{series_id}/season/{season}?api_key={API_KEY}"
            season_response = requests.get(season_url)
            season_data = season_response.json()

            if "episodes" in season_data:
                for episode in season_data["episodes"]:
                    episode_number = episode["episode_number"]
                    episode_title = episode.get("name", "No Title Available")
                    episode_list.append(f"Season {season}, Episode {episode_number}: {episode_title}")

        return series_title, episode_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, []

# Example usage
series_name = "Breaking Bad"  # Replace with any TV/Web/Anime series name
title, episodes = fetch_series_episodes(series_name)

if title:
    print(f"\nEpisodes for '{title}':")
    for ep in episodes:
        print(ep)
