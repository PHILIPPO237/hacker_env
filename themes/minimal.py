# -*- coding: utf-8 -*-
"""
Minimal theme for HACKER_ENV V2
Clean, simple design with neutral colors.
"""


class MinimalTheme:
    """Minimalist theme."""
    
    NAME = 'minimal'
    DESCRIPTION = 'Clean, simple design with neutral colors'
    
    # Color palette (R, G, B)
    COLORS = {
        'primary': (255, 255, 255),     # White
        'secondary': (192, 192, 192),   # Silver
        'accent': (30, 144, 255),       # Blue
        'success': (0, 200, 0),         # Green
        'warning': (255, 191, 0),       # Amber
        'error': (255, 50, 50),         # Red
        'info': (100, 149, 237),        # Cornflower blue
        'text': (255, 255, 255),        # White
        'dim': (128, 128, 128),         # Gray
    }
    
    # Theme-specific settings
    BANNER_STYLE = 'single'
    PROMPT_STYLE = 'minimal'
    
    def get_color(self, name: str) -> str:
        """Get ANSI color code for a color name."""
        if name in self.COLORS:
            r, g, b = self.COLORS[name]
            return f"\033[38;2;{r};{g};{b}m"
        return "\033[0m"
    
    def get_bold(self, name: str) -> str:
        """Get bold ANSI color code for a color name."""
        if name in self.COLORS:
            r, g, b = self.COLORS[name]
            return f"\033[1;38;2;{r};{g};{b}m"
        return "\033[1m"
