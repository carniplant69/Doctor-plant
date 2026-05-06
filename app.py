import streamlit as st
import google.generativeai as genai
from PIL import Image

# Config de la page
st.set_page_config(page_title="Dr. Plant Jungle Feed", page_icon="🌿")

# Récupération de la clé API cachée dans les réglages
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ La clé API n'est pas configurée dans les Secrets Streamlit.")

st.title("🌿 Doctor plant : Diagnostic Expert")
st.write("Identifiez vos parasites et trouvez la solution Jungle Feed adaptée.")

# Capture photo ou téléchargement
img_file = st.camera_input("📸 Prenez une photo d'une feuille")
if not img_file:
    img_file = st.file_uploader("OU choisissez une photo", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("Lancer l'analyse Jungle Feed 🚀"):
        with st.spinner("L'expert analyse votre plante..."):
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Instructions pour l'IA
            prompt = """
            Tu es l'expert agronome de la marque Jungle Feed. 
            1. Analyse cette photo et identifie la plante.
            2. Détecte s'il y a une maladie ou un parasite.
            3. Donne une solution précise.
            4. Recommande UN produit Jungle Feed parmi ceux-là :
               - Si Thrips ou Moucherons : 'Kit Anti-Thrips Ultime' (https://www.junglefeed.fr/products/kit-ultime-anti-thrips)
               - Si Cochenilles : 'Kit Spécial Cochenille' (https://www.junglefeed.fr/products/kit-special-cochenille-solution-complete-anti-cochenilles)
               - Si Pucerons : 'Anti-Pucerons Naturel Spray' (https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml)
            """
            
            response = model.generate_content([prompt, img])
            st.success("✅ Diagnostic terminé !")
            st.markdown(response.text)
