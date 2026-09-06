# -*- coding: utf-8 -*-
"""
Module d'effets visuels avancés
Inspiré de hacker_env.py : typewrite, glitch, rainbow, pulse, matrix, spinner
"""

import sys
import time
import os
import threading
import shutil
import random
from core.colors import NeonTheme, default_theme


def typewrite(text, color=None, speed=0.015, theme=None):
    """
    Écrit le texte caractère par caractère.

    Args:
        text: Texte à afficher.
        color: Couleur (utilise le thème si None).
        speed: Vitesse d'écriture.
        theme: Instance NeonTheme (optionnel).
    """
    theme = theme or default_theme
    color = color or theme.get('primary')

    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write(theme.colors['RST'] + "\n")


def typewrite_async(text, color=None, speed=0.015, theme=None):
    """
    Version asynchrone de typewrite (ne bloque pas le thread principal).
    """
    thread = threading.Thread(target=typewrite, args=(text, color, speed, theme))
    thread.start()
    return thread


def scanline(char="━", color=None, theme=None):
    """Affiche une ligne de séparation dynamique."""
    theme = theme or default_theme
    color = color or theme.get('primary')

    try:
        width = shutil.get_terminal_size().columns
    except:
        width = 50

    print(color + char * width + theme.colors['RST'])


def clear():
    """Nettoie le terminal de manière portable."""
    os.system('clear' if os.name != 'nt' else 'cls')


def spinner(msg="Chargement", color=None, theme=None):
    """
    Affiche un spinner animé.
    Usage : Utiliser dans un thread séparé pendant une opération longue.
    """
    theme = theme or default_theme
    color = color or theme.get('primary', True)
    spin_chars = '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    i = 0
    stop_flag = threading.Event()

    def _spin():
        nonlocal i
        while not stop_flag.is_set():
            i = (i + 1) % 10
            sys.stdout.write(f"\r  {color}{spin_chars[i]}{theme.colors['RST']}  {theme.colors['DIM']}{msg}...{theme.colors['RST']}")
            sys.stdout.flush()
            time.sleep(0.08)
        sys.stdout.write("\r" + " " * (len(msg) + 10) + "\r")
        sys.stdout.flush()

    thread = threading.Thread(target=_spin)
    thread.start()
    return stop_flag, thread


def stop_spinner(stop_flag, thread):
    """Arrête le spinner."""
    stop_flag.set()
    thread.join()


def glitch_text(text, color=None, theme=None):
    """Effet de texte glitché."""
    theme = theme or default_theme
    color = color or theme.get('primary', True)
    chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~"

    sys.stdout.write(color)
    for char in text:
        if char != " " and random.randint(0, 2) == 0:
            sys.stdout.write(f"{theme.get('RED', True)}{random.choice(chars)}")
            sys.stdout.flush()
            time.sleep(0.01)
            sys.stdout.write("\b")
        sys.stdout.write(f"{color}{char}")
        sys.stdout.flush()
        time.sleep(0.008)
    sys.stdout.write(theme.colors['RST'] + "\n")


def pulse_text(text, r=255, g=0, b=128, theme=None):
    """Effet de pulsation lumineuse."""
    theme = theme or default_theme

    for intensity in [255, 200, 150, 100, 150, 200, 255]:
        factor = intensity * 100 // 255
        color = theme._rgb(r * factor // 100, g * factor // 100, b * factor // 100)
        sys.stdout.write(f"\r{color}{theme.BLD}{text}{theme.colors['RST']}")
        sys.stdout.flush()
        time.sleep(0.06)
    print()


def matrix_intro(duration=2, theme=None):
    """
    Effet Matrix au démarrage.
    Garantit la restauration du curseur même en cas d'interruption.
    """
    theme = theme or default_theme
    chars = "0123456789ABCDEF"
    end_time = time.time() + duration

    try:
        cols, rows = shutil.get_terminal_size()
    except:
        cols, rows = 50, 20

    sys.stdout.write("\033[?25l")
    clear()

    try:
        while time.time() < end_time:
            col = random.randint(0, cols - 1)
            row = random.randint(0, rows - 1)
            char = random.choice(chars)
            color_code = 32 if random.random() > 0.5 else 82
            sys.stdout.write(f"\033[{row};{col}H\033[38;5;{color_code}m{char}\033[0m")
            sys.stdout.flush()
            time.sleep(0.008)
    finally:
        sys.stdout.write("\033[?25h")
        clear()


def rainbow_line(text, theme=None):
    """Affiche une ligne avec dégradé arc-en-ciel."""
    theme = theme or default_theme
    print(theme.rainbow(text))


def explode_text(text, color=None, theme=None):
    """Effet d'explosion de texte."""
    theme = theme or default_theme
    color = color or theme.get('GOLD', True)

    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)
    sys.stdout.write(theme.colors['RST'])
    time.sleep(0.15)
    for _ in range(3):
        sys.stdout.write("\b \b")
        sys.stdout.flush()
        time.sleep(0.03)
    print()


