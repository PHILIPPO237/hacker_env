# -*- coding: utf-8 -*-
"""
Module INTRO — écran-titre de l'outil lui-même.

Différent des 20 modèles de `modules/banners.py` : ceux-là sont les
bannières que l'UTILISATEUR choisit pour SON .zshrc. Celui-ci est le
logo de L'OUTIL, affiché une seule fois au lancement, avant même la
galerie de choix.
"""
import sys
import time
import shutil

from core.effects import boot_sequence, clear


def _width(default=56):
    try:
        return max(shutil.get_terminal_size().columns - 4, 40)
    except Exception:
        return default


def _boxed_line(text, width, theme, fill=" "):
    pad = width - len(text)
    left = pad // 2
    right = pad - left
    return f"  {theme.get('primary', True)}║{theme.colors['RST']}{fill * left}{text}{fill * right}{theme.get('primary', True)}║{theme.colors['RST']}"


def _rainbow_chars(text, theme, bold=True):
    """Calcule la couleur de chaque caractère visible de `text` en fonction
    de sa position dans le mot entier (pas dans un sous-appel isolé, sinon
    toutes les lettres ressortent dans la même teinte). Renvoie une liste
    de fragments déjà colorés, un par caractère de `text` (espaces inclus,
    non colorés)."""
    visible_count = sum(1 for c in text if c != " ")
    length = max(visible_count, 1)
    b = theme.BLD if bold else ""
    fragments = []
    idx = 0
    for ch in text:
        if ch == " ":
            fragments.append(" ")
            continue
        hue = idx * 300 // length  # 0-300 : évite de reboucler sur le rouge de départ
        if hue < 60:
            r, g, bl = 255, hue * 255 // 60, 0
        elif hue < 120:
            r, g, bl = 255 - (hue - 60) * 255 // 60, 255, 0
        elif hue < 180:
            r, g, bl = 0, 255, (hue - 120) * 255 // 60
        elif hue < 240:
            r, g, bl = 0, 255 - (hue - 180) * 255 // 60, 255
        else:
            r, g, bl = (hue - 240) * 255 // 60, 0, 255
        fragments.append(f"{theme._rgb(r, g, bl)}{b}{ch}{theme.colors['RST']}")
        idx += 1
    return fragments


def show_author_presentation(theme, author="PHILIPPO", project_name="TERMUX HACKER ENV",
                              tagline="Personnalise ton terminal : bannières, prompts, thèmes, modules",
                              version="2.0"):
    """Écran de présentation du projet, affiché en tout premier au lancement :
    nom du projet, auteur, description courte. Avant même le boot/logo."""
    clear()
    width = _width()

    for _ in range(2):
        print()

    pad = width - len(project_name)
    left = pad // 2

    print(f"  {theme.get('primary', True)}╔{'═' * width}╗{theme.colors['RST']}")
    print(_boxed_line("", width, theme))
    # révélation lettre par lettre, chaque lettre déjà dans sa teinte arc-en-ciel
    sys.stdout.write(f"  {theme.get('primary', True)}║{theme.colors['RST']}{' ' * left}")
    sys.stdout.flush()
    for fragment in _rainbow_chars(project_name, theme, bold=True):
        sys.stdout.write(fragment)
        sys.stdout.flush()
        time.sleep(0.02)
    sys.stdout.write(f"{' ' * (pad - left)}{theme.get('primary', True)}║{theme.colors['RST']}\n")

    print(_boxed_line("", width, theme))
    print(_boxed_line(f"par {author}  •  v{version}", width, theme))
    print(_boxed_line("", width, theme))
    print(f"  {theme.get('primary', True)}╠{'═' * width}╣{theme.colors['RST']}")
    print(_boxed_line(tagline, width, theme))
    print(_boxed_line("", width, theme))
    print(f"  {theme.get('primary', True)}╚{'═' * width}╝{theme.colors['RST']}")
    print()
    input(f"  {theme.get('GOLD', True)}Appuie sur Entrée pour continuer...{theme.colors['RST']} ")


def show_name_preview(theme, name):
    """Aperçu encadré du nom choisi par l'utilisateur, révélé en arc-en-ciel
    (gras), lettre par lettre — même style que show_author_presentation/
    show_splash. Appelé juste après la saisie du nom, pas d'input() ici :
    l'appelant enchaîne tout de suite avec un pulse_text()."""
    width = _width()
    pad = max(width - len(name), 0)
    left = pad // 2
    right = pad - left

    print(f"  {theme.get('primary', True)}╔{'═' * width}╗{theme.colors['RST']}")
    print(_boxed_line("", width, theme))
    sys.stdout.write(f"  {theme.get('primary', True)}║{theme.colors['RST']}{' ' * left}")
    sys.stdout.flush()
    for fragment in _rainbow_chars(name, theme, bold=True):
        sys.stdout.write(fragment)
        sys.stdout.flush()
        time.sleep(0.015)
    sys.stdout.write(f"{' ' * right}{theme.get('primary', True)}║{theme.colors['RST']}\n")
    print(_boxed_line("", width, theme))
    print(f"  {theme.get('primary', True)}╚{'═' * width}╝{theme.colors['RST']}")
    print()


def show_splash(theme, version="2.0", edition="Frame Gallery Edition"):
    """Affiche l'écran-titre animé de l'outil, puis rend la main.

    Enchaînement volontairement court (< 2s) : une petite séquence de
    boot façon BIOS, puis le logo qui se révèle lettre par lettre en
    arc-en-ciel (gras). Pas d'animation lourde (matrix/confettis) ici :
    celles-là sont réservées au premier lancement marquant ou à une
    commande manuelle, pour ne pas fatiguer à chaque ouverture.
    """
    clear()
    print()
    boot_sequence(theme=theme)
    time.sleep(0.2)
    clear()

    width = _width()
    top = f"  {theme.get('primary', True)}╔{'═' * width}╗{theme.colors['RST']}"
    bottom = f"  {theme.get('primary', True)}╚{'═' * width}╝{theme.colors['RST']}"
    sep = f"  {theme.get('primary', True)}╠{'═' * width}╣{theme.colors['RST']}"

    print()
    print(top)
    print(_boxed_line("", width, theme))

    # Titre lettre-espacé, révélé en arc-en-ciel (gras) lettre par lettre.
    title = " ".join("T E R M U X   H A C K E R   E N V".split())
    pad = width - len(title)
    left = pad // 2
    right = pad - left
    sys.stdout.write(f"  {theme.get('primary', True)}║{theme.colors['RST']}{' ' * left}")
    sys.stdout.flush()
    for fragment in _rainbow_chars(title, theme, bold=True):
        sys.stdout.write(fragment)
        sys.stdout.flush()
        time.sleep(0.015)
    sys.stdout.write(f"{' ' * right}{theme.get('primary', True)}║{theme.colors['RST']}\n")

    print(_boxed_line("", width, theme))
    print(_boxed_line(f"⚡ v{version} — {edition} ⚡", width, theme))
    print(_boxed_line("", width, theme))
    print(sep)
    print(_boxed_line("20 bannières • 7 prompts • 8 modules", width, theme))
    print(_boxed_line("Guide contextuel à chaque étape (tape ? pour de l'aide)", width, theme))
    print(_boxed_line("", width, theme))
    print(bottom)
    print()

    input(f"  {theme.get('GOLD', True)}Appuie sur Entrée pour commencer...{theme.colors['RST']} ")
