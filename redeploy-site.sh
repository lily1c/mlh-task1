#!/bin/bash
PROJECT_DIR="$HOME/mlh-task1"
cd "$PROJECT_DIR" || { echo "Project folder not found"; exit 1; }
git fetch && git reset origin/main --hard
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
echo "Redeployment complete."