"""
TaskShot Settings - Configuration management
"""

import json
from pathlib import Path


class Settings:
    """Manages application settings with persistence"""

    def __init__(self):
        self.config_path = Path.home() / ".taskshot_config.json"
        self.defaults = {
            # Capture settings
            'sound_feedback': True,
            'visual_flash': True,
            'circle_color': '#FF0000',
            'circle_size': 40,

            # Document settings
            'header_color': '#a23b84',
            'border_color': '#6f2fa6',
            'include_footer': True,
            'margin_size': '0.5"',

            # AI settings
            'ai_provider': 'ollama',  # 'ollama', 'openai', 'anthropic', 'custom'
            'ollama_url': 'http://localhost:11434',
            'ollama_model': 'llava:7b',
            'openai_api_key': '',
            'openai_model': 'gpt-4o',
            'anthropic_api_key': '',
            'anthropic_model': 'claude-sonnet-4-20250514',
            'custom_api_url': '',
            'custom_api_key': '',
            'custom_model': '',
            'ai_enabled': True
        }
        self._settings = {}
        self.load()

    def load(self):
        """Load settings from file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    self._settings = json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
            self._settings = {}

    def save(self):
        """Save settings to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self._settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get(self, key, default=None):
        """
        Get a setting value.

        Args:
            key: Setting key
            default: Default value if not found

        Returns:
            Setting value or default
        """
        if default is None:
            default = self.defaults.get(key)
        return self._settings.get(key, default)

    def set(self, key, value):
        """
        Set a setting value.

        Args:
            key: Setting key
            value: Setting value
        """
        self._settings[key] = value

    def reset(self):
        """Reset all settings to defaults"""
        self._settings = dict(self.defaults)
        self.save()

    def to_dict(self):
        """Get all settings as a dictionary"""
        result = dict(self.defaults)
        result.update(self._settings)
        return result
