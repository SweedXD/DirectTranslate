# -*- coding: utf-8 -*-

import os
import configparser
from pathlib import Path
from googletrans.constants import LANGUAGES

class SettingsManager:
    """Manages plugin settings for Direct Translate"""
    
    def __init__(self):
        self.plugin_dir = Path(__file__).parent.parent
        self.env_file = self.plugin_dir / ".env"
        self.settings_file = self.plugin_dir / "user_settings.ini"
        self.config = configparser.ConfigParser()
        self._load_settings()
    
    def _load_settings(self):
        """Load settings from both .env and user_settings.ini files"""
        # Create default settings file if it doesn't exist
        if not self.settings_file.exists():
            self._create_default_settings()
        
        # Load from settings file with proper encoding handling
        try:
            self.config.read(self.settings_file, encoding='utf-8')
        except UnicodeDecodeError:
            # If file has encoding issues, recreate it with defaults
            self._create_default_settings()
            self.config.read(self.settings_file, encoding='utf-8')
        except Exception:
            # If any other error, recreate with defaults
            self._create_default_settings()
    
    def _create_default_settings(self):
        """Create default settings file"""
        self.config['Translation'] = {
            'default_language': 'ar',
            'default_language_name': 'Arabic'
        }
        
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get_default_language(self):
        """Get the configured default language"""
        try:
            return self.config.get('Translation', 'default_language', fallback='ar')
        except:
            return 'ar'
    
    def set_default_language(self, lang_code, lang_name=None):
        """Set the default language"""
        if 'Translation' not in self.config:
            self.config['Translation'] = {}
        
        self.config['Translation']['default_language'] = lang_code
        if lang_name:
            self.config['Translation']['default_language_name'] = lang_name
        
        # Save to settings file
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
        
        # Update .env file for backward compatibility
        self._update_env_file(lang_code)
    
    def _update_env_file(self, lang_code):
        """Update the .env file with the new default language"""
        env_content = []
        env_updated = False
        
        if self.env_file.exists():
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith('default_language'):
                        env_content.append(f"default_language = '{lang_code}'  # Default target language for translation\n")
                        env_updated = True
                    else:
                        env_content.append(line)
        
        if not env_updated:
            env_content.append(f"default_language = '{lang_code}'  # Default target language for translation\n")
        
        with open(self.env_file, 'w', encoding='utf-8') as f:
            f.writelines(env_content)
    
    def get_available_languages(self):
        """Get list of available languages for translation"""
        # Convert Google Translate LANGUAGES dict to list of tuples with proper names
        all_languages = []
        
        # Add common languages first with native names for better UX
        priority_languages = {
            'ar': 'Arabic (العربية)',
            'zh-cn': 'Chinese Simplified (中文简体)',
            'zh-tw': 'Chinese Traditional (中文繁體)', 
            'en': 'English',
            'fr': 'French (Français)',
            'de': 'German (Deutsch)',
            'es': 'Spanish (Español)',
            'it': 'Italian (Italiano)',
            'ja': 'Japanese (日本語)',
            'ko': 'Korean (한국어)',
            'pt': 'Portuguese (Português)',
            'ru': 'Russian (Русский)',
            'tr': 'Turkish (Türkçe)',
            'hi': 'Hindi (हिन्दी)',
            'th': 'Thai (ไทย)',
            'vi': 'Vietnamese (Tiếng Việt)',
            'nl': 'Dutch (Nederlands)',
            'pl': 'Polish (Polski)',
            'sv': 'Swedish (Svenska)',
            'da': 'Danish (Dansk)',
            'no': 'Norwegian (Norsk)'
        }
        
        # Add all Google Translate supported languages
        for code, name in LANGUAGES.items():
            if code in priority_languages:
                # Use our enhanced name for priority languages
                all_languages.append((code, priority_languages[code]))
            else:
                # Use Google's name, capitalize first letter
                display_name = name.capitalize()
                all_languages.append((code, display_name))
        
        # Add Chinese variants that might not be in LANGUAGES
        if 'zh-cn' not in [lang[0] for lang in all_languages]:
            all_languages.append(('zh-cn', 'Chinese Simplified (中文简体)'))
        if 'zh-tw' not in [lang[0] for lang in all_languages]:
            all_languages.append(('zh-tw', 'Chinese Traditional (中文繁體)'))
        
        return sorted(all_languages, key=lambda x: x[1])
    
    def is_valid_language(self, lang_code):
        """Check if language code is valid"""
        return lang_code in LANGUAGES or lang_code in ['auto']

# Global settings manager instance
settings_manager = SettingsManager()
