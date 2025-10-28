"""
Agent de génération de CV
Génère le JSON Reactive Resume puis le PDF
Implémente les bonnes pratiques du PDF_GENERATION_GUIDE.md
"""

import json
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Import pour async file operations
try:
    import aiofiles
except ImportError:
    aiofiles = None
    logger.warning("aiofiles non disponible, certaines fonctionnalités seront limitées")

# Import corrigé
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.openrouter_client import OpenRouterClient
from utils.reactive_resume_client import ReactiveResumeClient, ReactiveResumeError
from config.settings import settings, validate_config

# Configuration du logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CVGenerator:
    """Agent pour générer les CV au format Reactive Resume"""

    def __init__(self):
        """Initialise le générateur de CV"""
        self.openrouter = OpenRouterClient()
        self.reactive_client = ReactiveResumeClient(
            timeout=settings.reactive_resume_timeout,
            max_retries=settings.reactive_resume_max_retries
        )

        # Validation de la configuration
        try:
            validate_config()
        except ValueError as e:
            logger.error(f"Configuration invalide: {e}")
            raise

    def build_cv_context(
        self,
        offer_analysis: str,
        identity_context: Dict[str, str],
        education_context: Dict[str, str],
        themes: list
    ) -> str:
        """
        Construit le prompt上下文 pour la génération du CV

        Args:
            offer_analysis: Analyse de l'offre d'emploi
            identity_context: Données personnelles et expérience pro
            education_context: Données d'éducation par thème
            themes: Thèmes extraits de l'offre

        Returns:
            Prompt complet pour l'IA
        """
        # Filtrer l'éducation selon les thèmes
        relevant_education = []
        for theme in themes:
            for key, content in education_context.items():
                if theme.lower() in key.lower() or theme.lower() in content.lower():
                    relevant_education.append(f"**{key}**: {content[:200]}...")

        education_text = "\n".join(relevant_education) if relevant_education else "Aucune éducation spécifique trouvée pour ces thèmes."

        context = f"""
CONTEXTE COMPLET POUR GÉNÉRATION CV:

=== ANALYSE DE L'OFFRE ===
{offer_analysis}

=== IDENTITÉ DU CANDIDAT ===
**Profil Personnel:**
{identity_context.get('personnal', 'Non disponible')}

**Expérience Professionnelle:**
{identity_context.get('xppro', 'Non disponible')}

=== ÉDUCATION PERTINENTE ===
{education_text}

=== THÈMES DE L'OFFRE ===
{', '.join(themes)}

INSTRUCTIONS:
Tu dois générer un CV JSON au format Reactive Resume qui MET EN VALEUR les expériences et compétences correspondent aux thèmes de l'offre.

1. Utilise UNIQUEMENT les informations du contexte ci-dessus
2. Adapte le contenu pour répondre aux exigences de l'offre
3. Respecte EXACTEMENT la structure JSON du guide Reactive Resume
4. Génère un UUID unique pour chaque item (utilise uuid.uuid4())
5. Utilise du HTML pour le summary et les descriptions (<p>, <ul>, <li>)
6. Assure-toi que le CV soit ATS-friendly

Structure JSON attendue:
{{
  "basics": {{ ... }},
  "sections": {{
    "summary": {{ ... }},
    "experience": {{ "items": [{{ ... }}] }},
    "education": {{ "items": [{{ ... }}] }},
    "skills": {{ "items": [{{ ... }}] }},
    "projects": {{ "items": [{{ ... }}] }},
    "languages": {{ "items": [{{ ... }}] }},
    "certifications": {{ "items": [{{ ... }}] }},
    "profiles": {{ "items": [{{ ... }}] }},
    "awards": {{ "items": [{{ ... }}] }},
    "volunteer": {{ "items": [{{ ... }}] }},
    "publications": {{ "items": [{{ ... }}] }},
    "references": {{ "visible": false, "items": [] }},
    "interests": {{ "items": [{{ ... }}] }},
    "custom": {{}}
  }},
  "metadata": {{
    "template": "pikachu",
    "layout": [...],
    "theme": {{ ... }},
    "typography": {{ ... }}
  }}
}}

Réponds UNIQUEMENT avec le JSON valide, sans aucun texte avant ou après.
"""

        return context

    async def generate_cv_json(
        self,
        offer_analysis: str,
        identity_context: Dict[str, str],
        education_context: Dict[str, str],
        themes: list
    ) -> Dict[str, Any]:
        """
        Génère le CV au format JSON

        Returns:
            Dictionnaire JSON du CV
        """
        print("  📝 Génération du CV par IA...")

        context = self.build_cv_context(
            offer_analysis, identity_context, education_context, themes
        )

        cv_json = await self.openrouter.generate_cv_json(context)

        print("  ✅ CV JSON généré avec succès")

        # Sauvegarde optionnelle du JSON pour debug
        from pathlib import Path
        BASE_DIR = Path(__file__).parent.parent.parent
        json_output = BASE_DIR / "outputs" / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_cv_debug.json"
        async with aiofiles.open(json_output, 'w') as f:
            await f.write(json.dumps(cv_json, indent=2, ensure_ascii=False))

        return cv_json

    async def send_to_reactive_resume(self, cv_json: Dict[str, Any], offer_name: str) -> str:
        """
        Envoie le CV JSON à Reactive Resume et récupère le PDF
        Utilise le flux correct : POST /api/resume → GET /api/resume/print/{id}

        Args:
            cv_json: CV au format JSON
            offer_name: Nom de l'offre

        Returns:
            Chemin vers le PDF généré (ou JSON si PDF échoue)

        Raises:
            Exception: Si la génération échoue définitivement
        """
        from pathlib import Path
        BASE_DIR = Path(__file__).parent.parent.parent

        print("  📤 Envoi à Reactive Resume...")

        # Construire le chemin de sortie
        output_path = BASE_DIR / "outputs" / f"{offer_name}_cv.pdf"

        try:
            # Utiliser le nouveau client avec retry et gestion d'erreurs
            result_path = await self.reactive_client.create_and_generate_pdf(cv_json, output_path)

            print(f"  ✅ PDF généré: {result_path}")
            return str(result_path)

        except ReactiveResumeError as e:
            logger.error(f"Erreur Reactive Resume: {e}")
            print(f"  ⚠️ Reactive Resume non disponible: {str(e)}")
            print(f"  💾 Sauvegarde du JSON à la place")

            # Fallback: sauvegarde du JSON
            json_path = BASE_DIR / "outputs" / f"{offer_name}_cv.json"

            try:
                import aiofiles
                async with aiofiles.open(json_path, 'w', encoding='utf-8') as f:
                    await f.write(json.dumps(cv_json, indent=2, ensure_ascii=False))
            except ImportError:
                # Fallback synchrone si aiofiles n'est pas disponible
                json_path.parent.mkdir(parents=True, exist_ok=True)
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(cv_json, f, indent=2, ensure_ascii=False)

            print(f"  ✅ JSON sauvegardé: {json_path}")
            return str(json_path)

        except Exception as e:
            logger.error(f"Erreur inattendue: {str(e)}", exc_info=True)
            print(f"  ❌ Erreur inattendue: {str(e)}")
            raise

    async def check_reactive_resume_health(self) -> bool:
        """
        Vérifie que Reactive Resume est accessible

        Returns:
            True si accessible, False sinon
        """
        print("  🔍 Vérification de Reactive Resume...")
        try:
            is_healthy = await self.reactive_client.check_health()
            if is_healthy:
                print("  ✅ Reactive Resume est accessible")
            else:
                print("  ⚠️ Reactive Resume ne répond pas correctement")
            return is_healthy
        except Exception as e:
            logger.error(f"Erreur lors du health check: {e}")
            print(f"  ❌ Erreur lors de la vérification: {str(e)}")
            return False
