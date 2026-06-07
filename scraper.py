import json
from pathlib import Path
from datetime import datetime, timezone

import requests

API_URL = "https://shopping-api.paylogic.com/resale/78c8dcf48ab34755b3c50590227174f4"
TARGET_UID = "f0ca64f50a3046b495cb993e06617826"

DATA_FILE = Path("docs/history.json")


def find_category(node):
    if isinstance(node, dict):

        if node.get("uid") == TARGET_UID:
            return node

        for value in node.values():
            result = find_category(value)

            if result:
                return result

    elif isinstance(node, list):

        for item in node:
            result = find_category(item)

            if result:
                return result

    return None


response = requests.get(API_URL, timeout=30)
response.raise_for_status()

data = response.json()

category = find_category(data)

if not category:
    raise Exception("Category not found")

stats = category["statistics"]

record = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "sold": stats["sold"],
    "available": stats["available"],
    "requested": stats["requested"]
}

if DATA_FILE.exists():
    history = json.loads(DATA_FILE.read_text())
else:
    history = []

# Avoid duplicates if action runs twice within same hour
if history:
    latest = history[-1]

    if (
        latest["sold"] == record["sold"]
        and latest["available"] == record["available"]
        and latest["requested"] == record["requested"]
    ):
        print("No changes detected")

history.append(record)

DATA_FILE.write_text(json.dumps(history, indent=2))

print(record)
