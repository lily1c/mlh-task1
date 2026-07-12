#!/bin/bash
# redeploy-site.sh - Redeploy the portfolio Flask site with the latest changes from GitHub.
#
# Usage (on the VPS): ~/redeploy-site.sh

PROJECT_DIR="$HOME/mlh-task1"
VENV_DIR="python3-virtualenv"   # change if your venv folder has a different name

# 1. Go to the project folder.
cd "$PROJECT_DIR" || { echo "Project folder $PROJECT_DIR not found"; exit 1; }

# 2. Sync the repo with the latest main branch on GitHub.
git fetch && git reset origin/main --hard

# 3. Enter the python virtual environment and install dependencies.
source "$VENV_DIR/bin/activate"
pip install -r requirements.txt
deactivate

# 4. Restart the myportfolio systemd service.
systemctl restart myportfolio

echo "Redeployment complete. Site should be live shortly."