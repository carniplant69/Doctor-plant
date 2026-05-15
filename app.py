# Doctor Plant — Application principale
# Diagnostic IA de plantes avec recommandations Jungle Feed

import streamlit as st
from PIL import Image

from gemini_engine import analyser_image, trouver_produits
from ui_components import inject_css, afficher_hero, afficher_diagnostic, afficher_produits

# ─── Configuration de la page ──────────────────────────────────────────
st.set_page_config(
    page_title="Doctor Plant · Jungle Feed",
    page_icon="🌿",
    layout="centered"
)

inject_css()
afficher_hero()

# ─── Clé API depuis les secrets Streamlit ─────────────────────────────
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("⚠️ Clé API Gemini manquante. Configure-la dans les secrets Streamlit.")
    st.stop()

# ─── Zone d'upload ────────────────────────────────────────────────────
st.markdown("### 📸 Prends une photo de ta plante")
st.caption("Formats acceptés : JPG, PNG, WEBP · Résolution recommandée : 800px minimum")

fichier = st.file_uploader(
    label="Glisse ta photo ici ou clique pour parcourir",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed"
)

# ─── Analyse ──────────────────────────────────────────────────────────
if fichier:
    image = Image.open(fichier)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(image, caption="Votre plante", use_container_width=True)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        lancer = st.button(
            "🔍 Lancer le diagnostic",
            type="primary",
            use_container_width=True
        )
    
    if lancer:
        with st.spinner("🌿 Dr. Plant analyse votre plante..."):
            resultat = analyser_image(image, API_KEY)
        
        if not resultat["succes"]:
            st.error(f"❌ {resultat['erreur']}")
            st.stop()
        
        diagnostic = resultat["data"]
        
        # Vérification que c'est bien une plante
        if not diagnostic.get("est_une_plante"):
            st.warning("🤔 Hmm, je ne vois pas de plante sur cette photo. Essaie avec une image plus nette ou plus proche !")
            st.stop()
        
        # Affichage du diagnostic
        afficher_diagnostic(diagnostic)
        
        # Recommandations produits
        recommandations = trouver_produits(diagnostic)
        afficher_produits(recommandations)
        
        # Footer CTA
        st.markdown("""
        <div style="text-align:center; margin-top:2rem; padding:1.5rem; 
                    background:#f0f7eb; border-radius:12px;">
            <p style="margin:0; color:#2D5016; font-weight:600;">
                🌿 Découvrez toute la gamme Jungle Feed
            </p>
            <p style="margin:0.3rem 0 1rem 0; color:#666; font-size:0.85rem;">
                100% naturel · Fabriqué en France · Livraison rapide
            </p>
            <a href="https://www.junglefeed.fr" target="_blank" 
               style="background:#2D5016; color:white; padding:0.6rem 1.8rem; 
                      border-radius:25px; text-decoration:none; font-weight:600;">
                Visiter la boutique →
            </a>
        </div>
        """, unsafe_allow_html=True)

# ─── État vide ────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div style="text-align:center; padding:3rem 1rem; color:#999;">
        <div style="font-size:4rem;">🪴</div>
        <p style="font-size:1.1rem; margin:0.5rem 0;">
            Upload une photo pour commencer le diagnostic
        </p>
        <p style="font-size:0.85rem;">
            Dr. Plant identifie maladies, nuisibles et carences en quelques secondes
        </p>
    </div>
    """, unsafe_allow_html=True)
