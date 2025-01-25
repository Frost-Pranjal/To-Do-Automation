import json
import requests

# Load the access token from the config.json
with open("/home/frost/Projects/To Do List Automator/config.json", "r") as file:
    config = json.load(file)

access_token = config["access_token"]

def get_task_lists(access_token):
    url = "https://graph.microsoft.com/v1.0/me/todo/lists"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("value", [])

def add_task(access_token, list_id, task_title):
    url = f"https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {"title": task_title}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def create_task_list(access_token, list_name):
    url = "https://graph.microsoft.com/v1.0/me/todo/lists"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {"displayName": list_name}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

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
                episode_list.append(f"Episode {episode_counter}: {episode_title}")  # Use the global episode counter
                episode_counter += 1  # Increment the counter for the next episode

            # Increment the page number for the next request
            page += 1

        # Return the final list of episodes
        return anime_title, episode_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, []

def main():
    print("Welcome to the Anime Episode Finder and To-Do List Automator!")
    anime_name = input("Enter the name of the anime: ")
    anime_title, episodes = fetch_anime_episodes_jikan(anime_name)

    if not episodes:
        print("No episodes found. Exiting.")
        return

    list_name = anime_title

    try:
        task_lists = get_task_lists(access_token)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching task lists: {e}")
        return

    selected_list = next((l for l in task_lists if l["displayName"] == list_name), None)

    if not selected_list:
        print(f"Task list '{list_name}' not found! Creating it...")
        try:
            selected_list = create_task_list(access_token, list_name)
            print(f"Created new task list: {selected_list['displayName']}")
        except requests.exceptions.RequestException as e:
            print(f"Error creating task list: {e}")
            return

    # Add tasks (episodes) to the task list
    for task in episodes:
        try:
            result = add_task(access_token, selected_list["id"], task)
            print(f"Added task: {result['title']}")
        except requests.exceptions.RequestException as e:
            print(f"Error adding task '{task}': {e}")

if __name__ == "__main__":
    main()