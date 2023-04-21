# -*- coding: utf-8 -*-

import copy
from typing import List

from flowlauncher import FlowLauncher

from googletrans import Translator
from googletrans.constants import LANGUAGES, SPECIAL_CASES
from plugin.templates import *
from plugin.extensions import _
import locale
import httpx
import httpcore
import os

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
proxy_config = os.path.join(basedir, "proxy_config")

class Main(FlowLauncher):
    items = []

    @staticmethod
    def system_lang():
        defaultlocale = locale.getdefaultlocale()
        lang = defaultlocale[0] if defaultlocale else "en"
        lang_code = lang[:2]

        # for chinese language
        lower_lang = lang.lower()
        if "chinese (simplified)" in lower_lang or "zh_cn" in lower_lang:
            lang_code = "zh-cn"
        elif "chinese (traditional)" in lower_lang or "zh_tw" in lower_lang:
            lang_code = "zh-tw"
        elif "chinese" in lower_lang or "zh" in lower_lang:
            lang_code = "zh-cn" # default to simplified chinese

        return lang_code

    def add_item(self, title: str, subtitle: str):
        self.items.append({'Title': title, 'SubTitle': subtitle, 'IcoPath': ICON_PATH})

    @staticmethod
    def valid_lang(lang: str) -> bool:
        return lang in LANGUAGES or lang in SPECIAL_CASES

    def write_proxy(self, url: str):
        try:
            with open(proxy_config, "w") as f:
                f.write(url)
            self.add_item("Success", f"Proxy set to {url}")
        except:
            self.add_item("Error", f"Failed to save proxy config to file: '{proxy_config}'")
        return self.items


    def read_proxy(self):
        try:
            with open(proxy_config, "r") as f:
                return f.read()
        except:
            return None

    def translate(self, src: str, dest: str, query: str):
        try:
            proxy = self.read_proxy()
            translator = Translator() if proxy is None else Translator(proxies = {
                "all": httpcore.SyncHTTPProxy(
                    proxy_url = httpx.Proxy(url = proxy).url.raw,
                )
            })

            if src == "auto":
                src = translator.detect(query).lang
                sources = src if isinstance(src, list) else [src]
            else: sources = [src]

            for src in sources:
                translation = translator.translate(query, src=src, dest=dest)
                self.add_item(_(str(translation.text)), f"{src} → {dest}   {query}")
        except Exception as error:
            self.add_item(_(str(error)), f"{src} → {dest}   {query}")
        return self.items

    def help_action(self):
        self.add_item("direct translate", _("<hotkey> <from language> <to language> <text>"))
        self.add_item("set proxy url", _("<hotkey> :set-proxy <proxy url>"))
        return self.items

    def query(self, param: str='') -> List[dict]:
        query = param.strip().lower()
        params = query.split(" ")
        if len(params) < 1 or len(params[0]) < 2: return self.help_action()

        try:
            # set proxy url
            if params[0] == ":set-proxy": return self.write_proxy(params[1])
            # no lang_code: <auto> -> <system language>
            if not self.valid_lang(params[0]): return self.translate("auto", self.system_lang(), query)
            # one lang_code: <auto> -> lang_code
            if not self.valid_lang(params[1]): return self.translate("auto", params[0], " ".join(params[1:]))
            # 2 lang_codes: lang1 -> lang2
            return self.translate(params[0], params[1], " ".join(params[2:]))
        except IndexError:
            return self.help_action()
