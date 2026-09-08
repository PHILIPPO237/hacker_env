# -*- coding: utf-8 -*-
"""
Neon theme for HACKER_ENV V2
Vibrant neon colors with glow effects.
"""


class NeonTheme:
    """Neon-inspired theme."""
    
    NAME = 'neon'
    DESCRIPTION = 'Vibrant neon colors with glow effects'
    
    # Color palette (R, G, B)
    COLORS = {
        'primary': (255, 0, 128),       # Hot pink
        'secondary': (0, 255, 255),     # Cyan
        'accent': (255, 255, 0),        # Yellow
        'success': (0, 255, 128),       # Spring green
        'warning': (255, 191, 0),       # Amber
        'error': (255, 50, 50),         # Red
        'info': (147, 0, 211),          # Purple
        'text': (255, 255, 255),        # White
        'dim': (128, 128, 128),         # Gray
    }
    
    # Theme-specific settings
    BANNER_STYLE = 'neon'
    PROMPT_STYLE = 'cyber'
    
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
