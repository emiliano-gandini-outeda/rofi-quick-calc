# Rofi Quick Calc

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=3776AB" alt="Python">
   <a href="https://github.com/emiliano-gandini-outeda/LibreCourse/commits/main">
    <img src="https://img.shields.io/github/last-commit/emiliano-gandini-outeda/LibreCourse?style=for-the-badge" alt="Last Commit">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License: MIT License">
  </a>
</p>

---

A lightning-fast, keyboard-driven calculator that integrates seamlessly with Rofi. Perform calculations instantly and have results automatically copied to your clipboard.

![Rofi Quick Calc UI](https://i.imgur.com/K2X7L47.png)

## ✨ Features

- **⚡ Instant Calculations**: Type math expressions and get results immediately
- **📋 Auto-Copy**: Results are automatically copied to clipboard
- **📚 History**: Maintains calculation history between sessions
- **🎯 Rofi Integration**: Native Rofi interface with theming support
- **🔢 Math Functions**: Full math library support (sin, cos, sqrt, log, etc.)
- **💻 Desktop Notifications**: Visual feedback for copied results
- **🔄 History Reuse**: Select previous calculations to copy results or reuse expressions

## 🚀 Installation

### Prerequisites

- Python 3.x
- Rofi (`sudo apt install rofi` on Debian/Ubuntu)
- Optional: `libnotify-bin` for desktop notifications

### Quick Install

1. Clone or download the script:
```bash
curl -o ~/bin/rofi-quick-calc.py https://raw.githubusercontent.com/emiliano-gandini-outeda/rofi-quick-calc/main/rofi-quick-calc.py
chmod +x ~/bin/rofi-quick-calc.py
```

2. Install Python dependencies:
```bash
pip install pyperclip
```

3. (Optional) Install notification support:
```bash
sudo apt install libnotify-bin
```

### Keyboard Shortcut Setup

Add a keyboard shortcut to launch the calculator:

**i3WM** (`~/.config/i3/config`):
```bash
bindsym $mod+c exec --no-startup-id python3 ~/bin/rofi-quick-calc.py
```

**GNOME** (Settings → Keyboard Shortcuts):
- Add custom shortcut: `python3 ~/bin/rofi-quick-calc.py`

**KDE** (System Settings → Shortcuts):
- Add custom shortcut with the same command

## 🎮 Usage

### Basic Calculation
1. Press your configured hotkey (e.g., `Super+C`)
2. Type a mathematical expression:
   - `2+2`
   - `sqrt(16)`
   - `sin(pi/2)`
   - `2^8` (exponentiation)
3. Press Enter
4. Result is calculated and copied to clipboard automatically

### History Features
- Previous calculations are shown in the Rofi menu
- Select any history item to copy its result to clipboard
- History persists between sessions (stored in `~/.calc_history`)

### Supported Operations

| Operation | Example | Result |
|-----------|---------|--------|
| Basic Math | `2+3*4` | `14` |
| Functions | `sqrt(25)` | `5` |
| Trigonometry | `sin(pi/2)` | `1` |
| Exponents | `2^8` or `2**8` | `256` |
| Constants | `pi * 2` | `6.28318` |

## 🛠️ Configuration

### Rofi Theme
The script uses the `Adapta-Nokto` theme by default. To change the theme:

1. Edit the script and modify the rofi command:
```python
cmd = [
    "rofi",
    "-dmenu", 
    "-p", "➤ Calculate:",
    "-theme", "your-theme-name",  # Change this
    # ... other options
]
```

2. Or use your system's default theme by removing the `-theme` line

### History Size
Modify the history limit in the script:
```python
# Change from 15 to your preferred number
if len(history) > 15:
    history.pop(0)
```

## 🐛 Troubleshooting

### Clipboard Issues
If copying doesn't work:
```bash
# Install pyperclip for better clipboard support
pip install pyperclip

# Or install system clipboard utilities
sudo apt install xclip  # For X11
# or
sudo apt install wl-clipboard  # For Wayland
```

### Rofi Not Found
```bash
sudo apt install rofi
```

### Notifications Not Working
```bash
sudo apt install libnotify-bin
```

## 📁 File Locations

- **Script**: `~/bin/rofi-quick-calc.py` (or your preferred location)
- **History**: `~/.calc_history`
- **Temporary Files**: `~/.calc_clipboard_temp` (fallback storage)

## 🔧 Advanced Usage

### Command Line Use
You can also use the calculator from the command line:
```bash
python3 ~/bin/rofi-quick-calc.py
```

### Custom Math Functions
The calculator supports all Python math functions:
- `log(x)`, `log10(x)`
- `degrees(x)`, `radians(x)`
- `factorial(x)`
- `hypot(x, y)`
- And many more...

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

---

**💡 Pro Tip**: Map this to a easily accessible hotkey for instant calculations anytime!
