# -*- coding: utf-8 -*-
"""
Module de bannières ASCII avancé
Inspiré de hacker_env.py : 20 modèles, cadres dynamiques, preview
"""

from dataclasses import dataclass
from typing import Optional
from core.colors import NeonTheme


@dataclass
class BannerModel:
    """Représentation d'un modèle de bannière"""
    id: str
    name: str
    description: str
    frame_style: str
    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str
    horizontal: str
    vertical: str
    primary_color: str
    secondary_color: str
    accent_color: str
    art: str


class BannerGallery:
    """Galerie des 20 modèles de bannières (inspirée de hacker_env.py)"""

    MODELS = {
        "1": BannerModel(
            id="1", name="Hacker Neon",
            description="Cadre double, vert néon/jaune. Look Matrix classique.",
            frame_style="double", top_left="╔", top_right="╗",
            bottom_left="╚", bottom_right="╝",
            horizontal="═", vertical="║",
            primary_color="GREEN", secondary_color="YELLOW", accent_color="CYAN",
            art=r"""
  ██████╗ ██╗██████╗  ██████╗ ██████╗ ██████╗ ███████╗
  ██╔══██╗██║██╔══██╗██╔═══██╗╚════██╗╚════██╗╚════██║
  ██████╔╝██║██████╔╝██║   ██║ █████╔╝ █████╔╝    ██╔╝
  ██╔═══╝ ██║██╔═══╝ ██║   ██║██╔═══╝  ╚═══██╗   ██╔╝
  ██║     ██║██║     ╚██████╔╝███████╗██████╔╝   ██║
  ╚═╝     ╚═╝╚═╝      ╚═════╝ ╚══════╝╚═════╝    ╚═╝"""
        ),
        "2": BannerModel(
            id="2", name="Cyberpunk 2077",
            description="Cadre double cyan/magenta, contraste vif.",
            frame_style="double", top_left="╔", top_right="╗",
            bottom_left="╚", bottom_right="╝",
            horizontal="═", vertical="║",
            primary_color="CYAN", secondary_color="PINK", accent_color="PURPLE",
            art=r"""
   ▄████████ ▄██   ▄      ▄████████    ▄████████  ▄██████▄  ███▄▄▄▄
  ███    ███ ███   ██▄   ███    ███   ███    ███ ███    ███ ███▀▀▀██▄
  ███    █▀  ███▄▄▄███   ███    █▀    ███    █▀  ███    ███ ███   ███
 ▄███▄▄▄     ▀▀▀▀▀▀███  ▄███▄▄▄      ▄███▄▄▄     ███    ███ ███   ███
▀▀███▀▀▀     ▄██   ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ███    ███ ███   ███
  ███        ███   ███   ███    █▄    ███    █▄  ███    ███ ███   ███
  ███        ███   ███   ███    ███   ███    ███ ███    ███ ███   ███
  ███         ▀█████▀    ██████████   ██████████  ▀██████▀   ▀█   █▀"""
        ),
        "3": BannerModel(
            id="3", name="Arrondi Moderne",
            description="Cadre arrondi, bleu/cyan doux.",
            frame_style="round", top_left="╭", top_right="╮",
            bottom_left="╰", bottom_right="╯",
            horizontal="─", vertical="│",
            primary_color="BLUE", secondary_color="CYAN", accent_color="WHITE",
            art=r"""
    ___    __  _____________   ________  ___   ____________
   /   |  /  |/  / ____/   | / ____/ / /   | / ___/_  ____/
  / /| | / /|_/ / /   / /| |/ /   / /_/ /| | \__ \ / /
 / ___ |/ /  / / /___/ ___ / /___/ __  / ___ |___/ // /
/_/  |_/_/  /_/\____/_/  |_\____/_/ /_/_/  |_/____//_/"""
        ),
        "4": BannerModel(
            id="4", name="Etoile Festif",
            description="Cadre etoiles, magenta/rose.",
            frame_style="star", top_left="★", top_right="★",
            bottom_left="★", bottom_right="★",
            horizontal="☆", vertical="★",
            primary_color="PURPLE", secondary_color="PINK", accent_color="CYAN",
            art=r"""
  ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★
  ☆  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  ☆
  ★  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  ★
  ☆  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  ☆
  ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★ ☆ ★"""
        ),
        "5": BannerModel(
            id="5", name="Minimaliste",
            description="Cadre simple, blanc/gris.",
            frame_style="single", top_left="+", top_right="+",
            bottom_left="+", bottom_right="+",
            horizontal="-", vertical="|",
            primary_color="WHITE", secondary_color="SILVER", accent_color="BLUE",
            art=r"""
  +--------------------------------------------------+
  |  _   _       _     _            _   _            |
  | | | | | __ _| |__ | | ___   ___| |_| | ___ _ __  |
  | | |_| |/ _` | '_ \| |/ _ \ / _ \ __| |/ _ \ '__| |
  | |  _  | (_| | | | | | (_) |  __/ |_| |  __/ |    |
  | |_| |_|\__,_|_| |_|_|\___/ \___|\__|_|\___|_|    |
  +--------------------------------------------------+"""
        ),
        "6": BannerModel(
            id="6", name="Sans Cadre",
            description="Pas de cadre, juste le titre.",
            frame_style="none", top_left="", top_right="",
            bottom_left="", bottom_right="",
            horizontal="", vertical="",
            primary_color="GREEN", secondary_color="YELLOW", accent_color="CYAN",
            art=r"""
    _    _  _____ ______ _   _ ______ _____
   | |  | |/ ____|  ____| \ | |  ____|  __ \
   | |__| | |    | |__  |  \| | |__  | |__) |
   |  __  | |    |  __| | . ` |  __| |  _  /
   | |  | | |____| |____| |\  | |____| | \ \
   |_|  |_|\_____|______|_| \_|______|_|  \_\\"""
        ),
        "7": BannerModel(
            id="7", name="Gothique",
            description="Cadre lourd, violet/noir.",
            frame_style="heavy", top_left="┏", top_right="┓",
            bottom_left="┗", bottom_right="┛",
            horizontal="━", vertical="┃",
            primary_color="PURPLE", secondary_color="LAVENDER", accent_color="SILVER",
            art=r"""
  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ┃  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  ┃
  ┃  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  ┃
  ┃  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  ┃
  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"""
        ),
        "8": BannerModel(
            id="8", name="Sunset Vaporwave",
            description="Cadre blocs, rose/orange/jaune.",
            frame_style="hash", top_left="▓", top_right="▓",
            bottom_left="▓", bottom_right="▓",
            horizontal="▒", vertical="░",
            primary_color="PINK", secondary_color="ORANGE", accent_color="YELLOW",
            art=r"""
  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  ░░  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  ░░
  ░░  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  ░░
  ░░  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  ░░
  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"""
        ),
        "9": BannerModel(
            id="9", name="Steampunk",
            description="Cadre engrenages, bronze/cuivre.",
            frame_style="emoji", top_left="⚙", top_right="⚙",
            bottom_left="⚙", bottom_right="⚙",
            horizontal="═", vertical="║",
            primary_color="BRONZE", secondary_color="GOLD", accent_color="SILVER",
            art=r"""
  ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙
  ⚙  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  ⚙
  ⚙  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  ⚙
  ⚙  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  ⚙
  ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙"""
        ),
        "10": BannerModel(
            id="10", name="Stealth Noir",
            description="Cadre double, noir + rouge sang.",
            frame_style="double", top_left="╔", top_right="╗",
            bottom_left="╚", bottom_right="╝",
            horizontal="═", vertical="║",
            primary_color="INDIGO", secondary_color="BLOOD", accent_color="SILVER",
            art=r"""
  ╔══════════════════════════════════════════════════╗
  ║  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  ║
  ║  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  ║
  ║  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  ║
  ╚══════════════════════════════════════════════════╝"""
        ),
        "11": BannerModel(
            id="11", name="Biohazard",
            description="Cadre cranes, vert toxique.",
            frame_style="zodiac", top_left="☠", top_right="☠",
            bottom_left="☠", bottom_right="☠",
            horizontal="═", vertical="║",
            primary_color="LIME", secondary_color="YELLOW", accent_color="GREEN",
            art=r"""
  ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠
  ☠  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  ☠
  ☠  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  ☠
  ☠  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  ☠
  ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠ ☠"""
        ),
        "12": BannerModel(
            id="12", name="Festif Noel",
            description="Cadre sapins, rouge/vert.",
            frame_style="emoji", top_left="🎄", top_right="🎄",
            bottom_left="🎁", bottom_right="🎁",
            horizontal="─", vertical="│",
            primary_color="EMERALD", secondary_color="GOLD", accent_color="RED",
            art=r"""
  🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄
  🎄  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  🎄
  🎄  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  🎄
  🎄  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  🎄
  🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄 🎄"""
        ),
        "13": BannerModel(
            id="13", name="Romantique",
            description="Cadre coeurs, rose/rouge.",
            frame_style="heart", top_left="♥", top_right="♥",
            bottom_left="♥", bottom_right="♥",
            horizontal="♡", vertical="♥",
            primary_color="PINK", secondary_color="RED", accent_color="LAVENDER",
            art=r"""
  ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥
  ♡  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  ♡
  ♥  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  ♥
  ♡  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  ♡
  ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥ ♡ ♥"""
        ),
        "14": BannerModel(
            id="14", name="Diamant",
            description="Cadre diamants, cyan/argent.",
            frame_style="diamond", top_left="◆", top_right="◆",
            bottom_left="◆", bottom_right="◆",
            horizontal="◇", vertical="◆",
            primary_color="CYAN", secondary_color="SILVER", accent_color="WHITE",
            art=r"""
  ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆
  ◇  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  ◇
  ◆  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  ◆
  ◇  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  ◇
  ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆"""
        ),
        "15": BannerModel(
            id="15", name="Fleche",
            description="Cadre fleches, orange/jaune.",
            frame_style="arrow", top_left="▶", top_right="◀",
            bottom_left="▶", bottom_right="◀",
            horizontal="─", vertical="▶",
            primary_color="ORANGE", secondary_color="YELLOW", accent_color="GOLD",
            art=r"""
  ▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶
  ─▶  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  ◀─
  ▶ ─▶  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  ─▶ ◀─
  ─▶  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  ◀─
  ▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶ ─▶"""
        ),
        "16": BannerModel(
            id="16", name="Musical",
            description="Cadre notes, violet/orchidee.",
            frame_style="music", top_left="♪", top_right="♪",
            bottom_left="♫", bottom_right="♫",
            horizontal="♪", vertical="♫",
            primary_color="PURPLE", secondary_color="LAVENDER", accent_color="PINK",
            art=r"""
  ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪
  ♫  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  ♫
  ♪  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  ♪
  ♫  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  ♫
  ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪"""
        ),
        "17": BannerModel(
            id="17", name="Cyber Grille",
            description="Cadre pixels, neon cyan/rose.",
            frame_style="pixel", top_left="▓", top_right="▓",
            bottom_left="▓", bottom_right="▓",
            horizontal="▒", vertical="█",
            primary_color="CYAN", secondary_color="PINK", accent_color="PURPLE",
            art=r"""
  ░░▒▒▓▓██▓▓▒▒░░░░▒▒▓▓██▓▓▒▒░░░░▒▒▓▓██▓▓▒▒░░
  ▒▒  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  ▒▒
  ▓▓  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  ▓▓
  ██  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  ██
  ░░▒▒▓▓██▓▓▒▒░░░░▒▒▓▓██▓▓▒▒░░░░▒▒▓▓██▓▓▒▒░░"""
        ),
        "18": BannerModel(
            id="18", name="Shadow Box",
            description="Cadre ombre, gris/argent.",
            frame_style="shadow", top_left="▛", top_right="▜",
            bottom_left="▙", bottom_right="▟",
            horizontal="▀", vertical="▌",
            primary_color="SILVER", secondary_color="CHARCOAL", accent_color="WHITE",
            art=r"""
  ▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜
  ▌  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  ▐
  ▌  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  ▐
  ▌  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  ▐
  ▙▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▟"""
        ),
        "19": BannerModel(
            id="19", name="Pixel Art",
            description="Cadre plein, rouge/crimson.",
            frame_style="pixel", top_left="█", top_right="█",
            bottom_left="█", bottom_right="█",
            horizontal="█", vertical="█",
            primary_color="CRIMSON", secondary_color="RED", accent_color="BLOOD",
            art=r"""
  ████████████████████████████████████████████
  █  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  █
  █  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  █
  █  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  █
  ████████████████████████████████████████████"""
        ),
        "20": BannerModel(
            id="20", name="Neon Glow",
            description="Cadre degrade, cyan/magenta/jaune.",
            frame_style="neon", top_left="▓", top_right="▓",
            bottom_left="▓", bottom_right="▓",
            horizontal="▒", vertical="░",
            primary_color="CYAN", secondary_color="PINK", accent_color="YELLOW",
            art=r"""
  ░▒▓██████▓▒░░░▒▓██████▓▒░░░▒▓██████▓▒░░░▒▓█
  ▒▓  ░█▀▀░█▀█░█▀█░█▀▀░█▀▀░█▀█░█▀█  ▓▒
  ▓▒  ░█░░░█▀█░█░█░█░█░█▀▀░█▀█░█░█  ▒▓
  █▓  ░▀▀▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀  ▓█
  ░▒▓██████▓▒░░░▒▓██████▓▒░░░▒▓██████▓▒░░░▒▓█"""
        ),
        # ── Nouveaux modeles (assortis aux themes recemment ajoutes
        # dans core/colors.py qui n'avaient pas encore de banniere) ──
        "21": BannerModel(
            id="21", name="Sakura",
            description="Cadre petales, rose blossom/menthe pastel.",
            frame_style="petal", top_left="✿", top_right="✿",
            bottom_left="✿", bottom_right="✿",
            horizontal=".", vertical=":",
            primary_color="BLOSSOM", secondary_color="MINT", accent_color="WHITE",
            art=r"""
   _____ _____ _____   ____ ___  ____ ______
  |  __ \_   _|  __ \ / __ \__ \|___ \____  |
  | |__) || | | |__) | |  | | ) | __) |  / /
  |  ___/ | | |  ___/| |  | |/ / |__ <  / /
  | |    _| |_| |    | |__| / /_ ___) |/ /
  |_|   |_____|_|     \____/____|____//_/"""
        ),
        "22": BannerModel(
            id="22", name="Blood Moon",
            description="Cadre dentele, rouge sang/braise/cramoisi.",
            frame_style="jagged", top_left="▚", top_right="▚",
            bottom_left="▚", bottom_right="▚",
            horizontal="▬", vertical="▌",
            primary_color="BLOOD", secondary_color="EMBER", accent_color="CRIMSON",
            art=r"""
  ______ ___________ _____  _____  _____  ______
  | ___ \_   _| ___ \  _  |/ __  \|____ ||___  /
  | |_/ / | | | |_/ / | | |`' / /'    / /   / /
  |  __/  | | |  __/| | | |  / /      \ \  / /
  | |    _| |_| |   \ \_/ /./ /___.___/ /./ /
  \_|    \___/\_|    \___/ \_____/\____/ \_/"""
        ),
        "23": BannerModel(
            id="23", name="Ocean Deep",
            description="Cadre onde, bleu abysse/turquoise/cyan.",
            frame_style="wave", top_left="≈", top_right="≈",
            bottom_left="≈", bottom_right="≈",
            horizontal="~", vertical="│",
            primary_color="DEEP_BLUE", secondary_color="TURQUOISE", accent_color="CYAN",
            art=r"""
      ____  ________  ____ ___  __________
     / __ \/  _/ __ \/ __ \__ \|__  /__  /
    / /_/ // // /_/ / / / /_/ / /_ <  / /
   / ____// // ____/ /_/ / __/___/ / / /
  /_/   /___/_/    \____/____/____/ /_/"""
        ),
        "24": BannerModel(
            id="24", name="Solar Flare",
            description="Cadre rayonnant, orange/or/rouge.",
            frame_style="radiant", top_left="☀", top_right="☀",
            bottom_left="☀", bottom_right="☀",
            horizontal="─", vertical="┃",
            primary_color="ORANGE", secondary_color="GOLD", accent_color="RED",
            art=r"""
  .______    __  .______     ______    ___    ____    ______
  |   _  \  |  | |   _  \   /  __  \  |__ \  |___ \  |____  |
  |  |_)  | |  | |  |_)  | |  |  |  |    ) |   __) |     / /
  |   ___/  |  | |   ___/  |  |  |  |   / /   |__ <     / /
  |  |      |  | |  |      |  `--'  |  / /_   ___) |   / /
  | _|      |__| | _|       \______/  |____| |____/   /_/"""
        ),
        "25": BannerModel(
            id="25", name="Monochrome",
            description="Cadre epure, gris clair/gris moyen/anthracite.",
            frame_style="single", top_left="┌", top_right="┐",
            bottom_left="└", bottom_right="┘",
            horizontal="─", vertical="│",
            primary_color="GRAY_LIGHT", secondary_color="GRAY_MID", accent_color="CHARCOAL",
            art=r"""
   ____ ___ ____   ___ ____  __________
  |  _ \_ _|  _ \ / _ \___ \|___ /___  |
  | |_) | || |_) | | | |__) | |_ \  / /
  |  __/| ||  __/| |_| / __/ ___) |/ /
  |_|  |___|_|    \___/_____|____//_/"""
        ),
        # ── Deuxieme vague de modeles : combinaisons de couleurs de la
        # palette de base encore inexploitees par les modeles precedents ──
        "26": BannerModel(
            id="26", name="Emerald Circuit",
            description="Cadre circuit imprime, emeraude/sarcelle/citron vert.",
            frame_style="circuit", top_left="╬", top_right="╬",
            bottom_left="╬", bottom_right="╬",
            horizontal="═", vertical="┃",
            primary_color="EMERALD", secondary_color="TEAL", accent_color="LIME",
            art=r"""
  +-+-+-+-+-+-+-+
  |P|I|P|O|2|3|7|
  +-+-+-+-+-+-+-+"""
        ),
        "27": BannerModel(
            id="27", name="Coral Reef",
            description="Cadre ondulant, corail/turquoise/blanc.",
            frame_style="reef", top_left="~", top_right="~",
            bottom_left="~", bottom_right="~",
            horizontal="∿", vertical="|",
            primary_color="CORAL", secondary_color="TURQUOISE", accent_color="WHITE",
            art=r"""
   __   __  __  __  __  ___
  |__)||__)/  \  _)  _)   /
  |   ||   \__/ /__ __)  /"""
        ),
        "28": BannerModel(
            id="28", name="Indigo Void",
            description="Cadre etoile, indigo/violet/argent.",
            frame_style="void", top_left="◆", top_right="◆",
            bottom_left="◆", bottom_right="◆",
            horizontal="·", vertical=":",
            primary_color="INDIGO", secondary_color="PURPLE", accent_color="SILVER",
            art=r"""
  .__ ._..__ .__. _,  _, __,
  [__) | [__)|  |'_) '_)  /
  |   _|_|   |__|/_. ._) /"""
        ),
        "29": BannerModel(
            id="29", name="Toxic Waste",
            description="Cadre danger, citron vert/jaune/sang.",
            frame_style="toxic", top_left="☣", top_right="☣",
            bottom_left="☣", bottom_right="☣",
            horizontal="▓", vertical="▒",
            primary_color="LIME", secondary_color="YELLOW", accent_color="BLOOD",
            art='''
  8""""8 8  8""""8 8"""88 eeee eeee eeeee
  8    8 8  8    8 8    8    8    8 8   8
  8eeee8 8e 8eeee8 8    8    8    8    e'
  88     88 88     8    8 eee8 eee8   e'
  88     88 88     8    8 8       88  8
  88     88 88     8eeee8 8eee eee88  8'''
        ),
        "30": BannerModel(
            id="30", name="Royal Gold",
            description="Cadre double ornemente, or/bronze/blanc.",
            frame_style="royal", top_left="♛", top_right="♛",
            bottom_left="♛", bottom_right="♛",
            horizontal="═", vertical="║",
            primary_color="GOLD", secondary_color="BRONZE", accent_color="WHITE",
            art=r"""
  '||'''|, |''||''| '||'''|, .|''''|,  ''|, ,'''|, '''''/
   ||   ||    ||     ||   || ||    || '  ||     ||    //
   ||...|'    ||     ||...|' ||    ||   .|'  '''||   //
   ||         ||     ||      ||    ||  //       ||  //
  .||      |..||..| .||      `|....|' ((... '...|' //"""
        ),
    }

    @classmethod
    def get(cls, model_id: str) -> Optional[BannerModel]:
        """Recupere un modele par ID"""
        return cls.MODELS.get(model_id)

    @classmethod
    def list_all(cls) -> list:
        """Liste tous les modeles disponibles"""
        return list(cls.MODELS.values())

    @classmethod
    def preview(cls, model_id: str, user_name: str = "Hacker", theme=None):
        """
        Affiche un apercu complet du modele (inspire de hacker_env.py)

        Args:
            model_id: ID du modele
            user_name: Nom de l'utilisateur
            theme: Instance NeonTheme (optionnel)
        """
        model = cls.get(model_id)
        if not model:
            print(f"Modele {model_id} introuvable")
            return

        theme = theme or NeonTheme('hacker_neon')

        # Couleurs du theme
        c1 = theme.get(model.primary_color)
        c2 = theme.get(model.secondary_color)
        c3 = theme.get(model.accent_color)

        print()
        # Ligne arc-en-ciel
        rainbow_text = theme.rainbow(f"  === MODELE {model.id} : {model.name} ===")
        print(rainbow_text)
        print(f"  {theme.colors['DIM']}{model.description}{theme.colors['RST']}")
        print(f"  {theme.get('SILVER')}Cadre : {model.frame_style}{theme.colors['RST']}")

        # Cadre
        if model.frame_style != "none":
            width = 50
            tl, tr, bl, br, h, v = (model.top_left, model.top_right, 
                                     model.bottom_left, model.bottom_right,
                                     model.horizontal, model.vertical)
            print(f"  {c1}{tl}{h * (width-2)}{tr}{theme.colors['RST']}")

        # Art ASCII
        for line in model.art.strip().split('\n'):
            print(f"  {c1}{theme.BLD}{line}{theme.colors['RST']}")

        # Info box
        emoji = "💀"
        title = "HACK THE PLANET"
        line_text = f"{emoji}  {user_name} — {title}  {emoji}"

        if model.frame_style != "none" and model.horizontal and model.vertical:
            box_width = len(line_text) + 4
            top = f"{c2}{theme.BLD}{model.top_left}{model.horizontal * box_width}{model.top_right}{theme.colors['RST']}"
            mid = f"{c2}{theme.BLD}{model.vertical} {c1}{theme.BLD}{line_text}{c2}{theme.BLD} {model.vertical}{theme.colors['RST']}"
            bot = f"{c2}{theme.BLD}{model.bottom_left}{model.horizontal * box_width}{model.bottom_right}{theme.colors['RST']}"
            print(f"  {top}\n  {mid}\n  {bot}")
        else:
            print(f"  {c2}{theme.BLD}{line_text}{theme.colors['RST']}")

        # Separateur degrade
        sep = ""
        for j in range(50):
            if j < 17:
                sep += f"{c1}─"
            elif j < 34:
                sep += f"{c2}─"
            else:
                sep += f"{c3}─"
        print(f"  {sep}{theme.colors['RST']}")

        # Infos systeme (simulees)
        from core.system import get_system_info
        info = get_system_info()

        print(f"  {c3}{theme.BLD}  📅 Date   :{theme.colors['RST']}  {__import__('datetime').datetime.now().strftime('%a %d %b %Y %H:%M')}")
        print(f"  {c3}{theme.BLD}  ⏱  Uptime :{theme.colors['RST']}  {info.get('uptime', 'n/a')}")
        print(f"  {c3}{theme.BLD}  🌐 IP     :{theme.colors['RST']}  {info.get('ip', 'offline')}")
        print(f"  {c3}{theme.BLD}  ⚡ CPU    :{theme.colors['RST']}  {info.get('cpu', 'n/a')}")
        print(f"  {c3}{theme.BLD}  🧠 RAM    :{theme.colors['RST']}  {info.get('ram', 'n/a')}")
        print(f"  {c3}{theme.BLD}  💾 DISK   :{theme.colors['RST']}  {info.get('disk', 'n/a')}")
        print(f"  {sep}{theme.colors['RST']}")
        print()


# Compatibilite ascendante
MODELS = {k: {"name": v.name, "art": v.art} for k, v in BannerGallery.MODELS.items()}
