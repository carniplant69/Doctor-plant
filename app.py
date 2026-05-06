import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURATION (Design & Icône)
st.set_page_config(page_title="Dr. Plant | Jungle Feed", page_icon="🌿", layout="wide")

# CSS pour un look "App Mobile"
st.markdown("""
    <style>
    .main { background-color: #f9fbf9; }
    .stButton>button {
        background: linear-gradient(135deg, #2D5A27 0%, #4A8B3F 100%);
        color: white; border-radius: 25px; height: 3.5em; width: 100%;
        font-weight: bold; font-size: 1.1rem; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .status-card {
        padding: 20px; border-radius: 15px; background-color: white;
        border-left: 5px solid #2D5A27; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 2. BARRE LATÉRALE (Sidebar)
with st.sidebar:
    st.image("https://www.junglefeed.fr/cdn/shop/files/Logo_Jungle_Feed_Web.png", width=150)
    st.title("Aide & Infos")
    st.info("Prenez une photo bien nette des feuilles (dessus et dessous) pour un meilleur diagnostic.")
    st.divider()
    st.write("📩 Un doute ? [Contactez le SAV](https://www.junglefeed.fr)")

# 3. EN-TÊTE
col_header1, col_header2 = st.columns([1, 4])
with col_header1:
    st.title("🌿")
with col_header2:
    st.title("Dr. Plant")
    st.caption("L'intelligence artificielle au service de vos plantes")

# 4. CONFIG IA
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("Clé API manquante dans les Secrets.")
    st.stop()

# 5. ZONE DE CAPTURE
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📸 Scanner")
    img_file = st.camera_input("Scanner", label_visibility="collapsed")
    if not img_file:
        img_file = st.file_uploader("Ou importer une photo", type=['jpg', 'png', 'jpeg'])

# 6. ANALYSE ET RÉSULTATS
if img_file:
    with col2:
        img = Image.open(img_file)
        st.image(img, use_container_width=True)
        
        if st.button("Lancer le diagnostic Jungle Feed 🚀"):
            with st.spinner("Analyse moléculaire en cours..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = "Expert agronome Jungle Feed. Nom plante, maladie précise, soin et produit https://www.junglefeed.fr. Format propre avec emojis."
                    
                    response = model.generate_content([prompt, img])
                    
                    st.markdown('<div class="status-card">', unsafe_allow_html=True)
                    st.markdown("### 📋 Rapport d'Expertise")
                    st.write(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.balloons()
                except Exception as e:
                    st.error(f"Erreur : {e}")
