import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. CONFIGURATION & DESIGN
st.set_page_config(page_title="Dr. Plant | Jungle Feed", page_icon="🌿", layout="centered")

# Initialisation de la mémoire de session
if "user_data_captured" not in st.session_state:
    st.session_state.user_data_captured = False

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
    .form-box {
        padding: 20px; border: 1px solid #e0e0e0; border-radius: 15px; background: #ffffff;
        margin-top: 20px;
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

SOINS & PURINS :
- Anti-Pucerons Naturel Spray : https://www.junglefeed.fr/products/anti-pucerons-naturel-spray-500ml
- Huile de Neem Prête à l'Emploi : https://www.junglefeed.fr/products/huile-de-neem-prete-a-lemploi-500-ml
- Purin d'Ortie / Fougère / Prêle / Ail / Sureau : https://www.junglefeed.fr/collections/soins
- Savon noir 500ml : https://www.junglefeed.fr/products/savon-noir-500ml-pret-a-lemploi-made-in-france

NUTRITION :
- Engrais Plantes d'Intérieur : https://www.junglefeed.fr/products/engrais-plantes-dinterieur-et-plantes-rares-500ml
- Jungle Stick (Lot de 4 ou 10) : https://www.junglefeed.fr/products/engrais-naturel-lot-de-4-jungle-stick
"""

# 4. INTERFACE
st.image("https://www.junglefeed.fr/cdn/shop/files/Logo_Jungle_Feed_Web.png", width=180)
st.title("🌿 Dr. Plant")
st.write("Diagnostic IA & Solutions Jungle Feed.")

img_file = st.camera_input("📸 Prenez une photo de la zone touchée")
if not img_file:
    img_file = st.file_uploader("Ou importez une photo", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    # --- LOGIQUE DE CAPTURE DE DATA ---
    if not st.session_state.user_data_captured:
        st.markdown('<div class="form-box">', unsafe_allow_html=True)
        st.subheader("📬 Recevoir mon diagnostic")
        email = st.text_input("Votre Email")
        ville = st.text_input("Votre Ville")
        
        st.markdown(f"<p style='font-size: 0.8rem; color: gray;'>RGPD : En validant, vous acceptez que Jungle Feed utilise votre email pour vous envoyer votre diagnostic et des conseils personnalisés.</p>", unsafe_allow_html=True)
        rgpd = st.checkbox("J'accepte les conditions")
        
        if st.button("Obtenir mon diagnostic Expert 🚀"):
            if email and ville and rgpd:
                # Stockage temporaire dans la session
                st.session_state.user_data_captured = True
                st.session_state.user_email = email
                st.session_state.user_ville = ville
                st.rerun()
            else:
                st.warning("Veuillez remplir tous les champs et cocher la case RGPD.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # --- LOGIQUE D'ANALYSE (S'affiche après capture) ---
    else:
        if st.button("Lancer l'analyse 🚀"):
            with st.spinner(f"Analyse en cours pour votre plante à {st.session_state.user_ville}..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"""
                    Tu es l'agronome expert Jungle Feed. Analyse cette photo. 
                    1. Identifie la plante et le problème.
                    2. Recommande EXCLUSIVEMENT un produit de cette liste : {CATALOGUE}.
                    3. Mentionne que le diagnostic est aussi envoyé à {st.session_state.user_email}.
                    Sois pro et utilise des emojis.
                    """
                    response = model.generate_content([prompt, img])
                    
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    st.markdown(f"### ✅ Diagnostic pour {st.session_state.user_email}")
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.balloons()
                except Exception as e:
                    st.error(f"Erreur d'analyse : {e}")

        if st.button("Réinitialiser (Scanner une autre plante)"):
            # On ne réinitialise PAS user_data_captured pour ne pas redemander le mail
            st.rerun()
