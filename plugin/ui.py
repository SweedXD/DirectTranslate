# -*- coding: utf-8 -*-

import copy
from typing import List

from flowlauncher import FlowLauncher

from googletrans import Translator
from googletrans.constants import LANGUAGES, SPECIAL_CASES
from plugin.templates import *
from plugin.extensions import _
from plugin.settings_manager import settings_manager
import locale


class Main(FlowLauncher):
    items = []

    @staticmethod
    def system_lang():
        lang = locale.getdefaultlocale()
        return lang[0][:2] if lang else "en"

    def add_item(self, title: str, subtitle: str, method: str = None, parameters: list = None):
        item = {'Title': title, 'SubTitle': subtitle, 'IcoPath': ICON_PATH}
        if method:
            item['JsonRPCAction'] = {
                'method': method,
                'parameters': parameters or []
            }
        self.items.append(item)

    @staticmethod
    def valid_lang(lang: str) -> bool:
        return lang in LANGUAGES or lang in SPECIAL_CASES

    def translate(self, src: str, dest: str, query: str):
        try:
            # Check if destination language is valid first
            if not self.valid_lang(dest):
                self.add_item(f"❌ Invalid language code: {dest}", f"'{dest}' is not supported by Google Translate")
                return self.items
                
            translator = Translator()
            if src == "auto":
                detected = translator.detect(query)
                src = detected.lang
                sources = src if isinstance(src, list) else [src]
            else: 
                sources = [src]

            for src in sources:
                translation = translator.translate(query, src=src, dest=dest)
                
                # Check if translation actually happened
                if translation.text.lower() == query.lower():
                    # Translation didn't change - show debug info
                    self.add_item(f"⚠️ {translation.text}", f"No change: {src} → {dest} (same text)")
                else:
                    # Normal translation result
                    self.add_item(str(translation.text), f"{src} → {dest}   {query}")
                    
        except Exception as error:
            error_msg = str(error)
            if "invalid destination language" in error_msg.lower():
                self.add_item(f"❌ Invalid language: {dest}", f"'{dest}' not supported - try 'tr list' for valid codes")
            else:
                self.add_item(f"❌ Error: {error_msg}", f"Failed: {src} → {dest}   {query}")
        return self.items

    def help_action(self):
        # Clean menu with just 3 items
        current_lang = settings_manager.get_default_language()
        self.add_item(f"📍 Default language: {current_lang}", "Current default translation language")
        
        # Show usage instructions
        self.add_item("📖 Usage", "<hotkey> <from language> <to language> <text>")
        
        # Add command instruction to show languages
        self.add_item("🌐 List Languages", "Type 'tr list' to see all available languages")
        
        return self.items
    
    def show_languages(self):
        """Show all available languages when 'tr list' is typed"""
        # Show all available languages with direct clickable options
        for code, name in settings_manager.get_available_languages():
            self.add_item(f"{code} - {name}", f"Click to set {name} as default", 
                        method="set_default_language", parameters=[code, name])
        return self.items

    def settings_action(self, params):
        """Handle 'set' command for changing language (tr set <code>)"""
        if len(params) >= 2:
            lang_code = params[1]
            if settings_manager.is_valid_language(lang_code):
                # Find the language name from available languages
                lang_name = lang_code.upper()  # Default fallback
                for code, name in settings_manager.get_available_languages():
                    if code == lang_code:
                        lang_name = name
                        break
                
                # Check if this is already the current language
                current_lang = settings_manager.get_default_language()
                if lang_code == current_lang:
                    self.add_item("ℹ️ Already Set", f"{lang_name} is already your default language")
                    return self.items
                
                # Show confirmation before changing
                current_lang = settings_manager.get_default_language()
                self.add_item("✅ Yes, Change Language", f"Click to confirm change to {lang_name}", 
                            method="confirm_language_change", parameters=[lang_code, lang_name])
                self.add_item("❌ Cancel", "Click to cancel and go back", 
                            method="cancel_language_change", parameters=[])
                return self.items
            else:
                self.add_item("❌ Invalid Language", f"'{lang_code}' is not a valid language code")
                self.add_item("💡 Available Languages", "Type 'tr' to see all options")
                return self.items
        else:
            self.add_item("❌ Missing Language Code", "Usage: tr set <language_code>")
            self.add_item("💡 Example", "tr set en")
            return self.items

    def query(self, param: str='') -> List[dict]:
        query = param.strip()
        params = query.lower().split(" ")
        
        # Show help only if completely empty
        if not query.strip(): 
            return self.help_action()

        # Handle 'set' command for changing language (tr set <code>)
        if params[0] == "set":
            return self.settings_action(params)
        
        # Handle 'list' command for showing languages (tr list)
        if params[0] == "list":
            return self.show_languages()

        # For any other input, try to translate
        try:
            # Check if we have multiple words and first word is a valid language code
            if len(params) >= 2 and self.valid_lang(params[0]):
                # Check if second word is also a language code
                if len(params) >= 3 and self.valid_lang(params[1]):
                    # Two language codes: translate from first to second
                    return self.translate(params[0], params[1], " ".join(params[2:]))
                else:
                    # Single language code: translate TO that language from auto-detected
                    return self.translate("auto", params[0], " ".join(params[1:]))
            else:
                # Either single word or first word is not a language code
                # Always translate entire query to default language
                return self.translate("auto", settings_manager.get_default_language(), query)
        except Exception:
            # If anything goes wrong, try to translate to default language
            return self.translate("auto", settings_manager.get_default_language(), query)
    
    def set_default_language(self, lang_code: str, lang_name: str):
        """Action method called when user clicks on a language option"""
        try:
            settings_manager.set_default_language(lang_code, lang_name)
            # Return False to prevent Flow Launcher from closing
            return False
        except Exception as e:
            # Return False to prevent Flow Launcher from closing even on error
            return False
    
    def confirm_language_change(self, lang_code: str, lang_name: str):
        """Action method called when user clicks confirm button"""
        try:
            settings_manager.set_default_language(lang_code, lang_name)
            # Return False to prevent Flow Launcher from closing
            return False
        except Exception as e:
            # Return False to prevent Flow Launcher from closing even on error
            return False
    
    def cancel_language_change(self):
        """Action method called when user clicks cancel button"""
        # Just return False to prevent Flow Launcher from closing
        # User can type 'tr settings' again to see the settings menu
        return False
