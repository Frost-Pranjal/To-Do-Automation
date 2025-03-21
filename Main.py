import json
from Series_Fetcher import fetch_series_episodes  # Updated module name
from ToDo_Manager import add_episodes_to_task_list

# Load the access token from the config.json
with open(r"/home/frost/Projects/To-Do-Automation/config.json", "r") as file:
    config = json.load(file)

access_token = config["access_token"]

def main():
    series_name = input("Enter the name of the TV/Web/Anime series: ")
    series_title, episodes = fetch_series_episodes(series_name)  # Updated function

    if not episodes:
        print("No episodes found. Exiting.")
        return

    add_episodes_to_task_list(access_token, series_title, episodes)

if __name__ == "__main__":
    main()
