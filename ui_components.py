import streamlit as st
import base64

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
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
        html, body, [class*="css"] {{
            font-family: 'Nunito', sans-serif;
            background-color: {COULEURS['vert_bg']};
        }}
        #MainMenu, footer, header {{visibility: hidden;}}
        .stButton > button {{
            background: linear-gradient(135deg, {COULEURS['vert_principal']}, {COULEURS['vert_clair']});
            color: white;
            border: none;
            border-radius: 50px;
            font-weight: 700;
            font-size: 1rem;
            padding: 0.7rem 2rem;
            width: 100%;
            box-shadow: 0 4px 15px rgba(46,125,50,0.3);
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: {COULEURS['vert_card']};
            border-radius: 16px;
            padding: 4px;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 12px;
            padding: 0.5rem 1.2rem;
            font-weight: 600;
            color: {COULEURS['texte_gris']};
        }}
        .stTabs [aria-selected="true"] {{
            background: {COULEURS['vert_principal']} !important;
            color: white !important;
        }}
        [data-testid="stImage"] img {{
            border-radius: 16px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }}
    </style>
    """, unsafe_allow_html=True)


def afficher_hero(logo_base64: str = ""):
    """Hero avec logo centré."""

    # Fond vert hero
    st.markdown(f"""
    <div style="
        background: linear-gradient(160deg, {COULEURS['vert_principal']} 0%, {COULEURS['vert_clair']} 100%);
        border-radius: 0 0 32px 32px;
        padding: 2rem 1.5rem 2.5rem 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(46,125,50,0.18);
    ">
    """, unsafe_allow_html=True)

    # Logo via st.image (pas HTML) pour éviter les bugs base64
    if logo_base64:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            import io, base64
            from PIL import Image
            img_bytes = base64.b64decode(logo_base64)
            img = Image.open(io.BytesIO(img_bytes))
            st.image(img, width=100)

    # Titre
    st.markdown("""
    <div style="text-align:center; margin-top:-1rem;">
        <h1 style="color:white; font-size:1.9rem; font-weight:800; margin:0;">
            Doctor Plant 🌿
        </h1>
        <p style="color:rgba(255,255,255,0.85); margin:0.3rem 0 0 0; font-size:0.95rem;">
            Diagnostic IA · Propulsé par Jungle Feed
        </p>
    </div>
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
        couleur_top = COULEURS['vert_clair']
        icone = "✅"
        titre = "Votre plante est en bonne santé !"
        badge_color = "#E8F5E9"
        badge_text_color = COULEURS['vert_principal']
        badge_label = "🌱 Plante saine"
    else:
        couleur_top = COULEURS['rouge']
        icone = "🔴"
        titre = "Problème détecté"
        badge_color = "#FFEBEE"
        badge_text_color = COULEURS['rouge']
        badge_label = "⚠️ Traitement nécessaire"

    tags_html = ""
    if problemes and etat == "malade":
        tags = "".join([
            f'<span style="background:#FFF3E0;color:{COULEURS["orange"]};border-radius:12px;padding:0.2rem 0.7rem;font-size:0.8rem;font-weight:600;margin:0.2rem 0.2rem 0 0;display:inline-block;">🔍 {p}</span>'
            for p in problemes
        ])
        tags_html = f'<div style="margin-top:0.8rem;">{tags}</div>'

    conseil_html = ""
    if conseil:
        conseil_html = f"""
        <div style="background:#F1F8E9;border-radius:12px;padding:0.8rem 1rem;margin-top:1rem;">
            <p style="margin:0;font-size:0.88rem;color:#2E7D32;">
                <strong>💡 Conseil immédiat :</strong> {conseil}
            </p>
        </div>
        """

    urgence_html = ""
    if etat == "malade":
        urgence_colors = {
            "eleve": ("#FFEBEE", COULEURS['rouge']),
            "moyen": ("#FFF8E1", COULEURS['jaune']),
            "faible": ("#E8F5E9", COULEURS['vert_principal'])
        }
        bg, fg = urgence_colors.get(urgence, ("#E8F5E9", COULEURS['vert_principal']))
        urgence_html = f'<span style="background:{bg};color:{fg};padding:0.25rem 0.8rem;border-radius:20px;font-size:0.78rem;font-weight:700;margin-left:0.5rem;">Urgence {urgence}</span>'

    st.markdown(f"""
    <div style="
        background:{COULEURS['blanc']};
        border-radius:20px;
        padding:1.5rem;
        margin:1rem 0;
        box-shadow:0 4px 20px rgba(0,0,0,0.07);
        border-top:5px solid {couleur_top};
    ">
        <span style="background:{badge_color};color:{badge_text_color};padding:0.25rem 0.8rem;border-radius:20px;font-size:0.78rem;font-weight:700;">
            {badge_label}
        </span>
        {urgence_html}
        <p style="font-size:1.2rem;font-weight:800;color:{COULEURS['texte_fonce']};margin:0.8rem 0 0.3rem 0;">
            {icone} {titre}
        </p>
        <p style="font-size:0.82rem;color:#9E9E9E;margin:0 0 0.5rem 0;">🌿 {plante}</p>
        <p style="color:{COULEURS['texte_gris']};font-size:0.95rem;line-height:1.6;margin:0;">
            {texte}
        </p>
        {tags_html}
        {conseil_html}
    </div>
    """, unsafe_allow_html=True)


