# -*- coding: utf-8 -*-
"""
WSL-specific operations for HACKER_ENV V2
Handles all Windows Subsystem for Linux functionality.
"""

import os
import subprocess
import re
from typing import List, Tuple, Optional


class WSLPlatform:
    """WSL-specific platform operations."""
    
    @staticmethod
    def is_available() -> bool:
        """Check if running on WSL."""
        # Check environment variable
        if os.environ.get('WSL_DISTRO_NAME'):
            return True
        
        # Check /proc/version for Microsoft
        try:
            with open('/proc/version', 'r') as f:
                content = f.read().lower()
                if 'microsoft' in content or 'wsl' in content:
                    return True
        except (IOError, PermissionError):
            pass
        
        # Check for WSLInterop
        if os.path.exists('/proc/sys/fs/binfmt_misc/WSLInterop'):
            return True
        
        return False
    
    @staticmethod
    def get_version() -> str:
        """Get WSL version (1 or 2)."""
        try:
            with open('/proc/version', 'r') as f:
                content = f.read().lower()
                if 'microsoft' in content and 'wsl' in content:
                    # WSL2 typically has a newer kernel version
                    if '5.' in content or '6.' in content:
                        return '2'
                    return '1'
        except (IOError, PermissionError):
            pass
        
        # Check uname -r for WSL2
        try:
            result = subprocess.run(
                ['uname', '-r'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.stdout.strip():
                version_match = re.search(r'(\d+)\.(\d+)', result.stdout)
                if version_match:
                    major = int(version_match.group(1))
                    if major >= 5:
                        return '2'
                    return '1'
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return 'unknown'
    
    @staticmethod
    def get_distribution() -> str:
        """Get WSL distribution name."""
        # Check WSL_DISTRO_NAME environment variable
        distro = os.environ.get('WSL_DISTRO_NAME')
        if distro:
            return distro
        
        # Try /etc/os-release
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('PRETTY_NAME='):
                        return line.split('=', 1)[1].strip().strip('"')
                    elif line.startswith('NAME='):
                        return line.split('=', 1)[1].strip().strip('"')
        except (IOError, PermissionError):
            pass
        
        return 'Unknown'
    
    @staticmethod
    def get_package_manager() -> str:
        """Get package manager command."""
        return 'apt'
    
    @staticmethod
    def update_packages() -> Tuple[bool, str, int]:
        """Update package lists."""
        try:
            result = subprocess.run(
                ['sudo', 'apt', 'update', '-y'],
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
                ['sudo', 'apt', 'upgrade', '-y'],
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
                ['sudo', 'apt', 'install', '-y', package],
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
                ['sudo', 'apt', 'install', '-y'] + packages,
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
    def get_essential_packages() -> List[str]:
        """Get list of essential packages for WSL."""
        return [
            "python3", "python3-pip", "git", "curl", "wget", "zsh", "nano", "vim",
            "zip", "unzip", "tar", "tree", "jq", "openssh-client",
            "build-essential", "cmake", "rustc", "nodejs",
            "htop", "neofetch", "openssl"
        ]
    
    @staticmethod
    def get_shell_config_files() -> List[str]:
        """Get shell config files for WSL."""
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
