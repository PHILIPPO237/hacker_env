# -*- coding: utf-8 -*-
"""
Cross-platform alias management for HACKER_ENV V2
Provides platform-specific aliases and functions.
"""

import os
from typing import Dict, List, Optional
from core.detector import get_platform_info


class AliasManager:
    """Manages aliases for different platforms."""
    
    # Base aliases (common to all platforms)
    BASE_ALIASES = {
        'cls': 'clear',
        '..': 'cd ..',
        '...': 'cd ../..',
        'll': 'ls -lah --color=auto',
        'la': 'ls -A --color=auto',
        'h': 'history',
        'myip': 'curl -s ifconfig.me',
        'reload': 'source ~/.zshrc',
        'grep': 'grep --color=auto',
    }
    
    # Platform-specific aliases
    PLATFORM_ALIASES = {
        'termux': {
            'install': 'pkg install',
            'update': 'pkg update && pkg upgrade',
            'upgrade': 'pkg update && pkg upgrade -y && pkg clean',
            'clean': 'pkg clean && rm -rf ~/.cache/* && rm -rf ~/.local/share/Trash/* 2>/dev/null',
        },
        'wsl': {
            'install': 'sudo apt install',
            'update': 'sudo apt update && sudo apt upgrade',
            'upgrade': 'sudo apt update && sudo apt upgrade -y',
            'clean': 'sudo apt autoremove && rm -rf ~/.cache/*',
            'sudo-keep': 'sudo -k',  # Reset sudo timeout
        },
        'linux': {
            'install': 'sudo apt install',
            'update': 'sudo apt update && sudo apt upgrade',
            'upgrade': 'sudo apt update && sudo apt upgrade -y',
            'clean': 'sudo apt autoremove && rm -rf ~/.cache/*',
        },
    }
    
    # Module aliases
    # NB : 'tmux' et 'weather' ne sont PAS ici — ils sont entierement geres
    # par des fonctions dans MODULE_FUNCTIONS ci-dessous (avec argument).
    # Les avoir aussi en simple alias provoque une collision nom-alias/
    # nom-fonction qui fait planter zsh/bash au chargement du shell
    # ("defining function based on alias" / "syntax error near unexpected token").
    MODULE_ALIASES = {
        'python': {
            'py': 'python3',
            'pip-upgrade': 'pip install --upgrade pip',
        },
    }
    
    # Module functions
    MODULE_FUNCTIONS = {
        'tmux': """
# -- TMUX ----------------------------------------------------------
tx() { tmux new-session -s "$1"; }
txl() { tmux list-sessions; }
txa() { tmux attach -t "$1"; }
tkill() { tmux kill-session -t "$1"; }
tks() { tmux kill-server; }
""",
        'backup': """
# -- SAUVEGARDE ----------------------------------------------------
backup() {
  local dest="${1:-$HOME/backup-config/config-$(date +%Y%m%d_%H%M%S).tar.gz}"
  mkdir -p "$(dirname "$dest")"
  tar -czf "$dest" ~/.zshrc ~/.bashrc ~/.oh-my-zsh ~/.tmux.conf 2>/dev/null
  echo "Sauvegarde : $dest"
  ls -lh "$dest"
}
restore() {
  local src="$1"
  if [[ -z "$src" || ! -f "$src" ]]; then
    echo "Fichier introuvable. Usage: restore <chemin>"
    return 1
  fi
  echo "Restauration en cours..."
  tar -xzf "$src" -C "$HOME" 2>/dev/null
  echo "Restaure. Recharge avec reload"
}
""",
        'weather': """
# -- METEO ----------------------------------------------------------
weather() {
  local city="${1:-Paris}"
  curl -s --max-time 5 "wttr.in/$city?format=3" || echo "Erreur meteo"
}
wttr() {
  local city="${1:-Paris}"
  curl -s --max-time 10 "wttr.in/$city" || echo "Erreur"
}
""",
        'genpass': """
# -- MOTS DE PASSE --------------------------------------------------
genpass() {
  local len="${1:-24}"
  tr -dc "A-Za-z0-9!@#$%^&*()_+?" < /dev/urandom | head -c "$len"
  echo
}
genpass-secure() {
  local len="${1:-32}"
  openssl rand -base64 48 | tr -dc "A-Za-z0-9" | head -c "$len"
  echo
}
""",
        'recon': r"""
# -- RESEAU (TON RESEAU UNIQUEMENT) ---------------------------------
scan() {
  local net="$1"
  if [[ -z "$net" ]]; then
    net=$(ip -o -f inet addr show 2>/dev/null | awk "!/ lo /{print \$4; exit}")
  fi
  if [[ -z "$net" ]]; then
    echo "Sous-reseau introuvable. Precise-le : scan 192.168.1.0/24"
    return 1
  fi
  echo "Scan du reseau : $net"
  nmap -sn "$net" 2>/dev/null || echo "nmap non installe"
}
scanall() { nmap -sS -p- -T4 -Pn "$@"; }
scanweb() { nmap -p80,443,8080,8443 -T4 "$@"; }
""",
        'python': """
# -- PYTHON ---------------------------------------------------------
venv() {
  if [[ -d .venv ]]; then
    source .venv/bin/activate && echo "Active"
  else
    python3 -m venv .venv && source .venv/bin/activate && echo "Cree et active"
  fi
}
""",
        'matrix': """
# -- MATRIX BOOT ----------------------------------------------------
matrix_boot() {
  local chars="0123456789ABCDEF"
  local end=$((SECONDS + 2))
  local cols=$(tput cols)
  local rows=$(tput lines)
  tput civis
  while [[ $SECONDS -lt $end ]]; do
    local col=$((RANDOM % cols))
    local row=$((RANDOM % rows))
    local char="${chars:$((RANDOM % 16)):1}"
    local color=$((RANDOM % 2 == 0 ? 32 : 82))
    tput cup $row $col
    printf "\033[38;5;%dm%s\033[0m" "$color" "$char"
    sleep 0.01
  done
  tput cnorm
  clear
}
""",
        'clock': r"""
# -- HORLOGE LIVE ---------------------------------------------------
autoload -Uz add-zsh-hook
_update_title() { print -Pn "\e]0;%* -- %~\a"; }
add-zsh-hook precmd _update_title
""",
    }
    
    def __init__(self, active_modules: Optional[List[str]] = None):
        """
        Initialize alias manager.
        
        Args:
            active_modules: List of modules to activate
        """
        self.platform_info = get_platform_info()
        self.active_modules = set(active_modules or [])
        self.aliases = {}
        self.functions = []
        self._build()
    
    def _build(self) -> None:
        """Build aliases and functions."""
        self.aliases = dict(self.BASE_ALIASES)
        self.functions = []
        
        # Add platform-specific aliases
        platform = self.platform_info.environment
        if platform in self.PLATFORM_ALIASES:
            self.aliases.update(self.PLATFORM_ALIASES[platform])
        
        # Add module aliases and functions
        for module_name in self.active_modules:
            # Add aliases
            if module_name in self.MODULE_ALIASES:
                self.aliases.update(self.MODULE_ALIASES[module_name])
            
            # Add functions
            if module_name in self.MODULE_FUNCTIONS:
                self.functions.append(self.MODULE_FUNCTIONS[module_name])
    
    def enable_module(self, module_name: str) -> None:
        """Enable a module."""
        self.active_modules.add(module_name)
        self._build()
    
    def disable_module(self, module_name: str) -> None:
        """Disable a module."""
        self.active_modules.discard(module_name)
        self._build()
    
    def list_modules(self) -> Dict[str, Dict]:
        """List all available modules."""
        return {
            name: {
                'description': self._get_module_desc(name),
                'active': name in self.active_modules
            }
            for name in self.MODULE_FUNCTIONS.keys()
        }
    
    @staticmethod
    def _get_module_desc(name: str) -> str:
        """Get module description."""
        descriptions = {
            'tmux': 'Sessions persistantes',
            'backup': 'Sauvegarde/restauration config',
            'weather': 'Meteo dans la banniere',
            'genpass': 'Generateur de mots de passe',
            'recon': 'Outils reseau (nmap, etc.)',
            'python': 'Gestionnaire venv Python',
            'matrix': 'Effet Matrix au demarrage',
            'clock': 'Horloge dans le titre',
        }
        return descriptions.get(name, 'Module inconnu')
    
    def generate_zshrc(self) -> str:
        """Generate aliases block for .zshrc."""
        lines = ["# -- Alias ----------------------------------------------------------"]
        
        # Simple aliases
        for name, cmd in sorted(self.aliases.items()):
            lines.append(f"alias {name}='{cmd}'")
        
        # Complex functions
        if self.functions:
            lines.append("")
            for func_block in self.functions:
                lines.append(func_block.strip())
        
        return "\n".join(lines)
    
    def generate_bashrc(self) -> str:
        """Generate aliases block for .bashrc."""
        lines = ["# -- Alias ----------------------------------------------------------"]
        
        # Simple aliases
        for name, cmd in sorted(self.aliases.items()):
            lines.append(f"alias {name}='{cmd}'")
        
        # Complex functions (bash compatible)
        if self.functions:
            lines.append("")
            for func_block in self.functions:
                # Convert zsh syntax to bash if needed
                bash_func = func_block.replace('autoload -Uz add-zsh-hook', '# bashrc compatible')
                lines.append(bash_func.strip())
        
        return "\n".join(lines)


# Compatibility alias
ALIASES = AliasManager().generate_zshrc()
