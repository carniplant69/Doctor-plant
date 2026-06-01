import streamlit as st
import base64
import io
from PIL import Image

COULEURS = {
    "vert_principal": "#2E7D32",
    "vert_clair": "#66BB6A",
    "vert_bg": "#F1F8E9",
    "vert_card": "#E8F5E9",
    "orange": "#FF9B3F",
    "blanc": "#FFFFFF",
    "texte_fonce": "#1B2F1E",
    "texte_gris": "#6D8B74",
    "rouge": "#E53935",
    "jaune": "#FFB300",
}

def get_logo_base64(logo_path: str) -> str:
    try:
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

def inject_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Nunito', sans-serif !important;
            background-color: #F1F8E9 !important;
        }

        #MainMenu, footer, header { visibility: hidden; }

        /* Supprime padding Streamlit */
        .block-container {
            padding-top: 0 !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 480px !important;
            margin: 0 auto !important;
        }

        /* Bouton principal */
        .stButton > button {
            background: linear-gradient(135deg, #2E7D32, #66BB6A) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            padding: 0.8rem 2rem !important;
            width: 100% !important;
            box-shadow: 0 4px 15px rgba(46,125,50,0.3) !important;
            margin-top: 0.5rem !important;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px !important;
            background: #E8F5E9 !important;
            border-radius: 16px !important;
            padding: 4px !important;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 12px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
        }
        .stTabs [aria-selected="true"] {
            background: #2E7D32 !important;
            color: white !important;
        }

        /* Images arrondies */
        [data-testid="stImage"] img {
            border-radius: 16px !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
        }

        /* Camera label en français */
        [data-testid="stCameraInput"] > label {
            font-size: 0.9rem !important;
            color: #6D8B74 !important;
        }
    </style>
    """, unsafe_allow_html=True)


def afficher_hero(logo_base64: str = ""):
    """Hero entièrement en HTML avec logo intégré en base64."""

    logo_tag = ""
    if logo_base64:
        logo_tag = f'<img src="data:image/png;base64,{logo_base64}" style="width:80px;height:80px;border-radius:50%;border:3px solid rgba(255,255,255,0.5);box-shadow:0 4px 16px rgba(0,0,0,0.2);margin-bottom:0.8rem;object-fit:cover;">'

    st.markdown(f"""
    <div style="
        background: linear-gradient(160deg, #2E7D32 0%, #66BB6A 100%);
        border-radius: 0 0 28px 28px;
        padding: 2.5rem 1.5rem 2rem 1.5rem;
        text-align: center;
        margin: -1rem -1rem 1.5rem -1rem;
        box-shadow: 0 8px 32px rgba(46,125,50,0.2);
    ">
        {logo_tag}
        <h1 style="
            color: white;
            font-size: 1.7rem;
            font-weight: 800;
            margin: 0 0 0.3rem 0;
            letter-spacing: -0.3px;
            font-family: 'Nunito', sans-serif;
        ">Doctor Plant 🌿</h1>
        <p style="
            color: rgba(255,255,255,0.85);
            margin: 0;
            font-size: 0.88rem;
            font-family: 'Nunito', sans-serif;
        ">Diagnostic IA · Propulsé par Jungle Feed</p>
    </div>
    """, unsafe_allow_html=True)


def afficher_diagnostic(diagnostic: dict):
    etat = diagnostic.get("etat", "inconnu")
    plante = diagnostic.get("plante_identifiee") or "Plante non identifiée"
    texte = diagnostic.get("diagnostic", "")
    urgence = diagnostic.get("niveau_urgence", "faible")
    conseil = diagnostic.get("conseils_immediats", "")
    problemes = diagnostic.get("problemes", [])

    if etat == "saine":
        couleur_top = "#66BB6A"
        icone = "✅"
        titre = "Plante en bonne santé !"
        badge_bg = "#E8F5E9"
        badge_fg = "#2E7D32"
        badge_label = "🌱 Plante saine"
    else:
        couleur_top = "#E53935"
        icone = "🔴"
        titre = "Problème détecté"
        badge_bg = "#FFEBEE"
        badge_fg = "#E53935"
        badge_label = "⚠️ Traitement nécessaire"

    urgence_colors = {
        "eleve": ("#FFEBEE", "#E53935"),
        "moyen": ("#FFF8E1", "#FFB300"),
        "faible": ("#E8F5E9", "#2E7D32")
    }
    urg_bg, urg_fg = urgence_colors.get(urgence, ("#E8F5E9", "#2E7D32"))

    urgence_html = ""
    if etat == "malade":
        urgence_html = f'<span style="background:{urg_bg};color:{urg_fg};padding:0.2rem 0.7rem;border-radius:20px;font-size:0.75rem;font-weight:700;margin-left:0.4rem;">Urgence {urgence}</span>'

    tags_html = ""
    if problemes and etat == "malade":
        tags = "".join([f'<span style="background:#FFF3E0;color:#FF9B3F;border-radius:10px;padding:0.2rem 0.6rem;font-size:0.78rem;font-weight:600;margin:0.2rem 0.2rem 0 0;display:inline-block;">🔍 {p}</span>' for p in problemes])
        tags_html = '<div style="margin-top:0.8rem;">' + tags + '</div>'

    conseil_html = ""
    if conseil:
        conseil_html = '<div style="background:#F1F8E9;border-radius:12px;padding:0.8rem 1rem;margin-top:1rem;"><p style="margin:0;font-size:0.85rem;color:#2E7D32;"><strong>💡 Conseil :</strong> ' + conseil + '</p></div>'

    st.markdown(
        '<div style="background:#FFFFFF;border-radius:20px;padding:1.3rem;margin:0.8rem 0;box-shadow:0 4px 20px rgba(0,0,0,0.07);border-top:4px solid ' + couleur_top + ';">'
        + '<div style="margin-bottom:0.6rem;">'
        + '<span style="background:' + badge_bg + ';color:' + badge_fg + ';padding:0.2rem 0.7rem;border-radius:20px;font-size:0.75rem;font-weight:700;">' + badge_label + '</span>'
        + urgence_html
        + '</div>'
        + '<p style="font-size:1.1rem;font-weight:800;color:#1B2F1E;margin:0 0 0.2rem 0;">' + icone + ' ' + titre + '</p>'
        + '<p style="font-size:0.8rem;color:#9E9E9E;margin:0 0 0.5rem 0;">🌿 ' + plante + '</p>'
        + '<p style="color:#6D8B74;font-size:0.9rem;line-height:1.6;margin:0;">' + texte + '</p>'
        + tags_html
        + conseil_html
        + '</div>',
        unsafe_allow_html=True
    )


def afficher_produits(recommandations: dict):
    type_reco = recommandations.get("type")
    produits = recommandations.get("produits", [])

    if type_reco == "curatif":
        titre_section = "🛒 Traitements recommandés"
        sous_titre = "Produits 100% naturels · Fabriqués en France"
    else:
        titre_section = "⭐ Entretenez cette belle santé !"
        sous_titre = "Nos produits préventifs Jungle Feed"

    st.markdown(
        '<p style="font-size:1.1rem;font-weight:800;color:#1B2F1E;margin:1.2rem 0 0.2rem 0;">' + titre_section + '</p>'
        + '<p style="color:#6D8B74;font-size:0.82rem;margin:0 0 0.8rem 0;">' + sous_titre + '</p>',
        unsafe_allow_html=True
    )

    for produit in produits:
        st.markdown(
            '<div style="background:#FFFFFF;border-radius:18px;padding:1rem 1.2rem;margin-bottom:0.8rem;box-shadow:0 2px 12px rgba(0,0,0,0.06);border:1px solid #E8F5E9;display:flex;align-items:center;gap:1rem;">'
            + '<div style="font-size:2.2rem;min-width:50px;text-align:center;">' + produit['emoji'] + '</div>'
            + '<div style="flex:1;">'
            + '<p style="font-size:0.9rem;font-weight:700;color:#1B2F1E;margin:0 0 0.2rem 0;">' + produit['nom'] + '</p>'
            + '<p style="font-size:0.78rem;color:#6D8B74;margin:0 0 0.5rem 0;">' + produit['description'] + '</p>'
            + '<a href="' + produit['url'] + '" target="_blank" style="display:inline-block;background:linear-gradient(135deg,#FF9B3F,#ffb347);color:white;padding:0.35rem 1rem;border-radius:50px;font-weight:700;font-size:0.8rem;text-decoration:none;">🛍️ Acheter</a>'
            + '</div></div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div style="background:linear-gradient(135deg,#2E7D32,#66BB6A);border-radius:20px;padding:1.3rem;text-align:center;margin-top:1rem;">'
        + '<h3 style="color:white;margin:0 0 0.3rem 0;font-size:1rem;font-weight:800;">🌿 Toute la gamme Jungle Feed</h3>'
        + '<p style="color:rgba(255,255,255,0.8);margin:0 0 0.8rem 0;font-size:0.82rem;">100% naturel · Fabriqué en France</p>'
        + '<a href="https://www.junglefeed.fr" target="_blank" style="display:inline-block;background:white;color:#2E7D32;padding:0.5rem 1.5rem;border-radius:50px;font-weight:800;font-size:0.85rem;text-decoration:none;">Visiter la boutique →</a>'
        + '</div>',
        unsafe_allow_html=True
    )
