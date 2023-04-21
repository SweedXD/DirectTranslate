# Direct Translate (Flow.Launcher.Plugin.DirectTranslate)

Translate plugin that translates between any languages supported by python googletrans library for [Flow Launcher](https://github.com/Flow-Launcher/Flow.Launcher).

![Translate](https://i.imgur.com/mVxnBk1.gif)

#### About


Plugin uses [googletrans](https://github.com/ssut/py-googletrans) to translate between any supported languages.


### Requirements

Python 3.6 or later installed on your system, with python.exe in your PATH variable and this path updated in the Flow Launcher settings (this is a general requirement to use Python plugins with Flow). As of v1.8, Flow Launcher should take care of the installation of Python for you if it is not on your system.


### Installing

#### Package Manager

Use the `pm install` command from within Flow itself.

#### Manual

Add the Flow.Launcher.Plugin.DirectTranslate directory to %APPDATA%\Roaming\FlowLauncher\Plugins\ and restart Flow.

#### Python Package Requirements

There is no requirement to install the packages as they will be packed with the release. 

If you still want to manually pip install them:

The `requirements.txt` file in this repo outlines which packages are needed. This can be found online here on Github, as well as in the local plugin directory once installed (%APPDATA%\Roaming\FlowLauncher\Plugins\Direct Translate-X.X.X\ where X.X.X is the currently installed version)

The easiest way to manually install these packages is to use the following command in a Windows Command Prompt or Powershell Prompt

`pip install -r requirements.txt -t ./lib`

Remember you need to be in the local directory containing the requirements text file.

### Usage

| Keyword                                                          | Description                                 |
| ---------------------------------------------------------------- | ------------------------------------------- |
| `tr {from language} {to language} {words to be translated}` | Translate `words to be translated` from `from language` to `to language` language. Example of usage is `tr en cs hello world` |
| tr :set-proxy {proxy url}                                        | Set up a proxy url for connecting to Google Translate server. Example of usage is `tr :set-proxy http://localhost:1080` . |

Alternatively:
- if you do no supply any language code, your input language will be auto-detected as 'from language' and your 'to language' will be your computer system default language, e.g. `tr mattina`.
- if you just supply one language code, this will be used as the 'to language' and your input will be auto-detected as the 'from language', e.g. `tr it morning`

**Full list of supported language codes:**

https://developers.google.com/admin-sdk/directory/v1/languages

### Problems, errors and feature requests

Open an issue in this repo.
