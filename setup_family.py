"""Put this family's projects in the pool and register its health checks. Run by the Setup workflow. Safe to run again."""
from scrape_hub_client import register_project, seed_queue, set_pool, set_probes

from family import FAMILY, HOST, PROBES, PROJECTS

print("health checks:", set_probes(FAMILY, PROBES))
for p in PROJECTS:
    register_project(p["name"], title=p["title"], unit_label=p["unit_label"], record_label=p["record_label"])
    host = p.get("host", HOST)
    set_pool(p["name"], FAMILY, p["task"], target=host, probe=f"{FAMILY}:{host}", geo="" if p["task"] == "questions" else "IN", max_workers=2 if "host" in p else 4, threads=1, delay_ms=1500 if "host" in p else 1000, pool=not p.get("hold"), proxy="IN" if p["task"] == "questions" else None)
    if p["items"]:
        print(p["name"], "queue:", seed_queue(p["name"], p["items"]))
