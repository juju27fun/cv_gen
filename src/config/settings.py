"""
Configuration centralisée du projet
Utilise Pydantic v1 BaseSettings pour gérer les variables d'environnement
"""

from pydantic.v1 import BaseSettings, Field
from typing import Optional

# Utilisons Pydantic v1 pour éviter les problèmes de compatibilité


class Settings(BaseSettings):
    """
    Configuration générale de l'application

    Les variables sont chargées depuis:
    1. Variables d'environnement système
    2. Fichier .env (si présent)
    """
    class Config:
        extra = 'ignore'
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"

    # === Reactive Resume ===
    reactive_resume_url: str = Field(default="http://localhost:3000", env="REACTIVE_RESUME_URL")
    reactive_resume_timeout: int = Field(default=30, env="REACTIVE_RESUME_TIMEOUT")
    reactive_resume_max_retries: int = Field(default=3, env="REACTIVE_RESUME_MAX_RETRIES")
    reactive_resume_retry_delay: float = Field(default=1.0, env="REACTIVE_RESUME_RETRY_DELAY")

    # === OpenRouter ===
    openrouter_api_key: str = Field(default="", env="OPENROUTER_API_KEY")
    openrouter_model: str = Field(default="deepseek/deepseek-v3.2-exp", env="OPENROUTER_MODEL")

    # === Données ===
    base_dir: str = Field(default=".", env="BASE_DIR")
    offres_file: str = Field(default="offres/offres.json", env="OFFRES_FILE")
    outputs_dir: str = Field(default="outputs", env="OUTPUTS_DIR")
    analysis_dir: str = Field(default="offres/offer_analysis", env="ANALYSIS_DIR")
    data_dir: str = Field(default="data", env="DATA_DIR")

    # === Logging ===
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # === Génération ===
    pdf_quality: str = Field(default="high", env="PDF_QUALITY")


# Instance globale de la configuration
settings = Settings()


def get_reactive_resume_url() -> str:
    """Retourne l'URL de Reactive Resume"""
    return settings.reactive_resume_url


def get_reactive_resume_api_url() -> str:
    """Retourne l'URL de l'API Reactive Resume"""
    return f"{settings.reactive_resume_url}/api"


def get_openrouter_api_key() -> str:
    """Retourne la clé API OpenRouter"""
    if not settings.openrouter_api_key:
        raise ValueError(
            "OPENROUTER_API_KEY non configurée. "
            "Vérifiez votre fichier .env ou les variables d'environnement."
        )
    return settings.openrouter_api_key


def get_openrouter_model() -> str:
    """Retourne le modèle OpenRouter"""
    return settings.openrouter_model


def get_output_dir() -> str:
    """Retourne le répertoire de sortie"""
    return settings.outputs_dir


def get_offres_file() -> str:
    """Retourne le fichier des offres"""
    return settings.offres_file


def get_analysis_dir() -> str:
    """Retourne le répertoire des analyses"""
    return settings.analysis_dir


def get_data_dir() -> str:
    """Retourne le répertoire des données"""
    return settings.data_dir


def get_pdf_quality() -> str:
    """Retourne la qualité du PDF"""
    return settings.pdf_quality


def is_production() -> bool:
    """Vérifie si l'application est en mode production"""
    import os
    return os.getenv("ENVIRONMENT", "development").lower() == "production"


def is_debug() -> bool:
    """Vérifie si l'application est en mode debug"""
    return settings.log_level.upper() == "DEBUG"


# Validation des configurations critiques
def validate_config():
    """
    Valide que les configurations critiques sont présentes

    Raises:
        ValueError: Si une configuration critique est manquante
    """
    errors = []

    # Vérification OpenRouter
    if not settings.openrouter_api_key:
        errors.append("OPENROUTER_API_KEY est requise")

    # Vérification Reactive Resume URL
    if not settings.reactive_resume_url:
        errors.append("REACTIVE_RESUME_URL est requise")

    if errors:
        error_msg = "Configuration invalide:\n" + "\n".join(f"- {e}" for e in errors)
        raise ValueError(error_msg)


# Export des constantes pour compatibilité
REACTIVE_RESUME_URL = f"{settings.reactive_resume_url}/api/resume"
OPENROUTER_MODEL = settings.openrouter_model
