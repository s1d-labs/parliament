"""The fetch step both tasks share."""
import time

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; s1d-labs public records crawl; +https://labs.s1d.me)", "Accept": "application/json, */*"}


def get(hub, s, url):
    t = time.time()
    try:
        r = s.get(url, timeout=(20, 120))
    except requests.RequestException:
        hub.metric("http_error")
        hub.error()
        return None
    hub.metric("n_http")
    hub.metric("t_http_s", time.time() - t)
    if r.status_code != 200:
        hub.metric(f"http_{r.status_code}")
        if r.status_code in (403, 429, 503):
            hub.block()
        return None
    return r
