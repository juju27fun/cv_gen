# OpenRouter pour projet Python — guide condensé et cohérent

## 1) Vue d’ensemble

OpenRouter est une API unifiée compatible avec le schéma “Chat Completions” d’OpenAI : un même endpoint donne accès à des centaines de modèles (OpenAI, Anthropic, Google, Mistral, xAI, etc.), avec routage/fallbacks et normalisation des réponses. ([OpenRouter][1])

**Base URL** : `https://openrouter.ai/api/v1` (vous utiliserez surtout `POST /chat/completions`). ([OpenRouter][2])

---

## 2) Pré-requis & sécurité

- Créez une clé API sur OpenRouter et stockez-la en variable d’environnement (p.ex. `OPENROUTER_API_KEY`). Authentification par **Bearer token**. ([OpenRouter][3])
- (Optionnel mais recommandé) Ajoutez des entêtes d’attribution pour vos analytics/rankings :

  - `HTTP-Referer`: URL de votre app
  - `X-Title`: nom lisible de l’app. ([OpenRouter][4])

---

## 3) Installer les dépendances

```bash
pip install requests
# Option SDK OpenAI compatible (fonctionne avec OpenRouter via base_url)
pip install openai
```

OpenRouter s’utilise soit en HTTP direct (requests), soit via le SDK OpenAI en pointant `base_url` vers OpenRouter. ([OpenRouter][3])

---

## 4) Authentification & entêtes (Python)

```python
import os

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    # Attribution (facultatif mais utile)
    "HTTP-Referer": "https://votre-app.example",
    "X-Title": "Mon Assistant IA",
}
```

Bearer + endpoint crédit (`GET /credits`) sont confirmés par la doc officielle et le document fourni. ([OpenRouter][5])

---

## 5) Appels essentiels

### a) Lister les modèles disponibles

```python
import requests

r = requests.get(f"{BASE_URL}/models")
r.raise_for_status()
models = r.json()["data"]
```

`GET /models` renvoie id, contexte, pricing et paramètres supportés par modèle. ([OpenRouter][6])

### b) Vérifier les crédits & limites

```python
import requests

# Solde total des crédits
print(requests.get(f"{BASE_URL}/credits", headers=DEFAULT_HEADERS).json())

# État de la clé (crédits restants, usage, limites)
print(requests.get(f"{BASE_URL}/key", headers=DEFAULT_HEADERS).json())
```

`GET /credits` retourne crédits achetés/utilisés ; `GET /key` expose crédits restants, usage journalier/hebdo/mensuel et infos de limites. ([OpenRouter][5])

### c) Chat Completions (réponse non-streamée)

```python
import requests, json

payload = {
    "model": "deepseek/deepseek-v3.2-exp",   # choisissez un id listé par /models
    "messages": [{"role": "user", "content": "Explique-moi le routage OpenRouter."}],
    # options courantes : temperature, top_p, max_tokens, seed, user, etc.
}
r = requests.post(f"{BASE_URL}/chat/completions", headers=DEFAULT_HEADERS, json=payload)
r.raise_for_status()
print(r.json()["choices"][0]["message"]["content"])
```

Schéma et paramètres (temperature, top_p, penalties, seed, stream, etc.) suivent l’API “Chat Completions”. ([OpenRouter][2])

### d) Chat Completions en streaming (SSE)

```python
import requests, json

payload = {
    "model": "deepseek/deepseek-v3.2-exp",
    "messages": [{"role": "user", "content": "Donne la réponse en streaming."}],
    "stream": True,
}
with requests.post(f"{BASE_URL}/chat/completions",
                   headers=DEFAULT_HEADERS, json=payload, stream=True) as resp:
    resp.raise_for_status()
    for line in resp.iter_lines(decode_unicode=True):
        if not line:
            continue
        if line.startswith("data: "):
            data = line[6:]
            if data == "[DONE]":
                break
            try:
                chunk = json.loads(data)
                delta = chunk["choices"][0]["delta"].get("content")
                if delta:
                    print(delta, end="", flush=True)
            except json.JSONDecodeError:
                pass
```

OpenRouter émet des événements SSE `data:` et peut envoyer des commentaires keep-alive (`: OPENROUTER PROCESSING`). Gérez aussi l’annulation/erreurs mid-stream si besoin. ([OpenRouter][7])

---

## 6) Option SDK OpenAI (Python)

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

resp = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Bonjour OpenRouter 👋"}],
    extra_headers={"HTTP-Referer": "https://votre-app.example", "X-Title": "Mon Assistant IA"},
)
print(resp.choices[0].message.content)
```

Le SDK OpenAI fonctionne en définissant `base_url` et la clé OpenRouter ; vous pouvez y injecter les entêtes d’attribution via `extra_headers`. ([OpenRouter][4])

---

## 7) Gestion des erreurs & limites

- **Codes fréquents** : `400` (mauvaise requête), `401` (clé invalide), `402` (crédits insuffisants), `429` (rate limit), `5xx` (erreur provider). En streaming, une erreur peut arriver **mid-stream** via un événement SSE avec `finish_reason: "error"`. ([OpenRouter][7])
- **Free tier & limites** : les modèles `:free` ont des plafonds (p.ex. 20 req/min, 50/jour si <10 crédits, 1000/jour si ≥10 crédits). Consultez aussi `GET /key` pour les crédits restants. ([OpenRouter][8])
- **Bonnes pratiques** : timeouts raisonnables, retries exponentiels sur `429`/`5xx`, journaliser `provider`/`model` renvoyés, et toujours protéger vos clés (rotation si fuite). ([OpenRouter][3])

---

## 8) BYOK (Bring Your Own Keys) — optionnel

Vous pouvez payer soit via crédits OpenRouter, soit rattacher vos **clés providers** (BYOK) pour contrôler coûts et limites côté fournisseur. Les clés sont chiffrées et utilisées pour router via le provider choisi. ([OpenRouter][9])

---

## 9) Checklist d’intégration (résumée)

1. **Clé** : créer `OPENROUTER_API_KEY` + stocker en env. ([OpenRouter][3])
2. **Entêtes** : `Authorization: Bearer …` (+ `HTTP-Referer`/`X-Title` facultatifs). ([OpenRouter][3])
3. **Modèles** : interroger `GET /models`, choisir l’id. ([OpenRouter][6])
4. **Appels** : `POST /chat/completions` (avec messages) ; activer `stream` si besoin. ([OpenRouter][2])
5. **Crédits/limites** : surveiller `GET /credits` et `GET /key`. ([OpenRouter][5])

---

## 10) Références utiles

- **Chat Completions** (schéma & paramètres). ([OpenRouter][2])
- **Streaming** (SSE, annulation, erreurs). ([OpenRouter][7])
- **Modèles disponibles**. ([OpenRouter][6])
- **Authentification** (clé, SDK OpenAI, entêtes). ([OpenRouter][3])
- **Attribution (HTTP-Referer/X-Title)**. ([OpenRouter][4])
- **Crédits & limites**. ([OpenRouter][5])
