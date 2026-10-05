#!/usr/bin/env bash
set -e

USERNAME="${1:-dracalar}"
NOPUSH="${2:-}"

echo "=========================================================="
echo " 🐳 Docker Workshop Image Builder & Publisher"
echo " Docker Hub Namespace: $USERNAME"
echo "=========================================================="

if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed or not in PATH."
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "[ERROR] Docker Daemon is not running. Please start Docker first."
    exit 1
fi

if [ "$NOPUSH" != "--no-push" ]; then
    echo ""
    echo "[AUTH] Ensuring Docker Hub authentication..."
    docker login
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

IMAGES=(
    "docker-workshop-explore:01-explore"
    "docker-workshop-broken:02-fix-the-dockerfile"
    "docker-workshop-notebook:03-volumes"
    "docker-workshop-api:04-networking/api"
    "docker-workshop-frontend:04-networking/frontend"
    "docker-workshop-vote-api:05-compose-voting-app/vote-api"
    "docker-workshop-vote-dashboard:05-compose-voting-app/dashboard"
)

TOTAL=${#IMAGES[@]}
INDEX=1

for ITEM in "${IMAGES[@]}"; do
    NAME="${ITEM%%:*}"
    PATH_DIR="${ITEM##*:}"
    TAG="$USERNAME/$NAME:latest"
    CONTEXT="$ROOT_DIR/$PATH_DIR"

    echo ""
    echo "----------------------------------------------------------"
    echo "[$INDEX/$TOTAL] Building: $TAG"
    echo "Context : $CONTEXT"

    docker build -t "$TAG" "$CONTEXT"

    if [ "$NOPUSH" != "--no-push" ]; then
        echo "Pushing $TAG to Docker Hub..."
        docker push "$TAG"
        echo "[SUCCESS] Pushed $TAG"
    fi

    INDEX=$((INDEX + 1))
done

echo ""
echo "=========================================================="
echo " 🎉 ALL $TOTAL WORKSHOP IMAGES READY!"
echo "=========================================================="
for ITEM in "${IMAGES[@]}"; do
    NAME="${ITEM%%:*}"
    echo "  ✔ $USERNAME/$NAME:latest"
done