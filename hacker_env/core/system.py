# -*- coding: utf-8 -*-
"""
System utilities for HACKER_ENV V2
Platform-agnostic system operations.
"""

import subprocess
import os
import shutil
from typing import Tuple, Optional, List
from core.detector import get_platform_info


def run_cmd(cmd, capture_output=False, timeout=30, silent=True):
    """
    Execute a system command with error handling.
    
    Args:
        cmd: Command as list (shell=False) or string (shell=True, NOT recommended).
        capture_output: If True, return stdout.
        timeout: Timeout in seconds.
        silent: If True, suppress output (ignored if capture_output=True).
        
    Returns:
        tuple (success: bool, output: str, return_code: int)
    """
    try:
        kwargs = {
            'timeout': timeout,
            'text': True
        }
        
        if isinstance(cmd, list):
            kwargs['shell'] = False
        else:
            # Secure fallback: only use shell=True for internal commands
            kwargs['shell'] = True
        
        if capture_output:
            kwargs['capture_output'] = True
        elif silent:
            kwargs['stdout'] = subprocess.DEVNULL
            kwargs['stderr'] = subprocess.DEVNULL
        
        result = subprocess.run(cmd, **kwargs)
        
        if capture_output:
            return result.returncode == 0, result.stdout, result.returncode
        return result.returncode == 0, "", result.returncode
    
    except subprocess.TimeoutExpired:
        return False, "", -1
    except KeyboardInterrupt:
        raise
    except Exception as e:
        return False, str(e), -2


def install_package(package: str, auto_yes: bool = True) -> bool:
    """
    Install a package using the appropriate package manager.
    
    Args:
        package: Package name.
        auto_yes: Add -y flag automatically.
        
    Returns:
        bool: True if installed or already present.
    """
    from platforms.manager import get_platform_manager
    
    manager = get_platform_manager()
    
    # Check if already installed
    if manager.is_package_installed(package):
        return True
    
    success, _, _ = manager.install_package(package)
    return success


def install_packages(packages: List[str], auto_yes: bool = True) -> bool:
    """
    Install multiple packages using the appropriate package manager.
    
    Args:
        packages: List of package names.
        auto_yes: Add -y flag automatically.
        
    Returns:
        bool: True if all installed successfully.
    """
    from platforms.manager import get_platform_manager
    
    manager = get_platform_manager()
    
    # Filter out already installed packages
    missing = [p for p in packages if not manager.is_package_installed(p)]
    
    if not missing:
        return True
    
    success, _, _ = manager.install_packages(missing)
    return success


def check_and_install_deps(deps: Optional[List[str]] = None) -> List[str]:
    """
    Check and install missing dependencies.
    
    Args:
        deps: List of required packages. If None, uses essential packages.
        
    Returns:
        list: Packages that failed to install.
    """
    from platforms.manager import get_platform_manager
    
    manager = get_platform_manager()
    
    if deps is None:
        deps = manager.get_essential_packages()
    
    failed = []
    for dep in deps:
        if not manager.is_package_installed(dep):
            if not install_package(dep):
                failed.append(dep)
    
    return failed


def check_space(required_mb: int = 500) -> Tuple[bool, int]:
    """
    Check available disk space.
    
    Args:
        required_mb: Minimum required space in MB.
        
    Returns:
        tuple (ok: bool, available_mb: int)
    """
    try:
        stat = shutil.disk_usage(os.path.expanduser('~'))
        available_mb = stat.free // (1024 * 1024)
        return available_mb >= required_mb, available_mb
    except Exception:
        return False, 0


def check_internet(host: str = "1.1.1.1", timeout: int = 3) -> bool:
    """Check internet connection via ping."""
    info = get_platform_info()
    
    # Use different ping syntax based on platform
    if info.is_termux:
        cmd = ["ping", "-c", "1", "-W", str(timeout), host]
    else:
        cmd = ["ping", "-c", "1", "-W", str(timeout), host]
    
    return run_cmd(cmd, silent=True)[0]


def get_system_info() -> dict:
    """
    Get system information with fallbacks.
    
    Returns:
        dict with uptime, ip, cpu, ram, disk.
    """
    info = {}
    
    # Uptime
    success, output, _ = run_cmd(["uptime", "-p"], capture_output=True)
    info['uptime'] = output.replace('up ', '').strip() if success else "n/a"
    
    # IP
    success, output, _ = run_cmd(
        ["sh", "-c", "ip route get 1.1.1.1 | awk '{print $7; exit}'"],
        capture_output=True
    )
    if not success or not output.strip():
        success, output, _ = run_cmd(
            ["curl", "-s", "--max-time", "3", "ifconfig.me"],
            capture_output=True
        )
    info['ip'] = output.strip() if success and output.strip() else "offline"
    
    # CPU load
    success, output, _ = run_cmd(
        ["sh", "-c", "uptime | awk -F'load average:' '{print $2}' | cut -d',' -f1 | xargs"],
        capture_output=True
    )
    info['cpu'] = output.strip() if success else "n/a"
    
    # RAM
    success, output, _ = run_cmd(
        ["sh", "-c", "free -h | awk '/^Mem:/ {print $3\"/\"$2}'"],
        capture_output=True
    )
    if not success:
        success, memtotal, _ = run_cmd(
            ["sh", "-c", "awk '/MemTotal/ {print int($2/1024)\"M\"}' /proc/meminfo"],
            capture_output=True
        )
        success, memavail, _ = run_cmd(
            ["sh", "-c", "awk '/MemAvailable/ {print int($2/1024)\"M\"}' /proc/meminfo"],
            capture_output=True
        )
        if memtotal.strip() and memavail.strip():
            output = f"{memavail.strip()}/{memtotal.strip()}"
    info['ram'] = output.strip() if success else "n/a"
    
    # Disk
    success, output, _ = run_cmd(
        ["sh", "-c", f"df -h $HOME | awk 'NR==2 {{print $3\"/\"$2}}'"],
        capture_output=True
    )
    info['disk'] = output.strip() if success else "n/a"
    
    return info


def get_cpu_usage() -> float:
    """Get CPU usage percentage."""
    try:
        success, output, _ = run_cmd(
            ["sh", "-c", "top -bn1 | grep 'Cpu(s)' | awk '{print $2}'"],
            capture_output=True
        )
        if success and output.strip():
            return float(output.strip().replace('%', ''))
    except (ValueError, TypeError):
        pass
    return 0.0


def get_memory_usage() -> float:
    """Get memory usage percentage."""
    try:
        success, output, _ = run_cmd(
            ["sh", "-c", "free | awk '/^Mem:/ {printf \"%.1f\", $3/$2 * 100}'"],
            capture_output=True
        )
        if success and output.strip():
            return float(output.strip())
    except (ValueError, TypeError):
        pass
    return 0.0


def get_disk_usage(path: str = '/') -> float:
    """Get disk usage percentage for a path."""
    try:
        stat = shutil.disk_usage(path)
        return (stat.used / stat.total) * 100
    except Exception:
        return 0.0
