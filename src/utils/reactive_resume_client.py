"""
Client robuste pour l'API Reactive Resume
Implémente les bonnes pratiques du PDF_GENERATION_GUIDE.md
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional
from pathlib import Path
import aiohttp
from aiohttp import ClientSession, ClientError, ClientTimeout
# Utilisons Pydantic v1 pour éviter les problèmes de compatibilité
from pydantic.v1 import BaseSettings, Field

logger = logging.getLogger(__name__)

# Import pour async file operations
try:
    import aiofiles
except ImportError:
    aiofiles = None
    logger.warning("aiofiles non disponible, certaines fonctionnalités seront limitées")


class Settings(BaseSettings):
    """Configuration pour Reactive Resume"""
    reactive_resume_url: str = Field(default="http://localhost:3000", env="REACTIVE_RESUME_URL")
    reactive_resume_timeout: int = Field(default=30, env="REACTIVE_RESUME_TIMEOUT")
    max_retries: int = Field(default=3, env="REACTIVE_RESUME_MAX_RETRIES")
    retry_delay: float = Field(default=1.0, env="REACTIVE_RESUME_RETRY_DELAY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class ReactiveResumeError(Exception):
    """Erreur personnalisée pour Reactive Resume"""
    pass


class ReactiveResumeClient:
    """
    Client robuste pour l'API Reactive Resume

    Implémente:
    - Retry logic avec backoff exponentiel
    - Gestion d'erreurs avancée
    - Validation des données
    - Logging structuré
    - Timeout configurable
    """

    def __init__(self, base_url: Optional[str] = None, timeout: int = 30, max_retries: int = 3):
        """
        Initialise le client Reactive Resume

        Args:
            base_url: URL de base de l'API (ex: http://localhost:3000)
            timeout: Timeout en secondes pour les requêtes
            max_retries: Nombre maximum de tentatives en cas d'échec
        """
        settings = Settings()
        self.base_url = base_url or settings.reactive_resume_url
        self.api_url = f"{self.base_url}/api"
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = settings.retry_delay

        logger.info(f"ReactiveResumeClient initialisé: {self.base_url}")

    async def create_resume(self, session: ClientSession, resume_data: Dict[str, Any], title: str = "CV Généré", slug: str = None) -> str:
        """
        Crée un nouveau resume et retourne son ID

        Args:
            session: Session aiohttp active
            resume_data: Données JSON du resume
            title: Titre du CV
            slug: Slug unique pour le CV (généré automatiquement si non fourni)

        Returns:
            ID du resume créé

        Raises:
            ReactiveResumeError: En cas d'erreur lors de la création
        """
        logger.info("Création d'un nouveau resume...")

        # Générer un slug unique si non fourni
        if not slug:
            import time
            slug = f"cv-{int(time.time())}"

        # Préparer les données selon le format de l'API Reactive Resume
        import_data = {
            "title": title,
            "slug": slug,
            "visibility": "private",
            "data": resume_data
        }

        try:
            async with session.post(
                f"{self.api_url}/resume/import",
                json=import_data,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:

                if response.status == 201:
                    result = await response.json()
                    resume_id = result.get("id")
                    logger.info(f"Resume créé avec succès: {resume_id}")
                    return resume_id
                elif response.status == 400:
                    error_text = await response.text()
                    logger.error(f"Données invalides (400): {error_text}")
                    raise ReactiveResumeError(f"Données invalides: {error_text}")
                elif response.status == 401:
                    logger.warning("Non autorisé - Authentification requise pour Reactive Resume")
                    logger.info("Le CV JSON sera sauvegardé sans génération PDF")
                    return None  # Indique qu'il faut utiliser le fallback
                elif response.status == 404:
                    logger.error("Endpoint non trouvé")
                    raise ReactiveResumeError("Endpoint non trouvé - Vérifiez l'URL de l'API")
                elif response.status >= 500:
                    error_text = await response.text()
                    logger.error(f"Erreur serveur {response.status}: {error_text}")
                    raise ReactiveResumeError(f"Erreur serveur {response.status}: {error_text}")
                else:
                    error_text = await response.text()
                    logger.error(f"Erreur HTTP {response.status}: {error_text}")
                    raise ReactiveResumeError(f"Erreur HTTP {response.status}: {error_text}")

        except asyncio.TimeoutError:
            logger.error(f"Timeout lors de la création du resume (> {self.timeout}s)")
            raise ReactiveResumeError(f"Timeout lors de la création du resume")
        except ClientError as e:
            logger.error(f"Erreur réseau: {str(e)}")
            raise ReactiveResumeError(f"Erreur réseau: {str(e)}")

    async def generate_pdf(self, session: ClientSession, resume_id: str) -> bytes:
        """
        Génère et récupère le PDF du resume

        Args:
            session: Session aiohttp active
            resume_id: ID du resume

        Returns:
            Bytes du PDF

        Raises:
            ReactiveResumeError: En cas d'erreur lors de la génération
        """
        logger.info(f"Génération du PDF pour le resume {resume_id}...")

        # Attendre que le resume soit traité
        await asyncio.sleep(2)

        try:
            async with session.get(
                f"{self.api_url}/resume/print/{resume_id}",
                headers={"Accept": "application/pdf"},
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:

                if response.status == 200:
                    pdf_content = await response.read()
                    logger.info(f"PDF généré avec succès ({len(pdf_content)} bytes)")
                    return pdf_content
                elif response.status == 404:
                    logger.error(f"Resume {resume_id} non trouvé")
                    raise ReactiveResumeError(f"Resume {resume_id} non trouvé")
                elif response.status >= 500:
                    error_text = await response.text()
                    logger.error(f"Erreur serveur {response.status}: {error_text}")
                    raise ReactiveResumeError(f"Erreur serveur {response.status}: {error_text}")
                else:
                    error_text = await response.text()
                    logger.error(f"Erreur HTTP {response.status}: {error_text}")
                    raise ReactiveResumeError(f"Erreur HTTP {response.status}: {error_text}")

        except asyncio.TimeoutError:
            logger.error(f"Timeout lors de la génération du PDF (> {self.timeout}s)")
            raise ReactiveResumeError(f"Timeout lors de la génération du PDF")
        except ClientError as e:
            logger.error(f"Erreur réseau: {str(e)}")
            raise ReactiveResumeError(f"Erreur réseau: {str(e)}")

    async def generate_pdf_preview(self, session: ClientSession, resume_id: str) -> bytes:
        """
        Génère et récupère l'aperçu (HTML) du resume

        Args:
            session: Session aiohttp active
            resume_id: ID du resume

        Returns:
            Bytes de l'aperçu HTML
        """
        logger.info(f"Génération de l'aperçu pour le resume {resume_id}...")

        try:
            async with session.get(
                f"{self.api_url}/resume/print/{resume_id}/preview",
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:

                if response.status == 200:
                    preview_content = await response.read()
                    logger.info(f"Aperçu généré avec succès ({len(preview_content)} bytes)")
                    return preview_content
                else:
                    error_text = await response.text()
                    logger.error(f"Erreur HTTP {response.status}: {error_text}")
                    raise ReactiveResumeError(f"Erreur HTTP {response.status}: {error_text}")

        except asyncio.TimeoutError:
            logger.error(f"Timeout lors de la génération de l'aperçu (> {self.timeout}s)")
            raise ReactiveResumeError(f"Timeout lors de la génération de l'aperçu")
        except ClientError as e:
            logger.error(f"Erreur réseau: {str(e)}")
            raise ReactiveResumeError(f"Erreur réseau: {str(e)}")

    async def get_resume(self, session: ClientSession, resume_id: str) -> Dict[str, Any]:
        """
        Récupère les données d'un resume

        Args:
            session: Session aiohttp active
            resume_id: ID du resume

        Returns:
            Données du resume
        """
        logger.info(f"Récupération du resume {resume_id}...")

        try:
            async with session.get(
                f"{self.api_url}/resume/{resume_id}",
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:

                if response.status == 200:
                    resume_data = await response.json()
                    logger.info(f"Resume récupéré avec succès")
                    return resume_data
                else:
                    error_text = await response.text()
                    logger.error(f"Erreur HTTP {response.status}: {error_text}")
                    raise ReactiveResumeError(f"Erreur HTTP {response.status}: {error_text}")

        except asyncio.TimeoutError:
            logger.error(f"Timeout lors de la récupération du resume (> {self.timeout}s)")
            raise ReactiveResumeError(f"Timeout lors de la récupération du resume")
        except ClientError as e:
            logger.error(f"Erreur réseau: {str(e)}")
            raise ReactiveResumeError(f"Erreur réseau: {str(e)}")

    async def check_health(self) -> bool:
        """
        Vérifie que Reactive Resume est accessible

        Returns:
            True si accessible, False sinon
        """
        logger.info("Vérification de la santé de Reactive Resume...")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/health",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        logger.info("✅ Reactive Resume est accessible")
                        return True
                    else:
                        logger.warning(f"⚠️ Reactive Resume répond avec code {response.status}")
                        return False
        except Exception as e:
            logger.error(f"❌ Reactive Resume non accessible: {str(e)}")
            return False

    async def create_and_generate_pdf(
        self,
        resume_data: Dict[str, Any],
        output_path: Path,
        title: str = None
    ) -> Path:
        """
        Crée un resume et génère son PDF en une seule opération

        Args:
            resume_data: Données JSON du resume
            output_path: Chemin où sauvegarder le PDF
            title: Titre du CV (généré automatiquement depuis output_path si non fourni)

        Returns:
            Chemin vers le PDF généré

        Raises:
            ReactiveResumeError: En cas d'erreur
        """
        logger.info(f"Génération complète du CV: {output_path}")

        # Générer le titre depuis le nom du fichier si non fourni
        if not title:
            title = output_path.stem.replace('_', ' ').replace('-', ' ').title()

        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    # Étape 1: Créer le resume
                    resume_id = await self.create_resume(session, resume_data, title=title)

                    # Si l'authentification a échoué (resume_id = None), utiliser le fallback
                    if resume_id is None:
                        logger.info("📄 Sauvegarde du CV JSON (fallback sans PDF)")
                        json_path = output_path.with_suffix('.json')
                        json_path.parent.mkdir(parents=True, exist_ok=True)
                        if aiofiles:
                            async with aiofiles.open(json_path, 'w', encoding='utf-8') as f:
                                import json
                                await f.write(json.dumps(resume_data, indent=2, ensure_ascii=False))
                        else:
                            import json
                            with open(json_path, 'w', encoding='utf-8') as f:
                                json.dump(resume_data, f, indent=2, ensure_ascii=False)
                        logger.info(f"💾 CV JSON sauvegardé: {json_path}")
                        return json_path

                    # Étape 2: Générer le PDF
                    pdf_content = await self.generate_pdf(session, resume_id)

                    # Étape 3: Sauvegarder
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    async with aiofiles.open(output_path, 'wb') as f:
                        await f.write(pdf_content)

                    logger.info(f"✅ PDF généré avec succès: {output_path}")
                    return output_path

            except ReactiveResumeError as e:
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2 ** attempt)  # Backoff exponentiel
                    logger.warning(f"Tentative {attempt + 1}/{self.max_retries} échouée: {e}")
                    logger.info(f"⏳ Retry dans {wait_time}s...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"❌ Échec après {self.max_retries} tentatives")
                    raise ReactiveResumeError(f"Échec après {self.max_retries} tentatives: {e}")

        # Cette ligne ne devrait jamais être atteinte, mais pour la forme
        raise ReactiveResumeError("Nombre de tentatives dépassé")


# Fonctions utilitaires pour compatibilité avec l'ancien code
async def generate_cv_with_retry(
    resume_data: Dict[str, Any],
    output_path: str,
    max_retries: int = 3
) -> str:
    """
    Génère un CV PDF avec retry en cas d'échec

    Args:
        resume_data: Données du CV
        output_path: Chemin de sortie
        max_retries: Nombre maximum de tentatives

    Returns:
        Chemin du PDF généré
    """
    client = ReactiveResumeClient(max_retries=max_retries)
    output_path_obj = Path(output_path)

    try:
        result_path = await client.create_and_generate_pdf(resume_data, output_path_obj)
        return str(result_path)
    except ReactiveResumeError:
        # Fallback: sauvegarde du JSON
        if aiofiles:
            json_path = output_path_obj.with_suffix('.json')
            import json
            async with aiofiles.open(json_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(resume_data, indent=2, ensure_ascii=False))
            logger.warning(f"💾 JSON sauvegardé à la place: {json_path}")
            return str(json_path)
        else:
            # Fallback synchrone
            json_path = output_path_obj.with_suffix('.json')
            import json
            json_path.parent.mkdir(parents=True, exist_ok=True)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(resume_data, f, indent=2, ensure_ascii=False)
            logger.warning(f"💾 JSON sauvegardé à la place: {json_path}")
            return str(json_path)
