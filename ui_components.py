# Composants UI réutilisables pour Doctor Plant

import streamlit as st

# ─── Palette Jungle Feed ───────────────────────────────────────────────
COULEURS = {
    "orange": "#FF9B3F",
    "vert_fonce": "#2D5016",
    "vert_clair": "#7CB342",
    "blanc": "#FFFFFF",
    "gris_clair": "#F5F5F5",
    "rouge_alerte": "#E53935",
    "jaune_warning": "#FFB300",
}

def inject_css():
    """Injecte le CSS global de l'application."""
    st.markdown(f"""
    <style>
        /* Police & fond général */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Poppins', sans-serif;
        }}
        
        .main {{ background-color: #FAFAFA; }}
        
        /* Header hero */
        .hero-banner {{
            background: linear-gradient(135deg, {COULEURS['vert_fonce']} 0%, {COULEURS['vert_clair']} 100%);
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .hero-banner h1 {{
            color: {COULEURS['blanc']};
            font-size: 2.2rem;
            font-weight: 700;
            margin: 0;
        }}
        
        .hero-banner p {{
            color: rgba(255,255,255,0.85);
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
        }}
        
        /* Cards produits */
        .product-card {{
            background: {COULEURS['blanc']};
            border-radius: 12px;
            padding: 1.2rem;
            border-left: 4px solid {COULEURS['orange']};
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
            transition: transform 0.2s;
        }}
        
        .product-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        }}
        
        .product-card h4 {{
            color: {COULEURS['vert_fonce']};
            margin: 0 0 0.3rem 0;
            font-size: 1rem;
            font-weight: 600;
        }}
        
        .product-card p {{
            color: #666;
            margin: 0 0 0.8rem 0;
            font-size: 0.85rem;
        }}
        
        /* Bouton CTA */
        .cta-button {{
            background: {COULEURS['orange']};
            color: white !important;
            padding: 0.5rem 1.2rem;
            border-radius: 25px;
            text-decoration: none !important;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
            transition: background 0.2s;
        }}
        
        .cta-button:hover {{
            background: #e8883a;
            color: white !important;
        }}
        
        /* Diagnostic box */
        .diagnostic-box {{
            background: {COULEURS['gris_clair']};
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid #E0E0E0;
        }}
        
        /* Badge urgence */
        .badge-eleve {{ 
            background: {COULEURS['rouge_alerte']}22; 
            color: {COULEURS['rouge_alerte']}; 
            padding: 0.2rem 0.8rem; 
            border-radius: 20px; 
            font-size: 0.8rem; 
            font-weight: 600;
        }}
        .badge-moyen {{ 
            background: {COULEURS['jaune_warning']}22; 
            color: {COULEURS['jaune_warning']}; 
            padding: 0.2rem 0.8rem; 
            border-radius: 20px; 
            font-size: 0.8rem; 
            font-weight: 600;
        }}
        .badge-faible {{ 
            background: {COULEURS['vert_clair']}22; 
            color: {COULEURS['vert_clair']}; 
            padding: 0.2rem 0.8rem; 
            border-radius: 20px; 
            font-size: 0.8rem; 
            font-weight: 600;
        }}
        
        /* Upload zone */
        .uploadedFile {{ border-radius: 12px !important; }}
        
        /* Masquer le menu Streamlit */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)


def afficher_hero():
    """Affiche le bandeau hero de l'application."""
    st.markdown("""
    <div class="hero-banner">
        <h1>🌿 Doctor Plant</h1>
        <p>Diagnostic IA pour vos plantes · Propulsé par Jungle Feed</p>
    </div>
    """, unsafe_allow_html=True)


def afficher_diagnostic(diagnostic: dict):
    """Affiche le résultat du diagnostic de manière visuelle."""
    etat = diagnostic.get("etat", "inconnu")
    plante = diagnostic.get("plante_identifiee") or "Plante"
    texte_diagnostic = diagnostic.get("diagnostic", "")
    urgence = diagnostic.get("niveau_urgence", "faible")
    conseil = diagnostic.get("conseils_immediats", "")
    problemes = diagnostic.get("problemes", [])

    # Icône & couleur selon état
    if etat == "saine":
        icone, titre, couleur_bord = "✅", "Plante en bonne santé !", COULEURS["vert_clair"]
    else:
        icone, titre, couleur_bord = "⚠️", "Problème détecté", COULEURS["rouge_alerte"]

    badge_class = f"badge-{urgence}"

    problemes_html = ""
    if problemes and etat == "malade":
        tags = " ".join([f'<span style="background:#FF9B3F22;color:#FF9B3F;padding:0.2rem 0.6rem;border-radius:12px;font-size:0.8rem;margin-right:0.3rem;">🔍 {p}</span>' for p in problemes])
        problemes_html = f'<div style="margin-top:0.8rem;">{tags}</div>'

    st.markdown(f"""
    <div class="diagnostic-box" style="border-left: 4px solid {couleur_bord};">
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.5rem;">
            <h3 style="margin:0; color:{COULEURS['vert_fonce']};">{icone} {titre}</h3>
            <span class="{badge_class}">Urgence : {urgence}</span>
        </div>
        <p style="color:#888; font-size:0.85rem; margin:0.3rem 0 0.8rem 0;">🌱 {plante}</p>
        <p style="margin:0; color:#444; line-height:1.6;">{texte_diagnostic}</p>
        {problemes_html}
        {"<hr style='margin:1rem 0; border-color:#eee;'><p style='margin:0;font-size:0.9rem;'><strong>💡 Conseil immédiat :</strong> " + conseil + "</p>" if conseil else ""}
    </div>
    """, unsafe_allow_html=True)


def afficher_produits(recommandations: dict):
    """Affiche les cartes produits avec CTA."""
    type_reco = recommandations.get("type")
    produits = recommandations.get("produits", [])

    if type_reco == "curatif":
        st.markdown(f"""
        <h3 style="color:{COULEURS['vert_fonce']}; margin-top:1.5rem;">
            🛒 Traitements recommandés par Jungle Feed
        </h3>
        <p style="color:#666; font-size:0.9rem;">Produits 100% naturels, fabriqués en France</p>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <h3 style="color:{COULEURS['vert_fonce']}; margin-top:1.5rem;">
            🌟 Entretenez cette belle santé !
        </h3>
        <p style="color:#666; font-size:0.9rem;">Nos produits préventifs pour garder vos plantes au top</p>
        """, unsafe_allow_html=True)

    cols = st.columns(min(len(produits), 3))
    for i, produit in enumerate(produits):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="product-card">
                <h4>{produit['emoji']} {produit['nom']}</h4>
                <p>{produit['description']}</p>
                <a href="{produit['url']}" target="_blank" class="cta-button">
                    🛍️ Acheter
                </a>
            </div>
            """, unsafe_allow_html=True)
