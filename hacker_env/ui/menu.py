# -*- coding: utf-8 -*-
"""
Menu system for HACKER_ENV V2
Provides interactive menus and user interface.
"""

import os
import sys
import shutil
from typing import List, Dict, Callable, Optional
from core.colors import NeonTheme, default_theme


class MenuItem:
    """Represents a menu item."""
    
    def __init__(self, key: str, label: str, description: str = "", action: Optional[Callable] = None):
        """
        Initialize menu item.
        
        Args:
            key: Key to select this item
            label: Display label
            description: Optional description
            action: Optional callback function
        """
        self.key = key
        self.label = label
        self.description = description
        self.action = action


class Menu:
    """Interactive menu system."""
    
    def __init__(self, title: str, items: List[MenuItem], theme: Optional[NeonTheme] = None):
        """
        Initialize menu.
        
        Args:
            title: Menu title
            items: List of menu items
            theme: Theme to use
        """
        self.title = title
        self.items = items
        self.theme = theme or default_theme
    
    def _get_box_chars(self) -> dict:
        """Get box drawing characters."""
        return {
            'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯',
            'h': '─', 'v': '│',
        }
    
    def _get_top_border(self, width: int, chars: dict) -> str:
        """Get top border."""
        color = self.theme.get('primary', True)
        rst = self.theme.colors['RST']
        return f"  {color}{chars['tl']}{chars['h'] * width}{chars['tr']}{rst}"
    
    def _get_title_line(self, title: str, width: int, chars: dict) -> str:
        """Get centered title line."""
        color = self.theme.get('primary', True)
        title_color = self.theme.get('primary', True)
        rst = self.theme.colors['RST']
        
        padding = width - len(title) - 4
        left_pad = padding // 2
        right_pad = padding - left_pad
        
        return f"  {color}{chars['v']}{rst}{' ' * left_pad}{title_color}{title}{rst}{' ' * right_pad}{color}{chars['v']}{rst}"
    
    def _get_bottom_border(self, width: int, chars: dict) -> str:
        """Get bottom border."""
        color = self.theme.get('primary', True)
        rst = self.theme.colors['RST']
        return f"  {color}{chars['bl']}{chars['h'] * width}{chars['br']}{rst}"
    
    def display(self) -> None:
        """Display the menu."""
        chars = self._get_box_chars()
        
        # Calculate width based on items
        max_width = len(self.title) + 4
        for item in self.items:
            item_width = len(f"{item.key}) {item.label}") + 4
            if item.description:
                item_width += len(item.description) + 4
            max_width = max(max_width, item_width)
        
        columns = shutil.get_terminal_size(fallback=(80, 20)).columns
        width = min(max_width, min(60, columns - 6))
        width = max(width, len(self.title) + 4)
        
        print()
        print(self._get_top_border(width, chars))
        print(self._get_title_line(self.title, width, chars))
        print(f"  {self.theme.get('primary', True)}{chars['h'] * (width + 2)}{self.theme.colors['RST']}")
        
        # Display items
        for item in self.items:
            key_color = self.theme.get('CYAN', True)
            label_color = self.theme.get('WHITE', True)
            desc_color = self.theme.colors['DIM']
            rst = self.theme.colors['RST']
            
            key_str = f"{key_color}{item.key}{rst}"
            label_str = f"{label_color}{item.label}{rst}"
            
            if item.description:
                desc_str = f"  {desc_color}{item.description}{rst}"
            else:
                desc_str = ""
            
            print(f"  {chars['v']}  {key_str}) {label_str}{desc_str}")
        
        print(self._get_bottom_border(width, chars))
        print()
    
    def get_choice(self) -> str:
        """Get user choice."""
        keys = [item.key for item in self.items]
        
        while True:
            choice = input(f"  {self.theme.get('CYAN')}➤  Select [{'/'.join(keys)}]: {self.theme.colors['RST']}").strip()
            
            if choice in keys:
                return choice
            
            print(f"  {self.theme.get('RED', True)}Invalid choice. Please try again.{self.theme.colors['RST']}")
    
    def execute(self) -> Optional[Callable]:
        """Display menu and execute selected action."""
        self.display()
        choice = self.get_choice()
        
        # Find and execute action
        for item in self.items:
            if item.key == choice and item.action:
                return item.action()
        
        return None


def create_main_menu(actions: Dict[str, Callable], theme: Optional[NeonTheme] = None) -> Menu:
    """
    Create the main menu.
    
    Args:
        actions: Dict mapping menu keys to callback functions
        theme: Theme to use
        
    Returns:
        Menu instance
    """
    items = []
    
    menu_mapping = {
        '1': ('Dashboard', 'View system information'),
        '2': ('Install', 'Complete installation'),
        '3': ('Setup', 'Platform-specific setup'),
        '4': ('Repair', 'Repair configuration'),
        '5': ('Update', 'Update packages'),
        '6': ('Theme', 'Change theme'),
        '7': ('Uninstall', 'Remove HACKER_ENV'),
        '8': ('Quit', 'Exit application'),
    }
    
    for key, (label, description) in menu_mapping.items():
        action = actions.get(key)
        items.append(MenuItem(key, label, description, action))
    
    return Menu("HACKER_ENV V2", items, theme)


def display_message(message: str, msg_type: str = 'info', theme: Optional[NeonTheme] = None) -> None:
    """
    Display a formatted message.
    
    Args:
        message: Message to display
        msg_type: Type of message ('info', 'success', 'warning', 'error')
        theme: Theme to use
    """
    theme = theme or default_theme
    
    icons = {
        'info': ('◈', 'CYAN'),
        'success': ('✓', 'GREEN'),
        'warning': ('⚠', 'YELLOW'),
        'error': ('✗', 'RED'),
    }
    
    icon, color_name = icons.get(msg_type, icons['info'])
    color = theme.get(color_name, True)
    rst = theme.colors['RST']
    
    print(f"  {color}{icon} {message}{rst}")


def display_progress(current: int, total: int, message: str = "", theme: Optional[NeonTheme] = None) -> None:
    """
    Display a progress indicator.
    
    Args:
        current: Current progress value
        total: Total progress value
        message: Optional message to display
        theme: Theme to use
    """
    theme = theme or default_theme
    
    percentage = (current / total) * 100 if total > 0 else 0
    bar_width = 30
    filled = int(bar_width * percentage / 100)
    empty = bar_width - filled
    
    bar = f"{'█' * filled}{'░' * empty}"
    
    color = theme.get('GREEN', True)
    rst = theme.colors['RST']
    
    if message:
        print(f"\r  {color}{bar} {percentage:.0f}% - {message}{rst}", end="", flush=True)
    else:
        print(f"\r  {color}{bar} {percentage:.0f}%{rst}", end="", flush=True)
    
    if current >= total:
        print()  # New line when complete
