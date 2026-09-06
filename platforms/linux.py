# -*- coding: utf-8 -*-
"""
Native Linux operations for HACKER_ENV V2
Handles all native Linux (non-WSL, non-Termux) functionality.
"""

import os
import subprocess
from typing import List, Tuple, Optional


class LinuxPlatform:
    """Native Linux platform operations."""
    
    @staticmethod
    def is_available() -> bool:
        """Check if running on native Linux."""
        # This is a fallback - should only be called if not Termux and not WSL
        return os.name == 'posix' and not os.path.exists('/data/data/com.termux')
    
    @staticmethod
    def detect_distro() -> str:
        """Detect Linux distribution."""
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('PRETTY_NAME='):
                        return line.split('=', 1)[1].strip().strip('"')
                    elif line.startswith('NAME='):
                        return line.split('=', 1)[1].strip().strip('"')
        except (IOError, PermissionError):
            pass
        
        # Fallback to lsb_release
        try:
            result = subprocess.run(
                ['lsb_release', '-d'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.split(':', 1)[1].strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return 'Linux'
    
    @staticmethod
    def detect_distro_id() -> str:
        """Detect distribution ID (e.g., ubuntu, debian, fedora)."""
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('ID='):
                        return line.split('=', 1)[1].strip().strip('"')
        except (IOError, PermissionError):
            pass
        
        return 'unknown'
    
    @staticmethod
    def get_package_manager() -> str:
        """Get package manager based on distribution."""
        distro_id = LinuxPlatform.detect_distro_id().lower()
        
        if distro_id in ('ubuntu', 'debian', 'linuxmint', 'pop'):
            return 'apt'
        elif distro_id in ('fedora', 'rhel', 'centos', 'rocky', 'alma'):
            return 'dnf'
        elif distro_id == 'arch' or distro_id == 'manjaro':
            return 'pacman'
        elif distro_id == 'opensuse-leap' or distro_id == 'opensuse-tumbleweed':
            return 'zypper'
        elif distro_id == 'alpine':
            return 'apk'
        
        # Fallback: try to detect available package managers
        for pm in ['apt', 'dnf', 'pacman', 'zypper', 'apk']:
            try:
                result = subprocess.run(
                    ['which', pm],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return pm
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        return 'unknown'
    
    @staticmethod
    def update_packages() -> Tuple[bool, str, int]:
        """Update package lists."""
        pm = LinuxPlatform.get_package_manager()
        
        commands = {
            'apt': ['sudo', 'apt', 'update'],
            'dnf': ['sudo', 'dnf', 'check-update'],
            'pacman': ['sudo', 'pacman', '-Sy'],
            'zypper': ['sudo', 'zypper', 'refresh'],
            'apk': ['sudo', 'apk', 'update'],
        }
        
        cmd = commands.get(pm)
        if not cmd:
            return False, f"Unknown package manager: {pm}", -1
        
        try:
            result = subprocess.run(
                cmd,
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
        pm = LinuxPlatform.get_package_manager()
        
        commands = {
            'apt': ['sudo', 'apt', 'upgrade', '-y'],
            'dnf': ['sudo', 'dnf', 'upgrade', '-y'],
            'pacman': ['sudo', 'pacman', '-Syu', '--noconfirm'],
            'zypper': ['sudo', 'zypper', 'update', '-y'],
            'apk': ['sudo', 'apk', 'upgrade'],
        }
        
        cmd = commands.get(pm)
        if not cmd:
            return False, f"Unknown package manager: {pm}", -1
        
        try:
            result = subprocess.run(
                cmd,
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
    def install_package(package: str) -> Tuple[bool, str, int]:
        """Install a single package."""
        pm = LinuxPlatform.get_package_manager()
        
        commands = {
            'apt': ['sudo', 'apt', 'install', '-y', package],
            'dnf': ['sudo', 'dnf', 'install', '-y', package],
            'pacman': ['sudo', 'pacman', '-S', '--noconfirm', package],
            'zypper': ['sudo', 'zypper', 'install', '-y', package],
            'apk': ['sudo', 'apk', 'add', package],
        }
        
        cmd = commands.get(pm)
        if not cmd:
            return False, f"Unknown package manager: {pm}", -1
        
        try:
            result = subprocess.run(
                cmd,
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
        pm = LinuxPlatform.get_package_manager()
        
        commands = {
            'apt': ['sudo', 'apt', 'install', '-y'] + packages,
            'dnf': ['sudo', 'dnf', 'install', '-y'] + packages,
            'pacman': ['sudo', 'pacman', '-S', '--noconfirm'] + packages,
            'zypper': ['sudo', 'zypper', 'install', '-y'] + packages,
            'apk': ['sudo', 'apk', 'add'] + packages,
        }
        
        cmd = commands.get(pm)
        if not cmd:
            return False, f"Unknown package manager: {pm}", -1
        
        try:
            result = subprocess.run(
                cmd,
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
            pass
        
        # Try rpm
        try:
            result = subprocess.run(
                ['rpm', '-q', package],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0 and 'is not installed' not in result.stdout
        except Exception:
            pass
        
        # Try pacman
        try:
            result = subprocess.run(
                ['pacman', '-Qi', package],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            pass
        
        return False
    
    @staticmethod
    def get_essential_packages() -> List[str]:
        """Get list of essential packages for native Linux."""
        return [
            "python3", "python3-pip", "git", "curl", "wget", "zsh", "nano", "vim",
            "zip", "unzip", "tar", "tree", "jq", "openssh-client",
            "build-essential", "cmake", "rustc", "nodejs",
            "htop", "neofetch", "openssl"
        ]
    
    @staticmethod
    def get_shell_config_files() -> List[str]:
        """Get shell config files for native Linux."""
        return [
            os.path.expanduser('~/.zshrc'),
            os.path.expanduser('~/.bashrc'),
            os.path.expanduser('~/.profile'),
        ]
    
    @staticmethod
    def is_sudo_available() -> bool:
        """Check if sudo is available."""
        try:
            result = subprocess.run(
                ['sudo', '-n', 'true'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
