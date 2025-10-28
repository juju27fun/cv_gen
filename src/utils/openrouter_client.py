"""
Client OpenRouter pour les appels IA
"""

import os
import json
import aiohttp
from typing import Optional, Dict, Any

# Chargement du fichier .env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

class OpenRouterClient:
    """Client asynchrone pour OpenRouter"""

    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.base_url = OPENROUTER_BASE_URL
        # Modèle plus stable pour éviter les rate limits
        self.model = "anthropic/claude-3-haiku"

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY non définie dans l'environnement")

    async def chat_completion(
        self,
        messages: list,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Effectue un appel de completion via OpenRouter

        Args:
            messages: Liste des messages [{"role": "user", "content": "..."}]
            model: Modèle à utiliser (défaut: deepseek/deepseek-v3.2-exp)
            temperature: Créativité de la réponse
            max_tokens: Nombre max de tokens
            stream: Streaming ou non

        Returns:
            Réponse de l'API
        """
        model = model or self.model

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://cv-generator.local",
            "X-Title": "CV & Lettre Generator"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Erreur OpenRouter {response.status}: {error_text}")

                return await response.json()

    async def analyze_offer(self, offer_content: str, analysis_prompt: str) -> str:
        """
        Analyse une offre d'emploi avec l'IA

        Args:
            offer_content: Contenu brut de l'offre
            analysis_prompt: Prompt d'analyse spécifique

        Returns:
            Analyse structurée en markdown
        """
        messages = [
            {
                "role": "system",
                "content": "Tu es un expert en analyse de recrutement. Tu analyses les offres d'emploi de manière structurée et précise."
            },
            {
                "role": "user",
                "content": f"{analysis_prompt}\n\nOFFRE À ANALYSER:\n{offer_content}"
            }
        ]

        response = await self.chat_completion(messages)
        return response["choices"][0]["message"]["content"]

    async def generate_themes(self, offer_analysis: str) -> list:
        """
        Extrait les thèmes pertinents d'une offre

        Returns:
            Liste des thèmes sous forme de liste Python
        """
        messages = [
            {
                "role": "system",
                "content": "Tu extrais les thèmes et mots-clés d'une offre d'emploi pour contextualiser la génération d'un CV. Réponds UNIQUEMENT avec une liste Python de chaînes."
            },
            {
                "role": "user",
                "content": f"""Extrait une liste de thèmes/mots-clés pertinents pour contextualiser un CV.
Format de sortie: ["thème1", "thème2", "thème3"]

Analyse de l'offre:
{offer_analysis}"""
            }
        ]

        response = await self.chat_completion(messages, temperature=0.3)
        content = response["choices"][0]["message"]["content"]

        try:
            # Parse la réponse comme une liste Python
            themes = eval(content)
            return themes
        except:
            # Fallback: extraction simple
            import re
            matches = re.findall(r'"([^"]+)"', content)
            return matches if matches else []

    async def generate_cv_json(self, prompt: str) -> Dict[str, Any]:
        """
        Génère le JSON du CV au format Reactive Resume

        Returns:
            Dictionnaire JSON du CV
        """
        messages = [
            {
                "role": "system",
                "content": "Tu génères des CV au format JSON Reactive Resume. Respecte EXACTEMENT la structure fournie dans le guide. Réponds uniquement avec le JSON valide, sansmarkdown."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = await self.chat_completion(messages, temperature=0.5, max_tokens=4000)
        content = response["choices"][0]["message"]["content"]

        # Parse le JSON
        try:
            # Nettoyage du JSON (suppression des ```json si présents)
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise Exception(f"Erreur parsing JSON: {e}\nContenu: {content[:500]}")

    async def generate_cover_letter(self, prompt: str) -> str:
        """
        Génère une lettre de motivation

        Returns:
            Lettre de motivation en Markdown
        """
        messages = [
            {
                "role": "system",
                "content": "Tu rédiges des lettres de motivation professionnelles, personnalisées et convaincantes en français. Utilise un ton professionnel mais chaleureux."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = await self.chat_completion(messages, temperature=0.7, max_tokens=2000)
        return response["choices"][0]["message"]["content"]
