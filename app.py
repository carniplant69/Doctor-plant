import streamlit as st
from PIL import Image
from gemini_engine import analyser_image, trouver_produits
from ui_components import (
    inject_css, afficher_hero,
    afficher_diagnostic, afficher_produits, get_logo_base64
)

# ─── Config page ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Doctor Plant · Jungle Feed",
    page_icon="🌿",
    layout="centered"
)

inject_css()

# ─── Logo ──────────────────────────────────────────────────────────────
logo_b64 = get_logo_base64("logo.png")
afficher_hero(logo_b64)

# ─── Clé API ───────────────────────────────────────────────────────────
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("⚠️ Clé API Gemini manquante dans les secrets Streamlit.")
    st.stop()

# ─── Upload / Caméra ───────────────────────────────────────────────────
st.markdown("### 📸 Prends une photo de ta plante")
st.caption("Photo nette, bien éclairée pour un meilleur diagnostic")

onglet_camera, onglet_upload = st.tabs(["📷 Prendre une photo", "🖼️ Uploader une image"])

fichier = None

with onglet_camera:
    photo = st.camera_input("Pointe ta caméra vers ta plante")
    if photo:
        fichier = photo

with onglet_upload:
    upload = st.file_uploader(
        label="Glisse ta photo ici",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )
    if upload:
        fichier = upload

# ─── Analyse ───────────────────────────────────────────────────────────
if fichier:
    image = Image.open(fichier)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(image, caption="Votre plante", use_container_width=True)
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        lancer = st.button("🔍 Lancer le diagnostic", type="primary", use_container_width=True)

    if lancer:
        with st.spinner("🌿 Dr. Plant analyse votre plante..."):
            resultat = analyser_image(image, API_KEY)

        if not resultat["succes"]:
            st.error(f"❌ {resultat['erreur']}")
            st.stop()

        diagnostic = resultat["data"]

        if not diagnostic.get("est_une_plante"):
            st.warning("🤔 Je ne vois pas de plante sur cette photo. Essaie avec une image plus nette !")
            st.stop()

        afficher_diagnostic(diagnostic)

        recommandations = trouver_produits(diagnostic)
        afficher_produits(recommandations)

else:
    st.markdown("""
    <div class="empty-state">
        <div class="big-emoji">🪴</div>
        <p><strong>Prends ou uploade une photo</strong><br>
        Dr. Plant identifie maladies, nuisibles<br>et carences en quelques secondes</p>
    </div>
    """, unsafe_allow_html=True)
