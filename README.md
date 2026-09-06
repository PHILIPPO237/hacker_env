# HACKER_ENV V2

Outil de personnalisation de terminal multi-plateforme, écrit en Python.
Bannières, thèmes de couleurs, styles de prompt et alias — tout se configure
via un assistant interactif, avec sauvegarde automatique de tes configs
existantes (`.zshrc`, `.bashrc`, `.profile`).

Développé par **PIPO237** — [Laboratoire du Free-Surf](https://github.com/PHILIPPO237)

## Plateformes supportées

- **Termux** (Android)
- **WSL** (Windows Subsystem for Linux)
- **Linux** natif

Détection automatique de la plateforme au lancement — aucune config manuelle
requise.

## Fonctionnalités

- 🎨 **30 modèles de bannières** — chacun avec son propre cadre et sa propre
  palette de couleurs (Cyberpunk, Sakura, Blood Moon, Ocean Deep, Solar Flare,
  Royal Gold, etc.)
- 🌈 **24 thèmes de couleurs** au total, appliqués à l'ensemble de
  l'interface (dashboard, menus, bannières)
- ⌨️ **10 styles de prompt** (Hacker Neon, Cyberpunk, Powerline, Anime,
  Steampunk...) avec aperçu réel avant de choisir
- 📊 **Dashboard système** — CPU, mémoire, disque, infos plateforme, avec
  barres de progression et largeur adaptée à ton terminal
- 🧩 **Modules d'alias** activables/désactivables à la carte
- 💾 Sauvegarde automatique de tes fichiers de config avant toute modification

## Installation

Aucune dépendance externe requise (Python standard uniquement).

### Termux (Android)

```bash
pkg install python git -y
git clone https://github.com/PHILIPPO237/hacker_env.git
cd hacker_env
bash install.sh
```

### WSL / Linux (PC)

```bash
sudo apt install python3 python3-pip git -y
git clone https://github.com/PHILIPPO237/hacker_env.git
cd hacker_env
bash install.sh
```

Le script `install.sh` détecte automatiquement la plateforme, vérifie
Python/pip, sauvegarde tes configs shell existantes, puis lance
l'application.

## Utilisation

```bash
python3 main.py              # Lance l'assistant interactif complet
python3 main.py --dashboard  # Affiche uniquement le dashboard système
python3 main.py --repair     # Régénère la config shell
python3 main.py --update     # Met à jour les modules installés
python3 main.py --setup      # Configuration spécifique à la plateforme
python3 main.py --version    # Affiche la version
```

## Structure du projet

```
hacker_env/
├── main.py              # Point d'entrée, assistant interactif
├── install.sh           # Script d'installation multi-plateforme
├── core/                # Détection plateforme, couleurs, effets, config
├── ui/                  # Dashboard et menus
├── modules/             # Bannières, prompts, alias
├── platforms/           # Logique spécifique Termux / WSL / Linux
└── themes/               # Définitions de thèmes visuels
```

## Licence

Projet personnel — tous droits réservés à PIPO237, sauf mention contraire.
