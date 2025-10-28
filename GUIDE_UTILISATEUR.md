# 🎯 Orchestrateur CV & Lettre de Motivation - GUIDE COMPLET

## ✅ Statut du Projet

**INFRASTRUCTURE PRÊTE** - Tous les composants sont configurés :

- ✅ **Pipeline Python** - Orchestrateur + Agents spécialisés avec IA
- ✅ **Dépendances** - aiofiles, aiohttp, PyPDF2, pydantic installés
- ✅ **Structure** - Offres à traiter détectées
- ✅ **Configuration centralisée** - Via .env et settings.py
- ✅ **Client robuste** - ReactiveResumeClient avec retry et health check
- ⏳ **Préqui** - Configuration OpenRouter + Reactive Resume nécessaire

### ✨ Nouvelles Fonctionnalités (v2.0)

- 🔄 **Retry automatique** : 3 tentatives avec backoff exponentiel
- 🏥 **Health check** : Vérification automatique de Reactive Resume
- 📊 **Logging structuré** : Traçabilité complète des opérations
- 💾 **Fallback intelligent** : Sauvegarde JSON si PDF échoue
- ⚙️ **Configuration centralisée** : Variables d'environnement validées
- 🛡️ **Gestion d'erreurs** : Messages explicites avec conseils

---

## 🚀 ÉTAPES DE LANCEMENT

### ÉTAPE 1: Configuration du Projet (OBLIGATOIRE)

**1. Configurez vos variables d'environnement :**

```bash
# Copiez le fichier d'exemple
cp .env.example .env

# Éditez .env avec vos paramètres :
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
REACTIVE_RESUME_URL=http://localhost:3000
```

**2. Obtenez votre clé API OpenRouter :**

1. **Créer un compte** : https://openrouter.ai
2. **Générer une clé** : https://openrouter.ai/keys
3. **Ajouter des crédits** (recommandé: $5-10 minimum)

**3. Validation de la configuration :**

```bash
# Installez les dépendances
poetry install
# ou
pip install pydantic

# Testez la configuration
python -c "from src.config.settings import validate_config; validate_config(); print('✅ Configuration valide')"
```

---

### ÉTAPE 2: Démarrage Reactive Resume (pour PDF)

**Option A - Docker Compose (recommandé) :**
```bash
docker-compose up -d
```

**Option B - Docker seul :**
```bash
# Démarrez Docker (Docker Desktop)
docker run -d --name reactive-resume -p 3000:3000 amrithpillai/reactive-resume:latest

# Vérifiez que c'est actif
curl http://localhost:3000/api/health
```

**Option C - Script automatisé :**
```bash
./start_reactive_resume.sh
```

**Note :** Si Reactive Resume n'est pas démarré, le pipeline :
1. Le détectera automatiquement via health check
2. Affichera un message d'aide
3. Sauvegardera les CVs en JSON (fallback intelligent)

---

### ÉTAPE 3: Installation des Dépendances

```bash
# Avec Poetry (recommandé)
poetry install

# Ou avec pip
pip install -r requirements.txt
```

---

### ÉTAPE 4: Lancement du Pipeline

**Option A - Poetry (recommandé) :**
```bash
poetry run start
```

**Option B - Script automatisé :**
```bash
./run_pipeline.sh
```

**Option C - Lancement direct :**
```bash
python src/main.py
```

Le pipeline vérifiera automatiquement :
- ✅ Configuration OpenRouter
- ✅ Santé de Reactive Resume
- ✅ Dossiers de données
- ✅ Fichiers d'offres

---

## 📊 CE QUE FAIT LE PIPELINE

### Pour chaque offre :

1. **📄 Extraction PDF**
   - Lecture du contenu du fichier PDF
   - Extraction du texte brut avec PyPDF2

2. **🤖 Analyse IA (OpenRouter)**
   - Analyse des 8 points de vigilance
   - Génération d'un rapport markdown détaillé
   - Sauvegarde dans `offres/offer_analysis/[nom_offre].md`

3. **🎯 Extraction des Thèmes**
   - Identification des mots-clés pertinents
   - Liste Python pour contextualisation

4. **📋 Génération CV**
   - Création du JSON au format Reactive Resume
   - Contexte intelligent basé sur l'offre
   - **Nouveau :** Vérification health check avant génération
   - **Nouveau :** Retry automatique en cas d'échec
   - Envoi à Reactive Resume pour PDF
   - **Fallback :** Sauvegarde JSON si PDF échoue

5. **✍️ Génération Lettre de Motivation**
   - Rédaction personnalisée en Markdown
   - Ton professionnel et chaleureux
   - 250-400 mots

6. **🔄 Mise à jour du Statut**
   - Booléen passe à `true` dans `offres.json`
   - Traçabilité des offres traitées

### 🆕 Fonctionnalités Robustesse (v2.0)

**Health Check Automatique :**
```
🔍 Vérification de Reactive Resume...
  ✅ Reactive Resume est accessible
```

**Retry avec Backoff Exponentiel :**
```
⚠️ Tentative 1/3 échouée: timeout
⏳ Retry dans 1s...
✅ PDF généré avec succès
```

