# -*- coding: utf-8 -*-
"""
Modern dashboard for HACKER_ENV V2
Displays system information in a beautiful, formatted way.
"""

import os
import sys
import shutil
import time
from datetime import datetime
from typing import Optional
from core.colors import NeonTheme, default_theme
from core.detector import get_platform_info, SystemInfo
from core.system import get_cpu_usage, get_memory_usage, get_disk_usage


def _get_progress_bar(value: float, width: int = 10, filled_char: str = '█', empty_char: str = '░') -> str:
    """
    Create a progress bar string.

    Args:
        value: Percentage value (0-100)
        width: Width of the bar
        filled_char: Character for filled portion
        empty_char: Character for empty portion

    Returns:
        Progress bar string
    """
    filled = int(width * min(max(value, 0), 100) / 100)
    empty = width - filled
    return f"{filled_char * filled}{empty_char * empty}"


def _format_size(size_bytes: int) -> str:
    """Format bytes to human readable size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


class Dashboard:
    """Modern dashboard displaying system information."""

    # Couleur "thème" attribuée à chaque ressource (identiques à l'ancienne
    # version : on ne bascule PAS sur un vert/jaune/rouge selon le seuil,
    # chaque ressource garde toujours la même couleur du thème actif).
    RESOURCE_COLOR = {
        'CPU': 'GREEN',
        'MEMORY': 'YELLOW',
        'DISK': 'CYAN',
    }

    MIN_WIDTH = 44
    MAX_WIDTH = 70

    def __init__(self, theme: Optional[NeonTheme] = None):
        """
        Initialize dashboard.

        Args:
            theme: Theme to use. If None, uses default theme.
        """
        self.theme = theme or default_theme
        self.platform_info = get_platform_info()

    def _get_box_chars(self) -> dict:
        """Get box drawing characters for the dashboard."""
        return {
            'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯',
            'h': '─', 'v': '│',
            'sep_left': '├', 'sep_right': '┤',
        }

    def _get_width(self) -> int:
        """Compute a box width adapted to the current terminal size."""
        columns = shutil.get_terminal_size(fallback=(80, 20)).columns
        # -6 pour la marge gauche ("  │  ") + la marge droite ("  │")
        width = columns - 6
        return max(self.MIN_WIDTH, min(width, self.MAX_WIDTH))

    def _format_line(self, label: str, value: str, width: int, chars: dict) -> str:
        """Format a single line with label and value."""
        label_color = self.theme.get('CYAN', True)
        value_color = self.theme.get('WHITE', True)
        dim_color = self.theme.colors['DIM']
        rst = self.theme.colors['RST']

        line = f"  {chars['v']}  {label_color}{label:<10}{rst} {dim_color}:{rst}  {value_color}{value}{rst}"
        return self._pad_line(line, label, value, width)

    def _format_resource_line(self, label: str, value: float, detail: str, width: int, chars: dict) -> str:
        """Format a single merged line: label + progress bar + percentage (+ detail)."""
        label_color = self.theme.get('CYAN', True)
        bar_color = self.theme.get(self.RESOURCE_COLOR.get(label, 'primary'), True)
        dim_color = self.theme.colors['DIM']
        rst = self.theme.colors['RST']

        bar = _get_progress_bar(value, 10)
        percentage = f"{value:5.1f}%"

        tail = f"{percentage}  {dim_color}{detail}{rst}" if detail else percentage
        visible = f"{label:<8}{bar}  {percentage}" + (f"  {detail}" if detail else "")
        line = f"  {chars['v']}  {label_color}{label:<8}{rst}{bar_color}{bar}{rst}  {tail}"
        return self._pad_line_raw(line, visible, width)

    def _pad_line(self, colored_line: str, label: str, value: str, width: int) -> str:
        visible_len = len(f"  {label:<10} :  {value}")
        return self._finish_pad(colored_line, visible_len, width)

    def _pad_line_raw(self, colored_line: str, visible_text: str, width: int) -> str:
        visible_len = len(f"  {visible_text}")
        return self._finish_pad(colored_line, visible_len, width)

    def _finish_pad(self, colored_line: str, visible_len: int, width: int) -> str:
        chars = self._get_box_chars()
        rst = self.theme.colors['RST']
        color = self.theme.get('primary', True)
        pad = max(0, width - visible_len)
        return f"{colored_line}{' ' * pad}  {color}{chars['v']}{rst}"

    def _get_top_border(self, width: int, chars: dict) -> str:
        """Get top border."""
        color = self.theme.get('primary', True)
        rst = self.theme.colors['RST']
        return f"  {color}{chars['tl']}{chars['h'] * (width + 4)}{chars['tr']}{rst}"

    def _get_title_line(self, title: str, width: int, chars: dict) -> str:
        """Get centered title line."""
        color = self.theme.get('primary', True)
        title_color = self.theme.get('primary', True)
        rst = self.theme.colors['RST']

        inner = width + 4
        padding = inner - len(title)
        left_pad = padding // 2
        right_pad = padding - left_pad

        return f"  {color}{chars['v']}{rst}{' ' * left_pad}{title_color}{title}{rst}{' ' * right_pad}{color}{chars['v']}{rst}"

    def _get_separator(self, width: int, chars: dict) -> str:
        """Get separator line."""
        color = self.theme.get('primary', True)
        rst = self.theme.colors['RST']
        return f"  {color}{chars['sep_left']}{chars['h'] * (width + 4)}{chars['sep_right']}{rst}"

    def _get_bottom_border(self, width: int, chars: dict) -> str:
        """Get bottom border."""
        color = self.theme.get('primary', True)
        rst = self.theme.colors['RST']
        return f"  {color}{chars['bl']}{chars['h'] * (width + 4)}{chars['br']}{rst}"

    def display(self) -> None:
        """Display the dashboard."""
        chars = self._get_box_chars()
        width = self._get_width()

        # Get system info
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        disk_usage = get_disk_usage()

        # Get memory details
        try:
            import psutil
            memory = psutil.virtual_memory()
            mem_info = f"{_format_size(memory.used)}/{_format_size(memory.total)}"
        except ImportError:
            mem_info = ""

        # Get disk details
        try:
            disk = shutil.disk_usage(os.path.expanduser('~'))
            disk_info = f"{_format_size(disk.used)}/{_format_size(disk.total)}"
        except Exception:
            disk_info = ""

        # Print dashboard
        print()
        print(self._get_top_border(width, chars))
        print(self._get_title_line("HACKER_ENV", width, chars))
        print(self._get_separator(width, chars))

        # System section
        print(self._format_line("OS", self.platform_info.os_name, width, chars))
        print(self._format_line("ENV", self.platform_info.environment.upper(), width, chars))
        print(self._format_line("SHELL", self.platform_info.shell, width, chars))
        print(self._format_line("ARCH", self.platform_info.architecture, width, chars))

        if self.platform_info.is_wsl:
            print(self._format_line("WSL", f"v{self.platform_info.wsl_version}", width, chars))
            print(self._format_line("DISTRO", self.platform_info.wsl_distribution, width, chars))

        print(self._get_separator(width, chars))

        # Resources section — une seule ligne fusionnée par ressource
        print(self._format_resource_line("CPU", cpu_usage, "", width, chars))
        print(self._format_resource_line("MEMORY", memory_usage, mem_info, width, chars))
        print(self._format_resource_line("DISK", disk_usage, disk_info, width, chars))

        print(self._get_separator(width, chars))

        # Info section
        now = datetime.now()
        print(self._format_line("DATE", now.strftime('%a %d %b %Y'), width, chars))
        print(self._format_line("TIME", now.strftime('%H:%M:%S'), width, chars))

        print(self._get_bottom_border(width, chars))
        print()


def display_dashboard(theme: Optional[NeonTheme] = None) -> None:
    """Display the dashboard (convenience function)."""
    dashboard = Dashboard(theme)
    dashboard.display()
