import streamlit as st
import hashlib
import re
from database import create_user, get_user_by_email

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email: str) -> bool:
    return bool(re.match(r'^[^@]+@[^@]+\.[^@]+$', email))

def is_valid_password(password: str) -> bool:
    return len(password) >= 8

def afficher_auth():
    st.markdown(
        '<div style="background:white;border-radius:20px;padding:1.5rem;margin:1rem 0;box-shadow:0 2px 12px rgba(0,0,0,0.06);">'
        + '<p style="font-size:1.1rem;font-weight:800;color:#111111;margin:0 0 0.3rem 0;">👤 Mon compte</p>'
        + '<p style="font-size:0.82rem;color:#777777;margin:0 0 1rem 0;">Connecte-toi pour sauvegarder tes diagnostics</p>'
        + '</div>',
        unsafe_allow_html=True
    )

    onglet_login, onglet_register = st.tabs(["🔑 Connexion", "✨ Inscription"])

    with onglet_login:
        email = st.text_input("Email", key="login_email", placeholder="ton@email.com")
        password = st.text_input("Mot de passe", type="password", key="login_password", placeholder="••••••••")

        if st.button("Se connecter", key="btn_login", use_container_width=True):
            if not email or not password:
                st.error("Remplis tous les champs")
            else:
                result = get_user_by_email(email)
                if result["succes"]:
                    user = result["data"]
                    if not user["is_active"]:
                        st.error("Compte désactivé. Contacte le support.")
                    elif user["password_hash"] == hash_password(password):
                        st.session_state["user"] = user
                        st.session_state["user_id"] = user["id"]
                        st.session_state["show_auth"] = False
                        st.session_state["rerun"] = True
                    else:
                        st.error("Email ou mot de passe incorrect")
                else:
                    st.error("Email ou mot de passe incorrect")

    with onglet_register:
        email_r = st.text_input("Email", key="reg_email", placeholder="ton@email.com")
        password_r = st.text_input("Mot de passe", type="password", key="reg_password", placeholder="8 caractères minimum")
        password_r2 = st.text_input("Confirme le mot de passe", type="password", key="reg_password2", placeholder="••••••••")

        st.markdown(
            '<div style="background:#F5F5F5;border-radius:12px;padding:1rem;margin:0.8rem 0;">'
            + '<p style="font-size:0.78rem;color:#555555;margin:0;line-height:1.6;">'
            + '🔒 <strong>Tes données sont protégées</strong><br>'
            + 'Conformément au RGPD, tes données sont utilisées uniquement '
            + 'pour sauvegarder tes diagnostics. Tu peux demander la '
            + 'suppression de ton compte à tout moment. '
            + 'Nous ne vendons jamais tes données.'
            + '</p></div>',
            unsafe_allow_html=True
        )

        rgpd = st.checkbox("J'accepte la politique de confidentialité et le traitement de mes données personnelles")

        if st.button("Créer mon compte", key="btn_register", use_container_width=True):
            if not email_r or not password_r or not password_r2:
                st.error("Remplis tous les champs")
            elif not is_valid_email(email_r):
                st.error("Email invalide")
            elif not is_valid_password(password_r):
                st.error("Le mot de passe doit contenir au moins 8 caractères")
            elif password_r != password_r2:
                st.error("Les mots de passe ne correspondent pas")
            elif not rgpd:
                st.error("Tu dois accepter la politique de confidentialité")
            else:
                result = create_user(email_r, hash_password(password_r), True)
                if result["succes"]:
                    user = result["data"]
                    st.session_state["user"] = user
                    st.session_state["user_id"] = user["id"]
                    st.session_state["show_auth"] = False
                    st.session_state["rerun"] = True
                else:
                    if "duplicate" in result["erreur"].lower():
                        st.error("Cet email est déjà utilisé")
                    else:
                        st.error("Erreur lors de la création du compte")
