# 🎮 JXR to PNG Converter

Just a note before the rest of the description which was completely written by Google Gemini: this is basically just a GUI with some commodity features i really needed in order to share screenshots i made with NVIDIA Share with my friends on Discord, telegram and so on...
The core of the project is - **[jxr_to_png](https://github.com/ledoge/jxr_to_png)** by **[ledoge](https://github.com/ledoge)**, which actually coded the program. Also thanks to **[hdrfix](https://github.com/bvibber/hdrfix)** by **[bvibber](https://github.com/bvibber)**.

A desktop application that **automatically monitors** NVIDIA screenshot directories for HDR `.jxr` files and converts them to high-quality SDR `.png` format with professional tone mapping.

Built with **PyQt5** — features a premium dark-mode UI, system tray integration, multi-language support, and multi-threaded parallel conversion.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-Desktop_App-green?logo=qt&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)

---

## ✨ Features

- **🔄 Automatic Monitoring** — Watches NVIDIA screenshot folders recursively via [Watchdog](https://github.com/gorakhargosh/watchdog), converting new `.jxr` files on the fly.
- **🎨 Professional Tone Mapping** — Two-stage pipeline: HDR decode → Hable tone mapping with boosted saturation for vivid, social-media-ready colors.
- **🌐 Multi-Language Support** — Available in 10 languages (IT, EN, ES, DE, FR, PT, JA, ZH, KO, RU) with automatic system language detection and in-app language selector.
- **🤫 Customizable Background Mode** — Toggle between "Minimize to Tray" or "Close App" on window close.
- **⚡ Parallel Conversion** — Multi-threaded processing (3 workers) for blazing fast batch conversions.
- **🛡️ Smart File Detection** — Automatically detects and fixes fake `.jxr` files that are actually mislabeled PNGs (a known NVIDIA bug).
- **🖥️ Premium Dark UI** — Glassmorphism-inspired interface with purple/blue accents, smooth animations, and a polished system tray experience.
- **📦 Single Instance Guard** — Prevents multiple instances from running simultaneously.
- **🔧 Persistent Configuration** — Settings stored in `%APPDATA%` for seamless operation even when installed in `C:\Program Files`.

---

## 🌐 Supported Languages

| Language | Code | Flag |
|----------|------|------|
| Italiano | `it` | 🇮🇹 |
| English | `en` | 🇬🇧 |
| Español | `es` | 🇪🇸 |
| Deutsch | `de` | 🇩🇪 |
| Français | `fr` | 🇫🇷 |
| Português | `pt` | 🇧🇷 |
| 日本語 | `ja` | 🇯🇵 |
| 中文 | `zh` | 🇨🇳 |
| 한국어 | `ko` | 🇰🇷 |
| Русский | `ru` | 🇷🇺 |

The app automatically detects your system language on first launch. You can change the language at any time from the in-app selector — it switches instantly without restart.

---

## 📸 How It Works

The conversion pipeline uses a two-step process to ensure maximum color fidelity:

```
┌──────────┐      ┌──────────────┐      ┌─────────────┐      ┌──────────┐
│  .jxr    │ ──▶  │ jxr_to_png   │ ──▶  │   hdrfix    │ ──▶  │  .png    │
│  (HDR)   │      │  (decode)    │      │ (tone map)  │      │  (SDR)   │
└──────────┘      └──────────────┘      └─────────────┘      └──────────┘
```

1. **Decode**: `jxr_to_png.exe` decodes the JPEG XR HDR file into a raw HDR PNG.
2. **Tone Map**: `hdrfix.exe` applies the **Hable** filmic tone mapping curve with `+20%` saturation boost, producing an SDR image that looks vivid even after social media compression (Telegram, WhatsApp, etc.).

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+**
- **Windows 10/11**

### From Source

```bash
# Clone the repository
git clone https://github.com/TargetMisser/JXRConverter.git
cd JXRConverter

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Build Standalone Executable

The included PowerShell script automates the full build and install process:

```powershell
# Run as Administrator
powershell -ExecutionPolicy Bypass -File build_and_install.ps1
```

This will:
1. Compile the app with PyInstaller
2. Bundle `jxr_to_png.exe` and `hdrfix.exe`
3. Install to `C:\Program Files\JXRConverter\`
4. Create a Desktop shortcut

### External Tools Required

You need to place these executables in the project root before building:

| Tool | Source | Purpose |
|------|--------|---------|
| `jxr_to_png.exe` | [ledoge/jxr_to_png](https://github.com/ledoge/jxr_to_png) | Decodes JPEG XR HDR files to PNG |
| `hdrfix.exe` | [bvibber/hdrfix](https://github.com/bvibber/hdrfix) | Applies tone mapping (HDR → SDR) |

---

## ⚙️ Configuration

On first launch, configure:

- **Watch Folder**: The NVIDIA screenshot directory to monitor (default: `C:\Users\<you>\Videos\NVIDIA`)
- **Tool Path**: Path to the folder containing `jxr_to_png.exe` and `hdrfix.exe`
- **Language**: Auto-detected from your system, or pick manually from the dropdown

Settings are persisted in `%APPDATA%\JXRConverter\config.json`.

---

## 🏗️ Project Structure

```
JXRConverter/
├── main.py              # Entry point, single-instance guard, High-DPI
├── ui.py                # PyQt5 GUI (dark mode, system tray, config, i18n)
├── converter.py         # Watchdog + ThreadPool conversion engine
├── translations.py      # Multi-language i18n system (10 languages)
├── styles.py            # QSS stylesheet (glassmorphism dark theme)
├── resources.py         # Inline SVG icons for window and tray
├── requirements.txt     # Python dependencies
└── build_and_install.ps1 # Automated build & deploy script
```

---

## 🙏 Credits & Acknowledgments

### External Tools

This project would not be possible without these excellent open-source tools:

- **[jxr_to_png](https://github.com/ledoge/jxr_to_png)** by **[ledoge](https://github.com/ledoge)** — JPEG XR to PNG decoder with HDR metadata support. Used as the first stage of the conversion pipeline.
- **[hdrfix](https://github.com/bvibber/hdrfix)** by **[bvibber](https://github.com/bvibber)** (Brion Vibber) — HDR to SDR tone mapping tool with multiple algorithms (Hable, ACES, Reinhard). Used as the second stage for professional-grade color conversion.

### Libraries

- **[PyQt5](https://www.riverbankcomputing.com/software/pyqt/)** — Cross-platform GUI framework by Riverbank Computing.
- **[Watchdog](https://github.com/gorakhargosh/watchdog)** — Filesystem monitoring library.
- **[PyInstaller](https://pyinstaller.org/)** — Used for packaging the standalone executable.

### Development

- Built with the assistance of **[Antigravity](https://blog.google/technology/google-deepmind/)** by Google DeepMind.

---

## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Note: The external tools (`jxr_to_png.exe`, `hdrfix.exe`) are **not included** in this repository and are subject to their own licenses. Please refer to their respective repositories for license information.

---

## 🐛 Known Issues & Notes

- NVIDIA occasionally saves screenshots with a `.jxr` extension that are actually PNG files internally. The app automatically detects and handles this case.
- The Hable tone mapping with `+20%` saturation is tuned to counteract the color desaturation that occurs when sharing images on platforms like Telegram and WhatsApp.
- `jxr_to_png.exe` already uses multi-threading internally (6 threads for decoding), so the app limits parallel workers to 3 to avoid CPU saturation.

---

## 📋 Changelog

### v1.2 — Multi-Language Support
- Added internationalization (i18n) with support for 10 languages
- Auto-detects system language on first launch
- In-app language selector with instant switching (no restart needed)
- New styled QComboBox for language selection

### v1.1 — Tray Toggle
- Added toggle for minimize-to-tray vs close behavior

### v1.0 — Initial Release
- Automatic HDR screenshot monitoring and conversion
- Two-stage conversion pipeline with Hable tone mapping
- Premium dark-mode UI with system tray integration