def afficher_produits(recommandations: dict):
    type_reco = recommandations.get("type")
    produits = recommandations.get("produits", [])

    if type_reco == "curatif":
        st.markdown(f"""
        <p style="font-size:1.15rem;font-weight:800;color:{COULEURS['texte_fonce']};margin:1.5rem 0 0.2rem 0;">
            🛒 Traitements recommandés
        </p>
        <p style="color:{COULEURS['texte_gris']};font-size:0.85rem;margin:0 0 1rem 0;">
            Produits 100% naturels · Fabriqués en France
        </p>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <p style="font-size:1.15rem;font-weight:800;color:{COULEURS['texte_fonce']};margin:1.5rem 0 0.2rem 0;">
            ⭐ Entretenez cette belle santé !
        </p>
        <p style="color:{COULEURS['texte_gris']};font-size:0.85rem;margin:0 0 1rem 0;">
            Nos produits préventifs Jungle Feed
        </p>
        """, unsafe_allow_html=True)

    cols = st.columns(min(len(produits), 3))
    for i, produit in enumerate(produits):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="
                background:{COULEURS['blanc']};
                border-radius:18px;
                padding:1.2rem;
                box-shadow:0 2px 16px rgba(0,0,0,0.06);
                border:1px solid #E8F5E9;
                text-align:center;
                height:100%;
            ">
                <div style="font-size:2rem;margin-bottom:0.5rem;">{produit['emoji']}</div>
                <p style="font-size:0.88rem;font-weight:700;color:{COULEURS['texte_fonce']};margin:0 0 0.3rem 0;line-height:1.3;">
                    {produit['nom']}
                </p>
                <p style="font-size:0.78rem;color:{COULEURS['texte_gris']};margin:0 0 0.8rem 0;line-height:1.4;">
                    {produit['description']}
                </p>
                <a href="{produit['url']}" target="_blank" style="
                    display:block;
                    background:linear-gradient(135deg,{COULEURS['orange']},#ffb347);
                    color:white;
                    text-align:center;
                    padding:0.45rem 0.8rem;
                    border-radius:50px;
                    font-weight:700;
                    font-size:0.82rem;
                    text-decoration:none;
                    box-shadow:0 3px 10px rgba(255,155,63,0.3);
                ">🛍️ Acheter</a>
            </div>
            """, unsafe_allow_html=True)

    # Footer boutique
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,{COULEURS['vert_principal']},{COULEURS['vert_clair']});
        border-radius:20px;
        padding:1.5rem;
        text-align:center;
        margin-top:2rem;
    ">
        <h3 style="color:white;margin:0 0 0.3rem 0;font-size:1.1rem;font-weight:800;">
            🌿 Toute la gamme Jungle Feed
        </h3>
        <p style="color:rgba(255,255,255,0.8);margin:0 0 1rem 0;font-size:0.85rem;">
            100% naturel · Fabriqué en France · Livraison rapide
        </p>
        <a href="https://www.junglefeed.fr" target="_blank" style="
            display:inline-block;
            background:white;
            color:{COULEURS['vert_principal']};
            padding:0.6rem 2rem;
            border-radius:50px;
            font-weight:800;
            font-size:0.9rem;
            text-decoration:none;
        ">Visiter la boutique →</a>
    </div>
    """, unsafe_allow_html=True)
