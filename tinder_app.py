import streamlit as st
from yelp_fetcher import geocode_location, fetch_yelp_activities, fetch_eventfrog_events
from app.ui_components import inject_custom_css
from layout.Layout_details import render_activity_details
from layout.layout_card import render_activity_card
from layout.carousel_card import render_carousel_card

# --- Inject global styles ---
inject_custom_css()

# --- App Title and Instructions ---
st.title("Tinder for Activities 💖")
st.write("Find cool places and events around you, and swipe through to find your favorites!")

# --- Sidebar: Location, Category, and Suggestion ---
st.sidebar.header("Search Filters")
city = st.sidebar.text_input("Enter a city or town in Switzerland:", "Zürich")
# Dropdown includes new options 'concerts' and 'parties' for events
category = st.sidebar.selectbox("What are you looking for?", [
    "restaurants", "bars", "coffee", "hiking", "cycling", "swimming", "sightseeing", "concerts", "parties"
])
radius_km = st.sidebar.slider("Search radius (km):", 1, 20, 5)

# Mood-based suggestion input
mood_input = st.sidebar.text_input("Describe your mood or preference:")
if st.sidebar.button("Suggest Category"):
    suggested_cat = None
    text = mood_input.lower()
    # Simple keyword-based NLP for category suggestion:contentReference[oaicite:4]{index=4}
    if "sunny" in text or "outside" in text or "weather" in text:
        # On a sunny day, suggest an outdoor water activity
        suggested_cat = "swimming"
    if "rain" in text or "cold" in text or "inside" in text:
        suggested_cat = "coffee"
    if "music" in text or "concert" in text or "band" in text:
        suggested_cat = "concerts"
    if "party" in text or "club" in text or "dance" in text or "night" in text:
        suggested_cat = "parties"
    if "hungry" in text or "eat" in text or "food" in text:
        suggested_cat = "restaurants"
    if "drink" in text or "beer" in text or "wine" in text:
        suggested_cat = "bars"
    if "coffee" in text or "tea" in text or "relax" in text:
        suggested_cat = "coffee"
    if "adventure" in text or "explore" in text or "trail" in text:
        suggested_cat = "hiking"
    if "bike" in text or "bicycle" in text:
        suggested_cat = "cycling"
    if "museum" in text or "art" in text or "history" in text:
        suggested_cat = "sightseeing"
    if suggested_cat:
        st.sidebar.info(f"Suggested category: **{suggested_cat}**")
    else:
        st.sidebar.info("Could not determine a category – please try different keywords.")

# --- Machine Learning/NLP Suggestion ---
st.sidebar.markdown("---")
st.sidebar.subheader("AI Activity Suggestion 🧠")
user_situation = st.sidebar.text_area("Describe your current situation, mood, or what you want to do:")
if st.sidebar.button("AI Suggest Activity"):
    import random
    # Simple ML/NLP logic (à remplacer par un vrai modèle si besoin)
    text = user_situation.lower()
    if any(word in text for word in ["sunny", "outside", "weather", "lake", "mountain"]):
        ai_suggested = "hiking" if "mountain" in text else "swimming"
    elif any(word in text for word in ["rain", "cold", "inside", "chill", "relax"]):
        ai_suggested = "coffee"
    elif any(word in text for word in ["music", "concert", "band"]):
        ai_suggested = "concerts"
    elif any(word in text for word in ["party", "club", "dance", "night"]):
        ai_suggested = "parties"
    elif any(word in text for word in ["hungry", "eat", "food"]):
        ai_suggested = "restaurants"
    elif any(word in text for word in ["drink", "beer", "wine"]):
        ai_suggested = "bars"
    elif any(word in text for word in ["bike", "bicycle", "cycling"]):
        ai_suggested = "cycling"
    elif any(word in text for word in ["museum", "art", "history"]):
        ai_suggested = "sightseeing"
    else:
        ai_suggested = random.choice(["restaurants", "bars", "coffee", "hiking", "cycling", "swimming", "sightseeing", "concerts", "parties"])
    st.sidebar.info(f"AI suggests: **{ai_suggested}**")

# --- Trigger Search ---
if st.sidebar.button("Find Activities"):
    # Geocode the city name to get latitude and longitude
    latlon = geocode_location(city)
    if not latlon:
        st.error("Location not found. Please enter a valid city or town.")
    else:
        lat, lon = latlon
        st.session_state.user_location = (lat, lon)  # store user location for route calculations

        # Fetch data from Yelp or Eventfrog based on category
        if category in ["concerts", "parties"]:
            # Use Eventfrog API for events (concerts or parties)
            activities = fetch_eventfrog_events(lat, lon, term=category, radius_m=radius_km * 1000)
        else:
            # Use Yelp API for places/activities
            activities = fetch_yelp_activities(lat, lon, category, radius_m=radius_km * 1000)

        if not activities:
            st.error("No results found nearby. Try a different category or location.")
        else:
            # Compute distance for each result and sort by distance
            from math import radians, sin, cos, sqrt, atan2
            def haversine(coord1, coord2):
                # Returns distance in kilometers between two (lat, lon) coordinates
                R = 6371.0
                lat1, lon1 = map(radians, coord1)
                lat2, lon2 = map(radians, coord2)
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                return R * c

            for act in activities:
                if act.get("lat") and act.get("lon"):
                    act["distance"] = haversine((lat, lon), (act["lat"], act["lon"]))
                else:
                    act["distance"] = None

            # Sort by distance (placing items with no distance at the end)
            activities.sort(key=lambda x: x["distance"] if x["distance"] is not None else float('inf'))
            st.session_state.activities = activities
            st.session_state.current = 0

# --- Main Area: Swipeable Cards ---
if "activities" in st.session_state and st.session_state.activities:
    index = st.session_state.get("current", 0)
    activities = st.session_state.activities

    if index < len(activities):
        activity = activities[index]
        def on_skip():
            st.session_state.current += 1
            st.session_state.carousel_index = 0  # reset carousel
        def on_match():
            st.session_state.match = activity
            st.session_state.current += 1
            st.session_state.carousel_index = 0  # reset carousel
        # Render the current activity/event card avec gestion des boutons
        render_carousel_card(activity, activity.get("distance", 0.0), on_skip=on_skip, on_match=on_match)
    else:
        st.success("You've reached the end of the list! 🎉")
        # Show details of the matched activity/event (if any)
        if "match" in st.session_state:
            render_activity_details(st.session_state.match)
        # Option to restart the process
        if st.button("🔄 Restart"):
            for key in ["activities", "current", "match", "carousel_index"]:
                st.session_state.pop(key, None)
