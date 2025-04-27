# bluesky-scrape

Scraping posts from BlueSky from public API (https://bsky.social/xrpc/app.bsky.feed.searchPosts) with authentification

## Requeriments:
* Python3
* Python modules: json, requests (use `pip install`)

## How to use:

* It retrieves posts using a keyword with the label `key`, as well as your BlueSky identifier and password. Optionally, you can also specify the starting date of the post (`since`), the final date (`until`), the language of the post (`lang`), and the maximum number of posts (`max`), where possible values of max >= 1 and <= 100. Examples of use:

```python bluesky-scraper.py key="trump" user="yourname.bsky.social" password="your_password"```

```python bluesky-scraper.py key="trump" user="yourname.bsky.social" password="your_password" since="2024-11-01" until="2024-11-12" lang="en" max=50```

## Output

Two output files are given: a json file with all the information provided by the API, and a txt file with just the text of each post.
