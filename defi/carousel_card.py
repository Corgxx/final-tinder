import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

def render_carousel_card(activity, distance_km=0.0, on_skip=None, on_match=None):
    if "carousel_index" not in st.session_state:
        st.session_state.carousel_index = 0

    index = st.session_state.carousel_index

    # DEBUG: afficher les images si elles sont présentes ou non
    st.write("IMAGE 1:", activity.get("image"))
    carousel_items = []
    if activity.get("image"):
        carousel_items.append({"type": "image", "content": activity["image"]})
    if activity.get("latitude") and activity.get("longitude"):
        carousel_items.append({"type": "map", "lat": activity["latitude"], "lon": activity["longitude"]})

    if not carousel_items:
        st.error("Aucun contenu à afficher pour cette activité.")
        return

    index = min(index, len(carousel_items) - 1)
    item = carousel_items[index]

    st.markdown("""
        <div style='background-color:white; padding: 1rem; border-radius: 1rem; box-shadow: 0 0 10px rgba(0,0,0,0.1);'>
    """, unsafe_allow_html=True)

    if item["type"] == "image":
        st.markdown(f"""
            <div style='text-align:center;'>
                <img src="{item['content']}" style="max-width:100%; height:auto; border-radius:10px; object-fit:cover;"/>
            </div>
        """, unsafe_allow_html=True)
    elif item["type"] == "map":
        df = pd.DataFrame([{"lat": item["lat"], "lon": item["lon"]}])
        st.map(df)

    st.markdown(f"<h4 style='margin-top:1rem;'>🏷️ {activity.get('name', 'No name')}</h4>", unsafe_allow_html=True)
    st.markdown(f"📍 {activity.get('address', 'Unknown location')}")
    if distance_km:
        st.markdown(f"📏 {distance_km:.1f} km")
    if activity.get("price"):
        st.markdown(f"💰 {activity['price']}")
    if activity.get("rating"):
        st.markdown(f"⭐ {activity['rating']} stars")

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️", key="prev") and index > 0:
            st.session_state.carousel_index = index - 1
            st.rerun()
    with col2:
        if st.button("❌ Pass", key="pass") and on_skip:
            st.session_state.carousel_index = 0
            on_skip()
            st.rerun()
        if st.button("❤️ Like", key="like") and on_match:
            st.session_state.carousel_index = 0
            on_match()
            st.stop()  # Stop app after showing match screen
    with col3:
        if st.button("➡️", key="next") and index < len(carousel_items) - 1:
            st.session_state.carousel_index = index + 1
            st.rerun()
