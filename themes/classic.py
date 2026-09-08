# -*- coding: utf-8 -*-
"""
Classic theme for HACKER_ENV V2
Traditional terminal colors.
"""


class ClassicTheme:
    """Classic terminal theme."""
    
    NAME = 'classic'
    DESCRIPTION = 'Traditional terminal colors'
    
    # Color palette (R, G, B)
    COLORS = {
        'primary': (0, 200, 0),         # Green
        'secondary': (0, 150, 0),       # Dark green
        'accent': (255, 255, 0),        # Yellow
        'success': (0, 200, 0),         # Green
        'warning': (255, 191, 0),       # Amber
        'error': (255, 0, 0),           # Red
        'info': (0, 200, 200),          # Cyan
        'text': (255, 255, 255),        # White
        'dim': (128, 128, 128),         # Gray
    }
    
    # Theme-specific settings
    BANNER_STYLE = 'double'
    PROMPT_STYLE = 'hacker'
    
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
