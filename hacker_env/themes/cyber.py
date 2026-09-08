# -*- coding: utf-8 -*-
"""
Cyber theme for HACKER_ENV V2
Futuristic cyan and magenta color scheme.
"""


class CyberTheme:
    """Cyberpunk-inspired theme."""
    
    NAME = 'cyber'
    DESCRIPTION = 'Futuristic cyan and magenta color scheme'
    
    # Color palette (R, G, B)
    COLORS = {
        'primary': (0, 255, 255),      # Cyan
        'secondary': (255, 0, 128),    # Magenta
        'accent': (147, 0, 211),       # Purple
        'success': (0, 255, 128),      # Green
        'warning': (255, 191, 0),      # Amber
        'error': (255, 50, 50),        # Red
        'info': (0, 200, 255),         # Light blue
        'text': (255, 255, 255),       # White
        'dim': (128, 128, 128),        # Gray
    }
    
    # Theme-specific settings
    BANNER_STYLE = 'double'
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