def draw_frame(style="double", width=50, c1=None, c2=None, theme=None):
    """Dessine un cadre décoratif."""
    theme = theme or default_theme
    c1 = c1 or theme.get('primary')
    c2 = c2 or theme.get('secondary')

    frames = {
        'single': ('┌', '┐', '┘', '└', '─', '│'),
        'double': ('╔', '╗', '╝', '╚', '═', '║'),
        'round': ('╭', '╮', '╯', '╰', '─', '│'),
        'heavy': ('┏', '┓', '┛', '┗', '━', '┃'),
        'hash': ('▓', '▓', '▓', '▓', '▒', '░'),
        'star': ('★', '★', '★', '★', '☆', '★'),
        'heart': ('♥', '♥', '♥', '♥', '♡', '♥'),
        'diamond': ('◆', '◆', '◆', '◆', '◇', '◆'),
        'pixel': ('█', '█', '█', '█', '█', '█'),
        'shadow': ('▛', '▜', '▙', '▟', '▀', '▌'),
        'neon': ('▓', '▓', '▓', '▓', '▒', '░'),
    }

    if style not in frames:
        return

    tl, tr, br, bl, h, v = frames[style]
    w = max(1, width - 2)

    print(f"  {c1}{tl}{h * w}{tr}{theme.colors['RST']}")
    print(f"  {c1}{v}{' ' * w}{v}{theme.colors['RST']}")
    print(f"  {c1}{bl}{h * w}{br}{theme.colors['RST']}")


def print_title_neon(title, subtitle="", c1=None, c2=None, theme=None):
    """Affiche un titre encadré."""
    theme = theme or default_theme
    c1 = c1 or theme.get('primary')
    c2 = c2 or theme.get('secondary')

    try:
        width = shutil.get_terminal_size().columns - 4
    except:
        width = 50

    line = "═" * width
    padding = (width - len(title) - 4) // 2

    print()
    print(f"  {c1}╔{line}╗{theme.colors['RST']}")
    print(f"  {c1}║{theme.colors['RST']}  {c2}{theme.BLD}{title:^{width-4}}{theme.colors['RST']}  {c1}║{theme.colors['RST']}")
    if subtitle:
        print(f"  {c1}║{theme.colors['RST']}  {theme.colors['DIM']}{subtitle:^{width-4}}{theme.colors['RST']}  {c1}║{theme.colors['RST']}")
    print(f"  {c1}╠{line}╣{theme.colors['RST']}")


def print_end_neon(c1=None, theme=None):
    """Ferme un bloc de titre."""
    theme = theme or default_theme
    c1 = c1 or theme.get('primary')

    try:
        width = shutil.get_terminal_size().columns - 4
    except:
        width = 50

    line = "═" * width
    print(f"  {c1}╚{line}╝{theme.colors['RST']}\n")


def print_success(text, theme=None):
    theme = theme or default_theme
    print(f"  {theme.get('GREEN', True)}✦ {text}{theme.colors['RST']}")


def print_warn(text, theme=None):
    theme = theme or default_theme
    print(f"  {theme.get('ORANGE', True)}▲ {text}{theme.colors['RST']}")


def print_error(text, theme=None):
    theme = theme or default_theme
    print(f"  {theme.get('RED', True)}✖ {text}{theme.colors['RST']}")


def print_info(text, icon="◈", theme=None):
    theme = theme or default_theme
    print(f"  {theme.get('CYAN')}{icon}  {theme.colors['DIM']}{text}{theme.colors['RST']}")


