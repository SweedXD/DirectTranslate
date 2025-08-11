# Direct Translate (Enhanced) for Flow Launcher
- Translate plugin that translates between any languages supported by python [googletrans](https://github.com/ssut/py-googletrans) library for [Flow Launcher](https://github.com/Flow-Launcher/Flow.Launcher).
- A completely overhauled version of the Direct Translate plugin, now with a powerful command interface and support for 100+ languages.

    ![Direct Translate Plugin Demo](https://github.com/user-attachments/assets/9116c13f-bb92-4987-b87d-ce471275688a)


## 🌟 Key Features
*   **Configurable Default Language:** Set your favorite language as the default.
*   **100+ Language Support:** Access the full Google Translate library.
*   **Command-Driven Interface:** Use `tr list` and `tr set <code>` to manage settings.
*   **Smarter Translation Logic:** The plugin is better at understanding your queries.

## 🚀 Installation

### ✅ Prerequisites

- **Python 3.6 or higher**, available in your system’s `PATH` (i.e., `python.exe` can be run from the terminal).
- **Flow Launcher v1.8+** can automatically install Python if it's missing.

> ℹ️ *Flow Launcher locates Python via your system `PATH`. If needed, manually set it under:*  
> `Settings → Plugin Settings → Python`

---

### 📦 Install from Flow Launcher Plugin Store

1. Launch Flow Launcher (`Alt + Space`)
2. Type `pm install` and search for Direct Translate (Enhanced) and hit **Enter**

That’s it — the plugin will be installed and ready to use instantly 🎉

---

### 🛠 Manual Installation

1. Download or clone the `DirectTranslate` folder.
2. Copy the folder into: `%APPDATA%\Roaming\FlowLauncher\Plugins\`
3. Restart Flow Launcher.

The plugin should now appear and be ready to use.



## 📋 Full Command Reference

| Command | Description |
| :--- | :--- |
| `tr` | Shows the main menu with current settings and usage info. |
| `tr list` | Displays the full list of 100+ supported languages. |
| `tr set <code>` | Begins the process of setting a new default language. |
| `tr <text>` | Translates text to your default language. |
| `tr <to> <text>` | Translates text TO the specified language. |
| `tr <from> <to> <text>` | Translates between a specific source and target language. |

**Examples:**
*   `tr hello world` -> Translates to your default language.
*   `tr es hello world` -> Translates "hello world" to Spanish.
*   `tr fr en maison` -> Translates "bonjour" from French to English.
*   `tr set fr` -> This will bring up a confirmation to set French as the default.

## 👨‍💼 Credits

*   Original updated plugin created by **@Drimix20**.
*   This enhanced version was updated by **@SweedXD**.