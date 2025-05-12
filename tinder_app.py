import streamlit as st
from math import radians, sin, cos, sqrt, atan2
import pydeck as pdk

from defi.yelp_fetcher import geocode_location, fetch_yelp_activities
from defi.ui_components import inject_custom_css
from defi.layout_details import render_activity_details
from defi.carousel_card import render_carousel_card
from defi.match import render_match_screen
# --- Inject global styles ---
inject_custom_css()

# --- App Title and Instructions ---
st.title("Tinder for Activities 💖")
st.write("Find cool places around you and swipe through to find your favorites!")

# --- Sidebar: Location, Category, and Filters ---
st.sidebar.header("Search Filters")
city = st.sidebar.text_input("Enter a city or town in Switzerland:", "Zürich")
category = st.sidebar.selectbox("What are you looking for?", [
    "restaurants", "bars", "coffee", "hotels"
])
radius_km = st.sidebar.slider("Search radius (km):", 1, 20, 5)

# --- Trigger Search ---
if st.sidebar.button("Find Activities"):
    latlon = geocode_location(city)
    if not latlon:
        st.error("Location not found. Please enter a valid city or town.")
    else:
        lat, lon = latlon
        st.session_state.user_location = (lat, lon)
        st.session_state.query_category = category

        activities = fetch_yelp_activities(lat, lon, category, radius_m=radius_km * 1000)

        if not activities:
            st.error("No results found nearby. Try a different category or location.")
        else:
            def haversine(coord1, coord2):
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
            st.session_state.carousel_index = 0

        def on_match():
            st.session_state.match = activity
            st.session_state.current += 1
            st.session_state.carousel_index = 0

        render_carousel_card(activity, activity.get("distance", 0.0), on_skip=on_skip, on_match=on_match)

    else:
        st.success("You've reached the end of the list! 🎉")
        if "match" in st.session_state:
            render_activity_details(st.session_state.match)
        if st.button("🔄 Restart"):
            for key in ["activities", "current", "match", "carousel_index"]:
                st.session_state.pop(key, None)
