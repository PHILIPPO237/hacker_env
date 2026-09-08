#!/bin/bash
# update.sh — Recupere les derniers changements depuis GitHub ET regenere
# immediatement ta config shell (.zshrc/.bashrc). Une seule commande.
#
# Usage :
#   bash update.sh

set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "→ Recuperation des dernieres modifications depuis GitHub..."
git pull origin main --no-rebase

echo "→ Regeneration de la config shell (--repair)..."
python3 main.py --repair

echo ""
echo "✓ Mise a jour terminee."
echo "  Tape 'exec zsh' (ou 'exec bash') maintenant pour recharger ton shell,"
echo "  ou ferme et rouvre simplement ton terminal."