**Fallback Intelligent :**
```
⚠️ Reactive Resume non disponible
💾 Sauvegarde du JSON à la place
✅ JSON sauvegardé: outputs/mon_cv.json
```

**Validation de Configuration :**
```
Configuration invalide:
- OPENROUTER_API_KEY est requise
❌ Erreur: Vérifiez votre fichier .env
```

---

## 📁 STRUCTURE DES SORTIES

```
outputs/
├── Guiding_in_Visible_internship_2026_cv.pdf
├── Guiding_in_Visible_internship_2026_lettre.md
├── IE-SCUBA_cv.pdf
├── IE-SCUBA_lettre.md
├── Internship_6_months_Microfluidic_cv.pdf
├── Internship_6_months_Microfluidic_lettre.md
├── Offre-de-stage-Master-25-26-HBIS_cv.pdf
├── Offre-de-stage-Master-25-26-HBIS_lettre.md
├── PhD-proposal-SiC-biosensors_GIMED_v2_cv.pdf
├── PhD-proposal-SiC-biosensors_GIMED_v2_lettre.md
├── sanfrancisco_1st_offer_cv.pdf
├── sanfrancisco_1st_offer_lettre.md
├── Sujet-master-CREATIS_cv.pdf
└── Sujet-master-CREATIS_lettre.md
```

**Fichiers d'analyse :**
```
offres/offer_analysis/
├── Guiding_in_Visible_internship_2026.md
├── IE-SCUBA.md
├── Internship_6_months_Microfluidic.md
├── Offre-de-stage-Master-25-26-HBIS.md
├── PhD-proposal-SiC-biosensors_GIMED_v2.md
├── sanfrancisco_1st_offer.md
└── Sujet-master-CREATIS.md
```

---

## ⚡ TEMPS D'EXÉCUTION ESTIMÉ

- **Par offre** : 2-3 minutes
- **Total (7 offres)** : 15-20 minutes

Répartition :
- Extraction PDF : 5-10s
- Analyse IA : 60-90s
- Génération CV : 30-60s
- Génération Lettre : 20-40s

---

## 🛠️ ARCHITECTURE TECHNIQUE

### Composants Principaux

1. **`src/main.py`**
   - Orchestrateur principal
   - Gestion du workflow complet
   - Mise à jour des statuts
   - Utilise la configuration centralisée

2. **`src/agents/offer_analyzer.py`**
   - Extraction PDF (PyPDF2)
   - Analyse IA (OpenRouter)
   - Génération des thèmes

3. **`src/agents/cv_generator.py`**
   - Génération JSON Reactive Resume
   - Contexte intelligent
   - **Nouveau :** Utilise ReactiveResumeClient
   - **Nouveau :** Health check intégré
   - **Nouveau :** Logging structuré

4. **`src/agents/letter_generator.py`**
   - Rédaction de lettres personnalisées
   - Format Markdown
   - Ton configurable

5. **`src/utils/openrouter_client.py`**
   - Client OpenRouter
   - Gestion des appels API
   - Retry & error handling

6. **`src/utils/reactive_resume_client.py` (NOUVEAU)**
   - Client robuste pour Reactive Resume
   - Flux API correct : POST /api/resume/import → GET /api/resume/print/{id}
   - Structure de données wrapper : {title, slug, visibility, data}
   - Retry automatique avec backoff exponentiel
   - Gestion d'erreurs avancée (ReactiveResumeError)
   - Health check et validation
   - Support des timeouts configurables

7. **`src/config/settings.py` (NOUVEAU)**
   - Configuration centralisée avec Pydantic
   - Support des variables d'environnement
   - Validation automatique des configs critiques
   - Fonctions utilitaires pour accéder aux configs

### Modèle IA

- **OpenRouter** : `deepseek/deepseek-v3.2-exp`
- **Prix** : ~$0.001-0.003 par offre
- **Contexte** : 4000 tokens max

### Flux de Génération PDF (v2.0)

```
CV JSON → ReactiveResumeClient
          ↓
    1. POST /api/resume/import (création avec wrapper title/slug/visibility/data)
          ↓
    2. Attente traitement (2s)
          ↓
    3. GET /api/resume/print/{id} (PDF)
          ↓
    4. Sauvegarde locale
```

**En cas d'échec :**
- Retry automatique (3 tentatives)
- Backoff exponentiel (1s, 2s, 4s)
- Fallback JSON si PDF échoue
- Logging détaillé pour débogage

---

## 🔧 DÉPANNAGE

### Erreur "Configuration invalide" (NOUVEAU)
```bash
# Le pipeline valide automatiquement la configuration au démarrage
# Vérifiez votre .env :

cat .env | grep OPENROUTER_API_KEY
# Doit afficher: OPENROUTER_API_KEY=sk-or-v1-...

# Test manuel :
python -c "from src.config.settings import validate_config; validate_config()"

# Si erreur :
cp .env.example .env
# Puis éditez .env avec vos vraies valeurs
```

