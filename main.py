#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HACKER_ENV V2 — Cross-Platform Terminal Environment
Supports Termux, WSL, and native Linux.
"""

import os
import sys
import json
import shutil
import random
import argparse
import shlex
import time
from datetime import datetime

# Import core modules
from core.colors import NeonTheme, Neon
from core.effects import (
    typewrite, typewrite_async, scanline, clear,
    spinner, stop_spinner, glitch_text, rainbow_line,
    pulse_text, matrix_intro, explode_text,
    draw_frame, print_title_neon, print_end_neon,
    print_success, print_warn, print_error, print_info,
    confetti_rain, boot_sequence, neon_buzz, fade_in_color, typewrite_cursor
)
from core.system import (
    run_cmd, install_package, check_and_install_deps,
    check_space, check_internet, get_system_info
)
from core.detector import get_platform_info, is_termux, is_wsl, is_linux
from core.config import get_config_manager
from core.backup import get_backup_manager

# Import platform modules
from platforms.manager import get_platform_manager

# Import UI modules
from ui.dashboard import display_dashboard
from ui.menu import create_main_menu, display_message

# Import modules
from modules.banners import BannerGallery
from modules.prompts import PromptGallery
from modules.aliases import AliasManager

# Import intro and effects
from core.intro import show_splash, show_author_presentation, show_name_preview
from core.bigfont import render_big_text, render_big_text_joined, fits_width
from core.guide import Guide

# Import themes
from themes import get_theme, list_themes


class HackerEnv:
    """Main class for HACKER_ENV V2."""
    
    VERSION = "2.0"
    AUTHOR = "PIPO237"
    
    def __init__(self):
        """Initialize HACKER_ENV."""
        # Get platform info
        self.platform_info = get_platform_info()
        
        # Get managers
        self.config = get_config_manager()
        self.backup = get_backup_manager()
        self.platform = get_platform_manager()
        
        # Load configuration
        self.user_name = self.config.get('user_name', 'Hacker')
        self.theme_name = self.config.get('theme', 'cyber')
        self.model_choice = self.config.get('banner_model', '1')
        self.prompt_style = self.config.get('prompt_style', '1')
        self.active_modules = self.config.get('modules', ['tmux', 'backup', 'weather', 'genpass', 'python'])
        self.use_name_as_big_art = self.config.get('use_name_as_big_art', False)
        self.use_custom_name_in_prompt = self.config.get('use_custom_name_in_prompt', False)
        
        # Initialize theme
        self.theme = NeonTheme(self.theme_name)
        
        # Initialize guide
        self.guide = Guide(self.theme, total_steps=7)
        
        # Create necessary directories
        os.makedirs(self.config.get_backup_dir(), exist_ok=True)
        os.makedirs(self.config.get_log_dir(), exist_ok=True)
    
    def show_intro(self):
        """Show introduction screen."""
        show_author_presentation(
            self.theme,
            author=self.AUTHOR,
            project_name="HACKER_ENV V2",
            version=self.VERSION
        )
        show_splash(
            self.theme,
            version=self.VERSION,
            edition="Cross-Platform Edition"
        )
    
    def stage_check(self):
        """System check stage."""
        self._stage_transition("0", "SYSTEM CHECK", self.theme.get('ORANGE', True))
        
        print_title_neon(
            "Diagnostics", "Space, Connection & Dependencies",
            self.theme.get('ORANGE'), self.theme.get('YELLOW'),
            self.theme
        )
        
        # Display platform info
        print_info(f"Plateforme : {self.platform_info.os_name}", "🖥️")
        print_info(f"Environnement : {self.platform_info.environment.upper()}", "🌐")
        print_info(f"Shell : {self.platform_info.shell}", "💻")
        print_info(f"Architecture : {self.platform_info.architecture}", "⚙️")
        
        # Check space
        ok, avail_mb = check_space(500)
        if ok:
            print_success(f"{avail_mb} Mo disponibles - OK")
        else:
            print_error(f"Espace insuffisant : {avail_mb} Mo / 500 Mo requis")
            sys.exit(1)
        
        # Check internet
        if check_internet():
            print_success("Connexion internet - OK")
            print_info("Utile pour OhMyZsh, les plugins et la météo", "💡")
        else:
            print_warn("Pas de connexion - certaines fonctions indisponibles")
        
        # Install dependencies
        failed = check_and_install_deps()
        if failed:
            print_warn(f"Dépendances non installées : {', '.join(failed)}")
        else:
            print_success("Toutes les dépendances sont OK")
        
        print_end_neon(self.theme.get('ORANGE'), self.theme)
    
    def stage_identity(self):
        """Identity configuration stage."""
        self._stage_transition("1", "IDENTITY", self.theme.get('CYAN', True))
        self.guide.step("Identity")
        
        print_title_neon(
            "WHO ARE YOU?", "Your configuration name",
            self.theme.get('CYAN'), self.theme.get('GREEN'),
            self.theme
        )
        print_info("Ce nom sera affiché dans la bannière et l'art ASCII", "👤")
        print_info("Garde-le court (8-15 caractères) pour un rendu optimal", "💡")
        print_end_neon(self.theme.get('CYAN'), self.theme)
        
        default_name = self.user_name or "HACKER_ENV"
        self.user_name = self.guide.ask(
            "Name", default=default_name,
            help_text="Ce nom apparaît dans ta bannière de terminal. Garde-le court (8-15 caractères)."
        )
        self.guide.remember("Name", self.user_name)
        
        show_name_preview(self.theme, self.user_name)
        pulse_text(f"  ✦ Configuration enregistrée : {self.user_name}", 57, 255, 20, self.theme)
        
        # Ask about using name as big art
        if fits_width(self.user_name, 60):
            self.use_name_as_big_art = self.guide.ask_yes_no(
                f"Display '{self.user_name}' in LARGE letters (instead of fixed art)?",
                default="o",
                help_text="Par défaut, l'art ASCII décoratif est fixe. Si oui, TON nom sera affiché en grandes lettres bloc."
            )
        else:
            print_warn(f"'{self.user_name}' est trop long pour les grandes lettres sur mobile")
            self.use_name_as_big_art = False
    
    def stage_banners(self):
        """Banner selection stage — navigation libre dans la galerie."""
        self._stage_transition("2", "BANNER GALLERY", self.theme.get('PINK', True))
        self.guide.step("Banner selection")

        all_models = BannerGallery.list_all()
        total = len(all_models)

        print_title_neon(
            "BANNER GALLERY", "Choose your visual style",
            self.theme.get('PINK'), self.theme.get('PURPLE'),
            self.theme
        )
        print_info(f"{total} modèles disponibles — navigue librement, dans l'ordre que tu veux", "🎨")
        print_info("Tape un numéro pour le prévisualiser en entier (cadre, couleurs, infos)", "🔎")
        print_info("Tape 'l' pour relister, 's' pour choisir le dernier vu", "💡")
        print_info("Appuie sur Entrée pour garder ton choix actuel", "⏎")
        print_end_neon(self.theme.get('PINK'), self.theme)

        def _print_index():
            for m in all_models:
                marker = "→" if m.id == self.model_choice else " "
                c1 = self.theme.get(m.primary_color, True)
                c2 = self.theme.get(m.secondary_color, True)
                c3 = self.theme.get(m.accent_color, True)
                rst = self.theme.colors['RST']
                swatch = f"{c1}██{c2}██{c3}██{rst}"
                print(f"  {marker} {self.theme.get('CYAN', True)}{m.id:>2}{rst}) "
                      f"{swatch}  "
                      f"{self.theme.get('WHITE')}{m.name}{rst}  "
                      f"{self.theme.colors['DIM']}{m.description}{rst}")

        _print_index()

        last_seen = self.model_choice
        while True:
            raw = input(
                f"\n  {self.theme.get('CYAN')}➤  Numero a previsualiser, 'l' liste, "
                f"'s' choisir '{last_seen}' [Enter garde '{self.model_choice}']: {self.theme.colors['RST']}"
            ).strip().lower()

            if raw == "":
                break
            if raw == "l":
                _print_index()
                continue
            if raw == "s":
                self.model_choice = last_seen
                break
            if raw in BannerGallery.MODELS:
                BannerGallery.preview(raw, self.user_name, self.theme)
                last_seen = raw
                continue
            print_warn(f"'{raw}' n'est pas une commande ou un numero de modele valide (1-{total})")

        self.guide.remember("Banner", BannerGallery.get(self.model_choice).name)

        model = BannerGallery.get(self.model_choice)
        explode_text(f"  ✦ Model chosen: {model.name} (frame {model.frame_style})",
                    self.theme.get('GREEN', True), self.theme)
    
    def stage_prompt(self):
        """Prompt selection stage."""
        self._stage_transition("3", "CUSTOMIZATION", self.theme.get('PURPLE', True))
        self.guide.step("Prompt style")
        
        print_title_neon(
            "PROMPT STYLE", f"{len(PromptGallery.STYLES)} designs available",
            self.theme.get('PURPLE'), self.theme.get('PINK'),
            self.theme
        )
        print_info("La ligne qui apparaît avant chaque commande", "⌨️")
        print_info("Chaque style a un vrai aperçu ci-dessous", "👇")
        print_end_neon(self.theme.get('PURPLE'), self.theme)
        
        # Show previews
        PromptGallery.preview_all(self.theme)
        
        self.prompt_style = self.guide.ask(
            "Your choice [1-7]", default=self.prompt_style,
            help_text="1=Hacker Neon, 2=Développeur Pro, 3=Minimaliste, 4=Cyberpunk, 5=Steampunk, 6=Anime, 7=Powerline.",
            choices=[str(i) for i in range(1, len(PromptGallery.STYLES) + 1)],
        )
        self.guide.remember("Prompt", PromptGallery.get(self.prompt_style).name)
        
        style = PromptGallery.get(self.prompt_style)
        pulse_text(f"  ✦ Prompt chosen: {style.name}", 255, 0, 128, self.theme)
        
        # Ask about custom name in prompt
        self.use_custom_name_in_prompt = self.guide.ask_yes_no(
            f"Display '{self.user_name}' in prompt instead of system name?",
            default="o",
            help_text=f"Par défaut, le prompt affiche ton nom d'utilisateur système. Si oui, il affichera '{self.user_name}' à la place."
        )
    
    def stage_modules(self):
        """Module selection stage."""
        self._stage_transition("4", "FEATURES", self.theme.get('YELLOW', True))
        self.guide.step("Optional modules")
        
        print_title_neon(
            "OPTIONAL MODULES", "Enable what you want",
            self.theme.get('YELLOW'), self.theme.get('ORANGE'),
            self.theme
        )
        print_info("Réponds O (ou Entrée) pour oui, n pour non", "🎮")
        print_end_neon(self.theme.get('YELLOW'), self.theme)
        
        manager = AliasManager()
        all_modules = manager.list_modules()
        
        # Default modules
        defaults = {
            'tmux': True, 'backup': True, 'weather': True,
            'genpass': True, 'recon': False, 'python': True,
            'matrix': False, 'clock': False
        }
        
        self.active_modules = []
        for name, info in all_modules.items():
            default = "o" if defaults.get(name, False) else "n"
            tip = self._get_module_tip(name)
            
            print()
            typewrite(f"  {info['description']}", self.theme.colors['DIM'], 0.01, self.theme)
            if tip:
                print_info(tip, "💡")
            
            ans = input(f"  {self.theme.get('CYAN')}➤  Enable? [{default}/n] : {self.theme.colors['RST']}")
            ans = (ans.strip() or default).lower()
            
            if ans in ('o', 'y', 'oui', 'yes', ''):
                self.active_modules.append(name)
                explode_text("  ✦ Enabled", self.theme.get('GREEN', True), self.theme)
            else:
                print(f"  {self.theme.colors['DIM']}○ Disabled{self.theme.colors['RST']}")
    
    def _get_module_tip(self, name):
        """Module tips."""
        tips = {
            'tmux': "Essential for background processes",
            'backup': "Backup: .zshrc, font, tmux.conf, plugins",
            'weather': "Uses wttr.in - requires internet",
            'genpass': "Generate strong passwords with /dev/urandom",
            'recon': "⚠️  ONLY on networks you own",
            'python': "Create and activate virtualenvs automatically",
            'matrix': "2 seconds of Matrix animation at terminal startup",
            'clock': "Update Termux window title in real-time",
        }
        return tips.get(name, "")
    
    def stage_theme(self):
        """Theme selection stage."""
        self._stage_transition("5", "THEME", self.theme.get('GREEN', True))
        self.guide.step("Theme selection")
        
        print_title_neon(
            "THEME SELECTION", "Choose your visual style",
            self.theme.get('GREEN'), self.theme.get('CYAN'),
            self.theme
        )
        print_info("Choisis un thème pour toute l'interface", "🎨")
        print_end_neon(self.theme.get('GREEN'), self.theme)
        
        # List available themes
        available_themes = list_themes()
        for i, theme_name in enumerate(available_themes, 1):
            theme = get_theme(theme_name)
            print(f"  {self.theme.get('CYAN', True)}{i}) {theme_name}{self.theme.colors['RST']}  {self.theme.colors['DIM']}{theme.DESCRIPTION}{self.theme.colors['RST']}")
        
        print()
        choice = input(f"  {self.theme.get('CYAN')}➤  Your choice [1-{len(available_themes)}] : {self.theme.colors['RST']}").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available_themes):
                self.theme_name = available_themes[idx]
                self.theme = NeonTheme(self.theme_name)
                self.guide = Guide(self.theme, total_steps=7)
                explode_text(f"  ✦ Theme '{self.theme_name}' applied!",
                            self.theme.get('GREEN', True), self.theme)
        except (ValueError, IndexError):
            print_warn("Invalid choice, keeping current theme")
    
    def stage_recap(self):
        """Recap stage."""
        self._stage_transition("6", "RECAP", self.theme.get('GREEN', True))
        
        model = BannerGallery.get(self.model_choice)
        prompt = PromptGallery.get(self.prompt_style)
        
        print_title_neon(
            "FINAL RECAP", self.user_name,
            self.theme.get('GREEN'), self.theme.get('CYAN'),
            self.theme
        )
        if getattr(self, 'use_name_as_big_art', False):
            print_info(f"Bannière : ton nom '{self.user_name}' en grandes lettres (cadre {model.frame_style})", "🎨")
        else:
            print_info(f"Bannière : {model.name} (cadre {model.frame_style})", "🎨")
        print_info(f"Prompt : {prompt.name}", "⌨️")
        print_info(f"Thème : {self.theme_name}", "🖌️")
        
        manager = AliasManager(self.active_modules)
        for mod_name in manager.list_modules():
            active = mod_name in self.active_modules
            status = "✅ ON" if active else "❌ OFF"
            print_info(f"{mod_name:10} : {status}", self._get_module_icon(mod_name))
        
        print_end_neon(self.theme.get('GREEN'), self.theme)
        
        confirm = input(f"  {self.theme.get('CYAN')}➤  Everything correct? (O/n) [O] : {self.theme.colors['RST']}")
        if confirm.strip().lower() not in ('o', 'y', 'oui', 'yes', ''):
            print_error("Installation cancelled.")
            sys.exit(0)
    
    def _get_module_icon(self, name):
        """Module icons."""
        icons = {
            'tmux': '🖥️', 'backup': '💾', 'weather': '🌤️',
            'genpass': '🔐', 'recon': '🌐', 'python': '🐍',
            'matrix': '💊', 'clock': '⏰',
        }
        return icons.get(name, '◈')
    
    def run_installation(self):
        """Execute complete installation."""
        clear()
        rainbow_line("  ═══════════════════════════════════════════════", self.theme)
        glitch_text("  INITIALIZING INSTALLATION...", self.theme.get('PINK', True))
        scanline("█", self.theme.get('CYAN'), self.theme)
        print()
        
        # Backup existing configurations
        self.backup.backup_shell_configs('before_install')
        
        # Generate shell config
        self._generate_shell_config()
        
        # Install OhMyZsh if not present
        self._install_ohmyzsh()
        
        # Install packages
        self._install_packages()
        
        # Configure shell
        self._setup_shell()
        
        # Save configuration
        self.config.update({
            'user_name': self.user_name,
            'theme': self.theme_name,
            'banner_model': self.model_choice,
            'prompt_style': self.prompt_style,
            'modules': self.active_modules,
            'use_name_as_big_art': getattr(self, 'use_name_as_big_art', False),
            'use_custom_name_in_prompt': getattr(self, 'use_custom_name_in_prompt', False),
        })
        self.config.save()
        
        # Final report
        self._final_report()
    
    def _generate_shell_config(self):
        """Generate shell configuration file."""
        print_title_neon("Generating Config", "Shell Configuration",
                        self.theme.get('CYAN'), self.theme.get('GREEN'), self.theme)
        
        # Determine which shell config to use
        shell = self.platform_info.shell
        if shell == 'zsh':
            config_path = os.path.expanduser('~/.zshrc')
        else:
            config_path = os.path.expanduser('~/.bashrc')
        
        # Backup existing config
        if os.path.exists(config_path):
            self.backup.backup_shell_configs('before_generate')
        
        # Generate config content
        safe_user_name = shlex.quote(self.user_name).strip("'")
        
        # Header
        header = f"""# <HACKER_ENV_V2>
