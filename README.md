# 🎮 Dungeon Defenders 2 Automation Tool
![GitHub all releases](https://img.shields.io/github/downloads/Deadly420/Dungeon-Defenders-2-Auto-G/total?color=brightgreen&label=Downloads&logo=github)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-success)

> 🧠 A **modern, feature-rich macro automation tool** for *Dungeon Defenders 2*, built with **CustomTkinter** and **Win32 API**.  
> Automate repetitive key actions (like pressing `G` and dropping mana) while maintaining full GUI control, keybind customization, and overlay display.

---

## ✨ Features

- 🎯 **Automated Key Actions**  
  Automatically presses `G` to ready up and `M` to drop mana automatically. 

- ⚡ **Threaded & Responsive**  
  Uses multithreading for smooth automation with zero interface lag.

- 🪟 **Window Targeting System**  
  Detects and sends input directly to the *Dungeon Defenders 2* game window.

- 🔄 **Real-Time Controls**  
  Start, pause, and stop macros instantly — or toggle mana dropping with a hotkey.

- 🎨 **CustomTkinter GUI**  
  Beautiful modern dark UI with smooth buttons, frames, and controls.

- 💬 **Draggable Overlay HUD**  
  Minimal, transparent overlay that shows real-time macro status and keybinds.  
  (Position is saved automatically between sessions.)

- ⌨️ **Fully Customizable Keybinds**  
  Change hotkeys (`Pause`, `Drop Mana`) directly through the GUI — saved to `info.json`.

- 💾 **Persistent Configuration**  
  Saves keybinds, overlay position, and window title between runs.

---

## 🧩 Requirements

Before running, install dependencies:

```bash
pip install customtkinter pywin32 keyboard
```

## ⚙️ Configuration

If your game window title differs from the default, update it in the app:

Locate the “🎯 Target Window Title” field in the main GUI.

Type the exact or partial name of your game window.
(e.g., Dungeon Defenders 2, DD2, etc.)

The app automatically searches for and targets all windows matching that title.

---
## 🧠 Hotkeys

| Action            | Default Key | Description                                |
| ----------------- | ----------- | ------------------------------------------ |
| 💤 Pause / Resume | `Q`         | Pauses or resumes the macro loop           |
| 💎 Drop Mana      | `M`         | Toggles automatic mana dropping            |
| 🪟 Overlay        | GUI Button  | Shows or hides the floating overlay window |

You can change hotkeys anytime via the Customize Keybinds menu in the GUI.

---
## 💾 Saving & Loading
All preferences (keybinds, overlay position, window title) are automatically saved in:
```
info.json
```
If this file is deleted, defaults will be restored on next launch.

---

## 🧑‍💻 Built With
| Component            | Purpose                                |
| -------------------- | -------------------------------------- |
| 🐍 **Python 3.9+**   | Core language                          |
| 🪟 **pywin32**       | Handles window-based input sending     |
| 🎨 **CustomTkinter** | Provides modern dark-themed GUI        |
| ⌨️ **keyboard**      | Global hotkey detection                |
| 🧵 **Threading**     | Background automation & responsiveness |
| 💾 **JSON / AST**    | Persistent keybind and window storage  |


---

## 📜 License

Distributed under the MIT License.
See LICENSE

---

## 💡 Author

Developed by [@Deadly](https://github.com/Deadly420)

---
