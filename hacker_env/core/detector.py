# -*- coding: utf-8 -*-
"""
Platform detection module for HACKER_ENV V2
Reliably detects Termux, WSL, and native Linux environments.
Uses multiple methods for confirmation - never trusts a single source.
"""

import os
import sys
import platform
import subprocess
import re
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class SystemInfo:
    """Container for system information."""
    os_name: str
    os_version: str
    environment: str  # 'termux', 'wsl', 'linux'
    shell: str
    architecture: str
    kernel: str
    hostname: str
    username: str
    home_dir: str
    python_version: str
    wsl_version: Optional[str] = None
    wsl_distribution: Optional[str] = None
    is_termux: bool = False
    is_wsl: bool = False
    is_linux: bool = False
    package_manager: str = ''
    terminal_width: int = 80
    terminal_height: int = 24


class PlatformDetector:
    """Detects the current platform and system information."""
    
    def __init__(self):
        self._cache: Optional[SystemInfo] = None
    
    def detect(self) -> SystemInfo:
        """Main detection method - returns SystemInfo with all details."""
        if self._cache:
            return self._cache
        
        info = SystemInfo(
            os_name=self._detect_os_name(),
            os_version=self._detect_os_version(),
            environment=self._detect_environment(),
            shell=self._detect_shell(),
            architecture=self._detect_architecture(),
            kernel=self._detect_kernel(),
            hostname=self._detect_hostname(),
            username=self._detect_username(),
            home_dir=os.path.expanduser('~'),
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        )
        
        # Set boolean flags
        info.is_termux = info.environment == 'termux'
        info.is_wsl = info.environment == 'wsl'
        info.is_linux = info.environment == 'linux'
        
        # Detect package manager
        info.package_manager = self._detect_package_manager()
        
        # Detect terminal size
        try:
            cols, rows = os.get_terminal_size()
            info.terminal_width = cols
            info.terminal_height = rows
        except (ValueError, OSError):
            pass
        
        # WSL-specific info
        if info.is_wsl:
            info.wsl_version = self._detect_wsl_version()
            info.wsl_distribution = self._detect_wsl_distribution()
        
        self._cache = info
        return info
    
    def _detect_environment(self) -> str:
        """
        Detect environment using multiple methods for reliability.
        Priority: Termux > WSL > Linux
        """
        # Method 1: Check for Termux (multiple indicators)
        if self._is_termux():
            return 'termux'
        
        # Method 2: Check for WSL (multiple indicators)
        if self._is_wsl():
            return 'wsl'
        
        # Method 3: Default to Linux
        return 'linux'
    
    def _is_termux(self) -> bool:
        """Check if running in Termux using multiple methods."""
        # Method 1: Check environment variable
        if os.environ.get('TERMUX_VERSION'):
            return True
        
        # Method 2: Check for Termux-specific path
        if os.path.exists('/data/data/com.termux'):
            return True
        
        # Method 3: Check for Termux-specific files
        if os.path.exists('/data/data/com.termux/files'):
            return True
        
        # Method 4: Check for pkg command (Termux package manager)
        try:
            result = subprocess.run(
                ['which', 'pkg'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and '/com.termux/' in result.stdout:
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Method 5: Check for Termux in process info
        try:
            result = subprocess.run(
                ['ps', '-o', 'comm=', '-p', str(os.getppid())],
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'termux' in result.stdout.lower():
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return False
    
    def _is_wsl(self) -> bool:
        """Check if running in WSL using multiple methods."""
        # Method 1: Check for WSL environment variable
        if os.environ.get('WSL_DISTRO_NAME'):
            return True
        
        # Method 2: Check /proc/version for Microsoft
        try:
            with open('/proc/version', 'r') as f:
                content = f.read().lower()
                if 'microsoft' in content or 'wsl' in content:
                    return True
        except (IOError, PermissionError):
            pass
        
        # Method 3: Check /proc/sys/fs/binfmt_misc/WSLInterop
        if os.path.exists('/proc/sys/fs/binfmt_misc/WSLInterop'):
            return True
        
        # Method 4: Check for WSL in uname
        try:
            result = subprocess.run(
                ['uname', '-r'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'microsoft' in result.stdout.lower() or 'wsl' in result.stdout.lower():
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Method 5: Check /etc/os-release for WSL
        try:
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'wsl' in content:
                    return True
        except (IOError, PermissionError):
            pass
        
        return False
    
    def _detect_os_name(self) -> str:
        """Detect OS name."""
        # Check for Termux first
        if self._is_termux():
            return 'Android (Termux)'
        
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
        
        # Fallback to platform module
        return platform.system()
    
    def _detect_os_version(self) -> str:
        """Detect OS version."""
        # Check for Termux version
        termux_version = os.environ.get('TERMUX_VERSION')
        if termux_version:
            return f"Termux {termux_version}"
        
        # Try /etc/os-release for version
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('VERSION_ID='):
                        return line.split('=', 1)[1].strip().strip('"')
                    elif line.startswith('VERSION='):
                        version = line.split('=', 1)[1].strip().strip('"')
                        if version:
                            return version
        except (IOError, PermissionError):
            pass
        
        # Fallback to platform
        return platform.release()
    
    def _detect_shell(self) -> str:
        """Detect current shell."""
        # Check SHELL environment variable
        shell = os.environ.get('SHELL', '')
        if shell:
            return os.path.basename(shell)
        
        # Check parent process
        try:
            ppid = os.getppid()
            result = subprocess.run(
                ['ps', '-o', 'comm=', '-p', str(ppid)],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.stdout.strip():
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Default based on platform
        if self._is_termux():
            return 'zsh'  # Termux typically uses zsh
        
        return 'bash'
    
    def _detect_architecture(self) -> str:
        """Detect system architecture."""
        return platform.machine()
    
    def _detect_kernel(self) -> str:
        """Detect kernel version."""
        return platform.release()
    
    def _detect_hostname(self) -> str:
        """Detect hostname."""
        return platform.node()
    
    def _detect_username(self) -> str:
        """Detect username."""
        # Try multiple methods
        username = os.environ.get('USER') or os.environ.get('LOGNAME')
        if username:
            return username
        
        try:
            import getpass
            return getpass.getuser()
        except ImportError:
            pass
        
        return 'user'
    
    def _detect_package_manager(self) -> str:
        """Detect available package manager."""
        # Check for Termux pkg
        if self._is_termux():
            return 'pkg'
        
        # Check for apt (Debian/Ubuntu)
        try:
            result = subprocess.run(
                ['which', 'apt'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return 'apt'
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Check for yum (RHEL/CentOS)
        try:
            result = subprocess.run(
                ['which', 'yum'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return 'yum'
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Check for pacman (Arch)
        try:
            result = subprocess.run(
                ['which', 'pacman'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return 'pacman'
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return 'unknown'
    
    def _detect_wsl_version(self) -> str:
        """Detect WSL version (1 or 2)."""
        # Check /proc/version for WSL2
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
                # WSL2 kernel version is typically 5.x or 6.x
                version_match = re.search(r'(\d+)\.(\d+)', result.stdout)
                if version_match:
                    major = int(version_match.group(1))
                    if major >= 5:
                        return '2'
                    return '1'
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return 'unknown'
    
    def _detect_wsl_distribution(self) -> str:
        """Detect WSL distribution name."""
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
    
    def get_display_info(self) -> str:
        """Get formatted display information."""
        info = self.detect()
        
        lines = []
        lines.append(f"OS       : {info.os_name} {info.os_version}")
        lines.append(f"ENV      : {info.environment.upper()}")
        lines.append(f"SHELL    : {info.shell}")
        lines.append(f"ARCH     : {info.architecture}")
        lines.append(f"KERNEL   : {info.kernel}")
        lines.append(f"HOSTNAME : {info.hostname}")
        lines.append(f"USER     : {info.username}")
        lines.append(f"PYTHON   : {info.python_version}")
        lines.append(f"PKGMGR   : {info.package_manager}")
        
        if info.is_wsl:
            lines.append(f"WSL_VER  : {info.wsl_version}")
            lines.append(f"WSL_DIST : {info.wsl_distribution}")
        
        return '\n'.join(lines)


# Singleton instance
detector = PlatformDetector()


def get_platform_info() -> SystemInfo:
    """Get platform information (convenience function)."""
    return detector.detect()


def is_termux() -> bool:
    """Check if running on Termux."""
    return detector.detect().is_termux


def is_wsl() -> bool:
    """Check if running on WSL."""
    return detector.detect().is_wsl


def is_linux() -> bool:
    """Check if running on native Linux."""
    return detector.detect().is_linux
