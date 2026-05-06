import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURATION DE LA PAGE (Look & Feel Pro)
st.set_page_config(
    page_title="Dr. Plant by Jungle Feed",
    page_icon="🌿",
    layout="centered"
)

# Design personnalisé aux couleurs de Jungle Feed
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        background-color: #2D5A27;
        color: white;
        border-radius: 12px;
        border: none;
        height: 3em;
        width: 100%;
        font-weight: bold;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #3d7a35;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 2. VÉRIFICATION DE LA CLÉ API
if "GEMINI_API_KEY" in st.secrets:
    # transport='rest' est crucial en 2026 pour la stabilité sur Streamlit Cloud
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("⚠️ Erreur : Clé API manquante. Ajoutez GEMINI_API_KEY dans les Secrets de Streamlit.")
    st.stop()

# 3. CATALOGUE JUNGLE FEED (Base de connaissances de l'IA)
CATALOGUE = """
Produits disponibles sur https://www.junglefeed.fr :
- Kit Anti-Thrips Ultime : https://www.junglefeed.fr/products/kit-ultime-anti-thrips (Pour thrips, moucherons, acariens)
- Kit Spécial Cochenille : https://www.junglefeed.fr/products/kit-special-cochenille-solution-complete-anti-cochenilles (Pour cochenilles farineuses ou à bouclier)
- Anti-Pucerons Naturel : https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml (Pour tous types de pucerons)
- Engrais Bio : https://www.junglefeed.fr/products/engrais-plantes-dinterieur-et-plantes-rares-500ml (Pour booster la croissance)
- Huile de Neem : https://www.junglefeed.fr/products/huile-de-neem-prete-a-lemploi-500-ml (Protection et brillant des feuilles)
"""

# 4. INTERFACE UTILISATEUR
st.image("https://www.junglefeed.fr/cdn/shop/files/Logo_Jungle_Feed_Web.png", width=200) # Optionnel : ajoute ton logo
st.title("🌿 Dr. Plant")
st.subheader("Diagnostic IA & Solutions Naturelles")

# Choix de la méthode
option = st.radio("Choisissez votre méthode :", ("📸 Prendre une photo", "📂 Charger une image"), label_visibility="collapsed")

if option == "📸 Prendre une photo":
    img_file = st.camera_input("Scanner la plante")
else:
    img_file = st.file_uploader("Choisir une image depuis votre galerie", type=['jpg', 'png', 'jpeg'])

# 5. LOGIQUE D'ANALYSE
if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True, caption="Analyse en cours...")
    
    if st.button("Lancer le diagnostic Jungle Feed 🚀"):
        with st.spinner("L'expert Jungle Feed analyse les cellules de votre plante..."):
            try:
                # Utilisation du modèle Gemini 2.5 Flash (Standard 2026)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"""
                Tu es l'agronome expert de la marque Jungle Feed. 
                Ton rôle est d'analyser cette photo de plante :
                1. Donne le nom de la plante.
                2. Identifie précisément la maladie ou le parasite (sois très spécifique).
                3. Propose une solution de soin immédiate.
                4. Recommande EXCLUSIVEMENT le produit le plus adapté dans cette liste : {CATALOGUE}.
                
                Réponds de manière pro, bienveillante et avec des emojis. 
                Si la plante est en parfaite santé, félicite l'utilisateur et propose l'Engrais Bio pour l'entretien.
                """
                
                response = model.generate_content([prompt, img])
                
                st.markdown("---")
                st.success("### ✅ Diagnostic de l'Expert")
                st.markdown(response.text)
                st.balloons()
                
            except Exception as e:
                if "429" in str(e):
                    st.error("⏳ Trop de demandes en même temps. Attendez 1 minute avant de recommencer.")
                else:
                    st.error(f"Une petite erreur est survenue. Vérifiez votre connexion. (Détails : {e})")
