import streamlit as st
import folium
from streamlit_folium import st_folium

def show_event_card(event):
    st.markdown("### 🎵 " + event["name"])
    
    if event["image"]:
        st.image(event["image"], use_column_width=True)

    st.markdown(f"📍 **Lieu :** {event['venue']}")
    st.markdown(f"🕒 **Quand :** {event['start_time']}")
    st.markdown(f"[🔗 Voir l'événement]({event['url']})")

    if event.get("latitude") and event.get("longitude"):
        m = folium.Map(location=[float(event["latitude"]), float(event["longitude"])], zoom_start=13)
        folium.Marker([float(event["latitude"]), float(event["longitude"])], tooltip=event["venue"]).add_to(m)
        st_folium(m, width=700, height=400)
    else:
        st.info("📍 Localisation non disponible pour cet événement.")