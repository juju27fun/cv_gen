"""
Agent de génération de lettre de motivation
"""

import sys
import aiofiles
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Import corrigé
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.openrouter_client import OpenRouterClient

class LetterGenerator:
    """Agent pour générer les lettres de motivation"""

    def __init__(self):
        self.openrouter = OpenRouterClient()

    def build_letter_context(
        self,
        offer_analysis: str,
        identity_context: Dict[str, str],
        themes: list
    ) -> str:
        """
        Construit le prompt上下文 pour la génération de la lettre

        Args:
            offer_analysis: Analyse de l'offre d'emploi
            identity_context: Données personnelles et expérience pro
            themes: Thèmes extraits de l'offre

        Returns:
            Prompt complet pour l'IA
        """
        context = f"""
CONTEXTE POUR LA LETTRE DE MOTIVATION:

=== ANALYSE DE L'OFFRE ===
{offer_analysis}

=== PROFIL DU CANDIDAT ===
**Informations Personnelles:**
{identity_context.get('personnal', 'Non disponible')}

**Expérience Professionnelle:**
{identity_context.get('xppro', 'Non disponible')}

=== THÈMES CLÉS DE L'OFFRE ===
{', '.join(themes)}

INSTRUCTIONS DE RÉDACTION:
Rédige une lettre de motivation professionnelle et personnalisée en français qui:

1. **Structure**:
   - En-tête (nom, contact, date)
   - Destinataire (à renseigner)
   - Objet: Candidature au poste [INTITULÉ]
   - Formule d'appel
   - Paragraphes de motivation (3-4 paragraphes)
   - Formule de politesse

2. **Contenu**:
   - Personalise le contenu selon l'offre analysée
   - Met en avant les expériences pertinentes pour les thèmes de l'offre
   - Démontre la compréhension de l'entreprise et du poste
   - Valorise les compétences qui répondent aux exigences
   - Ton professionnel mais chaleureux

3. **Style**:
   - 250-400 mots
   - Phrases claires et impactantes
   - Évite les clichés
   - Présent et futur (peu de passé)
   - Focus sur la valeur ajoutée

4. **Format Markdown**:
   - Utilise les balises markdown (# ## ### pour les sections)
   - Utilise **gras** pour les points clés
   - Utilise des listes à puces si nécessaire

Crée une lettre convaincante qui donne envie au recruteur de rencontrer le candidat.
"""

        return context

    async def generate_letter(
        self,
        offer_analysis: str,
        identity_context: Dict[str, str],
        themes: list,
        offer_name: str
    ) -> str:
        """
        Génère la lettre de motivation

        Args:
            offer_analysis: Analyse de l'offre
            identity_context: Contexte d'identité
            themes: Thèmes de l'offre
            offer_name: Nom de l'offre

        Returns:
            Chemin vers le fichier Markdown généré
        """
        print("  ✍️ Génération de la lettre de motivation...")

        from pathlib import Path
        BASE_DIR = Path(__file__).parent.parent.parent

        context = self.build_letter_context(offer_analysis, identity_context, themes)

        letter_content = await self.openrouter.generate_cover_letter(context)

        # Sauvegarde
        letter_path = BASE_DIR / "outputs" / f"{offer_name}_lettre.md"
        async with aiofiles.open(letter_path, 'w', encoding='utf-8') as f:
            await f.write(letter_content)

        print(f"  ✅ Lettre générée: {letter_path}")
        return str(letter_path)
