import streamlit as st
from PIL import Image
from gemini_engine import analyser_image, trouver_produits
from ui_components import (
    inject_css, afficher_hero,
    afficher_diagnostic, get_logo_base64
)
from auth import afficher_auth
from backoffice import afficher_backoffice
from database import save_diagnostic, save_product_click

st.set_page_config(
    page_title="Doctor Plant · Jungle Feed",
    page_icon="🌿",
    layout="centered"
)

inject_css()

# Initialisation session
for key, val in {
    "user": None,
    "user_id": None,
    "diagnostic_id": None,
    "show_auth": False,
    "page": "home"
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Clé API
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Clé API Gemini manquante.")
    st.stop()

user = st.session_state.get("user")

# Backoffice admin
if user and user.get("is_admin"):
    afficher_backoffice()
    st.stop()

# Hero
logo_b64 = get_logo_base64("logo.png")
afficher_hero(logo_b64)

# Navigation
if user:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            '<p style="font-size:0.85rem;color:#777777;margin:0 0 0.5rem 0;">👋 <strong>'
            + user["email"] + '</strong></p>',
            unsafe_allow_html=True
        )
    with col2:
        if st.button("🚪 Déco", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.stop()
else:
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("👤 Connexion", use_container_width=True):
            st.session_state["show_auth"] = not st.session_state["show_auth"]

# Page auth
if not user and st.session_state["show_auth"]:
    afficher_auth()
    st.stop()

# Page principale
st.markdown(
    '<div style="background:white;border-radius:20px;padding:1.2rem;'
    'margin-bottom:1rem;box-shadow:0 2px 12px rgba(0,0,0,0.06);">'
    '<p style="font-size:1rem;font-weight:800;color:#111111;margin:0 0 0.3rem 0;">'
    '📸 Diagnostique ta plante</p>'
    '<p style="font-size:0.82rem;color:#777777;margin:0;">'
    'Photo nette et bien éclairée pour un meilleur résultat</p>'
    '</div>',
    unsafe_allow_html=True
)

onglet_camera, onglet_upload = st.tabs(["📷 Caméra", "🖼️ Galerie"])
fichier = None

with onglet_camera:
    st.markdown(
        '<div style="background:#F5F5F5;border-radius:14px;padding:0.8rem 1rem;'
        'margin-bottom:0.8rem;border-left:3px solid #333333;">'
        '<p style="margin:0;font-size:0.82rem;color:#111111;">'
        '📌 <strong>Astuce :</strong> Approche-toi de la plante, '
        'assure-toi d\'avoir une bonne lumière</p></div>',
        unsafe_allow_html=True
    )
    photo = st.camera_input(
        label="Pointer vers la plante et appuyer sur le bouton ci-dessous",
        label_visibility="visible"
    )
    if photo:
        fichier = photo

with onglet_upload:
    st.markdown(
        '<div style="background:#F5F5F5;border-radius:14px;padding:0.8rem 1rem;'
        'margin-bottom:0.8rem;border-left:3px solid #333333;">'
        '<p style="margin:0;font-size:0.82rem;color:#111111;">'
        '📌 <strong>Astuce :</strong> Formats acceptés JPG, PNG, WEBP</p></div>',
        unsafe_allow_html=True
    )
    upload = st.file_uploader(
        label="Glisse ta photo ici",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )
    if upload:
        fichier = upload

if fichier:
    image = Image.open(fichier)

    st.markdown(
        '<div style="background:white;border-radius:20px;padding:1rem;'
        'margin:0.8rem 0;box-shadow:0 2px 12px rgba(0,0,0,0.06);">'
        '<p style="font-size:0.82rem;color:#777777;margin:0 0 0.5rem 0;'
        'font-weight:600;">📷 Votre photo</p></div>',
        unsafe_allow_html=True
    )
    st.image(image, use_container_width=True)
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    lancer = st.button(
        "🔍 Lancer le diagnostic",
        type="primary",
        use_container_width=True
    )

    if lancer:
        with st.spinner("🌿 Dr. Plant analyse votre plante..."):
            resultat = analyser_image(image, API_KEY)

        if not resultat["succes"]:
            st.error("❌ " + resultat["erreur"])
            st.stop()

        diagnostic = resultat["data"]

        if not diagnostic.get("est_une_plante"):
            st.markdown(
                '<div style="background:#FFF8E1;border-radius:16px;padding:1.2rem;'
                'text-align:center;margin-top:0.8rem;">'
                '<p style="font-size:1.5rem;margin:0 0 0.5rem 0;">🤔</p>'
                '<p style="font-weight:700;color:#F57F17;margin:0 0 0.3rem 0;">'
                'Aucune plante détectée</p>'
                '<p style="font-size:0.85rem;color:#777777;margin:0;">'
                'Essaie avec une photo plus nette ou plus proche</p></div>',
                unsafe_allow_html=True
            )
            st.stop()

        # Sauvegarde si connecté
        diag_id = None
        if st.session_state.get("user_id"):
            diag_id = save_diagnostic(
                st.session_state["user_id"], diagnostic
            )
            st.session_state["diagnostic_id"] = diag_id

        afficher_diagnostic(diagnostic)

        # Produits
        recommandations = trouver_produits(diagnostic)
        type_reco = recommandations.get("type")
        produits = recommandations.get("produits", [])

        titre_section = "🛒 Choisis ton traitement" if type_reco == "curatif" else "⭐ Garde ta plante en bonne santé !"
        sous_titre = "Tous ces produits traitent ton problème · 100% naturels · Fabriqués en France" if type_reco == "curatif" else "Choisis parmi nos produits préventifs · 100% naturels · Fabriqués en France"

        st.markdown(
            '<p style="font-size:1.1rem;font-weight:800;color:#111111;'
            'margin:1.2rem 0 0.2rem 0;">' + titre_section + '</p>'
            '<p style="color:#777777;font-size:0.82rem;margin:0 0 0.8rem 0;">'
            + sous_titre + '</p>',
            unsafe_allow_html=True
        )

        for produit in produits:
            col_prod, col_btn = st.columns([4, 1])
            with col_prod:
                st.markdown(
                    '<div style="background:white;border-radius:16px;'
                    'padding:0.9rem 1rem;box-shadow:0 2px 10px rgba(0,0,0,0.05);'
                    'border:1px solid #EEEEEE;display:flex;align-items:center;gap:0.8rem;">'
                    '<span style="font-size:1.8rem;">' + produit["emoji"] + '</span>'
                    '<div>'
                    '<p style="font-size:0.88rem;font-weight:700;color:#111111;margin:0;">'
                    + produit["nom"] + '</p>'
                    '<p style="font-size:0.75rem;color:#777777;margin:0;">'
                    + produit["description"] + '</p>'
                    '</div></div>',
                    unsafe_allow_html=True
                )
            with col_btn:
                st.link_button(
                    "🛍️",
                    produit["url"],
                    help="Acheter " + produit["nom"]
                )
                save_product_click(
                    st.session_state.get("user_id"),
                    produit["nom"],
                    produit["url"],
                    st.session_state.get("diagnostic_id")
                )

        st.markdown(
            '<div style="background:linear-gradient(135deg,#1A1A1A,#444444);'
            'border-radius:20px;padding:1.3rem;text-align:center;margin-top:1rem;">'
            '<h3 style="color:white;margin:0 0 0.3rem 0;font-size:1rem;font-weight:800;">'
            '🌿 Toute la gamme Jungle Feed</h3>'
            '<p style="color:rgba(255,255,255,0.7);margin:0 0 0.8rem 0;font-size:0.82rem;">'
            '100% naturel · Fabriqué en France</p>'
            '<a href="https://www.junglefeed.fr" target="_blank" style="'
            'display:inline-block;background:white;color:#1A1A1A;padding:0.5rem 1.5rem;'
            'border-radius:50px;font-weight:800;font-size:0.85rem;text-decoration:none;">'
            'Visiter la boutique →</a></div>',
            unsafe_allow_html=True
        )

else:
    st.markdown(
        '<div style="background:white;border-radius:20px;padding:2rem 1.5rem;'
        'text-align:center;margin-top:0.5rem;box-shadow:0 2px 12px rgba(0,0,0,0.05);">'
        '<div style="background:#F5F5F5;width:70px;height:70px;border-radius:50%;'
        'display:flex;align-items:center;justify-content:center;'
        'margin:0 auto 1rem auto;font-size:2rem;">🪴</div>'
        '<p style="font-weight:800;color:#111111;font-size:1rem;margin:0 0 1rem 0;">'
        'Comment ça marche ?</p>'
        '<div style="text-align:left;">'
        '<div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.8rem;">'
        '<div style="background:#EEEEEE;border-radius:50%;width:32px;height:32px;'
        'display:flex;align-items:center;justify-content:center;'
        'font-size:0.9rem;flex-shrink:0;">1️⃣</div>'
        '<p style="margin:0;font-size:0.88rem;color:#555555;">'
        'Prends une photo de ta plante</p></div>'
        '<div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.8rem;">'
        '<div style="background:#EEEEEE;border-radius:50%;width:32px;height:32px;'
        'display:flex;align-items:center;justify-content:center;'
        'font-size:0.9rem;flex-shrink:0;">2️⃣</div>'
        '<p style="margin:0;font-size:0.88rem;color:#555555;">'
        'L\'IA analyse et détecte les problèmes</p></div>'
        '<div style="display:flex;align-items:center;gap:0.8rem;">'
        '<div style="background:#EEEEEE;border-radius:50%;width:32px;height:32px;'
        'display:flex;align-items:center;justify-content:center;'
        'font-size:0.9rem;flex-shrink:0;">3️⃣</div>'
        '<p style="margin:0;font-size:0.88rem;color:#555555;">'
        'Nous te proposons les meilleurs produits naturels pour ta plante</p>'
        '</div></div></div>',
        unsafe_allow_html=True
    )
