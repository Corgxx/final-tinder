import streamlit as st
import html
from app.ui_components import inject_custom_css

def render_activity_details(activity):
    """
    Affiche une vue détaillée d'une activité matchée, avec toutes les infos utiles.
    """
    inject_custom_css()
    name = html.escape(activity.get("name", "Unknown"))
    category = html.escape(activity.get("category", "Activity"))
    rating = activity.get("rating", "N/A")
    price = activity.get("price", "")
    address = html.escape(activity.get("address", "No address available"))
    image_url = activity.get("image_url") or (activity.get("photos")[0] if activity.get("photos") else "https://source.unsplash.com/600x400/?activity")
    event_url = activity.get("url", "")
    date = activity.get("date", "")
    # Affichage enrichi
    info_parts = [f"<strong>{category}</strong>"]
    if rating and rating != "N/A":
        info_parts.append(f"⭐ {rating}")
    if price:
        info_parts.append(html.escape(price))
    info_line = " • ".join(info_parts)
    detail_html = f'<div class="card">'
    detail_html += f'<img src="{image_url}" alt="activity image">'
    detail_html += f'<h2>{name}</h2>'
    detail_html += f'<p>{info_line}</p>'
    detail_html += f'<p>{address}</p>'
    if date:
        detail_html += f'<p><strong>Date:</strong> {html.escape(date)}</p>'
    detail_html += '</div>'
    st.markdown(detail_html, unsafe_allow_html=True)
    # Lien externe
    if event_url:
        link_text = "View more details"
        if "yelp.com" in event_url:
            link_text = "View on Yelp"
        elif "eventfrog" in event_url:
            link_text = "View on Eventfrog"
        st.markdown(f"🔗 [{link_text}]({event_url})", unsafe_allow_html=True)
    # Lien Google Maps
    lat = activity.get("lat")
    lon = activity.get("lon")
    if lat and lon:
        maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        st.markdown(f"🗺️ [Open in Google Maps]({maps_url})", unsafe_allow_html=True)
    # Plus d'infos (ex: description, horaires, etc.)
    if "description" in activity:
        st.markdown(f"<p><strong>Description:</strong> {html.escape(activity['description'])}</p>", unsafe_allow_html=True)
    if "hours" in activity:
        st.markdown(f"<p><strong>Hours:</strong> {html.escape(str(activity['hours']))}</p>", unsafe_allow_html=True)
