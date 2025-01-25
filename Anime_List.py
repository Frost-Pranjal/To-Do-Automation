import requests
import csv

def fetch_anime_episodes_jikan(anime_name):
    try:
        # Jikan API search URL for anime
        search_url = f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1"
        search_response = requests.get(search_url)
        search_data = search_response.json()

        # Check if the anime was found
        if not search_data.get("data"):
            print("Anime not found. Please check the name and try again.")
            return None, []

        # Get the first search result
        anime = search_data["data"][0]
        anime_id = anime["mal_id"]
        anime_title = anime["title"]
        print(f"Fetching episodes for: {anime_title}\n")

        # Initialize the episode list and pagination parameters
        episode_list = []
        page = 1
        episode_counter = 1  # Initialize the global episode counter
        while True:
            # Jikan API endpoint to get episodes (with pagination)
            episodes_url = f"https://api.jikan.moe/v4/anime/{anime_id}/episodes?page={page}"
            episodes_response = requests.get(episodes_url)
            episodes_data = episodes_response.json()

            # Check if there are episodes in the current page
            if "data" not in episodes_data or len(episodes_data["data"]) == 0:
                break  # Exit loop if no more episodes

            # Extract episodes from the current page
            episodes = episodes_data["data"]
            for ep in episodes:
                episode_title = ep.get("title", "No Title Available")
                episode_list.append((episode_counter, episode_title))  # Use the global episode counter
                episode_counter += 1  # Increment the counter for the next episode

            # Increment the page number for the next request
            page += 1

        # Return the final list of episodes
        return anime_title, episode_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, []

def save_episodes_to_csv(anime_title, episode_list, filename="episodes.csv"):
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Episode Number", "Episode Title"])  # CSV header
            writer.writerows(episode_list)  # Write the episode data
        print(f"Episodes saved to {filename} successfully.")
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")

if __name__ == "__main__":
    print("Welcome to the Anime Episode Finder using Jikan API!")
    anime_name = input("Enter the name of the anime: ")
    anime_title, episode_list = fetch_anime_episodes_jikan(anime_name)

    if episode_list:
        print("\nEpisodes fetched successfully!")
        filename = f"{anime_title.replace(' ', '_')}.csv"
        save_episodes_to_csv(anime_title, episode_list, filename)
