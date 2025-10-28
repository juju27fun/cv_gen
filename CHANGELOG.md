# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-27

### Ajouté

#### Nouveau Client Reactive Resume
- **Client robuste** (`src/utils/reactive_resume_client.py`)
  - Implémentation complète du flux API correct (POST `/api/resume` → GET `/api/resume/print/{id}`)
  - Retry automatique avec backoff exponentiel (configurable)
  - Gestion d'erreurs avancée avec types d'erreurs spécifiques
  - Health check intégré pour vérifier la disponibilité du serveur
  - Support des timeouts configurables
  - Logging structuré pour le débogage

#### Configuration Centralisée
- **Fichier de settings** (`src/config/settings.py`)
  - Configuration via Pydantic BaseSettings
  - Support complet des variables d'environnement
  - Validation automatique des configurations critiques
  - Fonctions utilitaires pour accéder aux configs

- **Fichier .env.example mis à jour**
  - Ajout de toutes les variables Reactive Resume
  - Documentation inline pour chaque variable
  - Instructions de configuration claires

#### Fonctionnalités Améliorées
- **Health check automatique** avant génération de CV
- **Fallback JSON** : sauvegarde automatique du JSON si la génération PDF échoue
- **Messages d'erreur explicites** avec conseils de résolution
- **Logging structuré** avec différents niveaux (DEBUG, INFO, WARNING, ERROR)

### Modifié

#### Architecture
- **CVGenerator** (`src/agents/cv_generator.py`)
  - Utilisation du nouveau `ReactiveResumeClient`
  - Ajout du logging structuré
  - Validation de configuration au démarrage
  - Amélioration de la gestion d'erreurs
  - Méthode `check_reactive_resume_health()` pour vérification manuelle

- **Orchestrateur** (`src/main.py`)
  - Utilisation de la configuration centralisée
  - Suppression de l'import aiohttp (déplacé dans le client)
  - Amélioration du health check avec messages d'aide

#### URLs API Corrigées
- **Avant**: `http://localhost:3100/api/resumes` (incorrect)
- **Après**: `http://localhost:3100/api/resume` (correct, singulier)
- **Flux**: Implémentation du flux en 2 étapes comme spécifié dans l'API

### Corrigé

- **URLs API incorrectes** : Correction de `/api/resumes` vers `/api/resume`
- **Flux de génération** : Implémentation correcte avec création puis génération PDF
- **Gestion des sessions aiohttp** : Meilleure gestion des connexions
- **Timeouts** : Configuration via paramètres ou variables d'environnement

### Supprimé

- **Constantes hardcodées** dans `main.py` : déplacées vers `settings.py`
- **Import aiohttp redondant** dans `main.py`

### Documentation

- **README_START.md** : Mis à jour avec les nouvelles fonctionnalités
- **Guide client** (`docs/CLIENT_REACTIVE_RESUME.md`) : Documentation complète du nouveau client
- **.env.example** : Documentation inline améliorée

### Technique

#### Dépendances
- Ajout : `pydantic` pour la gestion des settings
- Recommandé : `aiofiles` pour les opérations de fichiers asynchrones

#### Breaking Changes
- **Configuration** : Les variables d'environnement doivent être configurées dans `.env`
- **URL par défaut** : `http://localhost:3100` (au lieu de ports spécifiques)
- **Exceptions** : `ReactiveResumeError` pour les erreurs spécifiques

### Sécurité

- Validation automatique des configurations critiques au démarrage
- Messages d'erreur informatifs sans exposition de données sensibles
- Support des timeouts pour éviter les blocages

### Performance

- Retry avec backoff exponentiel pour optimiser les tentatives
- Meilleure gestion des connexions HTTP avec aiohttp
- Logging optimisé pour ne pas impacter les performances

## [1.0.0] - Précédent

### Implémentation Initiale
- Génération de CV PDF via Reactive Resume
- Analyse d'offres d'emploi avec IA
- Génération de lettres de motivation
- Pipeline automatisé

---

## Migration depuis la version 1.x

### Étapes Required

1. **Mettre à jour .env**
   ```bash
   cp .env.example .env
   # Configurez vos variables
   ```

2. **Installer les nouvelles dépendances**
   ```bash
   poetry install
   # ou
   pip install pydantic
   ```

3. **Démarrer Reactive Resume**
   ```bash
   docker-compose up -d
   ```

4. **Lancer le pipeline**
   ```bash
   poetry run start
   ```

### Changements Incompatibles

- Les URLs API ont été corrigées
- La configuration est maintenant centralisée dans `settings.py`
- Les exceptions sont plus spécifiques (`ReactiveResumeError`)

### Nouvelles Fonctionnalités

- Health check automatique
- Retry avec backoff
- Fallback JSON
- Logging structuré
- Configuration via variables d'environnement