# ══════════════════════════════════════════════════════════════════
#  CONFIG - {safe_user_name}
#  Banner: {BannerGallery.get(self.model_choice).name}
#  Prompt: {PromptGallery.get(self.prompt_style).name}
#  Version: v{self.VERSION} | {datetime.now():%Y-%m-%d %H:%M}
#  Modules: {', '.join(self.active_modules)}
# ══════════════════════════════════════════════════════════════════
"""
        
        # OhMyZsh config (for zsh)
        if shell == 'zsh':
            header += """
export ZSH="$HOME/.oh-my-zsh"
if [ -d "$ZSH" ]; then
  ZSH_THEME="robbyrussell"
  plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
  source "$ZSH/oh-my-zsh.sh"
fi
"""
        
        # Truecolor helpers
        helpers = """
# Truecolor helpers
_rgb() { printf "\\033[38;2;%d;%d;%dm" "$1" "$2" "$3"; }
RST='\\033[0m'; BLD='\\033[1m'
"""
        
        # Colors
        model = BannerGallery.get(self.model_choice)
        c1 = self.theme.BASE_PALETTE.get(model.primary_color, (57, 255, 20))
        c2 = self.theme.BASE_PALETTE.get(model.secondary_color, (255, 255, 0))
        c3 = self.theme.BASE_PALETTE.get(model.accent_color, (0, 255, 255))
        
        colors = f"""
