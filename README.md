# 🎯 Générateur Automatique de CV & Lettre de Motivation

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Actif-success.svg)

**Générez automatiquement des CVs et lettres de motivation personnalisés pour chaque offre d'emploi, optimisés par IA.**

Ce projet utilise des agents IA pour analyser les offres d'emploi et générer des documents de candidature parfaitement adaptés à chaque poste.

---

## 🌟 Fonctionnalités Principales

### ✨ Automatisation Complète
- **Analyse intelligente** des offres d'emploi (PDF ou URL)
- **Génération de CV** au format PDF via Reactive Resume
- **Rédaction de lettres de motivation** personnalisées
- **Pipeline automatisé** pour traiter plusieurs offres en批次

### 🤖 IA Avancée
- **Analyse contextuelle** des offres avec extraction des thèmes clés
- **Matching intelligent** entre votre profil et les exigences
- **Génération adaptative** selon le secteur et le niveau de poste
- **Optimisation ATS** (Applicant Tracking System)

### 🛡️ Robustesse
- **Retry automatique** avec backoff exponentiel
- **Health check** pour vérifier la disponibilité des services
- **Fallback intelligent** (sauvegarde JSON si génération PDF échoue)
- **Gestion d'erreurs** avancée avec logging structuré

---

## 🏗️ Architecture du Projet

```
cv_vfin/
├── src/
│   ├── agents/
│   │   ├── offer_analyzer.py      # Agent d'analyse d'offres
│   │   ├── cv_generator.py        # Agent de génération de CV
│   │   └── letter_generator.py    # Agent de génération de lettres
│   ├── utils/
│   │   ├── openrouter_client.py   # Client OpenRouter pour l'IA
│   │   └── reactive_resume_client.py # Client Reactive Resume
│   ├── config/
│   │   └── settings.py            # Configuration centralisée
│   └── main.py                    # Orchestrateur principal
│
├── data/                          # Données du candidat
│   ├── identity/                  # Informations personnelles et professionnelles
│   └── education/                 # Formation par thématique
│
├── offres/                        # Offres d'emploi à traiter
│   ├── offres.json                # Liste des offres
│   └── offer_analysis/            # Analyses générées
│
├── outputs/                       # Documents générés
│   ├── *_cv.pdf                   # CVs en PDF
│   ├── *_cv.json                  # CVs en JSON (fallback)
│   └── *_lettre.md                # Lettres de motivation
│
├── docs/                          # Documentation
│   ├── PDF_GENERATION_GUIDE.md    # Guide génération PDF
│   ├── JSON_FORMAT_GUIDE.md       # Guide format JSON
│   ├── CLIENT_REACTIVE_RESUME.md  # Documentation client
│   └── openrouter.md              # Guide OpenRouter
│
├── .env.example                   # Configuration d'exemple
├── CHANGELOG.md                   # Historique des modifications
└── README.md                      # Ce fichier
```

---

## 🚀 Démarrage Rapide

### Prérequis

1. **Python 3.9+** installé sur votre système
2. **Docker** pour exécuter Reactive Resume
3. Une **clé API OpenRouter** (voir section "Configuration")

### Installation

```bash
# 1. Cloner le dépôt
git clone <url-du-repo>
cd cv_vfin

# 2. Installer les dépendances
poetry install
# ou
pip install -r requirements.txt

# 3. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

# 4. Démarrer Reactive Resume
docker-compose up -d

# 5. Lancer le pipeline
poetry run start
```

### Configuration

Éditez le fichier `.env` :

```env
# === OPENROUTER (IA) ===
OPENROUTER_API_KEY=votre_cle_api_ici
OPENROUTER_MODEL=deepseek/deepseek-v3.2-exp

# === REACTIVE RESUME (PDF) ===
REACTIVE_RESUME_URL=http://localhost:3000
REACTIVE_RESUME_TIMEOUT=30

# === DONNÉES ===
OUTPUTS_DIR=outputs
DATA_DIR=data
```

📝 **Obtenir une clé OpenRouter** : https://openrouter.ai/keys

---

## 📋 Utilisation

### Préparer les Données

1. **Vos informations** : Éditez les fichiers dans `data/identity/` et `data/education/`
2. **Offres d'emploi** : Ajoutez vos offres dans `offres/offres.json`

```json
{
  "Nom_Offre_1": ["offres/offre1.pdf", false],
  "Nom_Offre_2": ["https://exemple.com/offre2", false]
}
```

### Lancer le Pipeline

```bash
poetry run start
```

Le pipeline va :
1. 🔍 Analyser chaque offre non traitée
2. 🧠 Extraire les thèmes et mots-clés
3. 📝 Générer un CV personnalisé (JSON + PDF)
4. ✍️ Rédiger une lettre de motivation
5. 💾 Sauvegarder tout dans `outputs/`

### Traitement Individuel

Vous pouvez aussi traiter une offre spécifique :

```python
from src.main import CVGeneratorOrchestrator

async def main():
    orchestrator = CVGeneratorOrchestrator()
    await orchestrator.process_offer("Mon_Offre", "chemin/vers/offre.pdf")

asyncio.run(main())
```

---

## 🎨 Personnalisation

### Templates de CV

Le projet utilise les templates Reactive Resume :
- `pikachu` (par défaut), `gengar`, `glalie`, etc.

