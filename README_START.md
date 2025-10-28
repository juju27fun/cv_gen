# 🚀 Guide de Démarrage Rapide

## Prérequis

### 1. Configuration du Projet

```bash
# Copiez le fichier d'exemple et configurez vos variables
cp .env.example .env

# Éditez .env avec vos paramètres:
# - OPENROUTER_API_KEY: Votre clé OpenRouter
# - REACTIVE_RESUME_URL: URL du serveur (défaut: http://localhost:3000)
```

📝 **Obtenir la clé API OpenRouter:**
- Allez sur https://openrouter.ai/keys
- Connectez-vous ou créez un compte
- Créez une nouvelle clé API
- Ajoutez des crédits si nécessaire

### 2. Démarrage de Reactive Resume

Reactive Resume doit être démarré pour générer les PDFs:

```bash
# Option 1: Docker Compose (recommandé)
docker-compose up -d

# Option 2: Docker seul
docker run -d --name reactive-resume -p 3000:3000 amrithpillai/reactive-resume:latest

# Option 3: Vérification si déjà démarré
curl http://localhost:3000/api/health
```

### 3. Installation des Dépendances

```bash
# Avec Poetry (recommandé)
poetry install

# Ou avec pip
pip install -r requirements.txt
```

### 4. Lancement du Pipeline

```bash
# Avec Poetry
poetry run start

# Ou directement
python src/main.py
```

## Structure des Sorties

```
outputs/
├── Guiding_in_Visible_internship_2026_cv.pdf
├── Guiding_in_Visible_internship_2026_lettre.md
├── IE-SCUBA_cv.pdf
├── IE-SCUBA_lettre.md
└── ...
```

## Dépannage

### Erreur "OPENROUTER_API_KEY non définie"
→ Vérifiez que le fichier `.env` existe et contient votre clé

### Erreur "Reactive Resume non accessible"
→ Vérifiez que Docker est en cours d'exécution et le conteneur démarré

### Erreur "ModuleNotFoundError"
→ Installez les dépendances: `poetry install` ou `pip install -r requirements.txt`

### Erreur "Configuration invalide"
→ Vérifiez que toutes les variables requises sont dans votre `.env`

## ✨ Nouvelles Fonctionnalités

### Robustesse Améliorée
- **Retry automatique** : 3 tentatives avec backoff exponentiel en cas d'échec
- **Health check** : Vérification automatique de Reactive Resume avant génération
- **Gestion d'erreurs** : Messages d'erreur explicites et logging structuré
- **Fallback JSON** : Sauvegarde du JSON si la génération PDF échoue

### Configuration Centralisée
- **Fichier .env** : Toutes les configurations dans un seul fichier
- **Variables d'environnement** : Support complet des vars d'env et .env
- **Validation** : Vérification des configurations critiques au démarrage

### Client Reactive Resume Robuste
- **Flux API correct** : POST /api/resume/import → GET /api/resume/print/{id}
- **Structure wrapper** : {title, slug, visibility, data}
- **Timeout configurable** : Empêche les blocages
- **Logging détaillé** : Traçabilité complète des opérations

## Pipeline en Action

Le pipeline traite chaque offre:

1. **Extraction PDF** → Lecture du fichier PDF de l'offre
2. **Analyse IA** → Analyse des 8 points de vigilance via OpenRouter
3. **Extraction Thèmes** → Identification des mots-clés pertinents
4. **Génération CV** → Création du JSON Reactive Resume + PDF
5. **Génération Lettre** → Rédaction de la lettre de motivation
6. **Mise à jour Statut** → Marqueur "traité" dans offres.json

Temps estimé: 2-3 minutes par offre (selon la complexité et la réponse de l'IA)
