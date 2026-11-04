"""One page of questions: store them, and on page 1 add the later pages. Each page adds its answer PDFs to parliament-docs."""
import os
import signal
import sys
import time

import requests
from scrape_hub_client import HubClient, seed_queue

from common import HEADERS, get
from parse import doc_item, pages, rows, url

PROJECT = os.environ["SCRAPE_POOL_PROJECT"]
DOCS = "parliament-docs"
DEADLINE = time.time() + float(os.environ.get("SCRAPE_MAX_HOURS", "1")) * 3600 - 120
stop = False


def on_signal(*_):
    global stop
    stop = True


def main():
    hub = HubClient(PROJECT, job_index=int(os.environ.get("SCRAPE_JOB_INDEX", 0)), total_jobs=int(os.environ.get("SCRAPE_TOTAL_JOBS", 1)))
    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGTERM, on_signal)
    s = requests.Session()
    s.headers.update(HEADERS)
    while time.time() < DEADLINE and not stop:
        if hub.settings.get("paused"):
            time.sleep(30)
            continue
        items = hub.claim(1, steal=True, retry_failed=True)
        if not items:
            break
        it = items[0]
        p = it["payload"]
        r = get(hub, s, url(p["ls"], p["session"], p["page"]))
        if r is None:
            hub.complete([it["key"]], "failed", error="no answer")
            continue
        total, found = rows(r.json())
        for rid, rec in found:
            hub.record(rid, rec)
        if p["page"] == 1 and total:
            seed_queue(PROJECT, [{"key": f"ls{p['ls']}-s{p['session']}-p{n}", "payload": {"ls": p["ls"], "session": p["session"], "page": n}} for n in range(2, pages(total) + 1)])
        docs = [doc_item(rid, rec) for rid, rec in found if rec["pdf"]]
        if docs:
            seed_queue(DOCS, docs)
        hub.complete([it["key"]], "done", fetched=len(found))
        time.sleep(max(.5, hub.settings.get("delay_ms", 0) / 1000))
    hub.close("finished" if not stop else "failed", "" if not stop else "stopped by signal")


if __name__ == "__main__":
    sys.exit(main())
