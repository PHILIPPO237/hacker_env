# -*- coding: utf-8 -*-
"""
Module de gestion des couleurs pour Termux Hacker Env
Inspiré de hacker_env.py : palette néon dynamique, thèmes, génération RGB
"""

import random


class NeonTheme:
    """Générateur de thèmes de couleurs avec support RGB dynamique"""
    
    # Palette de base (inspirée de hacker_env.py)
    BASE_PALETTE = {
        'PINK': (255, 0, 128),
        'CYAN': (0, 255, 255),
        'GREEN': (57, 255, 20),
        'PURPLE': (147, 0, 211),
        'ORANGE': (255, 165, 0),
        'YELLOW': (255, 255, 0),
        'RED': (255, 50, 50),
        'GOLD': (255, 215, 0),
        'WHITE': (255, 255, 255),
        'LIME': (50, 205, 50),
        'BLUE': (30, 144, 255),
        'SILVER': (192, 192, 192),
        'BRONZE': (205, 127, 50),
        'BLOOD': (139, 0, 0),
        'EMERALD': (80, 200, 120),
        'TEAL': (0, 128, 128),
        'CORAL': (255, 127, 80),
        'LAVENDER': (230, 230, 250),
        'INDIGO': (75, 0, 130),
        'CRIMSON': (220, 20, 60),
        # Ajoutés pour les nouveaux thèmes
        'BLOSSOM': (255, 183, 206),
        'MINT': (152, 255, 204),
        'EMBER': (255, 69, 0),
        'DEEP_BLUE': (0, 60, 120),
        'TURQUOISE': (64, 224, 208),
        'GRAY_LIGHT': (200, 200, 200),
        'GRAY_MID': (150, 150, 150),
        'CHARCOAL': (60, 60, 60),
    }
    
    # Thèmes prédéfinis (inspirés des 20 modèles de hacker_env.py)
    THEMES = {
        'hacker_neon': {'primary': 'GREEN', 'secondary': 'YELLOW', 'accent': 'CYAN'},
        'cyberpunk': {'primary': 'CYAN', 'secondary': 'PINK', 'accent': 'PURPLE'},
        'modern': {'primary': 'BLUE', 'secondary': 'CYAN', 'accent': 'WHITE'},
        'festive': {'primary': 'PURPLE', 'secondary': 'PINK', 'accent': 'CYAN'},
        'minimal': {'primary': 'WHITE', 'secondary': 'SILVER', 'accent': 'BLUE'},
        'gothic': {'primary': 'PURPLE', 'secondary': 'LAVENDER', 'accent': 'INDIGO'},
        'sunset': {'primary': 'PINK', 'secondary': 'ORANGE', 'accent': 'YELLOW'},
        'steampunk': {'primary': 'BRONZE', 'secondary': 'GOLD', 'accent': 'SILVER'},
        'stealth': {'primary': 'INDIGO', 'secondary': 'BLOOD', 'accent': 'SILVER'},
        'biohazard': {'primary': 'LIME', 'secondary': 'YELLOW', 'accent': 'GREEN'},
        'christmas': {'primary': 'EMERALD', 'secondary': 'GOLD', 'accent': 'RED'},
        'romantic': {'primary': 'PINK', 'secondary': 'RED', 'accent': 'LAVENDER'},
        'diamond': {'primary': 'CYAN', 'secondary': 'SILVER', 'accent': 'WHITE'},
        'arrow': {'primary': 'ORANGE', 'secondary': 'YELLOW', 'accent': 'GOLD'},
        'musical': {'primary': 'PURPLE', 'secondary': 'LAVENDER', 'accent': 'PINK'},
        'cyber_grid': {'primary': 'CYAN', 'secondary': 'PINK', 'accent': 'PURPLE'},
        'shadow': {'primary': 'SILVER', 'secondary': 'SILVER', 'accent': 'WHITE'},
        'pixel': {'primary': 'CRIMSON', 'secondary': 'RED', 'accent': 'BLOOD'},
        'neon_glow': {'primary': 'CYAN', 'secondary': 'PINK', 'accent': 'YELLOW'},
        # ── Nouveaux thèmes ──────────────────────────────────────────────
        'sakura': {'primary': 'BLOSSOM', 'secondary': 'MINT', 'accent': 'WHITE'},
        'blood_moon': {'primary': 'BLOOD', 'secondary': 'EMBER', 'accent': 'CRIMSON'},
        'ocean_deep': {'primary': 'DEEP_BLUE', 'secondary': 'TURQUOISE', 'accent': 'CYAN'},
        'solar_flare': {'primary': 'ORANGE', 'secondary': 'GOLD', 'accent': 'RED'},
        'monochrome': {'primary': 'GRAY_LIGHT', 'secondary': 'GRAY_MID', 'accent': 'CHARCOAL'},
    }
    
    def __init__(self, theme_name='hacker_neon', custom_rgb=None):
        """
        Initialise un thème de couleurs
        
        Args:
            theme_name: Nom du thème prédéfini
            custom_rgb: Dict optionnel {'primary': (r,g,b), 'secondary': (r,g,b), 'accent': (r,g,b)}
        """
        self.theme_name = theme_name
        self.custom_rgb = custom_rgb or {}
        self.colors = self._generate_colors()
        # Attributs de style pour compatibilité
        self.RST = self.colors['RST']
        self.BLD = self.colors['BLD']
        self.DIM = self.colors['DIM']
    
    def _generate_colors(self):
        """Génère les codes ANSI pour le thème choisi"""
        theme = self.THEMES.get(self.theme_name, self.THEMES['hacker_neon'])
        colors = {}
        
        for role, color_name in theme.items():
            if role in self.custom_rgb:
                # Utiliser la couleur RGB personnalisée
                r, g, b = self.custom_rgb[role]
                colors[role] = self._rgb(r, g, b)
            else:
                # Utiliser la couleur de la palette de base
                r, g, b = self.BASE_PALETTE.get(color_name, (0, 255, 255))
                colors[role] = self._rgb(r, g, b)
        
        # Ajouter aussi les noms bruts de la palette (ex: 'PINK', 'CYAN', 'GREEN'...)
        # pour que theme.get('PINK') fonctionne, pas seulement theme.get('primary').
        for color_name, (r, g, b) in self.BASE_PALETTE.items():
            colors[color_name] = self._rgb(r, g, b)
        
        # Ajouter les couleurs de base
        colors['RST'] = "\033[0m"
        colors['BLD'] = "\033[1m"
        colors['DIM'] = "\033[2m"
        
        return colors
    
    @staticmethod
    def _rgb(r, g, b):
        """Génère un code ANSI RGB avec validation"""
        r = max(0, min(255, int(r)))
        g = max(0, min(255, int(g)))
        b = max(0, min(255, int(b)))
        return f"\033[38;2;{r};{g};{b}m"
    
    @staticmethod
    def _rgb_bold(r, g, b):
        """Génère un code ANSI RGB en gras"""
        return f"\033[1;38;2;{r};{g};{b}m"
    
    def get(self, color_name, bold=False):
        """Récupère une couleur du thème actuel"""
        if bold:
            return self.colors.get(color_name, self.colors['primary']).replace('[38;2', '[1;38;2')
        return self.colors.get(color_name, self.colors['primary'])
    
    def randomize(self):
        """Génère un thème aléatoire (inspiré de hacker_env.py)"""
        for role in ['primary', 'secondary', 'accent']:
            self.custom_rgb[role] = (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255)
            )
        self.colors = self._generate_colors()
        # Mettre à jour les attributs de style
        self.RST = self.colors['RST']
        self.BLD = self.colors['BLD']
        self.DIM = self.colors['DIM']
        return self
    
    def rainbow(self, text):
        """Applique un dégradé arc-en-ciel sur le texte"""
        result = ""
        length = len(text)
        for i, char in enumerate(text):
            hue = (i * 360) // length
            r, g, b = self._hue_to_rgb(hue)
            result += f"{self._rgb(r, g, b)}{self.BLD}{char}"
        result += self.colors['RST']
        return result
    
    @staticmethod
    def _hue_to_rgb(hue):
        """Convertit un angle HSL en RGB"""
        if hue < 60:
            return 255, (hue * 255) // 60, 0
        elif hue < 120:
            return (255 - (hue - 60) * 255 // 60), 255, 0
        elif hue < 180:
            return 0, 255, ((hue - 120) * 255 // 60)
        elif hue < 240:
            return 0, (255 - (hue - 180) * 255 // 60), 255
        elif hue < 300:
            return ((hue - 240) * 255 // 60), 0, 255
        else:
            return 255, 0, (255 - (hue - 300) * 255 // 60)
    
    def list_themes(self):
        """Liste tous les thèmes disponibles"""
        return list(self.THEMES.keys())
    
    def preview(self):
        """Affiche un aperçu du thème actuel"""
        preview = f"""
  {self.get('primary', True)}╔══════════════════════════════════════╗{self.colors['RST']}
  {self.get('primary', True)}║{self.colors['RST']}  {self.get('secondary', True)}THÈME : {self.theme_name.upper():20}{self.colors['RST']} {self.get('primary', True)}║{self.colors['RST']}
  {self.get('primary', True)}╠══════════════════════════════════════╣{self.colors['RST']}
  {self.get('primary', True)}║{self.colors['RST']}  {self.get('primary')}Primary   : ████████████{self.colors['RST']}  {self.get('primary', True)}║{self.colors['RST']}
  {self.get('primary', True)}║{self.colors['RST']}  {self.get('secondary')}Secondary : ████████████{self.colors['RST']}  {self.get('primary', True)}║{self.colors['RST']}
  {self.get('primary', True)}║{self.colors['RST']}  {self.get('accent')}Accent    : ████████████{self.colors['RST']}  {self.get('primary', True)}║{self.colors['RST']}
  {self.get('primary', True)}╚══════════════════════════════════════╝{self.colors['RST']}
"""
        return preview


# Compatibilité ascendante avec l'ancien module
class Neon:
    """Classe legacy pour compatibilité (inspirée de l'original)"""
    RST = "\033[0m"
    BLD = "\033[1m"
    DIM = "\033[2m"
    PINK = "\033[38;2;255;0;128m"
    CYAN = "\033[38;2;0;255;255m"
    GREEN = "\033[38;2;57;255;20m"
    PURPLE = "\033[38;2;147;0;211m"
    ORANGE = "\033[38;2;255;165;0m"
    YELLOW = "\033[38;2;255;255;0m"
    RED = "\033[38;2;255;50;50m"
    GOLD = "\033[38;2;255;215;0m"
    WHITE = "\033[38;2;255;255;255m"


# Instance par défaut pour import rapide
default_theme = NeonTheme('hacker_neon')
