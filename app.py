import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests  # Pour l'envoi vers Make.com

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Dr. Plant | Jungle Feed", page_icon="🌿", layout="centered")

# Design aux couleurs de Jungle Feed
st.markdown("""
    <style>
    .main { background-color: #f9fbf9; }
    .stButton>button {
        background: linear-gradient(135deg, #2D5A27 0%, #4A8B3F 100%);
        color: white; border-radius: 25px; height: 3.5em; width: 100%;
        font-weight: bold; font-size: 1.1rem; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .report-card {
        padding: 25px; border-radius: 15px; background-color: white;
        border-left: 8px solid #2D5A27; box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

# 2. CONFIGURATION IA
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("⚠️ Clé API manquante dans les Secrets Streamlit.")
    st.stop()

# 3. CATALOGUE JUNGLE FEED COMPLET
CATALOGUE = """
KITS COMPLETS :
- Kit Ultime Anti-Thrips : https://www.junglefeed.fr/products/kit-ultime-anti-thrips
- Kit Spécial Cochenille : https://www.junglefeed.fr/products/kit-special-cochenille-solution-complete-anti-cochenilles
- Kit Spécial Araignée Rouge : https://www.junglefeed.fr/products/kit-special-araignee-rouge-solution-complete-anti-acariens
- Kit Anti-Moucherons 3-en-1 : https://www.junglefeed.fr/products/kit-anti-moucherons-3-en-1-naturel-nematodes-diatomee-piege

INSECTICIDES & SOINS :
- Anti-Pucerons Naturel : https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml
- Huile de Neem : https://www.junglefeed.fr/products/huile-de-neem-prete-a-lemploi-500-ml
- Purin d'Ortie : https://www.junglefeed.fr/products/purin-dortie-agriculture-biologique-made-in-france
- Purin de Fougère : https://www.junglefeed.fr/products/purin-de-fougere-insecticide-repulsif-naturel-500ml
- Purin de Prêle : https://www.junglefeed.fr/products/purin-de-prele-agriculture-biologique-made-in-france
- Purin d'Ail : https://www.junglefeed.fr/products/purin-dail-fongicide-repulsif-total-pret-a-lemploi

NUTRITION :
- Engrais Plantes d'Intérieur : https://www.junglefeed.fr/products/engrais-plantes-dinterieur-et-plantes-rares-500ml
- Jungle Stick : https://www.junglefeed.fr/products/engrais-naturel-1-jungle-stick
"""

# 4. INTERFACE
st.image("https://www.junglefeed.fr/cdn/shop/files/Logo_Jungle_Feed_Web.png", width=180)
st.title("🌿 Dr. Plant")
st.write("Diagnostic IA instantané par Jungle Feed.")

img_file = st.camera_input("Prenez une photo de la zone touchée")
if not img_file:
    img_file = st.file_uploader("Ou importez une photo", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("Lancer le diagnostic Expert 🚀"):
        with st.spinner("L'expert Jungle Feed analyse votre plante..."):
            try:
                # Utilisation du modèle 2026
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"""
                Tu es l'agronome expert Jungle Feed. 
                1. Identifie la plante et le problème.
                2. Donne 2 conseils de soin immédiats.
                3. Recommande EXCLUSIVEMENT le produit adapté ici : {CATALOGUE}.
                """
                
                response = model.generate_content([prompt, img])
                
                # Affichage des résultats
                st.markdown('<div class="report-card">', unsafe_allow_html=True)
                st.markdown("### 📋 Rapport du Dr. Plant")
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                st.balloons()

                # --- PARTIE AUTOMATION (MAKE.COM) ---
                # Remplace l'URL ci-dessous par ton lien Webhook de Make
                webhook_url = "https://hook.eu1.make.com/78bx3x46hpkkn0ksaojisja7px9runbm" 
                
                # Création du paquet de données (Payload)
                payload = {
                    "source": "Dr. Plant App",
                    "status": "Success",
                    "diagnostic_resume": response.text[:500]
                }
                
                # Envoi des données
                try:
                    requests.post(webhook_url, json=payload, timeout=2)
                except:
                    pass # L'app ne plante pas si le Webhook échoue

            except Exception as e:
                st.error(f"Erreur d'analyse : {e}")
