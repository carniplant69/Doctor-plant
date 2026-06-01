import streamlit as st
import base64

COULEURS = {
    "principal": "#1A1A1A",
    "secondaire": "#333333",
    "bg": "#F5F5F5",
    "card": "#EEEEEE",
    "orange": "#FF9B3F",
    "blanc": "#FFFFFF",
    "texte_fonce": "#111111",
    "texte_gris": "#777777",
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
            background-color: #F5F5F5 !important;
        }

        #MainMenu, footer, header { visibility: hidden; }

        .block-container {
            padding-top: 0 !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 480px !important;
            margin: 0 auto !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #1A1A1A, #444444) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            padding: 0.8rem 2rem !important;
            width: 100% !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
            margin-top: 0.5rem !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 6px !important;
            background: #EEEEEE !important;
            border-radius: 16px !important;
            padding: 4px !important;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 12px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            color: #777777 !important;
        }

        .stTabs [aria-selected="true"] {
            background: #1A1A1A !important;
            color: white !important;
        }

        [data-testid="stImage"] img {
            border-radius: 16px !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
        }

        [data-testid="stCameraInputButton"] {
            font-size: 0 !important;
            background: linear-gradient(135deg, #1A1A1A, #444444) !important;
            border-radius: 50px !important;
            padding: 0.7rem !important;
            border: none !important;
            color: transparent !important;
            width: 100% !important;
            position: relative !important;
        }

        [data-testid="stCameraInputButton"]::after {
            content: "📸 Prendre la photo" !important;
            font-size: 1rem !important;
            color: white !important;
            font-weight: 700 !important;
            position: absolute !important;
            left: 50% !important;
            top: 50% !important;
            transform: translate(-50%, -50%) !important;
            font-family: 'Nunito', sans-serif !important;
            white-space: nowrap !important;
        }
    </style>
    """, unsafe_allow_html=True)


def afficher_hero(logo_base64: str = ""):
    logo_tag = ""
    if logo_base64:
        logo_tag = '<img src="data:image/png;base64,' + logo_base64 + '" style="width:80px;height:80px;border-radius:50%;border:3px solid rgba(255,255,255,0.4);box-shadow:0 4px 16px rgba(0,0,0,0.3);margin-bottom:0.8rem;object-fit:cover;">'

    st.markdown(
        '<div style="'
        'background:linear-gradient(160deg,#111111 0%,#333333 100%);'
        'border-radius:0 0 28px 28px;'
        'padding:2.5rem 1.5rem 2rem 1.5rem;'
        'text-align:center;'
        'margin:-1rem -1rem 1.5rem -1rem;'
        'box-shadow:0 8px 32px rgba(0,0,0,0.25);'
        '">'
        + logo_tag +
        '<h1 style="'
        'color:white;'
        'font-size:1.7rem;'
        'font-weight:800;'
        'margin:0 0 0.3rem 0;'
        'font-family:Nunito,sans-serif;'
        '">Doctor Plant 🌿</h1>'
        '<p style="'
        'color:rgba(255,255,255,0.7);'
        'margin:0;'
        'font-size:0.88rem;'
        'font-family:Nunito,sans-serif;'
        '">Diagnostic IA · Propulsé par Jungle Feed</p>'
        '</div>',
        unsafe_allow_html=True
    )


def afficher_diagnostic(diagnostic: dict):
    etat = diagnostic.get("etat", "inconnu")
    plante = diagnostic.get("plante_identifiee") or "Plante non identifiée"
    texte = diagnostic.get("diagnostic", "")
    urgence = diagnostic.get("niveau_urgence", "faible")
    conseil = diagnostic.get("conseils_immediats", "")
    problemes = diagnostic.get("problemes", [])

    if etat == "saine":
        couleur_top = "#4CAF50"
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
        "faible": ("#F5F5F5", "#333333")
    }
    urg_bg, urg_fg = urgence_colors.get(urgence, ("#F5F5F5", "#333333"))

    urgence_html = ""
    if etat == "malade":
        urgence_html = '<span style="background:' + urg_bg + ';color:' + urg_fg + ';padding:0.2rem 0.7rem;border-radius:20px;font-size:0.75rem;font-weight:700;margin-left:0.4rem;">Urgence ' + urgence + '</span>'

    tags_html = ""
    if problemes and etat == "malade":
        tags = "".join([
            '<span style="background:#FFF3E0;color:#FF9B3F;border-radius:10px;padding:0.2rem 0.6rem;font-size:0.78rem;font-weight:600;margin:0.2rem 0.2rem 0 0;display:inline-block;">🔍 ' + p + '</span>'
            for p in problemes
        ])
        tags_html = '<div style="margin-top:0.8rem;">' + tags + '</div>'

    conseil_html = ""
    if conseil:
        conseil_html = '<div style="background:#F5F5F5;border-radius:12px;padding:0.8rem 1rem;margin-top:1rem;border-left:3px solid #1A1A1A;"><p style="margin:0;font-size:0.85rem;color:#111111;"><strong>💡 Conseil :</strong> ' + conseil + '</p></div>'

    st.markdown(
        '<div style="background:#FFFFFF;border-radius:20px;padding:1.3rem;margin:0.8rem 0;box-shadow:0 4px 20px rgba(0,0,0,0.07);border-top:4px solid ' + couleur_top + ';">'
        + '<div style="margin-bottom:0.6rem;">'
        + '<span style="background:' + badge_bg + ';color:' + badge_fg + ';padding:0.2rem 0.7rem;border-radius:20px;font-size:0.75rem;font-weight:700;">' + badge_label + '</span>'
        + urgence_html
        + '</div>'
        + '<p style="font-size:1.1rem;font-weight:800;color:#111111;margin:0 0 0.2rem 0;">' + icone + ' ' + titre + '</p>'
        + '<p style="font-size:0.8rem;color:#999999;margin:0 0 0.5rem 0;">🌿 ' + plante + '</p>'
        + '<p style="color:#555555;font-size:0.9rem;line-height:1.6;margin:0;">' + texte + '</p>'
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
        titre_section = "⭐ Plante en pleine forme !"
        sous_titre = "Nous te proposons les meilleurs produits naturels pour ta plante"

    st.markdown(
        '<p style="font-size:1.1rem;font-weight:800;color:#111111;margin:1.2rem 0 0.2rem 0;">' + titre_section + '</p>'
        + '<p style="color:#777777;font-size:0.82rem;margin:0 0 0.8rem 0;">' + sous_titre + '</p>',
        unsafe_allow_html=True
    )

    for produit in produits:
        st.markdown(
            '<div style="background:#FFFFFF;border-radius:18px;padding:1rem 1.2rem;margin-bottom:0.8rem;box-shadow:0 2px 12px rgba(0,0,0,0.06);border:1px solid #EEEEEE;display:flex;align-items:center;gap:1rem;">'
            + '<div style="font-size:2.2rem;min-width:50px;text-align:center;">' + produit['emoji'] + '</div>'
            + '<div style="flex:1;">'
            + '<p style="font-size:0.9rem;font-weight:700;color:#111111;margin:0 0 0.2rem 0;">' + produit['nom'] + '</p>'
            + '<p style="font-size:0.78rem;color:#777777;margin:0 0 0.5rem 0;">' + produit['description'] + '</p>'
            + '<a href="' + produit['url'] + '" target="_blank" style="display:inline-block;background:linear-gradient(135deg,#FF9B3F,#ffb347);color:white;padding:0.35rem 1rem;border-radius:50px;font-weight:700;font-size:0.8rem;text-decoration:none;">🛍️ Acheter</a>'
            + '</div></div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div style="background:linear-gradient(135deg,#1A1A1A,#444444);border-radius:20px;padding:1.3rem;text-align:center;margin-top:1rem;">'
        + '<h3 style="color:white;margin:0 0 0.3rem 0;font-size:1rem;font-weight:800;">🌿 Toute la gamme Jungle Feed</h3>'
        + '<p style="color:rgba(255,255,255,0.7);margin:0 0 0.8rem 0;font-size:0.82rem;">100% naturel · Fabriqué en France</p>'
        + '<a href="https://www.junglefeed.fr" target="_blank" style="display:inline-block;background:white;color:#1A1A1A;padding:0.5rem 1.5rem;border-radius:50px;font-weight:800;font-size:0.85rem;text-decoration:none;">Visiter la boutique →</a>'
        + '</div>',
        unsafe_allow_html=True
    )
