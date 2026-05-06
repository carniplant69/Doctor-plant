import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURATION VISUELLE (Pro & Branding)
st.set_page_config(page_title="Dr. Plant | Jungle Feed", page_icon="🌿", layout="centered")

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

# 2. CONFIGURATION IA (Gemini 2.5 Flash - Mai 2026)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("⚠️ Clé API manquante dans les Secrets Streamlit.")
    st.stop()

# 3. CATALOGUE JUNGLE FEED (Base de données de l'expert)
CATALOGUE = """
KITS COMPLETS (S.O.S) :
- Kit Ultime Anti-Thrips (Thrips, moucherons, acariens) : https://www.junglefeed.fr/products/kit-ultime-anti-thrips
- Kit Spécial Cochenille (Tous types de cochenilles) : https://www.junglefeed.fr/products/kit-special-cochenille-solution-complete-anti-cochenilles
- Kit Spécial Araignée Rouge (Acariens) : https://www.junglefeed.fr/products/kit-special-araignee-rouge-solution-complete-anti-acariens
- Kit Anti-Moucherons 3-en-1 : https://www.junglefeed.fr/products/kit-anti-moucherons-3-en-1-naturel-nematodes-diatomee-piege

INSECTICIDES & SOINS CIBLÉS :
- Anti-Pucerons Naturel Spray : https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml
- Huile de Neem Prête à l'Emploi : https://www.junglefeed.fr/products/huile-de-neem-prete-a-lemploi-500-ml
- Savon noir Prêt à l'Emploi : https://www.junglefeed.fr/products/savon-noir-500ml-pret-a-lemploi-made-in-france
- Terre de diatomée : https://www.junglefeed.fr/products/terre-de-diatomee-pure-50g

LES PURINS (Arsenal Bio) :
- Purin d'Ortie (Fortifiant & Azote) : https://www.junglefeed.fr/products/purin-dortie-agriculture-biologique-made-in-france
- Purin de Fougère (Répulsif insectes) : https://www.junglefeed.fr/products/purin-de-fougere-insecticide-repulsif-naturel-500ml
- Purin de Prêle (Fongicide / Maladies cryptogamiques) : https://www.junglefeed.fr/products/purin-de-prele-agriculture-biologique-made-in-france
- Purin d'Ail (Répulsif total & fongicide) : https://www.junglefeed.fr/products/purin-dail-fongicide-repulsif-total-pret-a-lemploi
- Purin de Sureau (Bouclier préventif) : https://www.junglefeed.fr/products/purin-de-sureau-bouclier-naturel-500ml-nourrit-protege

NUTRITION & BOOST :
- Engrais Plantes d'Intérieur (500ml) : https://www.junglefeed.fr/products/engrais-plantes-dinterieur-et-plantes-rares-500ml
- Jungle Stick (Engrais lent) : https://www.junglefeed.fr/products/engrais-naturel-1-jungle-stick
- Engrais Orchidées : https://www.junglefeed.fr/products/engrais-orchidees-500ml-floraison-spectaculaire

SOINS DE SAISON :
- Rosée d'été (Protecteur chaleur) : https://www.junglefeed.fr/products/rosee-dete-protecteur-de-chaleur-pour-plantes
- Protecteur Hivernal (Anti-gel) : https://www.junglefeed.fr/products/protecteur-hivernal-jungle-feed-anti-gel-naturel-plantes-500ml
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
        with st.spinner("Analyse des tissus végétaux..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"""
                Tu es l'agronome expert officiel de Jungle Feed. 
                Ton but : rassurer l'utilisateur et vendre la solution adaptée.
                
                1. Identifie la plante et le problème (parasite ou maladie).
                2. Explique brièvement la cause.
                3. Donne 2 conseils de soin immédiats (ex: isoler la plante, doucher les feuilles).
                4. Recommande EXCLUSIVEMENT le produit le plus pertinent dans cette liste : {CATALOGUE}.
                
                Sois enthousiaste et pro. Utilise des emojis.
                """
                
                response = model.generate_content([prompt, img])
                
                st.markdown('<div class="report-card">', unsafe_allow_html=True)
                st.markdown("### 📋 Rapport du Dr. Plant")
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                st.balloons()
                
            except Exception as e:
                st.error(f"Une erreur est survenue lors de l'analyse : {e}")
