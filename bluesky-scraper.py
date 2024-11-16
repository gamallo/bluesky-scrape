import requests
import json
import sys
from datetime import datetime

# Default values
DEFAULT_SINCE = (datetime.now().strftime("%Y-%m-%d") + "T00:00:00Z")
DEFAULT_UNTIL = (datetime.now().strftime("%Y-%m-%d") + "T23:59:59Z")
DEFAULT_LANG = None  # No language filter
DEFAULT_MAX = 25     # API default limit

def parse_arguments():
    """
    Parse command-line arguments for the script.
    """
    arguments = {}
    for arg in sys.argv[1:]:
        key, value = arg.split("=")
        arguments[key] = value
    return arguments

def format_date(date, end_of_day=False):
    """
    Format the date to include the correct time suffix for the API.
    """
    if "T" not in date:  # Only add the suffix if it's missing
        return date + ("T23:59:59Z" if end_of_day else "T00:00:00Z")
    return date

def search_posts(query, since, until, sort='latest', limit=25, lang=None):
    """
    Perform a search query on BlueSky's public API.
    """
    url = 'https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts'
    params = {
        'q': query,
        'since': since,
        'until': until,
        'sort': sort,
        'limit': limit
    }
    if lang:
        params['lang'] = lang

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def write_to_json(result, output_file):
    """
    Save the API response to a JSON file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

def write_text_to_file(posts, output_file):
    """
    Write posts to a text file in TSV format.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for post in posts:
            date = post['record']['createdAt']
            text = remove_newlines(post['record']['text'])
            f.write(f"{date}\t{text}\n")

def remove_newlines(text):
    """
    Remove newline characters from the text.
    """
    return text.replace("\n", " ")

def main():
    # Parse command-line arguments
    args = parse_arguments()
    
    # Mandatory parameter
    query = args.get("key")
    if not query:
        print("Error: The 'key' parameter is required.")
        sys.exit(1)

    # Optional parameters with defaults
   # since = args.get("since", DEFAULT_SINCE)
   # until = args.get("until", DEFAULT_UNTIL)
    since = format_date(args.get("since", DEFAULT_SINCE))
    until = format_date(args.get("until", DEFAULT_UNTIL), end_of_day=True)
    lang = args.get("lang", DEFAULT_LANG)
    max_limit = int(args.get("max", DEFAULT_MAX))

    # Fetch posts
    try:
        result = search_posts(query, since, until, sort='latest', limit=max_limit, lang=lang)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Write results to files
    posts = result.get('posts', [])
    json_output_file = f"{query.replace(' ', '_')}_output.json"
    tsv_output_file = f"{query.replace(' ', '_')}_output.tsv"
    
    write_to_json(result, json_output_file)
    write_text_to_file(posts, tsv_output_file)

    print(f"Results written to:\n- JSON: {json_output_file}\n- TSV: {tsv_output_file}")

if __name__ == "__main__":
    main()
