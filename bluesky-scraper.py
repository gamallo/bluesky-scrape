import requests
import json
import sys
from datetime import datetime, timedelta

BASE_URL = "https://bsky.social/xrpc/app.bsky.feed.searchPosts"

def parse_arguments():
    """
    Parse command-line arguments into a dictionary.
    """
    arguments = {}
    for arg in sys.argv[1:]:
        key, value = arg.split("=")
        arguments[key] = value
    return arguments

def authenticate(username, password):
    """
    Authenticate to Bluesky and get an access token.
    """
    auth_url = "https://bsky.social/xrpc/com.atproto.server.createSession"
    data = {
        "identifier": username,
        "password": password
    }
    response = requests.post(auth_url, json=data)
    response.raise_for_status()
    return response.json().get("accessJwt")

def search_posts(keyword, access_token, start_date=None, end_date=None, limit=100, lang=None):
    """
    Search for posts containing the specified keyword.
    """
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "q": keyword,
        "limit": limit
    }
    if start_date:
        params["since"] = f"{start_date}T00:00:00Z"
    if end_date:
        params["until"] = f"{end_date}T23:59:59Z"
    if lang:
        params["lang"] = lang

    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("posts", [])

def save_to_file(keyword, posts):
    """
    Save posts to a JSON file.
    """
    filename = f"{keyword.replace(' ', '_')}_results.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)
    print(f"Saved results for '{keyword}' to {filename}")

def save_text_only(keyword, posts):
    """
    Save only the text of posts to a plain .txt file.
    """
    filename = f"{keyword.replace(' ', '_')}_results.txt"
    with open(filename, "w", encoding="utf-8") as file:
        for post in posts:
            text = post.get("record", {}).get("text", "")
            if text:
                file.write(text.replace("\n", " ").strip() + "\n")
    print(f"Saved text-only results for '{keyword}' to {filename}")


def main():
    args = parse_arguments()

    # Mandatory arguments
    keyword = args.get("keyword")
    username = args.get("user")
    password = args.get("password")

    if not all([keyword, username, password]):
        print("Error: 'keyword', 'user', and 'password' are required parameters.")
        sys.exit(1)

    # Optional arguments
    limit = int(args.get("limit", 100))
    lang = args.get("lang")

    # Dates
    since = args.get("since")
    until = args.get("until")
    if not since:
        since = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    if not until:
        until = datetime.now().strftime("%Y-%m-%d")

    # Authenticate
    try:
        access_token = authenticate(username, password)
    except requests.exceptions.RequestException as e:
        print(f"Authentication error: {e}")
        sys.exit(1)

    # Search posts
    try:
        posts = search_posts(keyword, access_token, start_date=since, end_date=until, limit=limit, lang=lang)
    except requests.exceptions.RequestException as e:
        print(f"Search error: {e}")
        sys.exit(1)

    for post in posts:
        text = post.get("record", {}).get("text", "No content")
        author = post.get("author", {}).get("displayName", "Unknown Author")
        created_at = post.get("record", {}).get("createdAt", "Unknown Date")
        print(f"Author: {author}\nCreated At: {created_at}\nContent: {text}\n{'-' * 40}")

    # Save posts
    save_to_file(keyword, posts)
    save_text_only(keyword, posts)

if __name__ == "__main__":
    main()
