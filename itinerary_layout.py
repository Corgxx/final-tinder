
import streamlit as st
import pydeck as pdk
from activities.hiking import get_hiking_route
from activities.cycling import get_cycling_route

def render_itinerary_card(activity, category):
    st.markdown("### " + activity.get("name", ""))
    st.image(activity.get("image_url", ""), use_column_width=True)

    coords = activity.get("coordinates", {})
    lat, lon = coords.get("latitude"), coords.get("longitude")

    if not lat or not lon:
        st.error("No coordinates available for this activity.")
        return

    # Get route based on activity type
    if category == "hiking":
        route_coords = get_hiking_route((lat, lon))
    elif category == "cycling":
        route_coords = get_cycling_route((lat, lon))
    else:
        st.warning("Unsupported category.")
        return

    if not route_coords:
        st.error("No route found.")
        return

    # Prepare route layer
    route_layer = pdk.Layer(
        "LineLayer",
        data=[{"path": route_coords}],
        get_path="path",
        get_width=5,
        get_color=[255, 0, 0],
        pickable=False
    )

    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=13,
        pitch=0
    )

    st.pydeck_chart(pdk.Deck(
        layers=[route_layer],
        initial_view_state=view_state
    ))

    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Match"):
            st.success("It's a match!")
    with col2:
        st.button("Pass")
