# -*- coding: utf-8 -*-
"""
Module de prompts Zsh avancé
Inspiré de hacker_env.py : 7 styles, preview, personnalisation, fonctions dynamiques
"""

from dataclasses import dataclass
from typing import Optional
from core.colors import NeonTheme


@dataclass
class PromptStyle:
    """Représentation d'un style de prompt"""
    id: str
    name: str
    description: str
    preview_text: str
    prompt_func: str
    prompt_code: str


class PromptGallery:
    """Galerie des 7 styles de prompts (inspirée de hacker_env.py)"""

    STYLES = {
        "1": PromptStyle(
            id="1",
            name="Hacker Neon",
            description="Cadre double, vert néon, look old-school",
            preview_text="""
     ╔══[u0_a123]══[~/projets]═══════
     ╚══➤ ls -la""",
            prompt_func="""
_prompt_hacker() {
  local G="%F{82}" Y="%F{227}" C="%F{80}" W="%F{white}" R="%f"
  echo "${G}╔══[${Y}%n${G}]══[${C}%~${G}]${R}"
  echo "${G}╚══➤ ${W}"
}""",
            prompt_code='PROMPT="$(_prompt_hacker)"'
        ),
        "2": PromptStyle(
            id="2",
            name="Développeur Pro",
            description="Branche Git + path complet + statut modifications",
            preview_text="""
     ┌──(u0_a123@localhost)──[~/projets/app] (main ✓)
     └──➤ git status""",
            prompt_func="""
_prompt_dev() {
  local G="%F{82}" B="%F{33}" C="%F{80}" Y="%F{227}" W="%F{255}" R="%f" O="%F{208}"
  local git_info="" dirty=""
  if git rev-parse --is-inside-work-tree &>/dev/null; then
    local branch=$(git branch --show-current 2>/dev/null)
    git diff --quiet 2>/dev/null || dirty=" ✗"
    git_info="${Y}(${branch}${dirty})${R} "
  fi
  local venv_info=""
  [[ -n "$VIRTUAL_ENV" ]] && venv_info="${C}(venv)${R} "
  echo "${B}┌──[${G}%n${B}@${C}%m${B}]──[${Y}%~${B}] ${git_info}${venv_info}"
  echo "${B}└──➤ ${W}"
}""",
            prompt_code='PROMPT="$(_prompt_dev)"'
        ),
        "3": PromptStyle(
            id="3",
            name="Minimaliste",
            description="Flèche verte, discret et rapide à lire",
            preview_text="""
     → ~/projets % nano README.md""",
            prompt_func="",
            prompt_code='PROMPT="%F{82}→ %f%~ %# "'
        ),
        "4": PromptStyle(
            id="4",
            name="Cyberpunk",
            description="Néon rose/cyan, icônes, heure intégrée",
            preview_text="""
     ◈ ~/projets 14:32
     └─➤ nmap -sn 192.168.1.0/24""",
            prompt_func="""
_prompt_cyber() {
  local P="%F{198}" C="%F{51}" Y="%F{227}" W="%F{white}" R="%f"
  local time_str=$(date +%H:%M)
  echo "${P}◈ ${C}%~ ${Y}${time_str}${R}"
  echo "${P}└─➤ ${W}"
}""",
            prompt_code='PROMPT="$(_prompt_cyber)"'
        ),
        "5": PromptStyle(
            id="5",
            name="Steampunk",
            description="Engrenages bronze, look industriel victorien",
            preview_text="""
     ⚙ [u0_a123] ⚙ [~/projets]
     ⚙──➤ ls -la""",
            prompt_func="""
_prompt_steampunk() {
  local B="%F{130}" G="%F{220}" S="%F{250}" W="%F{white}" R="%f"
  echo "${B}⚙ [${G}%n${B}] ⚙ [${S}%~${B}]${R}"
  echo "${B}⚙──➤ ${W}"
}""",
            prompt_code='PROMPT="$(_prompt_steampunk)"'
        ),
        "6": PromptStyle(
            id="6",
            name="Anime",
            description="Style kawaii avec emoji et couleurs pastel",
            preview_text="""
     🌸 ~/projets (✿◠‿◠)
     ♡──➤ echo 'kawaii'""",
            prompt_func="""
_prompt_anime() {
  local P="%F{212}" C="%F{51}" G="%F{82}" W="%F{white}" R="%f"
  echo "${P}🌸 ${C}%~ ${G}(✿◠‿◠)${R}"
  echo "${P}♡──➤ ${W}"
}""",
            prompt_code='PROMPT="$(_prompt_anime)"'
        ),
        "7": PromptStyle(
            id="7",
            name="Powerline",
            description="Bandes de fond pleines type Agnoster/Starship, avec Git et heure",
            preview_text="""
      root  ~/projects/app  main ✓  14:32 """,
            prompt_func="""
_prompt_powerline() {
  local seg1_bg=51 seg2_bg=238
  local time_bg=220
  local gbg gicon git_seg=""

  if git rev-parse --is-inside-work-tree &>/dev/null; then
    local branch
    branch=$(git branch --show-current 2>/dev/null)
    if git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
      gbg=82
      gicon="✓"
    else
      gbg=208
      gicon="✗"
    fi
    git_seg=" ${branch} ${gicon} "
  fi

  local line=""
  line+="%K{$seg1_bg}%F{0} %n %k"
  line+="%F{$seg1_bg}%K{$seg2_bg}▶%f"
  line+="%K{$seg2_bg}%F{255} %~ %k"

  if [[ -n "$git_seg" ]]; then
    line+="%F{$seg2_bg}%K{$gbg}▶%f"
    line+="%K{$gbg}%F{0}${git_seg}%k"
    line+="%F{$gbg}%K{$time_bg}▶%f"
  else
    line+="%F{$seg2_bg}%K{$time_bg}▶%f"
  fi

  line+="%K{$time_bg}%F{0} %D{%H:%M} %k"
  line+="%F{$time_bg}▶%f "

  echo "$line"
}""",
            prompt_code='PROMPT="$(_prompt_powerline)"'
        ),
        "8": PromptStyle(
            id="8",
            name="Néon Diamant",
            description="Losanges dégradés cyan→magenta, très épuré et élégant",
            preview_text="""
     ◆◇◆  u0_a123 ~/projets  ◆◇◆
     ➤ """,
            prompt_func="""
_prompt_diamant() {
  local C="%F{51}" M="%F{201}" W="%F{255}" R="%f" D="%F{240}"
  echo "${C}◆${M}◇${C}◆${R}  ${W}%n${R} ${D}%~${R}  ${C}◆${M}◇${C}◆${R}"
  echo "${M}➤ ${R}"
}""",
            prompt_code='PROMPT="$(_prompt_diamant)"'
        ),
        "9": PromptStyle(
            id="9",
            name="Aurora Boréale",
            description="Dégradé vert/cyan/violet façon aurore, avec heure discrète",
            preview_text="""
     ╭─ ~/projets ─ 22:14
     ╰─❯ """,
            prompt_func="""
_prompt_aurora() {
  local G="%F{85}" C="%F{80}" P="%F{140}" W="%F{255}" R="%f"
  local time_str=$(date +%H:%M)
  echo "${G}╭─ ${C}%~ ${P}─ ${W}${time_str}${R}"
  echo "${G}╰─❯ ${R}"
}""",
            prompt_code='PROMPT="$(_prompt_aurora)"'
        ),
        "10": PromptStyle(
            id="10",
            name="Gradient Ombré",
            description="Barre pleine en dégradé de couleurs, moderne type Starship",
            preview_text="""
      u0_a123  ~/projets  main ✓ 
     ❯ """,
            prompt_func="""
_prompt_gradient() {
  local c1=57 c2=93 c3=129 c4=165
  local git_seg=""
  if git rev-parse --is-inside-work-tree &>/dev/null; then
    local branch=$(git branch --show-current 2>/dev/null)
    local gicon="✓"
    git diff --quiet 2>/dev/null || gicon="✗"
    git_seg="%K{$c4}%F{255}  ${branch} ${gicon} %k%f"
  fi
  local line=""
  line+="%K{$c1}%F{255}  %n %k"
  line+="%F{$c1}%K{$c2}%f"
  line+="%K{$c2}%F{255}  %~ %k"
  line+="%F{$c2}%K{$c3}%f"
  if [[ -n "$git_seg" ]]; then
    line+="%K{$c3}${git_seg}"
    line+="%F{$c4}%k%f "
  else
    line+="%F{$c3}%k%f "
  fi
  echo "$line"
  echo "%F{$c1}❯%f "
}""",
            prompt_code='PROMPT="$(_prompt_gradient)"'
        ),
    }

    @classmethod
    def get(cls, style_id: str) -> Optional[PromptStyle]:
        """Récupère un style par ID"""
        return cls.STYLES.get(style_id)

    @classmethod
    def list_all(cls) -> list:
        """Liste tous les styles disponibles"""
        return list(cls.STYLES.values())

    @classmethod
    def preview_all(cls, theme=None):
        """Affiche l'aperçu de tous les styles."""
        theme = theme or NeonTheme('hacker_neon')

        print(f"\n  {theme.get('PURPLE', True)}╔══════════════════════════════════════════════════╗")
        print(f"  ║{theme.colors['RST']}  {theme.get('PINK', True)}STYLE DE PROMPT{theme.colors['RST']}  {theme.get('PURPLE', True)}{len(cls.STYLES)} designs disponibles{theme.colors['RST']}           {theme.get('PURPLE', True)}║")
        print(f"  ╚══════════════════════════════════════════════════╝{theme.colors['RST']}\n")

        for style in cls.list_all():
            print(f"  {theme.get('GREEN', True)}{style.id}) {style.name}{theme.colors['RST']}  {theme.colors['DIM']}— {style.description}{theme.colors['RST']}")
            print(f"     {style.preview_text}\n")

    @classmethod
    def generate_zshrc_prompt(cls, style_id: str, custom_name: str = None) -> tuple:
        """
        Génère le code Zsh pour le prompt choisi.

        Args:
            style_id: ID du style.
            custom_name: Nom personnalisé à afficher à la place de %n (optionnel).

        Returns:
            tuple (prompt_func, prompt_code, prompt_name)
        """
        style = cls.get(style_id)
        if not style:
            style = cls.get("1")  # Fallback

        func = style.prompt_func
        code = style.prompt_code

        # Si un nom personnalisé est demandé, on remplace %n par le nom échappé
        if custom_name:
            safe_name = custom_name.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')
            func = func.replace('%n', safe_name)
            code = code.replace('%n', safe_name)

        return func, code, style.name