# ═══════════════════════════════════════════════════════════════════════
#  NOUVELLES ANIMATIONS
# ═══════════════════════════════════════════════════════════════════════

def typewrite_cursor(text, color=None, speed=0.02, theme=None):
    """
    Écrit le texte lettre par lettre avec un curseur ▊ qui clignote au bout,
    façon terminal rétro.
    """
    theme = theme or default_theme
    color = color or theme.get('primary', True)
    cursor = "▊"

    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(f"{char}{cursor}\b")
        sys.stdout.flush()
        time.sleep(speed)
        sys.stdout.write("\b \b")

    # Petit clignotement final du curseur (3 fois) avant de continuer
    for _ in range(3):
        sys.stdout.write(cursor)
        sys.stdout.flush()
        time.sleep(0.15)
        sys.stdout.write("\b \b")
        sys.stdout.flush()
        time.sleep(0.15)
    sys.stdout.write(theme.colors['RST'] + "\n")


def fade_in_color(text, r=57, g=255, b=20, steps=6, theme=None):
    """
    Le texte apparaît en gris sombre puis "monte en couleur" progressivement
    vers sa teinte finale (r, g, b).
    """
    theme = theme or default_theme
    gray = 70

    for i in range(1, steps + 1):
        factor = i / steps
        cr = int(gray + (r - gray) * factor)
        cg = int(gray + (g - gray) * factor)
        cb = int(gray + (b - gray) * factor)
        color = theme._rgb(cr, cg, cb)
        sys.stdout.write(f"\r{color}{theme.BLD}{text}{theme.colors['RST']}")
        sys.stdout.flush()
        time.sleep(0.07)
    print()


def boot_sequence(lines=None, theme=None):
    """
    Petite séquence façon démarrage BIOS/Linux avant la bannière :
    des lignes "[ OK ] ..." qui défilent vite (moins de 2s au total).
    """
    theme = theme or default_theme
    ok = f"{theme.get('GREEN', True)}[ OK ]{theme.colors['RST']}"
    default_lines = [
        "Initialisation du noyau hacker...",
        "Chargement des modules truecolor...",
        "Montage de la partition /dev/neon...",
        "Vérification de l'intégrité du cadre ASCII...",
        "Démarrage des services de bannière...",
    ]
    lines = lines or default_lines

    for line in lines:
        sys.stdout.write(f"  {ok} {theme.colors['DIM']}{line}{theme.colors['RST']}\n")
        sys.stdout.flush()
        time.sleep(0.15)


def confetti_rain(duration=1.5, theme=None):
    """
    Petite pluie de confettis ASCII qui tombent.
    Garantit la restauration du curseur même en cas d'interruption.
    """
    theme = theme or default_theme
    symbols = "*✦░▪·"
    palette_names = ['PINK', 'CYAN', 'GREEN', 'YELLOW', 'GOLD', 'PURPLE']

    try:
        cols, rows = shutil.get_terminal_size()
    except Exception:
        cols, rows = 50, 20

    sys.stdout.write("\033[?25l")
    end_time = time.time() + duration
    try:
        while time.time() < end_time:
            col = random.randint(0, max(cols - 1, 0))
            row = random.randint(0, max(rows - 1, 0))
            char = random.choice(symbols)
            color = theme.get(random.choice(palette_names), True)
            sys.stdout.write(f"\033[{row};{col}H{color}{char}{theme.colors['RST']}")
            sys.stdout.flush()
            time.sleep(0.006)
    finally:
        sys.stdout.write("\033[?25h\n")


def neon_buzz(text, color=None, flickers=3, theme=None):
    """
    Le titre clignote comme un tube néon qui s'allume (2-3 flashs rapides
    et irréguliers) avant de se stabiliser dans sa couleur finale.
    """
    theme = theme or default_theme
    color = color or theme.get('primary', True)
    dim = theme.colors['DIM']
    rst = theme.colors['RST']

    pattern = [0.05, 0.08, 0.03, 0.12, 0.02, 0.2]
    for i, delay in enumerate(pattern):
        on = (i % 2 == 0)
        shown = f"{color}{theme.BLD}{text}{rst}" if on else f"{dim}{text}{rst}"
        sys.stdout.write(f"\r{shown}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(f"\r{color}{theme.BLD}{text}{rst}\n")
    sys.stdout.flush()
