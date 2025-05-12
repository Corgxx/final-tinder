import requests
from datetime import datetime, timedelta

# You will insert your Eventbrite token here
token = "EB-YourTokenHere"  # Replace with your real token

def get_events(city="Zurich", radius_km=30, days_ahead=14, max_results=10):
    base_url = "https://www.eventbriteapi.com/v3/events/search/"

    # Date range: now to now + X days
    now = datetime.utcnow()
    future = now + timedelta(days=days_ahead)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "location.address": city,
        "location.within": f"{radius_km}km",
        "start_date.range_start": now.isoformat("T") + "Z",
        "start_date.range_end": future.isoformat("T") + "Z",
        "categories": "103",  # Music category
        "expand": "venue,logo",
        "sort_by": "date",
        "page": 1,
        "page_size": max_results
    }

    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code != 200:
        print("Error fetching data:", response.text)
        return []

    events = []
    for event in response.json().get("events", []):
        events.append({
            "name": event.get("name", {}).get("text"),
            "url": event.get("url"),
            "image": event.get("logo", {}).get("url"),  # Photo for profile card
            "start_time": event.get("start", {}).get("local"),
            "venue": event.get("venue", {}).get("name"),
        })
    return events
