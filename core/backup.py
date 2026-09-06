# -*- coding: utf-8 -*-
"""
Backup and restore system for HACKER_ENV V2
Handles backing up and restoring shell configurations.
"""

import os
import shutil
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from core.detector import get_platform_info
from core.config import get_config_manager


class BackupManager:
    """Manages backups of shell configurations."""
    
    MARKER = "# <HACKER_ENV_V2>"
    
    def __init__(self):
        self.platform_info = get_platform_info()
        self.config = get_config_manager()
        self.backup_dir = self.config.get_backup_dir()
        
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def backup_shell_configs(self, reason: str = 'manual') -> Dict[str, str]:
        """
        Backup all shell configuration files.
        
        Args:
            reason: Reason for backup
            
        Returns:
            Dict mapping original paths to backup paths
        """
        backups = {}
        
        config_files = [
            os.path.expanduser('~/.zshrc'),
            os.path.expanduser('~/.bashrc'),
            os.path.expanduser('~/.profile'),
            os.path.expanduser('~/.bash_profile'),
        ]
        
        # Add Termux-specific files if on Termux
        if self.platform_info.is_termux:
            config_files.append(os.path.expanduser('~/.termux/termux.properties'))
            config_files.append(os.path.expanduser('~/.tmux.conf'))
        
        for config_file in config_files:
            if os.path.exists(config_file):
                backup_path = self._backup_file(config_file, reason)
                if backup_path:
                    backups[config_file] = backup_path
        
        return backups
    
    def _backup_file(self, filepath: str, reason: str) -> Optional[str]:
        """
        Backup a single file.
        
        Args:
            filepath: Path to file to backup
            reason: Reason for backup
            
        Returns:
            Path to backup file or None
        """
        if not os.path.exists(filepath):
            return None
        
        filename = os.path.basename(filepath)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'{filename}.{reason}.{timestamp}.bak'
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            shutil.copy2(filepath, backup_path)
            self.config.log(f"Backed up {filepath} to {backup_path}")
            return backup_path
        except (IOError, OSError) as e:
            self.config.log(f"Failed to backup {filepath}: {e}", 'ERROR')
            return None
    
    def restore_shell_configs(self, backup_mapping: Dict[str, str]) -> Tuple[int, int]:
        """
        Restore shell configurations from backups.
        
        Args:
            backup_mapping: Dict mapping backup paths to original paths
            
        Returns:
            Tuple of (success_count, failure_count)
        """
        success = 0
        failure = 0
        
        for backup_path, original_path in backup_mapping.items():
            if os.path.exists(backup_path):
                try:
                    shutil.copy2(backup_path, original_path)
                    self.config.log(f"Restored {backup_path} to {original_path}")
                    success += 1
                except (IOError, OSError) as e:
                    self.config.log(f"Failed to restore {backup_path}: {e}", 'ERROR')
                    failure += 1
            else:
                self.config.log(f"Backup not found: {backup_path}", 'WARNING')
                failure += 1
        
        return success, failure
    
    def list_backups(self) -> List[Dict]:
        """List all available backups."""
        backups = []
        
        if os.path.exists(self.backup_dir):
            for filename in sorted(os.listdir(self.backup_dir)):
                if filename.endswith('.bak'):
                    filepath = os.path.join(self.backup_dir, filename)
                    stat = os.stat(filepath)
                    backups.append({
                        'filename': filename,
                        'path': filepath,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    })
        
        return backups
    
    def clean_old_backups(self, keep_last: int = 10) -> int:
        """
        Clean old backups, keeping only the most recent ones.
        
        Args:
            keep_last: Number of backups to keep
            
        Returns:
            Number of backups removed
        """
        backups = self.list_backups()
        removed = 0
        
        if len(backups) > keep_last:
            # Sort by creation time (oldest first)
            backups.sort(key=lambda x: x['created'])
            
            # Remove oldest backups
            for backup in backups[:-keep_last]:
                try:
                    os.remove(backup['path'])
                    self.config.log(f"Removed old backup: {backup['filename']}")
                    removed += 1
                except (IOError, OSError) as e:
                    self.config.log(f"Failed to remove backup: {e}", 'ERROR')
        
        return removed
    
    def has_marker(self, filepath: str) -> bool:
        """Check if a file contains the HACKER_ENV marker."""
        if not os.path.exists(filepath):
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                return self.MARKER in content
        except (IOError, OSError):
            return False
    
    def clean_hacker_env_from_file(self, filepath: str) -> bool:
        """
        Remove HACKER_ENV configuration from a file.
        
        Args:
            filepath: Path to file to clean
            
        Returns:
            True if file was modified, False otherwise
        """
        if not os.path.exists(filepath):
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            new_lines = []
            skip_next = False
            
            for line in lines:
                if skip_next:
                    if 'exec zsh' in line or 'HACKER_ENV' in line:
                        skip_next = False
                        continue
                
                if self.MARKER in line:
                    skip_next = True
                    continue
                
                if 'exec zsh' not in line and 'HACKER_ENV' not in line:
                    new_lines.append(line)
            
            # Only write if content changed
            if len(new_lines) != len(lines):
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                self.config.log(f"Cleaned HACKER_ENV from {filepath}")
                return True
            
            return False
        except (IOError, OSError) as e:
            self.config.log(f"Failed to clean {filepath}: {e}", 'ERROR')
            return False
    
    def full_uninstall(self) -> Dict[str, bool]:
        """
        Perform complete uninstallation.
        
        Returns:
            Dict with operation results
        """
        results = {}
        
        # Clean shell config files
        for config_file in ['~/.zshrc', '~/.bashrc', '~/.profile']:
            filepath = os.path.expanduser(config_file)
            if os.path.exists(filepath):
                if self.has_marker(filepath):
                    results[filepath] = self.clean_hacker_env_from_file(filepath)
                else:
                    results[filepath] = False  # Not modified by us
        
        # Remove config directory
        config_dir = self.config.get_config_dir()
        if os.path.exists(config_dir):
            try:
                shutil.rmtree(config_dir)
                results[config_dir] = True
                self.config.log(f"Removed config directory: {config_dir}")
            except (IOError, OSError) as e:
                self.config.log(f"Failed to remove config directory: {e}", 'ERROR')
                results[config_dir] = False
        
        return results


# Singleton instance
_backup_manager: Optional[BackupManager] = None


def get_backup_manager() -> BackupManager:
    """Get backup manager instance."""
    global _backup_manager
    if _backup_manager is None:
        _backup_manager = BackupManager()
    return _backup_manager