### Erreur "OPENROUTER_API_KEY non définie"
```bash
# Vérifiez que le fichier .env existe
ls -la .env

# Vérifiez son contenu
cat .env | grep OPENROUTER_API_KEY

# Si vide, recréez-le
cp .env.example .env
# Puis éditez .env avec votre clé
```

### Erreur "Reactive Resume non accessible"
```bash
# Le pipeline affiche automatiquement les conseils :
# 💡 Assurez-vous que le serveur est démarré sur le port 3000
# 💡 URL attendue: http://localhost:3000
# 💡 Démarrez avec: docker-compose up -d

# Vérifications manuelles :
docker ps | grep reactive-resume

# Redémarrez le conteneur
docker-compose restart
# ou
docker restart reactive-resume

# Ou recréez-le
docker rm -f reactive-resume
docker run -d --name reactive-resume -p 3000:3000 amrithpillai/reactive-resume:latest

# Test manuel :
curl http://localhost:3000/api/health
```

### Erreur "Timeout lors de la génération du PDF" (NOUVEAU)
```bash
# Augmentez le timeout dans .env :
REACTIVE_RESUME_TIMEOUT=60

# Le client retry automatiquement (3 tentatives)
# Vous pouvez modifier le nombre de tentatives :
REACTIVE_RESUME_MAX_RETRIES=5
```

### Erreur "ModuleNotFoundError"
```bash
# Réinstallez les dépendances avec pydantic
poetry install
# ou
pip install -r requirements.txt --force-reinstall
# ou installez manuellement
pip install pydantic aiofiles aiohttp PyPDF2
```

### Erreur "Permission denied" (Linux/Mac)
```bash
chmod +x run_pipeline.sh
chmod +x start_reactive_resume.sh
```

### Erreur "aiofiles non disponible" (NOUVEAU)
```bash
# Le pipeline fonctionnera en mode fallback synchrone
# Installez aiofiles pour meilleures performances :
pip install aiofiles
# ou
poetry add aiofiles
```

### Logs de Débogage (NOUVEAU)

**Activez le mode DEBUG :**
```bash
# Dans .env
LOG_LEVEL=DEBUG

# Puis relancez
poetry run start
```

**Consultez les logs en temps réel :**
```python
# Le pipeline log automatiquement :
# [INFO] ReactiveResumeClient: Resume créé avec succès
# [WARNING] Tentative 1/3 échouée: timeout
# [ERROR] Erreur Reactive Resume: Connection refused
```

### Santé du Système (NOUVEAU)

**Test complet de la configuration :**
```bash
python -c "
from src.config.settings import validate_config
from src.utils.reactive_resume_client import ReactiveResumeClient
import asyncio

async def test():
    try:
        validate_config()
        print('✅ Configuration OK')

        client = ReactiveResumeClient()
        healthy = await client.check_health()
        if healthy:
            print('✅ Reactive Resume OK')
        else:
            print('⚠️ Reactive Resume non accessible')
    except Exception as e:
        print(f'❌ Erreur: {e}')

asyncio.run(test())
"
```

---

## 📞 SUPPORT

Si vous rencontrez des problèmes :

1. **Vérifiez la configuration** : `python -c "from src.config.settings import validate_config; validate_config()"`
2. **Consultez les logs** complets dans le terminal (mode DEBUG disponible)
3. **Health check** : Le pipeline vérifie automatiquement Reactive Resume
4. **Test manuel** : Utilisez le script de test de santé du système
5. **Documentation** : Consultez `docs/CLIENT_REACTIVE_RESUME.md`
6. **Credits OpenRouter** : Vérifiez vos crédits sur openrouter.ai

### Nouveautés v2.0 à Retenir

✅ **Configuration centralisée** : Tout est dans `.env` et `settings.py`
✅ **Retry automatique** : Plus besoin de relancer manuellement
✅ **Fallback intelligent** : JSON sauvegardé si PDF échoue
✅ **Messages explicites** : L'application vous guide en cas de problème
✅ **Validation au démarrage** : Les erreurs sont détectées tôt

---

## 🎯 PROCHAINES ÉTAPES

1. ✅ Configuration du projet (créer .env + clé OpenRouter)
2. ✅ Démarrage Reactive Resume (docker-compose up -d)
3. ✅ Installation des dépendances (poetry install)
4. ✅ Lancement du pipeline (poetry run start)
5. ✅ Vérification des outputs (dossier outputs/)
6. ✅ Itération & amélioration (si nécessaire)

**Le pipeline est entièrement automatisé et traitera les offres sans intervention !**

### Personnalisation Avancée (Optionnel)

**Changer le template de CV :**
```python
# Dans src/agents/cv_generator.py, ligne ~102
"metadata": {
    "template": "pikachu",  # Changez: gengar, glalie, etc.
    ...
}
```

**Modifier le thème :**
```python
"theme": {
    "background": "#ffffff",
    "text": "#000000",
    "primary": "#ca8a04"  # Votre couleur
}
```

**Ajuster la qualité PDF :**
```bash
# Dans .env
PDF_QUALITY=high  # high, medium, low
```
