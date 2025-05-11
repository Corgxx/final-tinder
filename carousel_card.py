import streamlit as st
import html
import pydeck as pdk
from app.ui_components import inject_custom_css
from activities.hiking import get_hiking_route
from activities.cycling import get_cycling_route

def render_carousel_card(activity, distance_km=None, on_skip=None, on_match=None):
    """
    Affiche une carte d'activité façon Tinder : grande photo, infos bien visibles, boutons swipe stylés.
    Carousel : 2 images puis la carte, navigation fluide.
    Les callbacks on_skip/on_match sont appelés si fournis.
    """
    inject_custom_css()
    name = html.escape(activity.get("name", "Unknown"))
    category = html.escape(activity.get("category", "Activity"))
    rating = activity.get("rating", "N/A")
    address = html.escape(activity.get("address", ""))
    price = activity.get("price", "")
    photos = activity.get("photos") or [activity.get("image_url")]
    lat = activity.get("lat")
    lon = activity.get("lon")

    # Carousel: 2 images puis la carte
    # Correction : filtrer les images vides et s'assurer d'avoir 2 images valides
    valid_photos = [p for p in photos if p]
    items = valid_photos[:2]
    while len(items) < 2:
        items.append(valid_photos[0] if valid_photos else None)
    if lat and lon:
        items.append("__map__")
    if "carousel_index" not in st.session_state:
        st.session_state.carousel_index = 0
    index = st.session_state.carousel_index
    max_index = len(items) - 1

    st.markdown("""
    <style>
    body, .stApp {
        background: linear-gradient(135deg, #232526 0%, #414345 100%) !important;
        min-height: 100vh;
    }
    .tinder-card {
        background: #fff !important;
        border-radius: 28px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.18);
        max-width: 420px;
        margin: 32px auto 16px;
        padding: 0;
        overflow: hidden;
        border: 2px solid #e91e63;
        position: relative;
        z-index: 10;
    }
    .tinder-img {
        width: 100%;
        aspect-ratio: 4/3;
        object-fit: cover;
        object-position: center;
        background: #f0f0f0;
        border-radius: 28px 28px 0 0;
        display: block;
        box-shadow: 0 2px 12px rgba(233,30,99,0.08);
    }
    .tinder-info {
        padding: 24px 20px 12px 20px;
        text-align: left;
        background: #fff !important;
    }
    .tinder-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0 0 8px 0;
        color: #e91e63;
        letter-spacing: 0.5px;
    }
    .tinder-meta {
        font-size: 1.15rem;
        color: #222;
        margin-bottom: 8px;
        font-weight: 500;
    }
    .tinder-address {
        font-size: 1.05rem;
        color: #666;
        margin-bottom: 8px;
        font-style: italic;
    }
    .tinder-distance {
        font-size: 1.05rem;
        color: #888;
        margin-bottom: 8px;
    }
    .tinder-btns {
        display: flex;
        justify-content: space-around;
        margin: 18px 0 8px 0;
        background: #fff !important;
        border-radius: 0 0 28px 28px;
        padding-bottom: 12px;
    }
    .tinder-btn {
        font-size: 2.2rem;
        border: none;
        background: none;
        cursor: pointer;
        transition: transform 0.1s, background 0.2s;
        border-radius: 16px;
        padding: 0.5em 1.2em;
        margin: 0 8px;
    }
    .tinder-btn.skip {
        background: #f8d7da;
        color: #c82333;
    }
    .tinder-btn.match {
        background: #ffe0f0;
        color: #e91e63;
    }
    .tinder-btn:active {
        transform: scale(1.15);
        background: #f3e5f5;
    }
    .tinder-nav {
        display: flex;
        justify-content: space-between;
        margin: 10px 0 0 0;
        background: #fff !important;
        border-radius: 0 0 28px 28px;
        padding: 0 16px 8px 16px;
    }
    .tinder-nav-btn {
        font-size: 1.1rem;
        border: none;
        background: #f0f0f0;
        color: #222;
        border-radius: 8px;
        padding: 0.3em 1.1em;
        cursor: pointer;
        margin: 0 2px;
    }
    .tinder-nav-btn:active {
        background: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="tinder-card">', unsafe_allow_html=True)
    # Affichage principal (image ou carte)
    if items[index] == "__map__":
        map_layers = [
            pdk.Layer(
                "ScatterplotLayer",
                data=[{"position": [lon, lat]}],
                get_position="position",
                get_color=[233, 30, 99, 180],
                get_radius=180
            ),
            pdk.Layer(
                "TextLayer",
                data=[{"position": [lon, lat], "text": name}],
                get_position="position",
                get_text="text",
                get_color=[0, 0, 0, 200],
                get_size=18,
                get_alignment_baseline="'bottom'"
            )
        ]
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=13, pitch=0),
            layers=map_layers
        ))
    else:
        image_url = items[index]
        st.markdown(f'<img class="tinder-img" src="{image_url}" alt="Activity Image">', unsafe_allow_html=True)

    # Infos profil
    st.markdown('<div class="tinder-info">', unsafe_allow_html=True)
    st.markdown(f'<div class="tinder-title">{name}</div>', unsafe_allow_html=True)
    meta = f"<span>{category}</span>"
    if rating and rating != "N/A":
        meta += f" • ⭐ {rating}"
    if price:
        meta += f" • {html.escape(price)}"
    st.markdown(f'<div class="tinder-meta">{meta}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tinder-address">{address}</div>', unsafe_allow_html=True)
    if distance_km is not None:
        st.markdown(f'<div class="tinder-distance">{distance_km:.1f} km away</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Navigation carousel stylée
    st.markdown('<div class="tinder-nav">', unsafe_allow_html=True)
    nav_cols = st.columns([1, 1])
    with nav_cols[0]:
        if st.button("⬅️ Photo", key=f"left-{name}"):
            st.session_state.carousel_index = max(index - 1, 0)
    with nav_cols[1]:
        if st.button("Photo ➡️", key=f"right-{name}"):
            st.session_state.carousel_index = min(index + 1, max_index)
    st.markdown('</div>', unsafe_allow_html=True)

    # Boutons swipe façon Tinder stylés
    st.markdown('<div class="tinder-btns">', unsafe_allow_html=True)
    btn_cols = st.columns([1, 1])
    skip_clicked = False
    match_clicked = False
    with btn_cols[0]:
        skip_clicked = st.button("❌", key=f"skip-{name}", help="Passer", use_container_width=True)
    with btn_cols[1]:
        match_clicked = st.button("💖", key=f"match-{name}", help="Match", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Appelle les callbacks si besoin
    if skip_clicked and on_skip:
        on_skip()
    if match_clicked and on_match:
        on_match()
