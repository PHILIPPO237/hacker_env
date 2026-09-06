# -*- coding: utf-8 -*-
"""
Theme system for HACKER_ENV V2
Provides configurable visual themes.
"""
from themes.cyber import CyberTheme
from themes.matrix import MatrixTheme
from themes.neon import NeonTheme
from themes.minimal import MinimalTheme
from themes.classic import ClassicTheme

AVAILABLE_THEMES = {
    'cyber': CyberTheme,
    'matrix': MatrixTheme,
    'neon': NeonTheme,
    'minimal': MinimalTheme,
    'classic': ClassicTheme,
}

def get_theme(name='cyber'):
    """Get theme by name."""
    theme_class = AVAILABLE_THEMES.get(name, CyberTheme)
    return theme_class()

def list_themes():
    """List all available themes."""
    return list(AVAILABLE_THEMES.keys())
