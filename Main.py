import json
from Anime_Fetcher import fetch_anime_episodes_jikan
from ToDo_Manager import add_episodes_to_task_list

# Load the access token from the config.json
with open("D:\Self_Projects\To Do List Automator\config.json", "r") as file:
    config = json.load(file)

access_token = config["access_token"]

def main():
    anime_name = input("Enter the name of the anime: ")
    anime_title, episodes = fetch_anime_episodes_jikan(anime_name)

    if not episodes:
        print("No episodes found. Exiting.")
        return

    add_episodes_to_task_list(access_token, anime_title, episodes)

if __name__ == "__main__":
    main()