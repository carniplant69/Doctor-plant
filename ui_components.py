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
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">',
        unsafe_allow_html=True
    )
    st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Nunito', sans-serif !important;
            background-color: #F5F5F5 !important;
        }

        #MainMenu, footer, header {
            visibility: hidden;
        }

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

        .stRadio > div {
            background: #EEEEEE !important;
            border-radius: 16px !important;
            padding: 4px !important;
            gap: 6px !important;
        }

        .stRadio > div > label {
            border-radius: 12px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            color: #777777 !important;
            cursor: pointer !important;
        }

        .stRadio > div > label[data-checked="true"] {
            background: #1A1A1A !important;
            color: white !important;
        }

        [data-testid="stImage"] img {
            border-radius: 16px !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
        }

        [data-testid="stCameraInputButton"] {
            background: linear-gradient(135deg, #1A1A1A, #444444) !important;
            border-radius: 50px !important;
            border: none !important;
            color: white !important;
            font-weight: 700 !important;
            width: 100% !important;
        }

        .stTextInput > div > div > input {
            border-radius: 12px !important;
            border: 1px solid #EEEEEE !important;
            padding: 0.6rem 1rem !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #1A1A1A !important;
            box-shadow: 0 0 0 2px rgba(26,26,26,0.1) !important;
        }

        .stCheckbox > label {
            font-size: 0.85rem !important;
            color: #555555 !important;
        }

        .stAlert {
            border-radius: 12px !important;
        }

        .stLinkButton > a {
            background: linear-gradient(135deg, #FF9B3F, #ffb347) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            font-weight: 700 !important;
            padding: 0.5rem 1rem !important;
            text-decoration: none !important;
        }
    </style>
    """, unsafe_allow_html=True)


def afficher_hero(logo_base64: str = ""):
    logo_tag = ""
    if logo_base64:
        logo_tag = (
            '<img src="data:image/png;base64,' + logo_base64 + '" '
            'style="width:80px;height:80px;border-radius:50%;'
            'border:3px solid rgba(255,255,255,0.4);'
            'box-shadow:0 4px 16px rgba(0,0,0,0.3);'
            'margin-bottom:0.8rem;object-fit:cover;">'
        )

    st.markdown(
        '<div style="'
        'background:linear-gradient(160deg,#111111 0%,#333333 100%);'
        'border-radius:0 0 28px 28px;'
        'padding:2.5rem 1.5rem 2rem 1.5rem;'
        'text-align:center;'
        'margin:-1rem -1rem 1.5rem -1rem;'
        'box-shadow:0 8px 32px rgba(0,0,0,0.25);">'
        + logo_tag
        + '<h1 style="color:white;font-size:1.7rem;font-weight:800;'
        'margin:0 0 0.3rem 0;font-family:Nunito,sans-serif;">'
        'Doctor Plant 🌿</h1>'
        '<p style="color:rgba(255,255,255,0.7);margin:0;'
        'font-size:0.88rem;font-family:Nunito,sans-serif;">'
        'Diagnostic IA · Propulsé par Jungle Feed</p>'
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
        urgence_html = (
            '<span style="background:' + urg_bg + ';color:' + urg_fg + ';'
            'padding:0.2rem 0.7rem;border-radius:20px;'
            'font-size:0.75rem;font-weight:700;margin-left:0.4rem;">'
            'Urgence ' + urgence + '</span>'
        )

    tags_html = ""
    if problemes and etat == "malade":
        tags = "".join([
            '<span style="background:#FFF3E0;color:#FF9B3F;'
            'border-radius:10px;padding:0.2rem 0.6rem;'
            'font-size:0.78rem;font-weight:600;'
            'margin:0.2rem 0.2rem 0 0;display:inline-block;">'
            '🔍 ' + p + '</span>'
            for p in problemes
        ])
        tags_html = '<div style="margin-top:0.8rem;">' + tags + '</div>'

    conseil_html = ""
    if conseil:
        conseil_html = (
            '<div style="background:#F5F5F5;border-radius:12px;'
            'padding:0.8rem 1rem;margin-top:1rem;'
            'border-left:3px solid #1A1A1A;">'
            '<p style="margin:0;font-size:0.85rem;color:#111111;">'
            '<strong>Conseil :</strong> ' + conseil + '</p></div>'
        )

    st.markdown(
        '<div style="background:#FFFFFF;border-radius:20px;'
        'padding:1.3rem;margin:0.8rem 0;'
        'box-shadow:0 4px 20px rgba(0,0,0,0.07);'
        'border-top:4px solid ' + couleur_top + ';">'
        '<div style="margin-bottom:0.6rem;">'
        '<span style="background:' + badge_bg + ';color:' + badge_fg + ';'
        'padding:0.2rem 0.7rem;border-radius:20px;'
        'font-size:0.75rem;font-weight:700;">'
        + badge_label + '</span>'
        + urgence_html
        + '</div>'
        '<p style="font-size:1.1rem;font-weight:800;color:#111111;'
        'margin:0 0 0.2rem 0;">' + icone + ' ' + titre + '</p>'
        '<p style="font-size:0.8rem;color:#999999;margin:0 0 0.5rem 0;">'
        '🌿 ' + plante + '</p>'
        '<p style="color:#555555;font-size:0.9rem;line-height:1.6;margin:0;">'
        + texte + '</p>'
        + tags_html
        + conseil_html
        + '</div>',
        unsafe_allow_html=True
    )
