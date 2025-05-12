import streamlit as st
import html
from defi.ui_components import inject_custom_css

def render_activity_details(activity):
    inject_custom_css()

    name = html.escape(activity.get("name", "Unknown"))
    category = html.escape(activity.get("category", "Activity"))
    rating = activity.get("rating", "N/A")
    price = activity.get("price", "")
    address = html.escape(activity.get("address", "No address available"))
    image_url = activity.get("image_url") or (activity.get("photos")[0] if activity.get("photos") else "https://source.unsplash.com/600x400/?activity")
    event_url = activity.get("url", "")
    date = activity.get("date", "")

    info_parts = [f"<strong>{category}</strong>"]
    if rating and rating != "N/A":
        info_parts.append(f"⭐ {rating}")
    if price:
        info_parts.append(html.escape(price))
    info_line = " • ".join(info_parts)

    detail_html = f'''
    <div style="
        background-color: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        max-width: 700px;
        margin: auto;
    ">
        <img src="{image_url}" alt="activity image" style="width:100%; border-radius: 15px; margin-bottom: 1rem;">
        <h2 style="margin-bottom: 0.5rem;">{name}</h2>
        <p style="color: #666;">{info_line}</p>
        <p style="color: #888; font-size: 0.95rem;">{address}</p>
    '''

    if date:
        detail_html += f'<p><strong>Date:</strong> {html.escape(date)}</p>'

    if "description" in activity:
        detail_html += f'<p><strong>Description:</strong> {html.escape(activity["description"])}</p>'

    if "hours" in activity:
        detail_html += f'<p><strong>Hours:</strong> {html.escape(str(activity["hours"]))}</p>'

    detail_html += '</div>'
    st.markdown(detail_html, unsafe_allow_html=True)

    # Liens externes
    if event_url:
        link_text = "View more details"
        if "yelp.com" in event_url:
            link_text = "View on Yelp"
        elif "eventfrog" in event_url:
            link_text = "View on Eventfrog"
        st.markdown(f"🔗 [{link_text}]({event_url})", unsafe_allow_html=True)

    lat = activity.get("lat")
    lon = activity.get("lon")
    if lat and lon:
        maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        st.markdown(f"🗺️ [Open in Google Maps]({maps_url})", unsafe_allow_html=True)
