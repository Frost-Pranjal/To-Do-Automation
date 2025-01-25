import requests

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

def add_episodes_to_task_list(access_token, anime_title, episodes):
    try:
        task_lists = get_task_lists(access_token)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching task lists: {e}")
        return

    selected_list = next((l for l in task_lists if l["displayName"] == anime_title), None)

    if not selected_list:
        print(f"Task list '{anime_title}' not found! Creating it...")
        try:
            selected_list = create_task_list(access_token, anime_title)
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