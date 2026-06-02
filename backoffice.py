import streamlit as st
from database import get_all_users, toggle_user_active, delete_user, get_stats, get_recent_diagnostics
from collections import Counter

def afficher_backoffice():
    st.markdown("""
    <div style="
        background:linear-gradient(160deg,#111111 0%,#333333 100%);
        border-radius:0 0 28px 28px;
        padding:2rem 1.5rem;
        text-align:center;
        margin:-1rem -1rem 1.5rem -1rem;
        box-shadow:0 8px 32px rgba(0,0,0,0.25);
    ">
        <h1 style="color:white;font-size:1.5rem;font-weight:800;margin:0 0 0.3rem 0;">
            ⚙️ Backoffice Doctor Plant
        </h1>
        <p style="color:rgba(255,255,255,0.7);margin:0;font-size:0.85rem;">
            Jungle Feed · Administration
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Stats globales
    stats = get_stats()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div style="background:white;border-radius:16px;padding:1rem;text-align:center;box-shadow:0 2px 12px rgba(0,0,0,0.06);">'
            + '<p style="font-size:1.8rem;font-weight:800;color:#111111;margin:0;">' + str(stats.get("total_users", 0)) + '</p>'
            + '<p style="font-size:0.75rem;color:#777777;margin:0;">Utilisateurs</p>'
            + '</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div style="background:white;border-radius:16px;padding:1rem;text-align:center;box-shadow:0 2px 12px rgba(0,0,0,0.06);">'
            + '<p style="font-size:1.8rem;font-weight:800;color:#111111;margin:0;">' + str(stats.get("total_diagnostics", 0)) + '</p>'
            + '<p style="font-size:0.75rem;color:#777777;margin:0;">Diagnostics</p>'
            + '</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div style="background:white;border-radius:16px;padding:1rem;text-align:center;box-shadow:0 2px 12px rgba(0,0,0,0.06);">'
            + '<p style="font-size:1.8rem;font-weight:800;color:#4CAF50;margin:0;">' + str(stats.get("saines", 0)) + '</p>'
            + '<p style="font-size:0.75rem;color:#777777;margin:0;">Plantes saines</p>'
            + '</div>',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            '<div style="background:white;border-radius:16px;padding:1rem;text-align:center;box-shadow:0 2px 12px rgba(0,0,0,0.06);">'
            + '<p style="font-size:1.8rem;font-weight:800;color:#E53935;margin:0;">' + str(stats.get("malades", 0)) + '</p>'
            + '<p style="font-size:0.75rem;color:#777777;margin:0;">Plantes malades</p>'
            + '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Top produits cliqués
    st.markdown(
        '<p style="font-size:1rem;font-weight:800;color:#111111;margin:1rem 0 0.5rem 0;">🛍️ Produits les plus cliqués</p>',
        unsafe_allow_html=True
    )

    top_produits = stats.get("top_produits", [])
    if top_produits:
        counter = Counter([p["product_nom"] for p in top_produits])
        for produit, nb in counter.most_common(10):
            pct = int((nb / len(top_produits)) * 100)
            st.markdown(
                '<div style="background:white;border-radius:12px;padding:0.8rem 1rem;margin-bottom:0.5rem;box-shadow:0 1px 8px rgba(0,0,0,0.05);">'
                + '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">'
                + '<p style="margin:0;font-size:0.88rem;font-weight:700;color:#111111;">' + produit + '</p>'
                + '<span style="background:#F5F5F5;color:#333333;padding:0.15rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:700;">' + str(nb) + ' clics</span>'
                + '</div>'
                + '<div style="background:#EEEEEE;border-radius:10px;height:6px;">'
                + '<div style="background:linear-gradient(135deg,#FF9B3F,#ffb347);width:' + str(pct) + '%;height:6px;border-radius:10px;"></div>'
                + '</div>'
                + '</div>',
                unsafe_allow_html=True
            )
    else:
        st.info("Aucun clic produit enregistré pour l'instant")

    # Diagnostics récents
    st.markdown(
        '<p style="font-size:1rem;font-weight:800;color:#111111;margin:1.5rem 0 0.5rem 0;">🔍 Diagnostics récents</p>',
        unsafe_allow_html=True
    )

    diagnostics = get_recent_diagnostics(20)
    if diagnostics:
        for d in diagnostics:
            email_user = d.get("users", {}).get("email", "Anonyme") if d.get("users") else "Anonyme"
            etat = d.get("etat", "")
            couleur = "#4CAF50" if etat == "saine" else "#E53935"
            badge = "✅ Saine" if etat == "saine" else "🔴 Malade"
            plante = d.get("plante_identifiee") or "Non identifiée"
            date = str(d.get("created_at", ""))[:10]

            st.markdown(
                '<div style="background:white;border-radius:12px;padding:0.8rem 1rem;margin-bottom:0.5rem;box-shadow:0 1px 8px rgba(0,0,0,0.05);border-left:3px solid ' + couleur + ';">'
                + '<div style="display:flex;justify-content:space-between;align-items:center;">'
                + '<div>'
                + '<p style="margin:0;font-size:0.85rem;font-weight:700;color:#111111;">🌿 ' + plante + '</p>'
                + '<p style="margin:0;font-size:0.75rem;color:#777777;">👤 ' + email_user + ' · 📅 ' + date + '</p>'
                + '</div>'
                + '<span style="background:' + couleur + '22;color:' + couleur + ';padding:0.2rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:700;">' + badge + '</span>'
                + '</div>'
                + '</div>',
                unsafe_allow_html=True
            )
    else:
        st.info("Aucun diagnostic pour l'instant")

    # Gestion utilisateurs
    st.markdown(
        '<p style="font-size:1rem;font-weight:800;color:#111111;margin:1.5rem 0 0.5rem 0;">👥 Gestion des utilisateurs</p>',
        unsafe_allow_html=True
    )

    users = get_all_users()
    if users:
        for user in users:
            col_info, col_actions = st.columns([3, 1])

            with col_info:
                statut = "✅ Actif" if user["is_active"] else "🚫 Bloqué"
                admin = " · 👑 Admin" if user.get("is_admin") else ""
                rgpd = " · 🔒 RGPD ok" if user.get("rgpd_consent") else " · ⚠️ RGPD non accepté"
                date = str(user.get("created_at", ""))[:10]

                st.markdown(
                    '<div style="background:white;border-radius:12px;padding:0.8rem 1rem;box-shadow:0 1px 8px rgba(0,0,0,0.05);">'
                    + '<p style="margin:0;font-size:0.85rem;font-weight:700;color:#111111;">📧 ' + user["email"] + '</p>'
                    + '<p style="margin:0;font-size:0.75rem;color:#777777;">' + statut + admin + rgpd + ' · 📅 ' + date + '</p>'
                    + '</div>',
                    unsafe_allow_html=True
                )

            with col_actions:
                if user["is_active"]:
                    if st.button("🚫", key="block_" + user["id"], help="Bloquer"):
                        toggle_user_active(user["id"], False)
                        st.rerun()
                else:
                    if st.button("✅", key="unblock_" + user["id"], help="Activer"):
                        toggle_user_active(user["id"], True)
                        st.rerun()

                if st.button("🗑️", key="del_" + user["id"], help="Supprimer"):
                    delete_user(user["id"])
                    st.rerun()

            st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
    else:
        st.info("Aucun utilisateur inscrit pour l'instant")

    # Déconnexion admin
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    if st.button("🚪 Déconnexion", use_container_width=True):
        st.session_state.clear()
        st.rerun()
