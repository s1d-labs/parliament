"""The fetch step both tasks share."""
from scrape_hub_client import timed_get

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; s1d-labs public records crawl; +https://labs.s1d.me)", "Accept": "application/json, */*"}


def get(hub, s, url):
    r = timed_get(hub, s, url, timeout=(20, 120))      # counts n_http, t_http_s, http_<code>, http_error for the hub
    return r if r is not None and r.status_code == 200 else None