G="$(_rgb {c1[0]} {c1[1]} {c1[2]})"
Y="$(_rgb {c2[0]} {c2[1]} {c2[2]})"
C="$(_rgb {c3[0]} {c3[1]} {c3[2]})"
"""
        
        # Banner — si l'utilisateur a choisi d'afficher SON nom en grandes
        # lettres, on remplace l'art fixe du modèle par le rendu de son nom.
        if getattr(self, 'use_name_as_big_art', False):
            art_source = render_big_text_joined(self.user_name)
        else:
            art_source = BannerGallery.get(self.model_choice).art
        art_escaped = art_source.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')
        
        banner = f"""
# Bannière
export HACKER_ENV_MODEL="{self.model_choice}"
_banner() {{
  local G="$G" Y="$Y" C="$C" R="\\033[0m" B="\\033[1m"
  echo -e "${{G}}${{B}}{art_escaped}${{R}}"

  local title="💀  {safe_user_name} — HACK THE PLANET  💀"
  local len=$(( ${{#title}} + 4 ))

  local top="${{Y}}${{B}}{model.top_left}"
  for ((i=0;i<len;i++)); do top="${{top}}{model.horizontal}"; done
  top="${{top}}{model.top_right}${{R}}"

  local mid="${{Y}}${{B}}{model.vertical} ${{R}}${{G}}${{B}}${{title}}${{R}}${{Y}}${{B}} {model.vertical}${{R}}"

  local bot="${{Y}}${{B}}{model.bottom_left}"
  for ((i=0;i<len;i++)); do bot="${{bot}}{model.horizontal}"; done
  bot="${{bot}}{model.bottom_right}${{R}}"

  echo -e "  ${{top}}\n  ${{mid}}\n  ${{bot}}"

  local sep=""
  for ((i=0;i<50;i++)); do
    if [ $i -lt 17 ]; then sep="${{sep}}${{G}}─"
    elif [ $i -lt 34 ]; then sep="${{sep}}${{Y}}─"
    else sep="${{sep}}${{C}}─"; fi
  done
  echo -e "  ${{sep}}${{R}}"

  local DATE=$(date '+%a %d %b %Y  %H:%M')
  local UPTIME=$(uptime -p 2>/dev/null | sed 's/up //' || echo "n/a")
  local IP=$(ip route get 1.1.1.1 2>/dev/null | awk '{{print $7; exit}}' || echo "offline")
  local CPU=$(uptime | awk -F'load average:' '{{print $2}}' | cut -d',' -f1 | xargs)
  local MEM=$(free -h 2>/dev/null | awk '/^Mem:/ {{print $3"/"$2}}' || echo "n/a")
  local DISK=$(df -h / 2>/dev/null | awk 'NR==2 {{print $3"/"$2}}' || echo "n/a")

  echo -e "  ${{C}}${{B}}  📅 Date   :${{R}}  ${{DATE}}"
  echo -e "  ${{C}}${{B}}  ⏱  Uptime :${{R}}  ${{UPTIME}}"
  echo -e "  ${{C}}${{B}}  🌐 IP     :${{R}}  ${{IP}}"
  echo -e "  ${{C}}${{B}}  ⚡ CPU    :${{R}}  ${{CPU}}"
  echo -e "  ${{C}}${{B}}  🧠 RAM    :${{R}}  ${{MEM}}"
  echo -e "  ${{C}}${{B}}  💾 DISK   :${{R}}  ${{DISK}}"
  echo -e "  ${{sep}}${{R}}"
}}

clear && _banner
"""
        
        # Prompt
        custom_name = self.user_name if self.use_custom_name_in_prompt else None
        prompt_func, prompt_code, prompt_name = PromptGallery.generate_zshrc_prompt(
            self.prompt_style, custom_name=custom_name
        )
        prompt_section = f"""
# Prompt: {prompt_name}
{prompt_func}
{prompt_code}
"""
        
        # Modules
        manager = AliasManager(self.active_modules)
        modules_section = manager.generate_zshrc() if shell == 'zsh' else manager.generate_bashrc()
        
        # Help
        help_section = """
# Interactive help
help() {
  echo -e "\033[38;2;0;255;255m\033[1m═══════════════════════════════════════════════\033[0m"
  echo -e "\033[38;2;255;0;128m\033[1m  📖 GUIDE HACKER_ENV V2\033[0m"
  echo -e "\033[38;2;0;255;255m\033[1m═══════════════════════════════════════════════\033[0m\n"
  echo -e "\033[38;2;57;255;20m  AVAILABLE COMMANDS :\033[0m"
  echo -e "  \033[38;2;192;192;192m  ll, la, cls, reload, upgrade, clean, .., ...\033[0m"
  echo -e "\033[38;2;0;255;255m\033[1m═══════════════════════════════════════════════\033[0m"
}
"""
        
        # Welcome message
        welcome = f"""
# Welcome message
echo -e "\033[38;2;57;255;20m✦ \033[0m\033[38;2;0;255;255mHACKER_ENV V2 loaded. Type 'help' for guide.\033[0m"
"""
        
        # Assemble file
        config_content = header + helpers + colors + banner + prompt_section + modules_section + help_section + welcome
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print_success(f"{config_path} generated successfully!")
        print_end_neon(self.theme.get('CYAN'), self.theme)
    
    def _install_ohmyzsh(self):
        """Install OhMyZsh if not present."""
        # Only install for zsh
        if self.platform_info.shell != 'zsh':
            print_info("OhMyZsh ignoré - zsh non utilisé", "ℹ️")
            return
        
        print_title_neon("Oh My Zsh", "Installation",
                        self.theme.get('PURPLE'), self.theme.get('PINK'), self.theme)
        
        omz_path = os.path.expanduser('~/.oh-my-zsh')
        if os.path.exists(omz_path):
            print_success("OhMyZsh already installed")
        else:
            print_warn("⚠️  OhMyZsh will be downloaded from GitHub.")
            print_info("Source: https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/...", "🔗")
            confirm = input(f"  {self.theme.get('CYAN')}➤  Continue? (O/n) [O] : {self.theme.colors['RST']}")
            if confirm.strip().lower() not in ('o', 'y', 'oui', 'yes', ''):
                print_warn("OhMyZsh not installed. Custom prompt won't work.")
                print_end_neon(self.theme.get('PURPLE'), self.theme)
                return
            
            print_info("Installation en cours...", "⬇️")
            success, _, _ = run_cmd(
                'RUNZSH=no CHSH=no sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"',
                timeout=120
            )
            if success:
                print_success("OhMyZsh installed")
            else:
                print_warn("OhMyZsh installation failed (no network?)")
        
        # Plugins
        plugins_dir = os.path.expanduser('~/.oh-my-zsh/custom/plugins')
        os.makedirs(plugins_dir, exist_ok=True)
        
        for plugin, url in [
            ("zsh-autosuggestions", "https://github.com/zsh-users/zsh-autosuggestions"),
            ("zsh-syntax-highlighting", "https://github.com/zsh-users/zsh-syntax-highlighting")
        ]:
            plugin_path = os.path.join(plugins_dir, plugin)
            if os.path.exists(plugin_path):
                print_success(f"Plugin {plugin} already installed")
            else:
                print_info(f"Installation de {plugin}...", "⬇️")
                success, _, _ = run_cmd(["git", "clone", "--depth=1", url, plugin_path], timeout=60)
                if success:
                    print_success(f"Plugin {plugin} installed")
                else:
                    print_warn(f"Failed to install {plugin}")
        
        print_end_neon(self.theme.get('PURPLE'), self.theme)
    
    def _install_packages(self):
        """Install optional packages."""
        print_title_neon("Optional Packages", "Installation",
                        self.theme.get('ORANGE'), self.theme.get('YELLOW'), self.theme)
        
        packages = []
        if 'tmux' in self.active_modules:
            packages.append('tmux')
        if 'recon' in self.active_modules:
            if self.platform_info.is_termux:
                packages.extend(['nmap', 'netcat-openbsd', 'tcpdump', 'bind-tools'])
            else:
                packages.extend(['nmap', 'netcat-openbsd', 'tcpdump', 'dnsutils'])
        if 'python' in self.active_modules:
            if self.platform_info.is_termux:
                packages.extend(['python', 'python-pip'])
            else:
                packages.extend(['python3', 'python3-pip'])
        
        for pkg in packages:
            install_package(pkg)
        
        print_end_neon(self.theme.get('ORANGE'), self.theme)
    
    def _setup_shell(self):
        """Configure shell as default."""
        if self.platform_info.shell == 'zsh':
            # Configure zsh as default
            bashrc_path = os.path.expanduser('~/.bashrc')
            zsh_launch = f"\n# <HACKER_ENV_V2>\n# Launch Zsh automatically\n[ -t 1 ] && exec zsh\n"
            
            if os.path.exists(bashrc_path):
                with open(bashrc_path, 'r') as f:
                    content = f.read()
                if 'exec zsh' not in content:
                    with open(bashrc_path, 'a') as f:
                        f.write(zsh_launch)
                    print_success("Zsh configured as default shell in .bashrc")
                else:
                    print_success("Zsh already configured in .bashrc")
            else:
                with open(bashrc_path, 'w') as f:
                    f.write(zsh_launch)
                print_success(".bashrc created with auto-launch Zsh")
        else:
            print_info(f"Utilisation du shell {self.platform_info.shell}", "ℹ️")
    
    def _final_report(self):
        """Display final report."""
        clear()
        rainbow_line("  ═══════════════════════════════════════════════", self.theme)
        glitch_text("  INSTALLATION COMPLETE!", self.theme.get('GREEN', True))
        scanline("█", self.theme.get('GREEN'), self.theme)
        print()
        
        print_title_neon(
            f"✦ COMPLETE ✦", f"{self.user_name} — v{self.VERSION}",
            self.theme.get('GREEN'), self.theme.get('GOLD'),
            self.theme
        )
        
        model = BannerGallery.get(self.model_choice)
        prompt = PromptGallery.get(self.prompt_style)
        
        print_info(f"Bannière : {model.name} (cadre {model.frame_style})", "🎨")
        print_info(f"Prompt : {prompt.name}", "⌨️")
        print_info(f"Thème : {self.theme_name}", "🖌️")
        
        for mod in self.active_modules:
            print_info(f"{mod:10} : ✅ ON", self._get_module_icon(mod))
        
        print_info(f"Config : {self.config.get_config_dir()}", "⚙️")
        print_end_neon(self.theme.get('GREEN'), self.theme)
        
        confetti_rain(duration=1.2, theme=self.theme)
        
        # Tips
        print()
        typewrite("  💡 Type 'reload' to reload configuration.",
                 self.theme.get('CYAN', True), 0.02, self.theme)
        if 'backup' in self.active_modules:
            typewrite("  💡 Type 'backup' to backup your config.",
                     self.theme.get('GREEN'), 0.02, self.theme)
        if 'weather' in self.active_modules:
            typewrite("  💡 Type 'weather [city]' for weather.",
                     self.theme.get('YELLOW'), 0.02, self.theme)
        if 'genpass' in self.active_modules:
            typewrite("  💡 Type 'genpass [length]' for a password.",
                     self.theme.get('PINK'), 0.02, self.theme)
        typewrite("  💡 Type 'help' to display the complete guide.",
                 self.theme.get('GOLD', True), 0.02, self.theme)
        
        # Final menu
        print()
        scanline("═", self.theme.get('PURPLE'), self.theme)
        print_title_neon("FINAL MENU", "What do you want to do?",
                        self.theme.get('PURPLE'), self.theme.get('PINK'), self.theme)
        print_info("1) Lancer le shell (recommandé)", "🚀")
        print_info("2) Voir les alias", "📜")
        print_info("3) Voir la config générée", "📄")
        print_info("4) Quitter", "👋")
        print_end_neon(self.theme.get('PURPLE'), self.theme)
        
        choice = input(f"  {self.theme.get('CYAN')}➤  Choice [1-4] [1] : {self.theme.colors['RST']}")
        choice = choice.strip() or "1"
        
        if choice == "2":
            os.system(r"grep '^alias\|^[a-zA-Z_]*()' ~/.zshrc 2>/dev/null | head -25 || grep '^alias\|^[a-zA-Z_]*()' ~/.bashrc 2>/dev/null | head -25")
            input("\nPress Enter to launch shell...")
            os.system("exec zsh 2>/dev/null || exec bash")
        elif choice == "3":
            shell = self.platform_info.shell
            config_file = '~/.zshrc' if shell == 'zsh' else '~/.bashrc'
            os.system(f"head -80 {config_file}")
            input("\nPress Enter to launch shell...")
            os.system("exec zsh 2>/dev/null || exec bash")
        elif choice == "4":
            print(f"{self.theme.get('PINK', True)}Goodbye! 👋{self.theme.colors['RST']}")
        else:
            os.system("exec zsh 2>/dev/null || exec bash")
    
    # ═══════════════════════════════════════════════════════════════════════
    #  MODES: REPAIR, UPDATE, UNINSTALL
    # ═══════════════════════════════════════════════════════════════════════
    
    def mode_repair(self):
        """Repair mode."""
        clear()
        print_title_neon("REPAIR MODE", "Configuration restoration",
                        self.theme.get('ORANGE'), self.theme.get('YELLOW'), self.theme)
        
        config_file = self.config.get_config_dir() + '/config.json'
        if not os.path.exists(config_file):
            print_error("No saved configuration found.")
            return
        
        self._generate_shell_config()
        print_success("Shell config regenerated")
        
        # Check auto-launch
        bashrc_path = os.path.expanduser('~/.bashrc')
        if os.path.exists(bashrc_path):
            with open(bashrc_path, 'r') as f:
                if 'exec zsh' not in f.read():
                    with open(bashrc_path, 'a') as f:
                        f.write(f"\n# <HACKER_ENV_V2>\n[ -t 1 ] && exec zsh\n")
                    print_success("Auto-launch Zsh repaired in .bashrc")
        
        print_end_neon(self.theme.get('ORANGE'), self.theme)
        typewrite("  ✅ Repair complete. Restart terminal or type 'exec zsh'.",
                 self.theme.get('GREEN', True), 0.02, self.theme)
    
    def mode_update(self):
        """Update mode."""
        clear()
        print_title_neon("UPDATE MODE", "Packages, OhMyZsh, Plugins",
                        self.theme.get('BLUE'), self.theme.get('CYAN'), self.theme)
        
        print_info("Mise à jour des paquets...", "📦")
        
        manager = get_platform_manager()
        manager.update_packages()
        manager.upgrade_packages()
        
        print_success("Packages updated")
        
        # OhMyZsh
        omz_path = os.path.expanduser('~/.oh-my-zsh')
        if os.path.exists(omz_path):
            print_info("Mise à jour de Oh My Zsh...", "⬆️")
            run_cmd(["git", "-C", omz_path, "pull"], timeout=60)
        
        # Plugins
        for plugin in ['zsh-autosuggestions', 'zsh-syntax-highlighting']:
            pdir = os.path.expanduser(f"~/.oh-my-zsh/custom/plugins/{plugin}")
            if os.path.exists(pdir):
                print_info(f"Mise à jour de {plugin}...", "⬆️")
                run_cmd(["git", "-C", pdir, "pull"], timeout=60)
        
        # Regenerate config
        config_file = self.config.get_config_dir() + '/config.json'
        if os.path.exists(config_file):
            self._generate_shell_config()
            print_success("Shell config regenerated")
        
        print_end_neon(self.theme.get('BLUE'), self.theme)
        typewrite("  ✅ Update complete.", self.theme.get('GREEN', True), 0.02, self.theme)
    
    def mode_uninstall(self):
        """Uninstall mode."""
        clear()
        print_title_neon("UNINSTALL MODE", "Remove HACKER_ENV V2",
                        self.theme.get('RED'), self.theme.get('BLOOD'), self.theme)
        
        print_warn("This action is irreversible!")
        confirm = input(f"  {self.theme.get('RED')}➤  Confirm? [n/o] : {self.theme.colors['RST']}")
        
        if confirm.strip().lower() in ('o', 'y', 'oui', 'yes'):
            # Check marker before deletion
            for f in ['~/.zshrc', '~/.tmux.conf']:
                path = os.path.expanduser(f)
                if os.path.exists(path):
                    if self.backup.has_marker(path):
                        self.backup.clean_hacker_env_from_file(path)
                        print_success(f"{f} cleaned (marker found)")
                    else:
                        print_warn(f"{f} doesn't contain marker - kept for safety")
            
            # Remove config directory
            config_dir = self.config.get_config_dir()
            if os.path.exists(config_dir):
                import shutil
                shutil.rmtree(config_dir)
                print_success("Configuration removed")
            
            print_success("Files removed")
            print_info("Pour réinstaller : relance le script", "🔄")
        else:
            print_info("Désinstallation annulée.", "🚫")
        
        print_end_neon(self.theme.get('RED'), self.theme)
    
    def mode_setup_platform(self):
        """Platform-specific setup."""
        if self.platform_info.is_termux:
            from core.setup_termux import TermuxSetup
            setup = TermuxSetup(theme=self.theme, log_dir=self.config.get_log_dir())
            setup.run()
        else:
            print_info("Aucune configuration spécifique requise pour cet environnement.", "ℹ️")
    
    # ═══════════════════════════════════════════════════════════════════════
    #  UTILITIES
    # ═══════════════════════════════════════════════════════════════════════
    
    def _stage_transition(self, num, name, color):
        """Stage transition."""
        print()
        scanline("▒", color, self.theme)
        for c in ["▹", "▸", "▷", "▶"]:
            print(f"\r  {color}{c}  STAGE {num}/7  {name}{self.theme.colors['RST']}", end="")
            time.sleep(0.1)
        print()
        scanline("▒", color, self.theme)
        print()
    
    def run(self, mode=None):
        """Main entry point."""
        if mode == 'repair':
            self.mode_repair()
        elif mode == 'update':
            self.mode_update()
        elif mode == 'uninstall':
            self.mode_uninstall()
        elif mode == 'setup':
            self.mode_setup_platform()
        elif mode == 'dashboard':
            display_dashboard(self.theme)
        else:
            # Complete installation flow
            self.show_intro()
            self.stage_check()
            self.stage_identity()
            self.stage_banners()
            self.stage_prompt()
            self.stage_modules()
            self.stage_theme()
            self.stage_recap()
            self.run_installation()
    
    def show_main_menu(self):
        """Display main menu loop."""
        while True:
            clear()
            rainbow_line("  ═══════════════════════════════════════════════", self.theme)
            glitch_text("  HACKER_ENV V2", self.theme.get('GREEN', True))
            scanline("█", self.theme.get('CYAN'), self.theme)
            print()
            
            print_title_neon(
                "MAIN MENU", f"v{self.VERSION}",
                self.theme.get('PURPLE'), self.theme.get('PINK'), self.theme
            )
            dim = self.theme.colors['DIM']
            rst = self.theme.colors['RST']

            def item(line, icon, explication):
                print_info(line, icon)
                print(f"       {dim}→ {explication}{rst}")

            item("1) 🖥️  Dashboard", "📊",
                 "Juste un coup d'œil rapide : CPU, RAM, disque, infos système. Rien n'est modifié.")
            item("2) 🎨 Complete Installation", "✨",
                 "L'assistant complet : bannière, thème de couleurs, style de prompt, alias — tout en un.")
            item("3) 🔧 Platform Setup", "⚙️",
                 "Reconfigure uniquement les réglages propres à ta plateforme (Termux/WSL/Linux).")
            item("4) 🔧 Repair Mode", "🛠️",
                 "Régénère ta config shell si ton terminal affiche des erreurs au démarrage.")
            item("5) ⬆️  Update Mode", "📦",
                 "Vérifie et met à jour les modules déjà installés.")
            item("6) 🎨 Change Theme", "🎨",
                 "Change juste les couleurs de l'interface, sans repasser par tout l'assistant.")
            item("7) 🗑️  Uninstall", "💣",
                 "Retire HACKER_ENV et restaure tes anciens fichiers de config sauvegardés.")
            item("8) 👋 Quit", "🚪",
                 "Ferme le programme, aucune modification n'est faite.")
            print_end_neon(self.theme.get('PURPLE'), self.theme)
            
            choice = input(f"  {self.theme.get('CYAN')}➤  Your choice [1-8] : {self.theme.colors['RST']}").strip()
            
            if choice == "1":
                display_dashboard(self.theme)
                input(f"\n  {self.theme.get('CYAN')}Press Enter to return to menu...{self.theme.colors['RST']} ")
            elif choice == "2":
                self.show_intro()
                self.stage_check()
                self.stage_identity()
                self.stage_banners()
                self.stage_prompt()
                self.stage_modules()
                self.stage_theme()
                self.stage_recap()
                self.run_installation()
                return
            elif choice == "3":
                self.mode_setup_platform()
                input(f"\n  {self.theme.get('CYAN')}Press Enter to return to menu...{self.theme.colors['RST']} ")
            elif choice == "4":
                self.mode_repair()
                input(f"\n  {self.theme.get('CYAN')}Press Enter to return to menu...{self.theme.colors['RST']} ")
            elif choice == "5":
                self.mode_update()
                input(f"\n  {self.theme.get('CYAN')}Press Enter to return to menu...{self.theme.colors['RST']} ")
            elif choice == "6":
                self.stage_theme()
                input(f"\n  {self.theme.get('CYAN')}Press Enter to return to menu...{self.theme.colors['RST']} ")
            elif choice == "7":
                self.mode_uninstall()
                input(f"\n  {self.theme.get('CYAN')}Press Enter to return to menu...{self.theme.colors['RST']} ")
            elif choice == "8":
                print(f"{self.theme.get('PINK', True)}Goodbye! 👋{self.theme.colors['RST']}")
                return
            else:
                print_warn("Invalid choice.")
                input("Press Enter to continue...")


def _print_aide_francaise(theme):
    """Affiche une explication détaillée, en français, de chaque option."""
    c1 = theme.get('primary', True)
    c2 = theme.get('secondary', True) if hasattr(theme, 'get') else c1
    rst = theme.colors['RST']
    dim = theme.colors['DIM']

    def titre(t):
        print(f"\n  {c1}{t}{rst}")
        print(f"  {dim}{'─' * len(t)}{rst}")

    def option(flag, court, quoi, quand):
        suffixe = f"{dim} (raccourci : {court}){rst}" if court else ""
        print(f"\n  {theme.get('CYAN', True)}{flag}{rst}{suffixe}")
        print(f"    • Ce que ça fait : {quoi}")
        print(f"    • Quand l'utiliser : {quand}")

    print(f"\n  {c1}╭──────────────────────────────────────────────╮{rst}")
    print(f"  {c1}│{rst}   {theme.get('WHITE', True)}HACKER_ENV V2 — AIDE EN FRANÇAIS{rst}          {c1}│{rst}")
    print(f"  {c1}╰──────────────────────────────────────────────╯{rst}")
    print(f"\n  Toutes les commandes se lancent avec : {theme.get('CYAN')}python3 main.py <option>{rst}")
    print(f"  Sans aucune option, l'assistant interactif complet démarre.")

    titre("LES OPTIONS DISPONIBLES")

    option(
        "--dashboard", "-d",
        "Affiche uniquement le tableau de bord (CPU, RAM, disque, infos système), sans lancer tout l'assistant.",
        "Pour un simple coup d'œil rapide sur l'état de ton téléphone/PC."
    )
    option(
        "--repair", "-r",
        "Régénère ton fichier de config shell (.bashrc / .zshrc) à partir de tes choix déjà enregistrés.",
        "Si ton terminal affiche des erreurs au démarrage ou si une config a été abîmée."
    )
    option(
        "--update", "-u",
        "Vérifie et met à jour les modules/paquets utilisés par HACKER_ENV.",
        "De temps en temps, pour garder l'outil à jour."
    )
    option(
        "--setup", "-s",
        "Relance uniquement la configuration spécifique à ta plateforme (Termux, WSL, ou Linux).",
        "Si tu changes d'appareil ou si la détection de plateforme a mal fonctionné."
    )
    option(
        "--uninstall", "",
        "Désinstalle HACKER_ENV et restaure tes anciens fichiers de config (sauvegardés automatiquement à l'installation).",
        "Si tu veux tout retirer proprement."
    )
    option(
        "--version", "-v",
        "Affiche juste la version installée et la plateforme détectée.",
        "Pour vérifier rapidement quelle version tu as."
    )
    option(
        "--aide", "-a",
        "Affiche ce message d'aide en français.",
        "Quand tu ne te souviens plus d'une commande."
    )

    titre("EXEMPLES CONCRETS")
    print(f"\n    {dim}# Voir juste le dashboard{rst}")
    print(f"    {theme.get('CYAN')}python3 main.py --dashboard{rst}")
    print(f"\n    {dim}# Réparer ma config apres une erreur{rst}")
    print(f"    {theme.get('CYAN')}python3 main.py --repair{rst}")
    print(f"\n    {dim}# Lancer l'assistant complet (bannières, thèmes, prompt...){rst}")
    print(f"    {theme.get('CYAN')}python3 main.py{rst}")
    print()


def main():
    """Parse arguments and launch application."""
    parser = argparse.ArgumentParser(
        description="HACKER_ENV V2 - Environnement de terminal personnalisable (Termux/WSL/Linux)"
    )
    parser.add_argument('--repair', '-r', action='store_true',
                         help="Regenere ta config shell (.bashrc/.zshrc)")
    parser.add_argument('--update', '-u', action='store_true',
                         help="Met a jour les modules installes")
    parser.add_argument('--uninstall', action='store_true',
                         help="Desinstalle HACKER_ENV et restaure tes anciennes configs")
    parser.add_argument('--setup', '-s', action='store_true',
                         help="Relance la configuration specifique a ta plateforme")
    parser.add_argument('--dashboard', '-d', action='store_true',
                         help="Affiche seulement le tableau de bord systeme")
    parser.add_argument('--version', '-v', action='store_true',
                         help="Affiche la version installee")
    parser.add_argument('--aide', '-a', action='store_true',
                         help="Affiche l'aide detaillee en francais pour chaque option")

    args = parser.parse_args()

    app = HackerEnv()

    try:
        if args.aide:
            _print_aide_francaise(app.theme)
        elif args.version:
            print(f"HACKER_ENV V2 - Version {app.VERSION}")
            print(f"Platform: {app.platform_info.environment.upper()}")
            print(f"OS: {app.platform_info.os_name}")
        elif args.repair:
            app.run('repair')
        elif args.update:
            app.run('update')
        elif args.uninstall:
            app.run('uninstall')
        elif args.setup:
            app.run('setup')
        elif args.dashboard:
            app.run('dashboard')
        else:
            app.show_main_menu()
    except KeyboardInterrupt:
        print(f"\n{Neon.RED}[!] Cancelled by user.{Neon.RST}")
        sys.exit(0)


if __name__ == "__main__":
    main()
