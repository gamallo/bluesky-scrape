# bluesky-scrape

Scraping posts from BlueSky (public API - https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts) without any authentification


## Requeriments:
* Python3
* Python modules: json, requests (use `pip install`)

## How to use:

* It retrieves posts using a keyword with the label `key`. Optionally, you can also specify the starting date of the post (`since`), the final date (`until`), the language of the post (`lang`), and the maximum number of posts (`max`). Examples of use:

```python bluesky-scraper.py key="trump"```

```python bluesky-scraper.py key="trump" since="2024-11-01" until="2024-11-12" lang="en" max=50```

## Output

Two output files are given: a json file with all the information provided by the API, and a tsv file with just the date and the text of each post.
