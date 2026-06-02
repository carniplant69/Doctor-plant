import streamlit as st
from PIL import Image
from gemini_engine import analyser_image, trouver_produits
from ui_components import inject_css, afficher_hero, afficher_diagnostic, get_logo_base64
from auth import afficher_auth
from backoffice import afficher_backoffice
from database import save_diagnostic, save_product_click

st.set_page_config(
    page_title="Doctor Plant · Jungle Feed",
    page_icon="🌿",
    layout="centered"
)

inject_css()

for key, val in {
    "user": None,
    "user_id": None,
    "diagnostic_id": None,
    "show_auth": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Clé API Gemini manquante.")
    API_KEY = None

user = st.session_state.get("user")
logo_b64 = get_logo_base64("logo.png")

# ── ADMIN ───────────────────────────────────────────────────────────────
if user and user.get("is_admin"):
    afficher_backoffice()

# ── AUTH ────────────────────────────────────────────────────────────────
elif not user and st.session_state["show_auth"]:
    afficher_hero(logo_b64)
    if st.button("← Retour", use_container_width=True):
        st.session_state["show_auth"] = False
    afficher_auth()

# ── PRINCIPALE ──────────────────────────────────────────────────────────
else:
    afficher_hero(logo_b64)

    # Navigation
    col1, col2 = st.columns([3, 1])
    if user:
        with col1:
            st.markdown(
                '<p style="font-size:0.85rem;color:#777777;margin:0 0 0.5rem 0;">'
                '👋 <strong>' + user["email"] + '</strong></p>',
                unsafe_allow_html=True
            )
        with col2:
            if st.button("🚪 Déco", use_container_width=True):
                st.session_state["user"] = None
                st.session_state["user_id"] = None
    else:
        with col2:
            if st.button("👤 Connexion", use_container_width=True):
                st.session_state["show_auth"] = True

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

    # Mode sélection
    st.markdown(
        '<p style="font-size:0.88rem;font-weight:700;color:#111111;'
        'margin:0 0 0.5rem 0;">Comment veux-tu ajouter ta photo ?</p>',
        unsafe_allow_html=True
    )

    col_cam, col_up = st.columns(2)
    with col_cam:
        btn_cam = st.button(
            "📷 Caméra",
            use_container_width=True,
            type="primary" if st.session_state.get("mode", "camera") == "camera" else "secondary"
        )
    with col_up:
        btn_up = st.button(
            "🖼️ Galerie",
            use_container_width=True,
            type="primary" if st.session_state.get("mode") == "upload" else "secondary"
        )

    if btn_cam:
        st.session_state["mode"] = "camera"
    if btn_up:
        st.session_state["mode"] = "upload"

    if "mode" not in st.session_state:
        st.session_state["mode"] = "camera"

    mode = st.session_state.get("mode", "camera")

    fichier = None

    st.markdown(
        '<div style="background:#F5F5F5;border-radius:14px;'
        'padding:0.8rem 1rem;margin:0.8rem 0;'
        'border-left:3px solid #333333;">'
        '<p style="margin:0;font-size:0.82rem;color:#111111;">'
        '📌 <strong>Astuce :</strong> '
        + ("Approche-toi de la plante, assure-toi d'avoir une bonne lumière"
           if mode == "camera"
           else "Formats acceptés JPG, PNG, WEBP")
        + '</p></div>',
        unsafe_allow_html=True
    )

    if mode == "camera":
        photo = st.camera_input(
            label="Pointer vers la plante",
            label_visibility="collapsed"
        )
        if photo:
            fichier = photo
    else:
        upload = st.file_uploader(
            label="Glisse ta photo ici",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed"
        )
        if upload:
            fichier = upload

    if fichier:
        image = Image.open(fichier)
        st.image(image, use_container_width=True)
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        lancer = st.button(
            "🔍 Lancer le diagnostic",
            type="primary",
            use_container_width=True
        )

        if lancer and API_KEY:
            with st.spinner("🌿 Dr. Plant analyse votre plante..."):
                resultat = analyser_image(image, API_KEY)

            if not resultat["succes"]:
                st.error("❌ " + resultat["erreur"])

            else:
                diagnostic = resultat["data"]

                if not diagnostic.get("est_une_plante"):
                    st.markdown(
                        '<div style="background:#FFF8E1;border-radius:16px;'
                        'padding:1.2rem;text-align:center;margin-top:0.8rem;">'
                        '<p style="font-size:1.5rem;margin:0 0 0.5rem 0;">🤔</p>'
                        '<p style="font-weight:700;color:#F57F17;'
                        'margin:0 0 0.3rem 0;">Aucune plante détectée</p>'
                        '<p style="font-size:0.85rem;color:#777777;margin:0;">'
                        'Essaie avec une photo plus nette ou plus proche</p></div>',
                        unsafe_allow_html=True
                    )

                else:
                    diag_id = None
                    if st.session_state.get("user_id"):
                        diag_id = save_diagnostic(
                            st.session_state["user_id"], diagnostic
                        )
                        st.session_state["diagnostic_id"] = diag_id

                    afficher_diagnostic(diagnostic)

                    recommandations = trouver_produits(diagnostic)
                    type_reco = recommandations.get("type")
                    produits = recommandations.get("produits", [])

                    if type_reco == "curatif":
                        titre_s = "🛒 Choisis ton traitement"
                        sous_t = "Tous ces produits traitent ton problème · 100% naturels · Fabriqués en France"
                    else:
                        titre_s = "⭐ Garde ta plante en bonne santé !"
                        sous_t = "Choisis parmi nos produits préventifs · 100% naturels · Fabriqués en France"

                    st.mark
