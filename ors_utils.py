import requests
import os

ORS_API_KEY = "5b3ce3597851110001cf6248ee3c2977b26a41be8e066e26be3f95bf"


def get_route_ors(start_lat, start_lon, end_lat, end_lon, profile="foot-hiking"):
    """
    Appelle OpenRouteService pour obtenir un itinéraire réel entre deux points.
    profile: 'foot-hiking' ou 'cycling-regular'
    Retourne une liste de [lat, lon] pour le tracé, la distance (m), la durée (s), l'ascension et la descente.
    """
    url = f"https://api.openrouteservice.org/v2/directions/{profile}"
    headers = {"Authorization": ORS_API_KEY, "Content-Type": "application/json"}
    body = {
        "coordinates": [[start_lon, start_lat], [end_lon, end_lat]],
        "elevation": True
    }
    try:
        resp = requests.post(url, json=body, headers=headers, timeout=15)
        data = resp.json()
        if "features" in data:
            feat = data["features"][0]
            coords = feat["geometry"]["coordinates"]
            # ORS: [lon, lat, elev] ou [lon, lat]
            path = [[lat, lon] for lon, lat, *_ in coords]
            props = feat["properties"]["summary"]
            distance = props["distance"]
            duration = props["duration"]
            ascent = feat["properties"].get("ascent", 0)
            descent = feat["properties"].get("descent", 0)
            return {
                "path": path,
                "distance": distance,
                "duration": duration,
                "ascent": ascent,
                "descent": descent
            }
    except Exception as e:
        print("ORS error:", e)
    return None
