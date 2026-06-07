import json
from pathlib import Path
from datetime import datetime, timezone

import requests

RESALE_URL = (
    "https://shopping-api.paylogic.com/resale/"
    "78c8dcf48ab34755b3c50590227174f4"
)

APPROVALS_URL = (
    "https://shopping-api.paylogic.com/ticket-transfer-approvals"
    "?sale=https://shopping-api.paylogic.com/sales/"
    "78c8dcf48ab34755b3c50590227174f4"
    "&product_category=f0ca64f50a3046b495cb993e06617826"
)

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


#
# SALES STATS
#

resale_response = requests.get(
    RESALE_URL,
    timeout=30
)

resale_response.raise_for_status()

resale_data = resale_response.json()

category = find_category(resale_data)

if not category:
    raise Exception("Weekend incl. campsite category not found")

sold = category["statistics"]["sold"]

#
# LIVE LISTINGS
#

approval_response = requests.get(
    APPROVALS_URL,
    timeout=30
)

approval_response.raise_for_status()

approval_data = approval_response.json()

listings = (
    approval_data
    .get("_embedded", {})
    .get("shop:ticket_transfer_approval", [])
)

prices = []
listing_ids = []

for listing in listings:

    try:

        approval_url = (
            listing["_links"]["self"]["href"]
        )

        listing_id = approval_url.split("/")[-1]

        listing_ids.append(listing_id)

        price = float(
            listing["asking_price"]["amount"]
        )

        prices.append(price)

    except Exception:
        continue

record = {
    "timestamp": datetime.now(
        timezone.utc
    ).isoformat(),

    "sold": sold,

    "listing_count": len(prices),

    "listing_ids": listing_ids,

    "prices": prices,

    "lowest_price":
        min(prices) if prices else None,

    "highest_price":
        max(prices) if prices else None,

    "avg_price":
        round(sum(prices) / len(prices), 2)
        if prices else None
}

if DATA_FILE.exists():
    history = json.loads(
        DATA_FILE.read_text()
    )
else:
    history = []

history.append(record)

DATA_FILE.write_text(
    json.dumps(history, indent=2)
)

print(
    json.dumps(record, indent=2)
)
