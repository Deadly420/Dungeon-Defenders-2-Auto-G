import time
import win32gui
import win32con
import win32api
import ctypes

import customtkinter as ctk
from tkinter import messagebox
from threading import Thread
import keyboard
import json
import os
import ast


class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Macro Controller")
        self.root.geometry("350x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.is_running = False
        self.is_paused = False
        self.overlay_visible = False
        self.target_window_title = "Dungeon Defenders 2"

        # Default keybinds (may be overwritten by load_info()
        self.keybinds = {
            "pause": "q",
            "drop_mana": "m",
        }

        # Settings
        self.drop_mana_enabled = ctk.BooleanVar(value=True)
        self.mana_speed = ctk.DoubleVar(value=0.05)

        # Threads / windows
        self.mana_thread = None
        self.overlay_window = None
        self.keybind_window = None

        # Load keybinds & register hotkeys
        self.load_info()
        self.register_hotkeys()

        # === UI ===
        self.status_label = ctk.CTkLabel(root, text="Status: Stopped", font=("Segoe UI Semibold", 16))
        self.status_label.grid(row=0, column=0, columnspan=2, pady=20, padx=10)

        # --- Button Grid ---
        self.start_button = ctk.CTkButton(root, text="Start Macro", command=self.start_macro, font=("Arial", 14), width=160)
        self.start_button.grid(row=1, column=0, padx=10, pady=10)

        self.pause_button = ctk.CTkButton(root, text=f"Pause Macro ({self.keybinds['pause'].upper()})", command=self.toggle_pause, font=("Arial", 14), width=160)
        self.pause_button.grid(row=1, column=1, padx=10, pady=10)

        self.stop_button = ctk.CTkButton(root, text="Stop Macro", command=self.stop_macro, font=("Arial", 14), width=160)
        self.stop_button.grid(row=2, column=0, padx=10, pady=10)

        self.customize_keys = ctk.CTkButton(root, text="Customize Keybinds", command=self.open_keybind_settings, font=("Arial", 14), width=160)
        self.customize_keys.grid(row=2, column=1, padx=10, pady=10)

        self.overlay_button = ctk.CTkButton(root, text="Show Overlay", command=self.toggle_overlay, font=("Arial", 14), width=160)
        self.overlay_button.grid(row=3, column=0, padx=10, pady=10)

        self.exit_button = ctk.CTkButton(root, text="Exit", command=self.exit_app, font=("Arial", 14), width=160)
        self.exit_button.grid(row=3, column=1, padx=10, pady=10)

        # --- Target Window Section ---
        self.title_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.title_frame.grid(row=4, column=0, columnspan=2, pady=20, padx=10)

        self.title_window_label = ctk.CTkLabel(self.title_frame, text="🎯 Target Window Title:", font=("Segoe UI Semibold", 16))
        self.title_window_label.grid(row=0, column=0, columnspan=2, pady=(0, 5))

        self.title_var = ctk.StringVar(value=self.target_window_title)
        self.title_window = ctk.CTkEntry(self.title_frame, textvariable=self.title_var, font=("Segoe UI", 14), height=36, width=250, corner_radius=10, justify="center",)
        self.title_window.grid(row=1, column=0, columnspan=2, pady=(0, 5))
        self.title_var.trace_add("write", self.update_target_window_title)

        # --- Settings ---
        self.drop_mana_check = ctk.CTkCheckBox(root, text=f"Drop Mana ({self.keybinds['drop_mana'].upper()})", variable=self.drop_mana_enabled,)
        self.drop_mana_check.grid(row=5, column=0, columnspan=2, pady=10)

        # Make grid resize nicely
        for i in range(2):
            self.root.grid_columnconfigure(i, weight=1)

        # =====================================================
        # ===============  KEYBIND WINDOW  ====================
        # =====================================================

    def open_keybind_settings(self):
        if self.keybind_window and self.keybind_window.winfo_exists():
            self.keybind_window.focus()
            return

        self.keybind_window = ctk.CTkToplevel(self.root)
        self.keybind_window.title("Keybind Settings")
        self.keybind_window.geometry("320x260")
        self.keybind_window.resizable(False, False)

        # Restore saved position
        pos = self.saved_positions.get("keybind_window")
        if pos:
            self.keybind_window.geometry(f"320x260+{pos[0]}+{pos[1]}")

        self.make_window_draggable(self.keybind_window)

        def on_close():
            try:
                if self.keybind_window.winfo_exists():
                    x, y = self.keybind_window.winfo_x(), self.keybind_window.winfo_y()
                    self.saved_positions["keybind_window"] = [x, y]
                    self.save_info()
            except:
                pass
            self.keybind_window.destroy()
            self.keybind_window = None

        self.keybind_window.protocol("WM_DELETE_WINDOW", on_close)

        ctk.CTkLabel(self.keybind_window, text="Customize Keybinds", font=("Segoe UI", 18, "bold")).pack(pady=10)

        entries = {}
        for action, key in self.keybinds.items():
            frame = ctk.CTkFrame(self.keybind_window, fg_color="transparent")
            frame.pack(pady=5, fill="x", padx=8)
            ctk.CTkLabel(frame, text=action.replace("_", " ").title(), width=130, anchor="w").pack(side="left", padx=5)
            entry = ctk.CTkEntry(frame, width=120)
            entry.insert(0, key)
            entry.pack(side="left", padx=5)
            entries[action] = entry

        def save_keys():
            for action, entry in entries.items():
                new_key = entry.get().lower().strip()
                if not new_key:
                    messagebox.showwarning("Invalid Key", f"Key for '{action}' is empty.")
                    return
                self.keybinds[action] = new_key

            self.save_info()
            self.register_hotkeys()
            self.update_overlay()
            try:
                self.drop_mana_check.configure(text=f"Drop Mana ({self.keybinds['drop_mana'].upper()})")
            except:
                pass
            on_close()

        ctk.CTkButton(self.keybind_window, text="Save", command=save_keys).pack(pady=12)

    #-------------------------------

    # --------------------------
    # Window Drag Helper Methods
    # --------------------------
    def make_window_draggable(self, window, target_widget=None):
        """Enable click-and-drag movement for a CTk or CTkToplevel window."""
        widget = target_widget or window
        drag_data = {"x": 0, "y": 0}

        def start_move(event):
            drag_data["x"] = event.x_root
            drag_data["y"] = event.y_root

        def do_move(event):
            dx = event.x_root - drag_data["x"]
            dy = event.y_root - drag_data["y"]
            new_x = window.winfo_x() + dx
            new_y = window.winfo_y() + dy
            window.geometry(f"+{new_x}+{new_y}")
            drag_data["x"] = event.x_root
            drag_data["y"] = event.y_root

        widget.bind("<ButtonPress-1>", start_move)
        widget.bind("<B1-Motion>", do_move)

    # =====================================================
    # ===============  OVERLAY WINDOW  ====================
    # =====================================================

    def toggle_overlay(self):
        if self.overlay_visible:
            self.hide_overlay()
        else:
            self.show_overlay()

    def hide_overlay(self):
        if not self.overlay_window:
            return
        try:
            if self.overlay_window.winfo_exists():
                x, y = self.overlay_window.winfo_x(), self.overlay_window.winfo_y()
                self.saved_positions["overlay_window"] = [x, y]
                self.save_info()
        except Exception as e:
            print(f"[WARN] Could not save overlay position: {e}")

        self.overlay_visible = False
        self.overlay_button.configure(text="Show Overlay")

        try:
            self.overlay_window.destroy()
        except:
            pass
        self.overlay_window = None

    def show_overlay(self):
        if self.overlay_window:
            return

        self.overlay_window = ctk.CTkToplevel(self.root)
        self.overlay_window.title("Macro Overlay")
        self.overlay_window.attributes("-topmost", True)
        self.overlay_window.overrideredirect(True)
        self.overlay_window.configure(fg_color="black")
        self.overlay_window.wm_attributes("-transparentcolor", "black")

        pos = self.saved_positions.get("overlay_window", [20, 400])
        self.overlay_window.geometry(f"230x150+{pos[0]}+{pos[1]}")

        frame = ctk.CTkFrame(self.overlay_window, fg_color="#141414", corner_radius=16, border_width=2,
                             border_color="#2f80ed")
        self.make_window_draggable(self.overlay_window, frame)
        frame.pack(expand=True, fill="both", padx=8, pady=8)

        ctk.CTkLabel(frame, text="🎮 Macro Overlay", font=("Segoe UI Semibold", 18), text_color="#7cdfff").pack(
            pady=(10, 5))

        self.overlay_status_label = ctk.CTkLabel(frame, text=self._get_status_text(), font=("Segoe UI Semibold", 16),
                                                 text_color="#00ffae", anchor="center")
        self.overlay_status_label.pack(pady=(0, 5))

        self.overlay_label = ctk.CTkLabel(frame, text=self._get_overlay_text(), font=("Segoe UI", 14), justify="left",
                                          text_color="#e8e8e8")
        self.overlay_label.pack(pady=(0, 10))

        self.overlay_visible = True
        self.overlay_button.configure(text="Hide Overlay")
        self.update_overlay()

    def _get_status_text(self):
        return f"Status: {'Paused' if self.is_paused else 'Running' if self.is_running else 'Stopped'}"

    def _get_overlay_text(self):
        return f"[{self.keybinds['pause'].upper()}] Pause / Resume\n[{self.keybinds['drop_mana'].upper()}] Drop Mana: {'ON' if self.drop_mana_enabled.get() else 'OFF'}"

    def update_overlay(self):
        if self.overlay_visible and self.overlay_window:
            try:
                self.overlay_status_label.configure(text=self._get_status_text())
                self.overlay_label.configure(text=self._get_overlay_text())
            except:
                pass
            self.overlay_window.after(300, self.update_overlay)

    def register_hotkeys(self):
        try:
            # Safely clear previous hotkeys if any
            if hasattr(keyboard, "unhook_all_hotkeys"):
                try:
                    keyboard.unhook_all_hotkeys()
                except AttributeError:
                    # fallback for newer versions of keyboard
                    for hook in getattr(keyboard, "_hotkeys", []):
                        try:
                            keyboard.remove_hotkey(hook)
                        except Exception:
                            pass
        except Exception as e:
            print(f"[WARN] Could not clear old hotkeys: {e}")

        # Register user-configurable keys
        try:
            keyboard.add_hotkey(self.keybinds["pause"], lambda: self.toggle_pause())
            keyboard.add_hotkey(self.keybinds["drop_mana"], lambda: self.toggle_drop_mana())
            print("[INFO] Hotkeys registered:", self.keybinds)
        except Exception as e:
            print(f"[ERROR] Failed to register hotkeys: {e}")

    def toggle_drop_mana(self):
        """Toggle the Drop Mana setting on/off via hotkey."""
        self.drop_mana_enabled.set(not self.drop_mana_enabled.get())
        print(f"[INFO] Drop Mana toggled: {'ON' if self.drop_mana_enabled.get() else 'OFF'}")
        # Update overlay text immediately
        self.update_overlay()
        # Update checkbox label to reflect new keybind
        try:
            self.drop_mana_check.configure(text=f"Drop Mana ({self.keybinds['drop_mana'].upper()})")
        except Exception:
            pass

    #--------------------------

    def update_target_window_title(self, *_):
        self.target_window_title = self.title_var.get()
        print(f"Target window title updated to: {self.target_window_title}")

    def send_key_to_window(self, hwnd, key):
        try:
            win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, key, 0)
            time.sleep(0.01)
            win32api.SendMessage(hwnd, win32con.WM_KEYUP, key, 0)
        except Exception:
            pass

    def get_window_handles(self):
        """Return a list of all window handles that match the target title."""
        handles = []

        def enum_window_callback(hwnd, _):
            title = win32gui.GetWindowText(hwnd)
            if self.target_window_title.lower() in title.lower() and win32gui.IsWindowVisible(hwnd):
                handles.append((hwnd, title))

        win32gui.EnumWindows(enum_window_callback, None)

        if not handles:
            messagebox.showerror("Error", f"No windows found with title containing '{self.target_window_title}'.")
            return []

        print("[INFO] Matching windows:")
        for hwnd, title in handles:
            print(f" - {title} (HWND: {hwnd})")
        return handles

    def press_m_loop_all(self, hwnd_list):
        while self.is_running and self.drop_mana_enabled.get():
            if self.is_paused:
                time.sleep(0.1)
                continue
            for hwnd, _ in hwnd_list:
                self.send_key_to_window(hwnd, ord('M'))
            time.sleep(self.mana_speed.get())

    def macro_loop(self):
        hwnd_list = self.get_window_handles()
        if not hwnd_list:
            self.stop_macro()
            return

        # Start mana dropper thread for all windows
        if self.drop_mana_enabled.get() and self.mana_thread is None:
            self.mana_thread = Thread(target=self.press_m_loop_all, args=(hwnd_list,), daemon=True)
            self.mana_thread.start()

        while self.is_running:
            if self.is_paused:
                self.status_label.configure(text="Status: Paused", text_color="#eed202")
                time.sleep(0.1)
                continue

            self.status_label.configure(
                text=f"Status: Running ({self.target_window_title})",
                text_color="#f5ce89"
            )

            # Send G to all matching windows
            for hwnd, _ in hwnd_list:
                self.send_key_to_window(hwnd, ord('G'))

            time.sleep(0.5)

            # Handle mana toggle
            if not self.drop_mana_enabled.get() and self.mana_thread is not None:
                self.mana_thread = None

            if self.drop_mana_enabled.get() and self.mana_thread is None:
                self.mana_thread = Thread(target=self.press_m_loop_all, args=(hwnd_list,), daemon=True)
                self.mana_thread.start()

    def start_macro(self):
        self.status_label.configure(text=f"Status: Running ({self.target_window_title})", text_color="#f5ce89")

        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.pause_button.configure(text=f"Pause Macro ({self.keybinds['pause'].upper()})")
            thread = Thread(target=self.macro_loop, daemon=True)
            thread.start()

    def toggle_pause(self):
        if self.is_running:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.status_label.configure(text="Status: Paused", text_color="#eed202")
                self.pause_button.configure(text=f"Resume Macro ({self.keybinds['pause'].upper()})")
            else:
                self.status_label.configure(text=f"Status: Running ({self.target_window_title})", text_color="#f5ce89")
                self.pause_button.configure(text=f"Pause Macro ({self.keybinds['pause'].upper()})")

    def stop_macro(self):
        self.is_running = False
        self.mana_thread = None
        self.status_label.configure(text="Status: Stopped", text_color="#cf142b")
        self.pause_button.configure(text=f"Pause Macro ({self.keybinds['pause'].upper()})")

    def exit_app(self):
        self.stop_macro()
        self.hide_overlay()
        # give keyboard lib a chance to unhook
        try:
            if hasattr(keyboard, "unhook_all_hotkeys"):
                keyboard.unhook_all_hotkeys()
        except:
            pass
        self.root.destroy()

    # =====================================================
    # ===============  SAVE / LOAD  =======================
    # =====================================================
    def save_info(self):
        data = {
            "keybinds": self.keybinds,
            "positions": self.saved_positions
        }
        try:
            with open("info.json", "w") as f:
                json.dump(data, f, indent=2)
            print("[INFO] Saved info:", data)
        except Exception as e:
            print(f"[ERROR] Failed to save info: {e}")

    def load_info(self):
        self.saved_positions = {}
        try:
            if os.path.exists("info.json"):
                with open("info.json", "r") as f:
                    data = json.load(f)

                if all(k in data for k in ("pause", "drop_mana")):
                    self.keybinds = {k: str(v).lower() for k, v in data.items()}
                elif "keybinds" in data:
                    kb = data["keybinds"]
                    if isinstance(kb, str):
                        kb = ast.literal_eval(kb)
                    self.keybinds = {k: str(v).lower() for k, v in kb.items()}
                    if isinstance(data.get("positions"), dict):
                        self.saved_positions = data["positions"]

                print("[INFO] Loaded info:", data)
        except Exception as e:
            print(f"[WARN] Could not load info: {e}")

        # Ensure defaults
        for k, v in {"pause": "q", "drop_mana": "m"}.items():
            if k not in self.keybinds:
                self.keybinds[k] = v

if __name__ == "__main__":
    root = ctk.CTk()
    app = MacroApp(root)
    root.mainloop()
