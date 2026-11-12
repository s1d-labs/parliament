"""One answer PDF: save the file and one record."""
import hashlib
import os
import sys
import time

import requests
from scrape_hub_client import HubClient, stop_flag

from common import HEADERS, get

PROJECT = os.environ["SCRAPE_POOL_PROJECT"]
DEADLINE = time.time() + float(os.environ.get("SCRAPE_MAX_HOURS", "1")) * 3600 - 120
stop = stop_flag(install=False)     # set on SIGINT / SIGTERM once main() installs the handlers


def main():
    hub = HubClient(PROJECT, job_index=int(os.environ.get("SCRAPE_JOB_INDEX", 0)), total_jobs=int(os.environ.get("SCRAPE_TOTAL_JOBS", 1)))
    stop_flag()
    s = requests.Session()
    s.headers.update(HEADERS)
    while time.time() < DEADLINE and not stop.is_set():
        if hub.settings.get("paused"):
            time.sleep(30)
            continue
        items = hub.claim(1, steal=True, retry_failed=True)
        if not items:
            break
        it = items[0]
        p = it["payload"]
        r = get(hub, s, p["url"])
        if r is None or not r.content.startswith(b"%PDF"):
            hub.complete([it["key"]], "failed", error="no PDF")
            continue
        path = f"ls{p['ls']}/s{p['session']}/{it['key']}.pdf"
        hub.upload_many([(path, r.content, "application/pdf")])
        hub.record(it["key"], {"question": p["question"], "url": p["url"], "file": path, "bytes": len(r.content), "sha256": hashlib.sha256(r.content).hexdigest()})
        hub.complete([it["key"]], "done", fetched=1)
        time.sleep(max(.5, hub.settings.get("delay_ms", 0) / 1000))
    hub.close("finished" if not stop.is_set() else "failed", "" if not stop.is_set() else "stopped by signal")


if __name__ == "__main__":
    sys.exit(main())
