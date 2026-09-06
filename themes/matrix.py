# -*- coding: utf-8 -*-
"""
Matrix theme for HACKER_ENV V2
Classic green-on-black hacker aesthetic.
"""


class MatrixTheme:
    """Matrix-inspired theme."""
    
    NAME = 'matrix'
    DESCRIPTION = 'Classic green-on-black hacker aesthetic'
    
    # Color palette (R, G, B)
    COLORS = {
        'primary': (57, 255, 20),       # Matrix green
        'secondary': (0, 255, 0),       # Bright green
        'accent': (50, 205, 50),        # Lime green
        'success': (0, 255, 0),         # Green
        'warning': (255, 255, 0),       # Yellow
        'error': (255, 50, 50),         # Red
        'info': (0, 255, 128),          # Spring green
        'text': (255, 255, 255),        # White
        'dim': (100, 100, 100),         # Dark gray
    }
    
    # Theme-specific settings
    BANNER_STYLE = 'heavy'
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