Modifiez dans `src/agents/cv_generator.py` :
```python
"metadata": {
    "template": "pikachu",  # Changez ici
    ...
}
```

### Prompts IA

Les prompts sont dans `Prompts/` (référencés dans le code) :
- Analyse d'offres
- Génération de CV
- Rédaction de lettre

### Styles et Thèmes

Configurez l'apparence dans `src/agents/cv_generator.py` :
```python
"theme": {
    "background": "#ffffff",
    "text": "#000000",
    "primary": "#ca8a04"  # Couleur primaire
}
```

---

## 🔧 Configuration Avancée

### Variables d'Environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `OPENROUTER_API_KEY` | Clé API OpenRouter | - |
| `OPENROUTER_MODEL` | Modèle IA à utiliser | `deepseek/deepseek-v3.2-exp` |
| `REACTIVE_RESUME_URL` | URL serveur Reactive Resume | `http://localhost:3000` |
| `REACTIVE_RESUME_TIMEOUT` | Timeout requêtes (s) | `30` |
| `REACTIVE_RESUME_MAX_RETRIES` | Nb max tentatives | `3` |
| `LOG_LEVEL` | Niveau de log | `INFO` |
| `PDF_QUALITY` | Qualité PDF | `high` |

### Répertoires

Vous pouvez personnaliser les répertoires dans `.env` :
- `OUTPUTS_DIR` : Où sauvegarder les documents
- `DATA_DIR` : Où trouver vos données
- `ANALYSIS_DIR` : Où stocker les analyses

---

## 🧪 Tests

```bash
# Lancer tous les tests
poetry run test

# Tests spécifiques
poetry run pytest tests/test_cv_generator.py -v
```

---

## 📊 Exemple de Sortie

```
🚀 Démarrage de l'orchestrateur CV & Lettre de Motivation
============================================================

📂 Chargement des offres...
👤 Chargement des données d'identité...
🎓 Chargement des données d'éducation...

🔍 Vérification de Reactive Resume...
  ✅ Reactive Resume est accessible

============================================================
🎯 Traitement de l'offre: Offre_Stage_IA
============================================================

🔍 Analyse de l'offre: Offre_Stage_IA
  ✅ Analyse terminée

📋 Génération du CV pour: Offre_Stage_IA
  📝 Génération du CV par IA...
  ✅ CV JSON généré avec succès

📤 Envoi à Reactive Resume...
  ✅ PDF généré: outputs/Offre_Stage_IA_cv.pdf

✍️ Génération de la lettre de motivation pour: Offre_Stage_IA
  ✅ Lettre générée: outputs/Offre_Stage_IA_lettre.md

✅ Offre Offre_Stage_IA traitée!
   📄 CV: outputs/Offre_Stage_IA_cv.pdf
   📝 Lettre: outputs/Offre_Stage_IA_lettre.md
```

**Fichiers générés dans `outputs/` :**
- `Offre_Stage_IA_cv.pdf` - CV personnalisé au format PDF
- `Offre_Stage_IA_cv.json` - CV au format JSON (debug)
- `Offre_Stage_IA_lettre.md` - Lettre de motivation en Markdown

---

## 🔍 Dépannage

### Erreur "OPENROUTER_API_KEY non définie"

```bash
# Vérifiez que le fichier .env existe
ls -la .env

# Vérifiez son contenu
cat .env | grep OPENROUTER_API_KEY
```

### Erreur "Reactive Resume non accessible"

```bash
# Vérifiez que Docker est démarré
docker ps

# Vérifiez le conteneur Reactive Resume
docker ps | grep reactive-resume

# Redémarrez si nécessaire
docker-compose restart
```

### Erreur "Configuration invalide"

```bash
# Validez votre .env
python -c "from src.config.settings import validate_config; validate_config()"
```

### Erreur "ModuleNotFoundError"

```bash
# Réinstallez les dépendances
poetry install

# Ou installez manuellement
pip install -r requirements.txt
```

---

## 📚 Documentation Complète

- **[Guide de Démarrage](README_START.md)** - Démarrage étape par étape
- **[Génération PDF](docs/PDF_GENERATION_GUIDE.md)** - Détails sur Reactive Resume
- **[Format JSON](docs/JSON_FORMAT_GUIDE.md)** - Schéma Reactive Resume
- **[Client Reactive Resume](docs/CLIENT_REACTIVE_RESUME.md)** - API client avancée
- **[OpenRouter](docs/openrouter.md)** - Configuration IA
- **[Changelog](CHANGELOG.md)** - Historique des versions

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Veuillez :

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Standards de Code

- **PEP 8** pour Python
- **Type hints** requis
- **Tests** pour nouvelles fonctionnalités
- **Documentation** mise à jour

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 🆘 Support

- **Issues GitHub** : [Créer une issue](https://github.com/votre-repo/issues)
- **Documentation** : Consultez le dossier `docs/`
- **Chat** : Discord/Slack (lien à ajouter)

---

## 🎯 Fonctionnalités Futures

- [ ] Interface web graphique
- [ ] Support multi-langues
- [ ] Templates de CV additionnels
- [ ] Intégration ATS (LinkedIn,Indeed)
- [ ] API REST pour intégration externe
- [ ] Base de données pour historique
- [ ] Génération de portfolios

---

**Développé avec ❤️ pour automatiser votre recherche d'emploi**

⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile !
