#!/bin/bash
# deploy.sh — Synchronise le projet depuis le stockage partagé Android
# puis commit + push vers GitHub. Un seul script, une seule commande.
#
# Usage :
#   bash deploy.sh "message du commit"
#
# Si aucun message n'est donné, un message par defaut est utilise.

set -e

SOURCE="/storage/emulated/0/MT2/FREE-SURF/hacker_env"
DEST="$HOME/hacker_env"
MSG="${1:-Mise a jour}"

if [ -d "$SOURCE" ] && [ "$SOURCE" != "$DEST" ]; then
    echo "→ Stockage partage Android detecte, synchronisation..."
    mkdir -p "$DEST"
    cp -rf "$SOURCE"/. "$DEST"/
else
    echo "→ Pas de stockage partage Android (PC) — utilisation directe de $DEST"
    mkdir -p "$DEST"
fi

cd "$DEST"

if [ ! -d ".git" ]; then
    echo "→ Depot git non initialise, initialisation..."
    git init
    git remote add origin https://github.com/PHILIPPO237/hacker_env.git
    git branch -M main
fi

echo "→ Verification de la connexion a GitHub..."
if ! ping -c 1 -W 3 github.com &> /dev/null; then
    echo "✗ Impossible de joindre github.com (DNS ou reseau)."
    echo "  Verifie ta connexion / coupe le VPN actif et reessaie."
    exit 1
fi

echo "→ Ajout et commit des changements..."
git add .
if git diff --cached --quiet; then
    echo "  (rien de nouveau a committer)"
else
    git commit -m "$MSG"
fi

echo "→ Envoi vers GitHub..."
git push -u origin main

echo "✓ Deploiement termine."
