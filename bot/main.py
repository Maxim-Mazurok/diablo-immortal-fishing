import time
import mss
import numpy as np
import cv2
from analyze_bar import analyze_bar

import pygetwindow as gw
import win32gui

GAME_TITLE = "Diablo Immortal"  # Change this to your window title

def get_window_region(title):
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        raise Exception(f"Window with title '{title}' not found.")
    window = windows[0]
    hwnd = window._hWnd
    # Get client rect (excludes window borders)
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    # Convert client coords to screen coords
    screen_left, screen_top = win32gui.ClientToScreen(hwnd, (left, top))
    screen_right, screen_bottom = win32gui.ClientToScreen(hwnd, (right, bottom))
    width = screen_right - screen_left
    height = screen_bottom - screen_top
    return {
        "top": screen_top,
        "left": screen_left,
        "width": width,
        "height": height
    }

def main():
    # Detect the region of the game window
    monitor_region = get_window_region(GAME_TITLE)

    with mss.mss() as sct:
        while True:
            screenshot = sct.grab(monitor_region)
            img = np.array(screenshot)

            # Remove alpha channel if present
            if img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            analyze_bar(img)
            time.sleep(0.01)  # Limit FPS ~100

if __name__ == "__main__":
    main()
