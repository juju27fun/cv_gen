#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrateur Principal - Génération CV & Lettre de Motivation
Traite les offres d'emploi et génère automatiquement CV PDF et Lettre MD
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import asyncio
import aiofiles

# Configuration UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# Configuration des chemins
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from agents.offer_analyzer import OfferAnalyzer
from agents.cv_generator import CVGenerator
from agents.letter_generator import LetterGenerator
from config.settings import settings

# Constants - Utilisation de la configuration centralisée
OFFRES_FILE = BASE_DIR / settings.offres_file
OUTPUTS_DIR = BASE_DIR / settings.outputs_dir
ANALYSIS_DIR = BASE_DIR / settings.analysis_dir
DATA_DIR = BASE_DIR / settings.data_dir

class CVGeneratorOrchestrator:
    """Orchestrateur principal pour la génération de CV et lettres de motivation"""

    def __init__(self):
        self.offers_data = {}
        self.offer_analysis_results = {}
        self.identity_context = {}
        self.education_context = {}

        # Initialisation des agents
        self.offer_analyzer = OfferAnalyzer()
        self.cv_generator = CVGenerator()
        self.letter_generator = LetterGenerator()

    async def load_offers(self) -> Dict:
        """Charge les offres depuis offres.json"""
        print("📂 Chargement des offres...")
        async with aiofiles.open(OFFRES_FILE, 'r') as f:
            content = await f.read()
            return json.loads(content)

    async def load_identity_data(self):
        """Charge les données d'identité"""
        print("👤 Chargement des données d'identité...")
        identity_files = {
            'personnal': DATA_DIR / "identity" / "personnal.md",
            'xppro': DATA_DIR / "identity" / "xppro.md"
        }

        for key, file_path in identity_files.items():
            if file_path.exists():
                async with aiofiles.open(file_path, 'r') as f:
                    self.identity_context[key] = await f.read()
            else:
                print(f"  ⚠️ Fichier non trouvé: {file_path}")

    async def load_education_data(self):
        """Charge les données d'éducation"""
        print("🎓 Chargement des données d'éducation...")
        # Parcourir bio/ et info/
        for subdir in ['bio', 'info']:
            dir_path = DATA_DIR / "education" / subdir
            if dir_path.exists():
                for file_path in dir_path.glob('*.md'):
                    async with aiofiles.open(file_path, 'r') as f:
                        content = await f.read()
                        self.education_context[f"{subdir}/{file_path.stem}"] = content

    async def process_offer(self, offer_name: str, offer_path: str) -> bool:
        """
        Traite une offre complète : analyse + génération CV + lettre

        Returns:
            True si succès, False sinon
        """
        print(f"\n{'='*60}")
        print(f"🎯 Traitement de l'offre: {offer_name}")
        print(f"{'='*60}")

        try:
            # 1. Extraction et analyse de l'offre
            analysis_result = await self.analyze_offer(offer_name, offer_path)
            offer_analysis = analysis_result['analysis']
            themes = analysis_result['themes']

            # 2. Génération du CV (JSON + PDF)
            cv_json = await self.generate_cv_json(offer_name, offer_analysis, themes)
            cv_path = await self.send_to_reactive_resume(cv_json, offer_name)

            # 3. Génération de la lettre de motivation
            letter_path = await self.generate_cover_letter(offer_name, offer_analysis, themes)

            print(f"\n✅ Offre {offer_name} traitée!")
            print(f"   📄 CV: {cv_path}")
            print(f"   📝 Lettre: {letter_path}")

            return True

        except Exception as e:
            print(f"\n❌ Erreur lors du traitement de {offer_name}: {str(e)}")
            # Import manquant dans certains contextes
            try:
                import traceback
                traceback.print_exc()
            except:
                pass
            return False

    async def analyze_offer(self, offer_name: str, offer_path: str) -> Dict:
        """Analyse complète d'une offre d'emploi"""
        print(f"\n🔍 Analyse de l'offre: {offer_name}")

        result = await self.offer_analyzer.analyze_offer(
            offer_name,
            offer_path,
            ANALYSIS_DIR
        )

        # Stockage des résultats
        self.offer_analysis_results[offer_name] = result

        return result

    async def generate_cv_json(self, offer_name: str, offer_analysis: str, themes: list) -> Dict:
        """Génère le CV au format JSON Reactive Resume"""
        print(f"\n📋 Génération du CV pour: {offer_name}")

        cv_json = await self.cv_generator.generate_cv_json(
            offer_analysis=offer_analysis,
            identity_context=self.identity_context,
            education_context=self.education_context,
            themes=themes
        )

        return cv_json

    async def send_to_reactive_resume(self, cv_json: Dict, offer_name: str) -> str:
        """Envoie le JSON à Reactive Resume et récupère le PDF"""
        print(f"\n📤 Envoi à Reactive Resume...")

        pdf_path = await self.cv_generator.send_to_reactive_resume(cv_json, offer_name)
        return pdf_path

    async def generate_cover_letter(self, offer_name: str, offer_analysis: str, themes: list) -> str:
        """Génère la lettre de motivation"""
        print(f"\n✍️ Génération de la lettre de motivation pour: {offer_name}")

        letter_path = await self.letter_generator.generate_letter(
            offer_analysis=offer_analysis,
            identity_context=self.identity_context,
            themes=themes,
            offer_name=offer_name
        )

        return letter_path

    async def update_offer_status(self, offer_name: str, processed: bool):
        """Met à jour le statut de l'offre dans offres.json"""
        print(f"\n🔄 Mise à jour du statut de {offer_name}: {processed}")

        # Lecture du fichier actuel
        async with aiofiles.open(OFFRES_FILE, 'r') as f:
            content = await f.read()
            data = json.loads(content)

        # Mise à jour
        if offer_name in data:
            path, _ = data[offer_name]
            data[offer_name] = [path, processed]

            # Sauvegarde
            async with aiofiles.open(OFFRES_FILE, 'w') as f:
                await f.write(json.dumps(data, indent=2, ensure_ascii=False))

    async def check_reactive_resume(self):
        """Vérifie que Reactive Resume est accessible"""
        print("\n🔍 Vérification de Reactive Resume...")

        # Utiliser la nouvelle méthode du CVGenerator
        is_healthy = await self.cv_generator.check_reactive_resume_health()

        if not is_healthy:
            print(f"  💡 Assurez-vous que le serveur est démarré sur le port 3000")
            print(f"  💡 URL attendue: {settings.reactive_resume_url}")
            print(f"  💡 Démarrez avec: docker-compose up -d")
            raise ConnectionError("Reactive Resume n'est pas accessible")

    async def run(self):
        """Exécute le pipeline complet"""
        print("🚀 Démarrage de l'orchestrateur CV & Lettre de Motivation")
        print("="*60)

        # Chargement des données
        self.offers_data = await self.load_offers()
        await self.load_identity_data()
        await self.load_education_data()

        # Vérification des prérequis
        await self.check_reactive_resume()

        # Traitement des offres non traitées
        processed_count = 0
        failed_count = 0

        for offer_name, (offer_path, is_processed) in self.offers_data.items():
            if not is_processed:
                success = await self.process_offer(offer_name, offer_path)
                if success:
                    processed_count += 1
                    await self.update_offer_status(offer_name, True)
                else:
                    failed_count += 1
                    print(f"⚠️ Échec du traitement de {offer_name}")
            else:
                print(f"⏭️ Offre {offer_name} déjà traitée, ignorée")

        print(f"\n{'='*60}")
        print(f"✅ Pipeline terminé:")
        print(f"   {processed_count} offre(s) traitée(s) avec succès")
        print(f"   {failed_count} offre(s) en échec")
        print(f"{'='*60}")

async def main():
    """Point d'entrée principal"""
    orchestrator = CVGeneratorOrchestrator()
    await orchestrator.run()

if __name__ == "__main__":
    asyncio.run(main())
