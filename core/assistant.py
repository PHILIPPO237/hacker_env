# -*- coding: utf-8 -*-
"""
Assistant guide complet pour HACKER_ENV V2
Fournit une aide interactive et contextuelle à chaque étape.
"""

import sys
import time
from typing import Optional, Callable
from core.colors import NeonTheme, default_theme
from core.effects import typewrite, clear, print_success, print_warn, print_info


class GuideAssistant:
    """Assistant guide interactif pour HACKER_ENV V2."""
    
    def __init__(self, theme: Optional[NeonTheme] = None):
        """
        Initialiser l'assistant guide.
        
        Args:
            theme: Thème à utiliser
        """
        self.theme = theme or default_theme
        self.step = 0
        self.history = []
        self.tips = []
    
    def show_welcome(self) -> None:
        """Afficher l'accueil de l'assistant."""
        clear()
        rst = self.theme.colors['RST']
        cyan = self.theme.get('CYAN', True)
        green = self.theme.get('GREEN', True)
        yellow = self.theme.get('YELLOW', True)
        pink = self.theme.get('PINK', True)
        
        print(f"""
  {cyan}╭──────────────────────────────────────────────────────╮{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}│{rst}          {pink}🤖 ASSISTANT GUIDE HACKER_ENV V2{rst}            {cyan}│{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}├──────────────────────────────────────────────────────┤{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}│{rst}  {green}Bienvenue dans l'assistant guide !{rst}                    {cyan}│{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}│{rst}  Je vais vous accompagner à chaque étape de           {cyan}│{rst}
  {cyan}│{rst}  la configuration de votre environnement terminal.    {cyan}│{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}│{rst}  {yellow}Commandes disponibles :{rst}                              {cyan}│{rst}
  {cyan}│{rst}    • {green}tappez ? à tout moment pour l'aide{rst}              {cyan}│{rst}
  {cyan}│{rst}    • {green}appuyez sur Entrée pour continuer{rst}               {cyan}│{rst}
  {cyan}│{rst}    • {green}tapez 'q' pour quitter l'assistant{rst}              {cyan}│{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}╰──────────────────────────────────────────────────────╯{rst}
""")
        input(f"  {yellow}Appuyez sur Entrée pour commencer...{rst} ")
    
    def show_step_intro(self, step_num: int, title: str, description: str) -> None:
        """
        Afficher l'introduction d'une étape.
        
        Args:
            step_num: Numéro de l'étape
            title: Titre de l'étape
            description: Description de l'étape
        """
        self.step = step_num
        rst = self.theme.colors['RST']
        cyan = self.theme.get('CYAN', True)
        green = self.theme.get('GREEN', True)
        dim = self.theme.colors['DIM']
        
        # Barre de progression
        total_steps = 7
        bar_width = 30
        filled = int(bar_width * step_num / total_steps)
        empty = bar_width - filled
        bar = f"{green}{'█' * filled}{dim}{'░' * empty}{rst}"
        
        print(f"""
  {cyan}╭──────────────────────────────────────────────────────╮{rst}
  {cyan}│{rst}  {green}Étape {step_num}/{total_steps}{rst}  {bar}                          {cyan}│{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}│{rst}  {green}{title}{rst}                                              {cyan}│{rst}
  {cyan}│{rst}  {dim}{description}{rst}                                           {cyan}│{rst}
  {cyan}╰──────────────────────────────────────────────────────╯{rst}
""")
    
    def show_tip(self, tip: str, icon: str = "💡") -> None:
        """
        Afficher un conseil.
        
        Args:
            tip: Texte du conseil
            icon: Icône à afficher
        """
        rst = self.theme.colors['RST']
        yellow = self.theme.get('YELLOW', True)
        dim = self.theme.colors['DIM']
        
        print(f"  {yellow}{icon} {tip}{rst}")
        self.tips.append(tip)
    
    def show_warning(self, message: str) -> None:
        """
        Afficher un avertissement.
        
        Args:
            message: Message d'avertissement
        """
        rst = self.theme.colors['RST']
        orange = self.theme.get('ORANGE', True)
        
        print(f"  {orange}⚠️  {message}{rst}")
    
    def show_error(self, message: str) -> None:
        """
        Afficher une erreur.
        
        Args:
            message: Message d'erreur
        """
        rst = self.theme.colors['RST']
        red = self.theme.get('RED', True)
        
        print(f"  {red}✖ {message}{rst}")
    
    def show_success(self, message: str) -> None:
        """
        Afficher un succès.
        
        Args:
            message: Message de succès
        """
        rst = self.theme.colors['RST']
        green = self.theme.get('GREEN', True)
        
        print(f"  {green}✓ {message}{rst}")
    
    def show_info(self, message: str) -> None:
        """
        Afficher une information.
        
        Args:
            message: Message d'information
        """
        rst = self.theme.colors['RST']
        cyan = self.theme.get('CYAN', True)
        dim = self.theme.colors['DIM']
        
        print(f"  {cyan}◈ {dim}{message}{rst}")
    
    def ask_question(self, question: str, options: Optional[list] = None, 
                     default: Optional[str] = None, help_text: Optional[str] = None) -> str:
        """
        Poser une question avec options.
        
        Args:
            question: Question à poser
            options: Liste d'options valides
            default: Valeur par défaut
            help_text: Texte d'aide
            
        Returns:
            Réponse de l'utilisateur
        """
        rst = self.theme.colors['RST']
        cyan = self.theme.get('CYAN', True)
        yellow = self.theme.get('YELLOW', True)
        dim = self.theme.colors['DIM']
        
        while True:
            # Afficher la question
            if options:
                options_str = f" [{'/'.join(options)}]"
            else:
                options_str = ""
            
            default_str = f" [{default}]" if default else ""
            help_hint = f" {yellow}[?=aide]{rst}" if help_text else ""
            
            print(f"\n  {cyan}➤{rst} {question}{default_str}{options_str}{help_hint}")
            answer = input(f"    {cyan}→{rst} ").strip()
            
            # Aide
            if answer == '?' and help_text:
                print(f"\n  {yellow}💡 Aide :{rst}")
                typewrite(f"    {help_text}", dim, 0.01, self.theme)
                print()
                continue
            
            # Valeur par défaut
            if not answer and default:
                return default
            
            # Validation
            if options and answer not in options:
                print(f"  {self.theme.get('RED', True)}✖ Choix invalide. Options : {', '.join(options)}{rst}")
                continue
            
            return answer
    
    def ask_yes_no(self, question: str, default: str = "o", 
                   help_text: Optional[str] = None) -> bool:
        """
        Poser une question oui/non.
        
        Args:
            question: Question à poser
            default: Valeur par défaut ('o' ou 'n')
            help_text: Texte d'aide
            
        Returns:
            True si oui, False si non
        """
        rst = self.theme.colors['RST']
        cyan = self.theme.get('CYAN', True)
        yellow = self.theme.get('YELLOW', True)
        
        while True:
            help_hint = f" {yellow}[?=aide]{rst}" if help_text else ""
            default_hint = f" [O/n]" if default == 'o' else " [o/N]"
            
            print(f"\n  {cyan}➤{rst} {question}{default_hint}{help_hint}")
            answer = input(f"    {cyan}→{rst} ").strip().lower()
            
            # Aide
            if answer == '?' and help_text:
                print(f"\n  {yellow}💡 Aide :{rst}")
                typewrite(f"    {help_text}", self.theme.colors['DIM'], 0.01, self.theme)
                print()
                continue
            
            # Valeur par défaut
            if not answer:
                return default == 'o'
            
            # Validation
            if answer in ('o', 'y', 'oui', 'yes'):
                return True
            elif answer in ('n', 'non', 'no'):
                return False
            else:
                print(f"  {self.theme.get('RED', True)}✖ Réponse invalide. Tapez 'o' ou 'n'{rst}")
    
    def show_progress(self, current: int, total: int, message: str = "") -> None:
        """
        Afficher une progression.
        
        Args:
            current: Valeur actuelle
            total: Valeur totale
            message: Message à afficher
        """
        rst = self.theme.colors['RST']
        green = self.theme.get('GREEN', True)
        
        percentage = (current / total) * 100 if total > 0 else 0
        bar_width = 30
        filled = int(bar_width * percentage / 100)
        empty = bar_width - filled
        
        bar = f"{green}{'█' * filled}{'░' * empty}{rst}"
        
        if message:
            print(f"\r  {bar} {percentage:.0f}% - {message}", end="", flush=True)
        else:
            print(f"\r  {bar} {percentage:.0f}%", end="", flush=True)
        
        if current >= total:
            print()
    
    def show_summary(self, title: str, items: dict) -> None:
        """
        Afficher un résumé.
        
        Args:
            title: Titre du résumé
            items: Dict label -> valeur
        """
        rst = self.theme.colors['RST']
        cyan = self.theme.get('CYAN', True)
        green = self.theme.get('GREEN', True)
        dim = self.theme.colors['DIM']
        
        print(f"""
  {cyan}╭──────────────────────────────────────────────────────╮{rst}
  {cyan}│{rst}  {green}{title}{rst}                                                   {cyan}│{rst}
  {cyan}├──────────────────────────────────────────────────────┤{rst}""")
        
        for label, value in items.items():
            print(f"  {cyan}│{rst}  {cyan}{label:<15}{rst} {dim}:{rst}  {green}{value}{rst}")
        
        print(f"  {cyan}╰──────────────────────────────────────────────────────╯{rst}")
    
    def show_help(self) -> None:
        """Afficher l'aide complète."""
        rst = self.theme.colors['RST']
        cyan = self.theme.get('CYAN', True)
        green = self.theme.get('GREEN', True)
        yellow = self.theme.get('YELLOW', True)
        pink = self.theme.get('PINK', True)
        
        print(f"""
  {cyan}╭──────────────────────────────────────────────────────╮{rst}
  {cyan}│{rst}          {pink}📖 GUIDE HACKER_ENV V2{rst}                     {cyan}│{rst}
  {cyan}├──────────────────────────────────────────────────────┤{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}│{rst}  {green}COMMANDES DU TERMINAL :{rst}                              {cyan}│{rst}
  {cyan}│{rst}    • {yellow}ll{rst}          Lister les fichiers (détail)       {cyan}│{rst}
  {cyan}│{rst}    • {yellow}la{rst}          Lister tous les fichiers          {cyan}│{rst}
  {cyan}│{rst}    • {yellow}cls{rst}         Effacer l'écran                   {cyan}│{rst}
  {cyan}│{rst}    • {yellow}reload{rst}      Recharger la configuration       {cyan}│{rst}
  {cyan}│{rst}    • {yellow}upgrade{rst}     Mettre à jour les paquets        {cyan}│{rst}
  {cyan}│{rst}    • {yellow}backup{rst}      Sauvegarder la configuration     {cyan}│{rst}
  {cyan}│{rst}    • {yellow}weather{rst}     Afficher la météo                 {cyan}│{rst}
  {cyan}│{rst}    • {yellow}genpass{rst}     Générer un mot de passe          {cyan}│{rst}
  {cyan}│{rst}    • {yellow}help{rst}        Afficher cette aide               {cyan}│{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}│{rst}  {green}MODULES DISPONIBLES :{rst}                                {cyan}│{rst}
  {cyan}│{rst}    • {yellow}tmux{rst}        Sessions persistantes             {cyan}│{rst}
  {cyan}│{rst}    • {yellow}backup{rst}      Sauvegarde/restauration          {cyan}│{rst}
  {cyan}│{rst}    • {yellow}weather{rst}     Météo dans la bannière            {cyan}│{rst}
  {cyan}│{rst}    • {yellow}genpass{rst}     Générateur de mots de passe       {cyan}│{rst}
  {cyan}│{rst}    • {yellow}python{rst}      Gestionnaire venv Python          {cyan}│{rst}
  {cyan}│{rst}    • {yellow}matrix{rst}      Effet Matrix au démarrage         {cyan}│{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}╰──────────────────────────────────────────────────────╯{rst}
""")
    
    def show_contextual_help(self, context: str) -> None:
        """
        Afficher l'aide contextuelle.
        
        Args:
            context: Contexte actuel (ex: 'identity', 'banner', etc.)
        """
        rst = self.theme.colors['RST']
        yellow = self.theme.get('YELLOW', True)
        dim = self.theme.colors['DIM']
        
        help_texts = {
            'identity': {
                'title': 'Choix du nom',
                'text': '''Le nom que vous choisissez sera affiché dans la bannière
de votre terminal à chaque ouverture. Il est recommandé
de garder un nom court (8-15 caractères) pour un rendu
optimal dans la bannière ASCII.

Exemples : PHILIPPO, HACKER, CYBER, etc.'''
            },
            'banner': {
                'title': 'Choix de la bannière',
                'text': '''La bannière est l'art ASCII qui s'affiche en haut de
votre terminal. Chaque modèle a un style différent :

  • Modèles 1-5 : Plus sobres, lisibles sur petit écran
  • Modèles 6-20 : Plus décoratifs et colorés

Vous pouvez visualiser chaque modèle avant de choisir.'''
            },
            'prompt': {
                'title': 'Style de prompt',
                'text': '''Le prompt est la ligne qui apparaît avant chaque commande.
Choisissez un style qui vous convient :

  1. Hacker Neon   - Classique, vert néon
  2. Développeur Pro - Avec branche Git
  3. Minimaliste    - Simple et rapide
  4. Cyberpunk      - Avec heure intégrée
  5. Steampunk      - Style engrenages
  6. Anime          - Style kawaii
  7. Powerline      - Bandes colorées'''
            },
            'modules': {
                'title': 'Modules optionnels',
                'text': '''Les modules ajoutent des fonctionnalités supplémentaires.

Recommandés pour débuter :
  • tmux     - Pour garder des sessions actives
  • backup   - Pour sauvegarder votre configuration
  • weather  - Pour la météo rapide
  • genpass  - Pour générer des mots de passe

Modules avancés (à utiliser avec précaution) :
  • recon    - Outils réseau (uniquement sur votre réseau !)'''
            },
            'theme': {
                'title': 'Thème visuel',
                'text': '''Le thème détermine les couleurs de toute l'interface.

  • cyber    - Cyan et magenta futuriste
  • matrix   - Vert sur noir (style hacker classique)
  • neon     - Couleurs néon vibrantes
  • minimal  - Design épuré et neutre
  • classic  - Couleurs de terminal traditionnelles

Vous pouvez changer de thème à tout moment.'''
            }
        }
        
        help_info = help_texts.get(context)
        if help_info:
            print(f"\n  {yellow}💡 {help_info['title']} :{rst}")
            for line in help_info['text'].split('\n'):
                print(f"    {dim}{line}{rst}")
            print()
    
    def show_completion(self) -> None:
        """Afficher l'écran de fin."""
        rst = self.theme.colors['RST']
        green = self.theme.get('GREEN', True)
        cyan = self.theme.get('CYAN', True)
        yellow = self.theme.get('YELLOW', True)
        pink = self.theme.get('PINK', True)
        
        print(f"""
  {cyan}╭──────────────────────────────────────────────────────╮{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}│{rst}          {pink}✅ CONFIGURATION TERMINÉE !{rst}                 {cyan}│{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}├──────────────────────────────────────────────────────┤{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}│{rst}  {green}Votre environnement terminal est prêt !{rst}              {cyan}│{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}│{rst}  {yellow}Prochaines étapes :{rst}                                  {cyan}│{rst}
  {cyan}│{rst}    • Redémarrez votre terminal                        {cyan}│{rst}
  {cyan}│{rst}    • Tapez {green}'help'{rst} pour voir les commandes         {cyan}│{rst}
  {cyan}│{rst}    • Tapez {green}'reload'{rst} pour recharger la config      {cyan}│{rst}
  {cyan}│{rst}                                                      {cyan}│{rst}
  {cyan}╰──────────────────────────────────────────────────────╯{rst}
""")
    
    def show_goodbye(self) -> None:
        """Afficher le message d'au revoir."""
        rst = self.theme.colors['RST']
        pink = self.theme.get('PINK', True)
        
        print(f"\n  {pink}Au revoir ! 👋{rst}\n")


# Instance globale de l'assistant
_guide_assistant: Optional[GuideAssistant] = None


def get_guide_assistant(theme: Optional[NeonTheme] = None) -> GuideAssistant:
    """
    Obtenir l'instance de l'assistant guide.
    
    Args:
        theme: Thème à utiliser
        
    Returns:
        Instance de GuideAssistant
    """
    global _guide_assistant
    if _guide_assistant is None:
        _guide_assistant = GuideAssistant(theme)
    return _guide_assistant
