import requests

# Your keys
YELP_API_KEY = "3CDquv2YIfVJBzNuoyau9lsDbqv21Zohj2ewjXvFlJDovEAGaiJWihHDxImRJatHXFA--wY1vVGuvLUX2bMyS-ipwsXjyDII3afybeUrgoisA1GbR8o0oOSB5bIYaHYx"
ORS_API_KEY = "3CDquv2YIfVJBzNuoyau9lsDbqv21Zohj2ewjXvFlJDovEAGaiJWihHDxImRJatHXFA--wY1vVGuvLUX2bMyS-ipwsXjyDII3afybeUrgoisA1GbR8o0oOSB5bIYaHYx"

YELP_API_URL = "https://api.yelp.com/v3/businesses/search"
GEOCODE_API_URL = "https://api.openrouteservice.org/geocode/search"

HEADERS = {
    "Authorization": f"Bearer {"3CDquv2YIfVJBzNuoyau9lsDbqv21Zohj2ewjXvFlJDovEAGaiJWihHDxImRJatHXFA--wY1vVGuvLUX2bMyS-ipwsXjyDII3afybeUrgoisA1GbR8o0oOSB5bIYaHYx"}"
}


def geocode_location(location_name):
    """
    Converts a location name into latitude/longitude using ORS.
    """
    params = {
        "api_key": ORS_API_KEY,
        "text": location_name,
        "size": 1
    }
    response = requests.get(GEOCODE_API_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Geocoding error: {response.status_code} - {response.text}")

    features = response.json().get("features")
    if not features:
        raise Exception("No geocoding results found.")

    coords = features[0]["geometry"]["coordinates"]  # [lon, lat]
    return coords[1], coords[0]  # return (lat, lon)


def fetch_yelp_data(term, location, radius=3000, limit=20, categories=None):
    """
    Raw Yelp data fetcher by city name.
    """
    params = {
        "term": term,
        "location": location,
        "radius": radius,
        "limit": limit
    }

    if categories:
        params["categories"] = categories

    response = requests.get(YELP_API_URL, headers=HEADERS, params=params)

    if response.status_code != 200:
        raise Exception(f"Yelp API error: {response.status_code} - {response.text}")

    businesses = response.json().get("businesses", [])

    results = []
    for biz in businesses:
        result = {
            "name": biz.get("name"),
            "id": biz.get("id"),
            "rating": biz.get("rating"),
            "price": biz.get("price", "N/A"),
            "distance_km": round(biz.get("distance", 0) / 1000, 2),
            "address": ", ".join(biz["location"].get("display_address", [])),
            "image": biz.get("image_url"),
            "categories": [cat["title"] for cat in biz.get("categories", [])],
            "latitude": biz["coordinates"]["latitude"],
            "longitude": biz["coordinates"]["longitude"],
            "phone": biz.get("phone", "N/A"),
            "url": biz.get("url")
        }
        results.append(result)

    return results


def fetch_yelp_activities(activity_type, location_name, radius=3000, limit=20):
    """
    Combines geocoding and Yelp fetch. Used in app.py to simplify logic.
    """
    return fetch_yelp_data(
        term=activity_type,
        location=location_name,
        radius=radius,
        limit=limit,
        categories=activity_type  # can be customized more precisely
    )
