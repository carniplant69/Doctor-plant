import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuration de l'IA (On récupère la clé plus tard)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🌿 Dr. Plant : Diagnostic Jungle Feed")
st.write("Prenez une photo de votre plante pour identifier le problème.")

# 2. Capture de la photo
img_file = st.camera_input("Scanner une feuille")

if img_file:
    img = Image.open(img_file)
    st.image(img, caption="Analyse en cours...")

    # 3. Les instructions pour l'IA
    prompt = """Identifie la plante et sa maladie. 
    Donne une solution courte. 
    Si besoin de produit, propose : 'Le Kit Anti-Thrips' 
    avec ce lien : https://www.junglefeed.fr/products/kit-ultime-anti-thrips"""

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, img])
    
    st.success("Résultat de l'analyse :")
    st.write(response.text)
