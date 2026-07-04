#!/bin/bash
# redeploy-site.sh - Redeploy the portfolio Flask site with the latest changes from GitHub.
#
# Usage (on the VPS): ~/redeploy-site.sh

PROJECT_DIR="$HOME/mlh-task1"
VENV_DIR="python3-virtualenv"   # change if your venv folder has a different name
SESSION_NAME="flask"

# 1. Kill all existing tmux sessions (stops any running Flask server).
tmux kill-server 2>/dev/null

# 2. Go to the project folder.
cd "$PROJECT_DIR" || { echo "Project folder $PROJECT_DIR not found"; exit 1; }

# 3. Sync the repo with the latest main branch on GitHub.
git fetch && git reset origin/main --hard

# 4. Enter the python virtual environment and install dependencies.
source "$VENV_DIR/bin/activate"
pip install -r requirements.txt
deactivate

# 5. Start a new detached tmux session that enters the project directory,
#    activates the venv, and starts the Flask server.
tmux new-session -d -s "$SESSION_NAME" \
    "cd $PROJECT_DIR && source $VENV_DIR/bin/activate && flask run --host=0.0.0.0"

echo "Redeployment complete. Site should be live shortly."
