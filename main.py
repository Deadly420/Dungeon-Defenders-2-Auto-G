# import pydirectinput
# import keyboard
# import time
#
# while True:
#     if keyboard.is_pressed("esc"):
#         print("Macro stopped.")
#         break
#
#     # # Press keys down
#     pydirectinput.keyDown("w")
#     pydirectinput.keyDown("a")
#     pydirectinput.keyDown("s")
#     pydirectinput.keyDown("d")
#
#     # Release keys
#     pydirectinput.keyUp("w")
#     pydirectinput.keyUp("a")
#     pydirectinput.keyUp("s")
#     pydirectinput.keyUp("d")

# import pyautogui
# import keyboard
# import time
#
# print("Move your mouse to the desired position and press ESC to stop...")
#
# while True:
#     x, y = pyautogui.position()
#     print(f"X: {x} | Y: {y}", end="\r")
#     time.sleep(0.05)
#
#     if keyboard.is_pressed("esc"):
#         print(f"\nFinal position: ({x}, {y})")
#         break

import time
import win32gui
import win32con
import win32api

import customtkinter as ctk
from tkinter import messagebox
from threading import Thread

class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Macro Controller")
        self.root.geometry("400x420")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.is_running = False
        self.is_paused = False
        self.target_window_title = "Dungeon Defenders 2"

        # Settings
        self.drop_mana_enabled = ctk.BooleanVar(value=True)   # toggle for M
        self.mana_speed = ctk.DoubleVar(value=0.05)           # delay between M presses (seconds)

        # Threads
        self.mana_thread = None

        # UI Components
        self.status_label = ctk.CTkLabel(root, text="Status: Stopped", font=("Segoe UI Semibold", 16))
        self.status_label.pack(pady=20)

        self.start_button = ctk.CTkButton(root, text="Start Macro", command=self.start_macro, font=("Arial", 14), width=200)
        self.start_button.pack(pady=10)

        self.pause_button = ctk.CTkButton(root, text="Pause Macro", command=self.toggle_pause, font=("Arial", 14), width=200)
        self.pause_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(root, text="Stop Macro", command=self.stop_macro, font=("Arial", 14), width=200)
        self.stop_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(root, text="Exit", command=self.exit_app, font=("Arial", 14), width=200)
        self.exit_button.pack(pady=10)

        self.title_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.title_frame.pack(pady=15)

        self.title_window_label = ctk.CTkLabel(self.title_frame,text="🎯 Target Window Title:",font=("Segoe UI Semibold", 16))
        self.title_window_label.pack(pady=(0, 5))

        self.title_var = ctk.StringVar(value=self.target_window_title)
        self.title_window = ctk.CTkEntry(self.title_frame, textvariable=self.title_var, font=("Segoe UI", 14), height=36, width=200, corner_radius=10, justify="center")
        self.title_window.pack()

        self.title_var.trace_add("write", self.update_target_window_title)

        # Settings UI
        self.drop_mana_check = ctk.CTkCheckBox(root, text="Drop Mana (M)", variable=self.drop_mana_enabled)
        self.drop_mana_check.pack(pady=10)

        # Keyboard Listener for Q key (pause/resume)
        self.root.bind("<KeyPress-q>", lambda _: self.toggle_pause())

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

    def get_window_handle(self):
        hwnd = win32gui.FindWindow(None, self.target_window_title)
        if hwnd:
            return hwnd
        else:
            messagebox.showerror("Error", f"Window titled '{self.target_window_title}' not found.")
            return None

    def press_m_loop(self, hwnd):
        """Dedicated mana dropper loop"""
        while self.is_running and self.drop_mana_enabled.get():
            if self.is_paused:
                time.sleep(0.1)
                continue
            self.send_key_to_window(hwnd, ord('M'))
            time.sleep(self.mana_speed.get())

    def macro_loop(self):
        hwnd = self.get_window_handle()
        if not hwnd:
            self.stop_macro()
            return

        # Start mana spam thread once
        if self.drop_mana_enabled.get() and self.mana_thread is None:
            self.mana_thread = Thread(target=self.press_m_loop, args=(hwnd,), daemon=True)
            self.mana_thread.start()

        while self.is_running:
            if self.is_paused:
                self.status_label.configure(text="Status: Paused", text_color="#eed202")
                time.sleep(0.1)
                continue

            self.status_label.configure(text=f"Status: Running ({self.target_window_title})", text_color="#f5ce89")

            # Always press G
            self.send_key_to_window(hwnd, ord('G'))
            time.sleep(0.5)

            # If mana checkbox gets unchecked mid-run, stop mana thread
            if not self.drop_mana_enabled.get() and self.mana_thread is not None:
                self.mana_thread = None

            # If mana is re-enabled and no thread exists, restart it
            if self.drop_mana_enabled.get() and self.mana_thread is None:
                self.mana_thread = Thread(target=self.press_m_loop, args=(hwnd,), daemon=True)
                self.mana_thread.start()

    def start_macro(self):
        print(f"✅ Starting macro for: {''.join(self.target_window_title)}")
        self.status_label.configure(text=f"Status: Running ({self.target_window_title})", text_color="#f5ce89")

        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.is_running = True
            self.status_label.configure(text=f"Status: Running ({self.target_window_title})", text_color="#f5ce89")
            self.pause_button.configure(text="Pause Macro")
            thread = Thread(target=self.macro_loop, daemon=True)
            thread.start()

    def toggle_pause(self):
        if self.is_running:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.status_label.configure(text="Status: Paused", text_color="#eed202")
                self.pause_button.configure(text="Resume Macro")
            else:
                self.status_label.configure(text=f"Status: Running ({self.target_window_title})", text_color="#f5ce89")
                self.pause_button.configure(text="Pause Macro")

    def stop_macro(self):
        self.is_running = False
        self.mana_thread = None
        self.status_label.configure(text="Status: Stopped", text_color="#cf142b")
        self.pause_button.configure(text="Pause Macro")

    def exit_app(self):
        self.stop_macro()
        self.root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = MacroApp(root)
    root.mainloop()
