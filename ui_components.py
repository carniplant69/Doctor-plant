import streamlit as st
import base64
from pathlib import Path

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
    """Convertit le logo en base64 pour l'affichage HTML."""
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

        /* Cache menu Streamlit */
        #MainMenu, footer, header {{visibility: hidden;}}

        /* Hero header */
        .hero {{
            background: linear-gradient(160deg, {COULEURS['vert_principal']} 0%, {COULEURS['vert_clair']} 100%);
            border-radius: 0 0 32px 32px;
            padding: 2rem 1.5rem 2.5rem 1.5rem;
            text-align: center;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 32px rgba(46,125,50,0.18);
        }}

        .hero-logo {{
            width: 90px;
            height: 90px;
            border-radius: 50%;
            border: 3px solid rgba(255,255,255,0.4);
            margin-bottom: 0.8rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }}

        .hero h1 {{
            color: white;
            font-size: 1.9rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.5px;
        }}

        .hero p {{
            color: rgba(255,255,255,0.85);
            margin: 0.3rem 0 0 0;
            font-size: 0.95rem;
        }}

        /* Tabs style */
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

        /* Upload zone */
        [data-testid="stFileUploader"] {{
            background: {COULEURS['blanc']};
            border: 2px dashed {COULEURS['vert_clair']};
            border-radius: 20px;
            padding: 1.5rem;
        }}

        /* Bouton principal */
        .stButton > button {{
            background: linear-gradient(135deg, {COULEURS['vert_principal']}, {COULEURS['vert_clair']});
            color: white;
            border: none;
            border-radius: 50px;
            font-weight: 700;
            font-size: 1rem;
            padding: 0.7rem 2rem;
            width: 100%;
            transition: all 0.2s;
            box-shadow: 0 4px 15px rgba(46,125,50,0.3);
        }}

        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(46,125,50,0.4);
        }}

        /* Card diagnostic */
        .diag-card {{
            background: {COULEURS['blanc']};
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.07);
        }}

        .diag-saine {{
            border-top: 5px solid {COULEURS['vert_clair']};
        }}

        .diag-malade {{
            border-top: 5px solid {COULEURS['rouge']};
        }}

        .diag-title {{
            font-size: 1.2rem;
            font-weight: 800;
            color: {COULEURS['texte_fonce']};
            margin: 0 0 0.5rem 0;
        }}

        .diag-text {{
            color: {COULEURS['texte_gris']};
            font-size: 0.95rem;
            line-height: 1.6;
            margin: 0;
        }}

        .badge {{
            display: inline-block;
            padding: 0.25rem 0.8rem;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }}

        .badge-saine {{
            background: #E8F5E9;
            color: {COULEURS['vert_principal']};
        }}

        .badge-malade {{
            background: #FFEBEE;
            color: {COULEURS['rouge']};
        }}

        .badge-urgence-eleve {{
            background: #FFEBEE;
            color: {COULEURS['rouge']};
        }}

        .badge-urgence-moyen {{
            background: #FFF8E1;
            color: {COULEURS['jaune']};
        }}

        .badge-urgence-faible {{
            background: #E8F5E9;
            color: {COULEURS['vert_principal']};
        }}

        /* Tags problèmes */
        .tag-probleme {{
            display: inline-block;
            background: #FFF3E0;
            color: {COULEURS['orange']};
            border-radius: 12px;
            padding: 0.2rem 0.7rem;
            font-size: 0.8rem;
            font-weight: 600;
            margin: 0.2rem 0.2rem 0 0;
        }}

        /* Section produits */
        .section-title {{
            font-size: 1.15rem;
            font-weight: 800;
            color: {COULEURS['texte_fonce']};
            margin: 1.5rem 0 0.3rem 0;
        }}

        .section-subtitle {{
            color: {COULEURS['texte_gris']};
            font-size: 0.85rem;
            margin: 0 0 1rem 0;
        }}

        /* Card produit */
        .product-card {{
            background: {COULEURS['blanc']};
            border-radius: 18px;
            padding: 1.2rem;
            box-shadow: 0 2px 16px rgba(0,0,0,0.06);
            height: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid #E8F5E9;
        }}

        .product-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(46,125,50,0.12);
        }}

        .product-emoji {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}

        .product-name {{
            font-size: 0.92rem;
            font-weight: 700;
            color: {COULEURS['texte_fonce']};
            margin: 0 0 0.3rem 0;
            line-height: 1.3;
        }}

        .product-desc {{
            font-size: 0.8rem;
            color: {COULEURS['texte_gris']};
            margin: 0 0 0.8rem 0;
            line-height: 1.4;
        }}

        .btn-acheter {{
            display: block;
            background: linear-gradient(135deg, {COULEURS['orange']}, #ffb347);
            color: white !important;
            text-align: center;
            padding: 0.45rem 0.8rem;
            border-radius: 50px;
            font-weight: 700;
            font-size: 0.82rem;
            text-decoration: none !important;
            box-shadow: 0 3px 10px rgba(255,155,63,0.3);
            transition: all 0.2s;
        }}

        .btn-acheter:hover {{
            transform: translateY(-1px);
            box-shadow: 0 5px 15px rgba(255,155,63,0.4);
        }}

        /* Footer boutique */
        .footer-cta {{
            background: linear-gradient(135deg, {COULEURS['vert_principal']}, {COULEURS['vert_clair']});
            border-radius: 20px;
            padding: 1.5rem;
            text-align: center;
            margin-top: 2rem;
        }}

        .footer-cta h3 {{
            color: white;
            margin: 0 0 0.3rem 0;
            font-size: 1.1rem;
            font-weight: 800;
        }}

        .footer-cta p {{
            color: rgba(255,255,255,0.8);
            margin: 0 0 1rem 0;
            font-size: 0.85rem;
        }}

        .btn-boutique {{
            display: inline-block;
            background: white;
            color: {COULEURS['vert_principal']} !important;
            padding: 0.6rem 2rem;
            border-radius: 50px;
            font-weight: 800;
            font-size: 0.9rem;
            text-decoration: none !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}

        /* Zone vide */
        .empty-state {{
            text-align: center;
            padding: 2.5rem 1rem;
            background: {COULEURS['blanc']};
            border-radius: 20px;
            margin-top: 1rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        }}

        .empty-state .big-emoji {{
            font-size: 3.5rem;
            margin-bottom: 0.8rem;
        }}

        .empty-state p {{
            color: {COULEURS['texte_gris']};
            margin: 0;
            font-size: 0.95rem;
            line-height: 1.6;
        }}

        /* Image preview arrondie */
        [data-testid="stImage"] img {{
            border-radius: 16px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }}

    </style>
    """, unsafe_allow_html=True)


def afficher_hero(logo_base64: str = ""):
    """Affiche le hero avec logo."""
    logo_html = ""
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="hero-logo"><br>'

    st.markdown(f"""
    <div class="hero">
        {logo_html}
        <h1>Doctor Plant 🌿</h1>
        <p>Diagnostic IA · Propulsé par Jungle Feed</p>
    </div>
    """, unsafe_allow_html=True)


def afficher_diagnostic(diagnostic: dict):
    """Affiche le diagnostic de façon moderne."""
    etat = diagnostic.get("etat", "inconnu")
    plante = diagnostic.get("plante_identifiee") or "Plante non identifiée"
    texte = diagnostic.get("diagnostic", "")
    urgence = diagnostic.get("niveau_urgence", "faible")
    conseil = diagnostic.get("conseils_immediats", "")
    problemes = diagnostic.get("problemes", [])

    if etat == "saine":
        icone = "✅"
        titre = "Votre plante est en bonne santé !"
        classe_card = "diag-saine"
        classe_badge = "badge-saine"
        texte_badge = "🌱 Plante saine"
    else:
        icone = "🔴"
        titre = "Problème détecté"
        classe_card = "diag-malade"
        classe_badge = "badge-malade"
        texte_badge = "⚠️ Traitement nécessaire"

    tags_html = ""
    if problemes and etat == "malade":
        tags_html = "<div style='margin-top:0.8rem;'>" + "".join(
            [f'<span class="tag-probleme">🔍 {p}</span>' for p in problemes]
        ) + "</div>"

    conseil_html = ""
    if conseil:
        conseil_html = f"""
        <div style="background:#F1F8E9; border-radius:12px; padding:0.8rem 1rem; margin-top:1rem;">
            <p style="margin:0; font-size:0.88rem; color:#2E7D32;">
                <strong>💡 Conseil immédiat :</strong> {conseil}
            </p>
        </div>
        """

    urgence_badge = f'<span class="badge badge-urgence-{urgence}" style="margin-left:0.5rem;">Urgence {urgence}</span>' if etat == "malade" else ""

    st.markdown(f"""
    <div class="diag-card {classe_card}">
        <span class="badge {classe_badge}">{texte_badge}</span>
        {urgence_badge}
        <p class="diag-title">{icone} {titre}</p>
        <p style="font-size:0.82rem; color:#9E9E9E; margin:0 0 0.5rem 0;">🌿 {plante}</p>
        <p class="diag-text">{texte}</p>
        {tags_html}
        {conseil_html}
    </div>
    """, unsafe_allow_html=True)


def afficher_produits(recommandations: dict):
    """Affiche les cartes produits."""
    type_reco = recommandations.get("type")
    produits = recommandations.get("produits", [])

    if type_reco == "curatif":
        st.markdown("""
        <p class="section-title">🛒 Traitements recommandés</p>
        <p class="section-subtitle">Produits 100% naturels · Fabriqués en France · Jungle Feed</p>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <p class="section-title">⭐ Entretenez cette belle santé !</p>
        <p class="section-subtitle">Nos produits préventifs pour des plantes toujours au top</p>
        """, unsafe_allow_html=True)

    cols = st.columns(min(len(produits), 3))
    for i, produit in enumerate(produits):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="product-card">
                <div class="product-emoji">{produit['emoji']}</div>
                <p class="product-name">{produit['nom']}</p>
                <p class="product-desc">{produit['description']}</p>
                <a href="{produit['url']}" target="_blank" class="btn-acheter">
                    🛍️ Acheter
                </a>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer-cta">
        <h3>🌿 Toute la gamme Jungle Feed</h3>
        <p>100% naturel · Fabriqué en France · Livraison rapide</p>
        <a href="https://www.junglefeed.fr" target="_blank" class="btn-boutique">
            Visiter la boutique →
        </a>
    </div>
    """, unsafe_allow_html=True)
