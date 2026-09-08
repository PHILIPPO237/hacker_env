# -*- coding: utf-8 -*-
"""
Termux-specific operations for HACKER_ENV V2
Handles all Termux-specific functionality.
"""

import os
import subprocess
from typing import List, Tuple, Optional


class TermuxPlatform:
    """Termux-specific platform operations."""
    
    TERMUX_PATH = '/data/data/com.termux'
    TERMUX_HOME = '/data/data/com.termux/files/home'
    TERMUX_PREFIX = '/data/data/com.termux/files/usr'
    
    @staticmethod
    def is_available() -> bool:
        """Check if running on Termux."""
        return os.path.exists('/data/data/com.termux')
    
    @staticmethod
    def get_package_manager() -> str:
        """Get package manager command."""
        return 'pkg'
    
    @staticmethod
    def update_packages() -> Tuple[bool, str, int]:
        """Update package lists."""
        try:
            result = subprocess.run(
                ['pkg', 'update', '-y'],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0, result.stdout, result.returncode
        except subprocess.TimeoutExpired:
            return False, "Timeout", -1
        except Exception as e:
            return False, str(e), -2
    
    @staticmethod
    def upgrade_packages() -> Tuple[bool, str, int]:
        """Upgrade all packages."""
        try:
            result = subprocess.run(
                ['pkg', 'upgrade', '-y'],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0, result.stdout, result.returncode
        except subprocess.TimeoutExpired:
            return False, "Timeout", -1
        except Exception as e:
            return False, str(e), -2
    
    @staticmethod
    def install_package(package: str) -> Tuple[bool, str, int]:
        """Install a single package."""
        try:
            result = subprocess.run(
                ['pkg', 'install', '-y', package],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0, result.stdout, result.returncode
        except subprocess.TimeoutExpired:
            return False, "Timeout", -1
        except Exception as e:
            return False, str(e), -2
    
    @staticmethod
    def install_packages(packages: List[str]) -> Tuple[bool, str, int]:
        """Install multiple packages."""
        try:
            result = subprocess.run(
                ['pkg', 'install', '-y'] + packages,
                capture_output=True,
                text=True,
                timeout=600
            )
            return result.returncode == 0, result.stdout, result.returncode
        except subprocess.TimeoutExpired:
            return False, "Timeout", -1
        except Exception as e:
            return False, str(e), -2
    
    @staticmethod
    def is_package_installed(package: str) -> bool:
        """Check if a package is installed."""
        try:
            result = subprocess.run(
                ['dpkg', '-l', package],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0 and 'ii' in result.stdout
        except Exception:
            return False
    
    @staticmethod
    def setup_storage() -> Tuple[bool, str, int]:
        """Setup Termux storage access."""
        try:
            result = subprocess.run(
                ['termux-setup-storage'],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0, result.stdout, result.returncode
        except subprocess.TimeoutExpired:
            return False, "Timeout", -1
        except Exception as e:
            return False, str(e), -2
    
    @staticmethod
    def get_android_version() -> str:
        """Get Android version."""
        try:
            result = subprocess.run(
                ['getprop', 'ro.build.version.release'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return 'unknown'
    
    @staticmethod
    def get_essential_packages() -> List[str]:
        """Get list of essential packages for Termux."""
        return [
            "python", "git", "curl", "wget", "zsh", "nano", "vim",
            "zip", "unzip", "tar", "tree", "jq", "openssh",
            "clang", "make", "cmake", "rust", "nodejs",
            "proot", "proot-distro", "htop", "neofetch", "openssl-tool"
        ]
    
    @staticmethod
    def get_shell_config_files() -> List[str]:
        """Get shell config files for Termux."""
        return [
            os.path.expanduser('~/.zshrc'),
            os.path.expanduser('~/.bashrc'),
            os.path.expanduser('~/.termux/termux.properties'),
        ]
