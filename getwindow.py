import win32gui

def find_windows_by_title(keyword):
    """Return a list of (hwnd, title) for windows containing the keyword."""
    matches = []

    def callback(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        if keyword.lower() in title.lower() and win32gui.IsWindowVisible(hwnd):
            matches.append((hwnd, title))

    win32gui.EnumWindows(callback, None)
    return matches

target_keyword = ""
targets = find_windows_by_title(target_keyword)

if not targets:
    print(f"No windows found for: {target_keyword}")
else:
    print(f"Found {len(targets)} matching windows:")
    for hwnd, title in targets:
        print(f" - {title} (HWND: {hwnd})")
