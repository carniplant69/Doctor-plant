import google.generativeai as genai
import json
import re
from catalogue import KEYWORDS_MAP, PRODUITS_CURATIFS, PRODUITS_PREVENTIFS

PROMPT_SYSTEME = """
Tu es Dr. Plant, un expert botaniste spécialisé dans les maladies des plantes et les nuisibles.
Tu travailles pour Jungle Feed, marque française de produits 100% naturels pour plantes.

INSTRUCTIONS STRICTES :
1. Analyse attentivement la photo de plante fournie.
2. Réponds UNIQUEMENT en JSON valide, sans markdown ni texte autour.
3. Structure ta réponse selon ce schéma exact :

{
  "est_une_plante": true ou false,
  "etat": "saine" ou "malade",
  "plante_identifiee": "nom de la plante si identifiable, sinon null",
  "problemes": ["liste des problèmes détectés, ex: thrips, cochenilles, etc."],
  "diagnostic": "description claire du diagnostic en 2-3 phrases maximum",
  "niveau_urgence": "faible" ou "moyen" ou "élevé",
  "conseils_immediats": "1 conseil actionnable immédiat en une phrase"
}

RÈGLES :
- Si ce n'est pas une plante : est_une_plante = false, tous les autres champs = null
- Problèmes possibles : thrips, cochenilles, araignées rouges, moucherons, pucerons, champignon, moisissure, mildiou, oïdium, carence, surrosage, manque eau, insectes
- Sois précis et bienveillant dans le diagnostic
- Langue : français uniquement
"""

def analyser_image(image_pil, api_key: str) -> dict:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        response = model.generate_content([PROMPT_SYSTEME, image_pil])

        texte = response.text.strip()
        texte = re.sub(r'```json\s*|\s*```', '', texte).strip()

        resultat = json.loads(texte)
        return {"succes": True, "data": resultat}

    except json.JSONDecodeError:
        return {
            "succes": False,
            "erreur": "Réponse IA invalide. Veuillez réessayer avec une autre photo."
        }
    except Exception as e:
        return {
            "succes": False,
            "erreur": f"Erreur d'analyse : {str(e)}"
        }


def trouver_produits(diagnostic: dict) -> dict:
    if diagnostic.get("etat") == "saine":
        return {
            "type": "preventif",
            "produits": PRODUITS_PREVENTIFS
        }

    problemes = diagnostic.get("problemes", [])
    produits_trouves = []
    ids_vus = set()

    for probleme in problemes:
        probleme_lower = probleme.lower()
        for keyword, cle_catalogue in KEYWORDS_MAP.items():
            if keyword in probleme_lower:
                produits = PRODUITS_CURATIFS.get(cle_catalogue, [])
                for p in produits:
                    uid = p["nom"]
                    if uid not in ids_vus:
                        ids_vus.add(uid)
                        produits_trouves.append(p)

    if not produits_trouves:
        produits_trouves = PRODUITS_CURATIFS.get("insectes", [])

    return {
        "type": "curatif",
        "produits": produits_trouves
    }
