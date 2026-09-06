# -*- coding: utf-8 -*-
"""
Configuration management for HACKER_ENV V2
Handles loading, saving, and managing configuration files.
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, Any, Optional
from core.detector import get_platform_info


class ConfigManager:
    """Manages HACKER_ENV configuration."""
    
    # Default configuration
    DEFAULT_CONFIG = {
        'version': '2.0',
        'user_name': 'Hacker',
        'theme': 'cyber',
        'prompt_style': '1',
        'banner_model': '1',
        'modules': ['tmux', 'backup', 'weather', 'genpass', 'python'],
        'custom_rgb': {},
        'use_custom_name_in_prompt': True,
        'use_name_as_big_art': False,
        'created_at': None,
        'updated_at': None,
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Custom config directory. If None, uses ~/.hacker_env/
        """
        self.platform_info = get_platform_info()
        
        if config_dir:
            self.config_dir = config_dir
        else:
            self.config_dir = os.path.expanduser('~/.hacker_env')
        
        self.config_file = os.path.join(self.config_dir, 'config.json')
        self.backup_dir = os.path.join(self.config_dir, 'backups')
        self.log_dir = os.path.join(self.config_dir, 'logs')
        
        # Create directories
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Load configuration
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Merge with defaults to handle missing keys
                merged = self.DEFAULT_CONFIG.copy()
                merged.update(config)
                return merged
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config: {e}")
        
        return self.DEFAULT_CONFIG.copy()
    
    def save(self) -> bool:
        """Save configuration to file."""
        try:
            self.config['updated_at'] = datetime.now().isoformat()
            if not self.config.get('created_at'):
                self.config['created_at'] = self.config['updated_at']
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            # Set restrictive permissions on Unix-like systems
            if os.name == 'posix':
                try:
                    os.chmod(self.config_file, 0o600)
                except OSError:
                    pass
            
            return True
        except (IOError, OSError) as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple configuration values."""
        self.config.update(updates)
    
    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()
    
    def backup(self, reason: str = 'manual') -> Optional[str]:
        """
        Create a backup of current configuration.
        
        Args:
            reason: Reason for backup (e.g., 'before_update', 'manual')
            
        Returns:
            Path to backup file or None on failure
        """
        if not os.path.exists(self.config_file):
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'config_{reason}_{timestamp}.json'
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            shutil.copy2(self.config_file, backup_path)
            return backup_path
        except (IOError, OSError) as e:
            print(f"Error creating backup: {e}")
            return None
    
    def restore(self, backup_path: str) -> bool:
        """
        Restore configuration from backup.
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(backup_path):
            print(f"Backup not found: {backup_path}")
            return False
        
        try:
            # Validate backup is valid JSON
            with open(backup_path, 'r', encoding='utf-8') as f:
                json.load(f)
            
            # Create backup of current config before restore
            self.backup('before_restore')
            
            # Restore
            shutil.copy2(backup_path, self.config_file)
            self.config = self._load_config()
            return True
        except (json.JSONDecodeError, IOError, OSError) as e:
            print(f"Error restoring backup: {e}")
            return False
    
    def list_backups(self) -> list:
        """List available backups."""
        backups = []
        if os.path.exists(self.backup_dir):
            for filename in sorted(os.listdir(self.backup_dir)):
                if filename.startswith('config_') and filename.endswith('.json'):
                    filepath = os.path.join(self.backup_dir, filename)
                    stat = os.stat(filepath)
                    backups.append({
                        'filename': filename,
                        'path': filepath,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    })
        return backups
    
    def log(self, message: str, level: str = 'INFO') -> None:
        """Write to log file."""
        log_file = os.path.join(
            self.log_dir,
            f'hacker_env_{datetime.now():%Y%m%d}.log'
        )
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except (IOError, OSError):
            pass
    
    def get_config_dir(self) -> str:
        """Get configuration directory path."""
        return self.config_dir
    
    def get_backup_dir(self) -> str:
        """Get backup directory path."""
        return self.backup_dir
    
    def get_log_dir(self) -> str:
        """Get log directory path."""
        return self.log_dir


# Singleton instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """Get configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
