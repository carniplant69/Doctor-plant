from supabase import create_client
import streamlit as st

def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def create_user(email: str, password_hash: str, rgpd: bool) -> dict:
    sb = get_supabase()
    try:
        res = sb.table("users").insert({
            "email": email,
            "password_hash": password_hash,
            "rgpd_consent": rgpd,
            "rgpd_consent_date": "NOW()"
        }).execute()
        return {"succes": True, "data": res.data[0]}
    except Exception as e:
        return {"succes": False, "erreur": str(e)}

def get_user_by_email(email: str) -> dict:
    sb = get_supabase()
    try:
        res = sb.table("users").select("*").eq("email", email).execute()
        if res.data:
            return {"succes": True, "data": res.data[0]}
        return {"succes": False, "erreur": "Utilisateur non trouvé"}
    except Exception as e:
        return {"succes": False, "erreur": str(e)}

def save_diagnostic(user_id: str, diagnostic: dict) -> str:
    sb = get_supabase()
    try:
        res = sb.table("diagnostics").insert({
            "user_id": user_id,
            "plante_identifiee": diagnostic.get("plante_identifiee"),
            "etat": diagnostic.get("etat"),
            "problemes": diagnostic.get("problemes", []),
            "niveau_urgence": diagnostic.get("niveau_urgence"),
            "diagnostic_texte": diagnostic.get("diagnostic")
        }).execute()
        return res.data[0]["id"]
    except Exception:
        return None

def save_product_click(user_id: str, product_nom: str, product_url: str, diagnostic_id: str = None):
    sb = get_supabase()
    try:
        sb.table("product_clicks").insert({
            "user_id": user_id,
            "product_nom": product_nom,
            "product_url": product_url,
            "diagnostic_id": diagnostic_id
        }).execute()
    except Exception:
        pass

def get_all_users():
    sb = get_supabase()
    try:
        res = sb.table("users").select("id, email, created_at, is_active, is_admin, rgpd_consent").order("created_at", desc=True).execute()
        return res.data
    except Exception:
        return []

def toggle_user_active(user_id: str, is_active: bool):
    sb = get_supabase()
    sb.table("users").update({"is_active": is_active}).eq("id", user_id).execute()

def delete_user(user_id: str):
    sb = get_supabase()
    sb.table("users").delete().eq("id", user_id).execute()

def get_stats():
    sb = get_supabase()
    try:
        total_users = sb.table("users").select("id", count="exact").execute().count
        total_diagnostics = sb.table("diagnostics").select("id", count="exact").execute().count
        total_clicks = sb.table("product_clicks").select("id", count="exact").execute().count
        malades = sb.table("diagnostics").select("id", count="exact").eq("etat", "malade").execute().count
        saines = sb.table("diagnostics").select("id", count="exact").eq("etat", "saine").execute().count
        top_produits = sb.table("product_clicks").select("product_nom").execute().data
        return {
            "total_users": total_users or 0,
            "total_diagnostics": total_diagnostics or 0,
            "total_clicks": total_clicks or 0,
            "malades": malades or 0,
            "saines": saines or 0,
            "top_produits": top_produits or []
        }
    except Exception:
        return {}

def get_recent_diagnostics(limit: int = 20):
    sb = get_supabase()
    try:
        res = sb.table("diagnostics").select("*, users(email)").order("created_at", desc=True).limit(limit).execute()
        return res.data
    except Exception:
        return []
