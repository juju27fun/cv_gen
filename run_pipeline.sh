#!/bin/bash
# Script de vérification et lancement du pipeline

echo "🚀 Orchestrateur CV & Lettre de Motivation"
echo "=========================================="
echo ""

# Vérification de la clé API
echo "1. Vérification de la clé OpenRouter..."
if [ -z "$OPENROUTER_API_KEY" ]; then
    if [ -f ".env" ]; then
        echo "   📝 Chargement du fichier .env..."
        export $(grep -v '^#' .env | xargs)
    fi
fi

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "   ❌ OPENROUTER_API_KEY non définie!"
    echo "   💡 Configurez-la dans .env (voir .env.example)"
    echo ""
    echo "   Étapes:"
    echo "   1. cp .env.example .env"
    echo "   2. Éditez .env et ajoutez votre clé OpenRouter"
    echo "   3. Relancez ce script"
    exit 1
else
    echo "   ✅ Clé OpenRouter configurée"
fi

# Vérification des dépendances Python
echo ""
echo "2. Vérification des dépendances Python..."
python -c "import aiofiles, aiohttp, PyPDF2" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ Dépendances installées"
else
    echo "   ⚠️ Installation des dépendances..."
    pip install -r requirements.txt
fi

# Vérification de Reactive Resume
echo ""
echo "3. Vérification de Reactive Resume..."
curl -s http://localhost:3000/api/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Reactive Resume accessible"
else
    echo "   ⚠️ Reactive Resume non accessible"
    echo "   💡 Démarrez-le avec: ./start_reactive_resume.sh"
    echo "   💡 Ou manuellement:"
    echo "      docker run -d --name reactive-resume -p 3000:3000 amrithpillai/reactive-resume:latest"
    echo ""
    read -p "Voulez-vous continuer sans Reactive Resume? (Les CVs ne seront pas générés en PDF) [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Lancement du pipeline
echo ""
echo "4. Lancement du pipeline..."
echo "=========================================="
echo ""

python src/main.py

echo ""
echo "✅ Pipeline terminé!"
echo "📁 Consultez les résultats dans outputs/"
