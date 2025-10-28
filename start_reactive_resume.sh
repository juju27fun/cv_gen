#!/bin/bash
# Script de démarrage de Reactive Resume

echo "🚀 Démarrage de Reactive Resume..."

# Vérification que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    exit 1
fi

# Vérification que Docker est en cours d'exécution
if ! docker info &> /dev/null; then
    echo "⚠️ Docker n'est pas en cours d'exécution, tentative de démarrage..."
    # Démarrage de Docker Desktop sur Windows
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        echo "⏳ Attente du démarrage de Docker (30 secondes)..."
        sleep 30
    fi
fi

# Lancement de Reactive Resume
echo "📦 Lancement du conteneur Reactive Resume..."
docker run -d \
    --name reactive-resume \
    -p 3000:3000 \
    --restart unless-stopped \
    amruthpillai/reactive-resume:latest

echo "✅ Reactive Resume démarré sur http://localhost:3000"
echo "⏳ Attente que le service soit prêt (15 secondes)..."
sleep 15

# Test de connectivité
echo "🔍 Test de connectivité..."
if curl -s http://localhost:3000/api/health > /dev/null 2>&1; then
    echo "✅ Reactive Resume est accessible!"
else
    echo "⚠️ Reactive Resume peut prendre plus de temps à démarrer"
    echo "💡 Vérifiez manuellement: http://localhost:3000"
fi
