# -*- coding: utf-8 -*-
"""
Module BIGFONT — convertit un texte tapé par l'utilisateur en grandes
lettres bloc (5 lignes de haut), pour remplacer l'art décoratif fixe
d'un modèle par SON PROPRE nom/texte dans la bannière.
"""

FONT = {
    'A': [".##.", "#..#", "####", "#..#", "#..#"],
    'B': ["###.", "#..#", "###.", "#..#", "###."],
    'C': [".###", "#...", "#...", "#...", ".###"],
    'D': ["###.", "#..#", "#..#", "#..#", "###."],
    'E': ["####", "#...", "###.", "#...", "####"],
    'F': ["####", "#...", "###.", "#...", "#..."],
    'G': [".###", "#...", "#.##", "#..#", ".###"],
    'H': ["#..#", "#..#", "####", "#..#", "#..#"],
    'I': ["###", ".#.", ".#.", ".#.", "###"],
    'J': ["..##", "...#", "...#", "#..#", ".##."],
    'K': ["#..#", "#.#.", "##..", "#.#.", "#..#"],
    'L': ["#...", "#...", "#...", "#...", "####"],
    'M': ["#...#", "##.##", "#.#.#", "#...#", "#...#"],
    'N': ["#...#", "##..#", "#.#.#", "#..##", "#...#"],
    'O': [".##.", "#..#", "#..#", "#..#", ".##."],
    'P': ["###.", "#..#", "###.", "#...", "#..."],
    'Q': [".##.", "#..#", "#..#", "#.#.", ".###"],
    'R': ["###.", "#..#", "###.", "#.#.", "#..#"],
    'S': [".###", "#...", ".##.", "...#", "###."],
    'T': ["###", ".#.", ".#.", ".#.", ".#."],
    'U': ["#..#", "#..#", "#..#", "#..#", ".##."],
    'V': ["#...#", "#...#", ".#.#.", ".#.#.", "..#.."],
    'W': ["#...#", "#...#", "#.#.#", "##.##", "#...#"],
    'X': ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"],
    'Y': ["#...#", ".#.#.", "..#..", "..#..", "..#.."],
    'Z': ["####", "...#", "..#.", ".#..", "####"],
    '0': [".##.", "#..#", "#..#", "#..#", ".##."],
    '1': [".#.", "##.", ".#.", ".#.", "###"],
    '2': ["###.", "...#", ".##.", "#...", "####"],
    '3': ["###.", "...#", "..##", "...#", "###."],
    '4': ["#..#", "#..#", "####", "...#", "...#"],
    '5': ["####", "#...", "###.", "...#", "###."],
    '6': [".###", "#...", "###.", "#..#", ".##."],
    '7': ["####", "...#", "..#.", ".#..", ".#.."],
    '8': [".##.", "#..#", ".##.", "#..#", ".##."],
    '9': [".##.", "#..#", ".###", "...#", ".##."],
    ' ': ["..", "..", "..", "..", ".."],
    '-': ["...", "...", "###", "...", "..."],
    '_': ["...", "...", "...", "...", "###"],
    '.': [".", ".", ".", ".", "#"],
}

# Ajusté pour tenir sur un terminal mobile standard (50-60 cols)
# Chaque lettre fait ~4-5 caractères de large + 1 espace = ~6 max.
# 60 / 6 = 10 caractères max.
MAX_CHARS = 10


def render_big_text(text, block="█"):
    """Renvoie une liste de 5 chaînes formant `text` en grandes lettres bloc.
    Caractères non reconnus (emoji, accents...) traités comme un espace."""
    text = text.upper()[:MAX_CHARS]
    rows = ["", "", "", "", ""]
    for ch in text:
        glyph = FONT.get(ch, FONT[' '])
        for i in range(5):
            rows[i] += glyph[i].replace('#', block).replace('.', ' ') + " "
    return [row.rstrip() for row in rows]


def render_big_text_joined(text, block="█"):
    """Comme render_big_text mais renvoie une seule chaîne, lignes séparées
    par \n — pratique pour l'insérer directement dans un template."""
    return "\n".join(render_big_text(text, block))


def fits_width(text, max_width=60):
    """Estime si le rendu tiendra dans un terminal de `max_width` colonnes."""
    lines = render_big_text(text)
    return max((len(l) for l in lines), default=0) <= max_width
