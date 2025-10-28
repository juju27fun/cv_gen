"""
Agent d'analyse d'offres d'emploi
Extrait, analyse et génère les thèmes des offres
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
import PyPDF2
import io
import aiofiles

# Import corrigé
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.openrouter_client import OpenRouterClient

class OfferAnalyzer:
    """Agent pour analyser les offres d'emploi"""

    def __init__(self):
        self.openrouter = OpenRouterClient()
        self.analysis_prompt = """
Analyse cette offre d'emploi en français et génère un rapport structuré en markdown.

Tu dois couvrir EXACTEMENT ces 8 points:

## 1. Exigences Obligatoires
Les critères non négociables (diplômes, années d'expérience, certifications, etc.)
Liste détaillée avec量化ations si présentes.

## 2. Qualifications Souhaitables
Les compétences et expériences qui constituent un atout majeur
ÀHighlighter les avantages concurrentiels.

## 3. Responsabilités et Tâches Principales
Les activités concrètes et les missions quotidiennes du poste
Organisation en bullet points avec verbes d'action.

## 4. Défis et Objectifs Stratégiques Implicites
Les problèmes que le candidat devra résoudre et les buts de l'entreprise
Analyse de la value proposition du poste.

## 5. Intitulé de Poste Exact
Le titre exact tel qu'il apparaît dans l'offre.

## 6. Compétences Techniques (Hard Skills)
Liste des compétences techniques requises
Organisation par catégorie si possible.

## 7. Compétences Comportementales (Soft Skills)
Compétences humaines et comportementales attendues
Avec contexte d'usage.

## 8. Valeurs et Culture d'Entreprise
Les valeurs et la culture d'entreprise déductibles de l'offre
Impact sur le profil recherché.

Conclus ton analyse par un résumé executive de 3-4 lignes.
"""

    async def extract_pdf_content(self, pdf_path: Path) -> str:
        """
        Extrait le contenu textuel d'un PDF

        Args:
            pdf_path: Chemin vers le fichier PDF

        Returns:
            Contenu textuel du PDF
        """
        print(f"  📄 Extraction du PDF: {pdf_path}")

        try:
            content = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    content += f"\n--- Page {page_num + 1} ---\n{text}\n"

            return content.strip()

        except Exception as e:
            raise Exception(f"Erreur extraction PDF {pdf_path}: {str(e)}")

    async def analyze_offer(self, offer_name: str, offer_path: str, output_dir: Path) -> Dict[str, str]:
        """
        Analyse complète d'une offre

        Args:
            offer_name: Nom de l'offre
            offer_path: Chemin vers l'offre (PDF)
            output_dir: Dossier de sortie pour l'analyse

        Returns:
            Dictionnaire avec analyse et thèmes
        """
        print(f"\n🔍 Analyse de l'offre: {offer_name}")

        # 1. Extraction du PDF
        pdf_path = Path(offer_path)
        if not pdf_path.exists():
            raise Exception(f"Fichier non trouvé: {pdf_path}")

        pdf_content = await self.extract_pdf_content(pdf_path)

        # 2. Analyse avec IA
        print("  🤖 Analyse par IA...")
        analysis = await self.openrouter.analyze_offer(pdf_content, self.analysis_prompt)

        # 3. Extraction des thèmes
        print("  🎯 Extraction des thèmes...")
        themes_list = await self.openrouter.generate_themes(analysis)

        # 4. Sauvegarde de l'analyse
        output_file = output_dir / f"{offer_name}.md"
        async with aiofiles.open(output_file, 'w', encoding='utf-8') as f:
            await f.write(analysis)

        print(f"  💾 Analyse sauvegardée: {output_file}")
        print(f"  📊 {len(themes_list)} thème(s) extrait(s)")

        return {
            'analysis': analysis,
            'themes': themes_list,
            'output_file': str(output_file)
        }

    async def batch_analyze(self, offers: Dict[str, tuple], output_dir: Path) -> Dict[str, Dict]:
        """
        Analyse plusieurs offres en lot

        Args:
            offers: Dictionnaire {nom: (path, bool)}
            output_dir: Dossier de sortie

        Returns:
            Résultats d'analyse par offre
        """
        results = {}

        for offer_name, (offer_path, is_processed) in offers.items():
            if is_processed:
                continue

            try:
                result = await self.analyze_offer(offer_name, offer_path, output_dir)
                results[offer_name] = result
                print(f"✅ Analyse terminée: {offer_name}")

            except Exception as e:
                print(f"❌ Erreur analyse {offer_name}: {str(e)}")
                results[offer_name] = {'error': str(e)}

        return results
