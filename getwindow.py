import win32gui # pip install pywin32

def list_open_windows():
    def callback(hwnd, windows):
        title = win32gui.GetWindowText(hwnd)
        if title:
            windows.append(title)
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

print("Open windows:")
for window in list_open_windows():
    print(window)
