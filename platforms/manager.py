# -*- coding: utf-8 -*-
"""
Platform manager for HACKER_ENV V2
Provides unified interface to platform-specific operations.
"""

from typing import List, Tuple, Optional
from core.detector import get_platform_info, SystemInfo
from platforms.termux import TermuxPlatform
from platforms.wsl import WSLPlatform
from platforms.linux import LinuxPlatform


class PlatformManager:
    """Unified interface for platform-specific operations."""
    
    def __init__(self):
        self.info = get_platform_info()
        self._platform = self._get_platform_handler()
    
    def _get_platform_handler(self):
        """Get the appropriate platform handler."""
        if self.info.is_termux:
            return TermuxPlatform
        elif self.info.is_wsl:
            return WSLPlatform
        else:
            return LinuxPlatform
    
    def get_package_manager(self) -> str:
        """Get package manager command."""
        return self._platform.get_package_manager()
    
    def update_packages(self) -> Tuple[bool, str, int]:
        """Update package lists."""
        return self._platform.update_packages()
    
    def upgrade_packages(self) -> Tuple[bool, str, int]:
        """Upgrade all packages."""
        return self._platform.upgrade_packages()
    
    def install_package(self, package: str) -> Tuple[bool, str, int]:
        """Install a single package."""
        return self._platform.install_package(package)
    
    def install_packages(self, packages: List[str]) -> Tuple[bool, str, int]:
        """Install multiple packages."""
        return self._platform.install_packages(packages)
    
    def is_package_installed(self, package: str) -> bool:
        """Check if a package is installed."""
        return self._platform.is_package_installed(package)
    
    def get_essential_packages(self) -> List[str]:
        """Get list of essential packages."""
        return self._platform.get_essential_packages()
    
    def get_shell_config_files(self) -> List[str]:
        """Get shell config files."""
        return self._platform.get_shell_config_files()
    
    def get_display_info(self) -> str:
        """Get formatted display information."""
        return self.info.get_display_info()


# Singleton instance
_platform_manager: Optional[PlatformManager] = None


def get_platform_manager() -> PlatformManager:
    """Get platform manager instance."""
    global _platform_manager
    if _platform_manager is None:
        _platform_manager = PlatformManager()
    return _platform_manager
