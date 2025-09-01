# -*- coding: utf-8 -*-

import json
import os
from textwrap import dedent
from typing import List

import click

from plugin import (
    ICON_PATH,
    PLUGIN_ACTION_KEYWORD,
    PLUGIN_AUTHOR,
    PLUGIN_EXECUTE_FILENAME,
    PLUGIN_ID,
    PLUGIN_PROGRAM_LANG,
    PLUGIN_URL,
    PLUGIN_URL_DOWNLOAD,
    PLUGIN_URL_SOURCE_CODE,
    PLUGIN_ZIP_NAME,
    TRANSLATIONS_PATH,
    __long_description__,
    __package_name__,
    __short_description__,
    __version__,
    basedir,
)

# constants
# folder
build_path = basedir / "build"
build_path.mkdir(exist_ok=True)
lib_path = basedir / "lib"
lib_path.mkdir(exist_ok=True)

# file
build_ignore_path = basedir / ".buildignore"
build_ignore_path.touch()  # if no existed, would be created
plugin_info_path = basedir / "plugin.json"
zip_path = build_path / f"{PLUGIN_ZIP_NAME}"

plugin_infos = {
    "ID": PLUGIN_ID,
    "ActionKeyword": PLUGIN_ACTION_KEYWORD,
    "Name": __package_name__,
    "Description": __short_description__,
    "Author": PLUGIN_AUTHOR,
    "Version": __version__,
    "Language": PLUGIN_PROGRAM_LANG,
    "Website": PLUGIN_URL,
    "IcoPath": ICON_PATH,
    "ExecuteFileName": PLUGIN_EXECUTE_FILENAME,
    "UrlDownload": PLUGIN_URL_DOWNLOAD,
    "UrlSourceCode": PLUGIN_URL_SOURCE_CODE,
}


def get_build_ignores(comment: str = "#") -> List[str]:
    """
    Ignore file or folder when building a plugin, similar to '.gitignore'.
    """
    ignore_list = []

    with open(build_ignore_path, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line and not line.startswith(comment):
                ignore_list.append(line)

    return ignore_list


def hook_env_snippet(exec_file: str = PLUGIN_EXECUTE_FILENAME) -> str:
    """Hook lib folder path to python system environment variable path."""

    env_snippet = dedent(
        f"""\
    import os
    import sys

    basedir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(basedir, "{lib_path.name}"))
    """
    )

    temp_path = build_path / exec_file
    entry_src = basedir / exec_file
    with open(entry_src, "r") as f_r:
        with open(temp_path, "w") as f_w:
            f_w.write(env_snippet + f_r.read())

    return temp_path


@click.group()
def translate(self, src: str, dest: str, query: str):
    """Translation and localization commands."""
    try:
        translator = Translator()
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


@translate.command()
@click.argument("locale")
def init(locale):
    """Initialize a new language."""

    if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    if os.system(f"pybabel init -i messages.pot -d {TRANSLATIONS_PATH} -l {locale}"):
        raise RuntimeError("init command failed")
    os.remove("messages.pot")

    click.echo("Done.")


@translate.command()
def update():
    """Update all languages."""
    if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    if os.system(f"pybabel update -i messages.pot -d {TRANSLATIONS_PATH}"):
        raise RuntimeError("update command failed")
    os.remove("messages.pot")

    click.echo("Done.")


@translate.command()
def compile():
    """Compile all languages."""

    if os.system(f"pybabel compile -d {TRANSLATIONS_PATH}"):
        raise RuntimeError("compile command failed")

    click.echo("Done.")


@click.group()
def plugin():
    """Plugin commands."""
    ...


@plugin.command()
def gen_plugin_info():
    """Auto generate the 'plugin.json' file for Flow."""

    with open(plugin_info_path, "w") as f:
        json.dump(plugin_infos, f, indent=4)

    click.echo("Done.")


@plugin.command()
def build():
    "Pack plugin to a zip file."

    zip_path.unlink(missing_ok=True)

    ignore_list = get_build_ignores()
    ignore_string = "'" + "' '".join(ignore_list) + "'"
    os.system(f"zip -r {zip_path} . -x {ignore_string}")

    entry_src_hooked = hook_env_snippet()
    os.system(f"zip -j {zip_path} {entry_src_hooked}")
    entry_src_hooked.unlink()

    click.echo("Done.")


@click.group()
def env():
    ...


@env.command()
def setup_env():
    """
    Set up the environment for the first time.
    This installs requirements.txt and requirements-dev.txt
    """

    os.system("pip install -r requirements.txt --upgrade")
    os.system("pip install -r requirements-dev.txt --upgrade")

    click.echo("Environment ready to go.")


@env.command()
def setup_env_to_lib():
    """
    Install dependencies to local.
    """

    os.system(f"pip install -r requirements.txt -t {lib_path} --upgrade")

    # Write Python 3.13+ compatibility shim for deprecated stdlib 'cgi'
    # Old versions of httpx import cgi.parse_header, which was removed in 3.13 (PEP 594).
    # Ensure lib/cgi.py exists in the packaged artifact.
    shim_path = lib_path / "cgi.py"
    try:
        shim_src = '''# Minimal compatibility shim for Python 3.13+ (PEP 594)
# Provides cgi.parse_header used by older httpx versions.
from typing import Dict, Tuple

__all__ = ["parse_header"]

def parse_header(line: str) -> Tuple[str, Dict[str, str]]:
    if not line:
        return "", {}
    parts = [p.strip() for p in line.split(";")]
    content_type = parts[0].lower() if parts else ""
    params: Dict[str, str] = {}
    for item in parts[1:]:
        if not item:
            continue
        if "=" in item:
            k, v = item.split("=", 1)
            k = k.strip().lower()
            v = v.strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
                v = v[1:-1]
            params[k] = v
        else:
            params[item.lower()] = ""
    return content_type, params
'''
        with open(shim_path, "w", encoding="utf-8") as f:
            f.write(shim_src)
    except Exception as e:
        click.echo(f"Warning: failed to write cgi shim: {e}")

    click.echo("Done.")


@click.group()
def clean():
    """Clean commands."""
    ...


@clean.command()
def clean_build():
    """Remove build artifacts"""

    os.system("rm -fr build/")
    click.echo("Done.")


@clean.command()
def clean_pyc():
    "Remove Python file artifacts"

    os.system(f"find {basedir} -name '*.pyc' -exec rm -f {{}} +")
    os.system(f"find {basedir} -name '*.pyo' -exec rm -f {{}} +")
    os.system(f"find {basedir} -name '*~' -exec rm -f {{}} +")

    click.echo("Done.")


if __name__ == "__main__":
    cli = click.CommandCollection(
        sources=[
            clean,
            env,
            plugin,
            translate,
        ]
    )
    cli()
