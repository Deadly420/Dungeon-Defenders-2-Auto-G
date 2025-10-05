# 🎮 Macro Controller — Dungeon Defenders 2 Automation Tool

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-success)

> 🧠 A lightweight, modern GUI-based macro controller built in Python using **CustomTkinter** and **Win32 API**, designed to automate repetitive key actions in *Dungeon Defenders 2* with precision and ease.

---

## ✨ Features

- 🎯 **Automated Key Actions** — Presses `G` to ready up and `M` to drop mana automatically.  
- 🧩 **Threaded Performance** — Smooth multithreaded handling for simultaneous key loops.  
- 🪟 **Window Targeting** — Automatically finds the *Dungeon Defenders 2* window and sends input directly.  
- ⚙️ **Customizable Settings** — Toggle mana dropping and adjust press delay in real time.  
- 🎨 **Modern Dark-Themed Interface** — Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for a professional, sleek look.

---

## 🧩 Requirements

Install dependencies before running:
  ```
  pip install customtkinter pywin32
  ```

---

## ⚙️ Configuration

If your game window title differs from the default, update this line in the script:
  ```
  self.target_window_title = "Dungeon Defenders 2"
  ```

---

## 🧑‍💻 Built With

| Component            | Purpose                |
| -------------------- | ---------------------- |
| 🐍 **Python 3**      | Core language          |
| 🪟 **pywin32**       | Simulated window input |
| 🎨 **CustomTkinter** | Modern themed GUI      |
| 🧵 **Threading**     | Background automation  |

---

## 📜 License

Distributed under the MIT License.
See LICENSE

---

## 💡 Author

[@Deadly](https://github.com/Deadly420) — Developer & Designer of Macro

---
