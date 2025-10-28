# AGENTS.md

## Vision

Générer automatiquement un **CV** et une **lettre de motivation** adaptés à une offre (lien ou fichier), avec IA agentique, exportables et éditables.

## Stack Technique

- **Python** (poetry, pyenv)
- **LLM via OpenRouter** (agents outillés)
- **Reactive Resume server** (port **3000**) pour rendu CV à partir d'un JSON
- **Stockage/FS** simple (local) + connecteurs web
- Se référer à `docs/` pour les détails fonctionnels et `Prompts/`pour les prompts

## Architecture (générale)

```
src/
tests/
docs/
```

## Entités

- **JobOffer** : source (url/path), texte, mots-clés, thèmes
- **CandidateProfile** : compétences, expériences, éducation
- **Experience** : pro/scolaire, tags, preuves
- **ResumeJSON** : schéma Reactive Resume (entrée rendu)
- **DocumentBundle** : CV (json/pdf) + Lettre (md/pdf)

## Flux Principal

1. **Ingestion** : offre depuis **URL** ou **path** (web search IA ou FS).
2. **Analyse** : extraction **mots-clés** + **thèmes** (LLM).
3. **Récupération** : sélection d’expériences pertinentes (matching par thèmes).
4. **Rédaction parallèle** :

   - CV → **ResumeJSON** → rendu via Reactive Resume (PDF/JSON)
   - **Lettre** ciblée (structure standard, ton configurable)

5. **Export & Feedback** : fichiers en `outputs/` + itération possible.

## Conventions

- **Config** : `.env` (jamais commit). Ports & clés centralisés dans `config/`.
- **Logging** : structuré, pas de `print`. Traces minimalistes sur étapes critiques.
- **Prompts** : versionnés sous `Prompts/` (source de vérité).

## Qualité & Tests

- Tests unitaires sur **domain** et **pipelines**.
- Fixtures d’offres et de profils (voir `docs/`).
- Contrôles basiques : longueur, duplication, cohérence mots-clés.

## Commandes

```bash
pyenv local <version>
poetry install
poetry run start         # lance orchestrateur/API/CLI
poetry run test          # tests
```

## Règles Agents

- **Pattern** : validate → plan → act → reflect (réessais idempotents).
- **Ne pas figer** le framework HTTP/DB : rester modulaire.
- **Timeouts & rate-limits** gérés côté tools (OpenRouter).
- **Reactive Resume** doit être joignable (port **3000**) avant rendu.
- **Docs-first** : alignement systématique avec `docs/` pour variantes et prompts.

### Développement & Tests

- **Code minimal** : uniquement le nécessaire, testé et aligné conventions
- **Documentation** : modifier fichiers existants uniquement
- **Solutions directes** : implémentation immédiate, pas de sur-ingénierie

### Contraintes Opérationnelles

- **Langue** : français obligatoire
- **Git** : interdiction de `git reset` sans validation humaine
- **Sécurité** : aucun contournement des contrôles d'accès
- **Performance** : optimisation prioritaire, monitoring obligatoire

### Exécution des AGENTS IA

- **Autonomie complète** : les agents doivent s'exécuter de manière autonome jusqu'à completion de la tâche
- **Arrêt automatique** : stop automatique lorsque la tâche est terminée (sauf questions critiques pour l'humain)
- **Précision des tools** : appels de tools précis et exacts, sans exposition dans les réponses à l'utilisateur
- **Efficacité opérationnelle** : chaque action doit être justifiée et orientée résultat

### Exigences Techniques

- **Reactive Resume** doit être joignable (port **3000**) avant rendu.
