import json
from datetime import datetime, timezone
from pathlib import Path

import requests

URL = "https://shopping-api.paylogic.com/resale/78c8dcf48ab34755b3c50590227174f4"

TOKEN = "YOUR_BEARER_TOKEN"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
}


def find_statistics(node):
    """
    Recursively find statistics blocks.
    """
    results = []

    if isinstance(node, dict):
        if "statistics" in node:
            results.append(node["statistics"])

        for value in node.values():
            results.extend(find_statistics(value))

    elif isinstance(node, list):
        for item in node:
            results.extend(find_statistics(item))

    return results


response = requests.get(URL, headers=HEADERS, timeout=30)
response.raise_for_status()

data = response.json()

stats = find_statistics(data)

# Weekend incl. campsite
sold = stats[0]["sold"]

record = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "sold": sold,
}

history_file = Path("data/history.json")
history_file.parent.mkdir(exist_ok=True)

history = []

if history_file.exists():
    history = json.loads(history_file.read_text())

history.append(record)

history_file.write_text(json.dumps(history, indent=2))

print(f"Sold: {sold}")
