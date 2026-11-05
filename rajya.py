"""One Rajya Sabha session: one record per question, with the text, and the raw answer in the bucket. Uses the query that the sansad.in question page sends."""
import gzip
import os
import signal
import sys
import time

import requests
from scrape_hub_client import HubClient

from common import HEADERS, get
from parse import rs_rows, rs_url

PROJECT = os.environ["SCRAPE_POOL_PROJECT"]
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
        n = it["payload"]["session"]
        r = get(hub, s, rs_url(n))
        if r is None:
            hub.complete([it["key"]], "failed", error="no answer")
            continue
        got = rs_rows(r.json())
        for rid, rec in got:
            hub.record(rid, rec)
        if got:
            hub.upload_many([(f"rs/s{n}.json.gz", gzip.compress(r.content), "application/gzip")])
        hub.complete([it["key"]], "done", fetched=len(got))
        time.sleep(max(1, hub.settings.get("delay_ms", 0) / 1000))
    hub.close("finished" if not stop else "failed", "" if not stop else "stopped by signal")


if __name__ == "__main__":
    sys.exit(main())
