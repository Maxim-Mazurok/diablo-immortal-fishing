import time
import mss
import numpy as np
import cv2
from analyze_bar import analyze_bar
import pygetwindow as gw
import win32gui
import keyboard

GAME_TITLE = "Diablo Immortal"  # Change this to your window title

fish_type_on_the_line = "unknown"
fish_type_on_the_line_last_updated = 0
last_start_fishing = 0

def get_window_region(title):
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        raise Exception(f"Window with title '{title}' not found.")
    window = windows[0]
    hwnd = window._hWnd
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
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
    
def start_fishing_if_needed(img):
    crop_top = 684
    crop_left = 1591
    crop_height = 39
    crop_width = 43
    crop = img[crop_top:crop_top+crop_height, crop_left:crop_left+crop_width]
    # Calculate a simple hash sum of pixel colors
    pixel_sum = np.sum(crop)
    # print(f"Pixel color sum for crop: {pixel_sum}")
    
    if pixel_sum == 100859:
        print("Starting fishing: pressing 5")
        time.sleep(1) # Wait a bit before pressing the key to avoid "fighting" and going out of the spot
        keyboard.press_and_release('5')
        time.sleep(1)
        return True
        
    return False

def start_catching(img):
    crop_top = 129
    crop_left = 933
    crop_height = 46
    crop_width = 51
    crop = img[crop_top:crop_top+crop_height, crop_left:crop_left+crop_width]

    # Calculate the sum of pixel values in the crop
    pixel_sum = np.sum(crop)
    # print(f"Pixel color sum for crop: {pixel_sum}")

    # Use the selection data from the screen: top left (858, 81), size 42x32
    crop_top2 = 81
    crop_left2 = 858
    crop_height2 = 32
    crop_width2 = 42
    crop2 = img[crop_top2:crop_top2+crop_height2, crop_left2:crop_left2+crop_width2]
    # Count grey and blue-ish pixels
    # Grey: R,G,B all close (diff < 10), value between 80 and 200
    # Blue-ish: B > 120, B > R+30, B > G+30
    grey_count = 0
    blue_count = 0
    for row in crop2:
        for pixel in row:
            b, g, r = pixel
            if abs(int(r) - int(g)) < 10 and abs(int(r) - int(b)) < 10 and 80 < r < 200:
                grey_count += 1
            # Blue-ish: B > 120, B > R+30, B > G+30
            elif b > 120 and b > r + 20 and b > g + 10:
                blue_count += 1

    # print(f"Grey pixels: {grey_count}, Blue-ish pixels: {blue_count}")

    if 410000 < pixel_sum < 411000 and grey_count > blue_count:
        print("Catching fish: pressing space")
        keyboard.press_and_release('space')

def catch_fish(img):
    global fish_type_on_the_line
    global fish_type_on_the_line_last_updated
    global last_start_fishing
    
    top = 123
    left = 575
    height = 24
    width = 755
    crop = img[top:top+height, left:left+width]
    result = analyze_bar(crop, visualize=False)
    [type, action] = result
    print(f"Action: {action}, Type: {type}")
    
    if type != "unknown":
        fish_type_on_the_line_last_updated = time.time()
        fish_type_on_the_line = type
    
    if fish_type_on_the_line != "mythic":
        if (time.time() - last_start_fishing) < 4*60+30:
            print(f"Detected {fish_type_on_the_line} fish, ignoring...")
            return
        else:
            print(f"Catching whatever, because it's getting late")
    
    print(f"Detected {fish_type_on_the_line} fish, performing action: {action}")
    if action == "click":
        keyboard.press_and_release('space')

def main():
    global fish_type_on_the_line
    global fish_type_on_the_line_last_updated
    global last_start_fishing
    
    with mss.mss() as sct:
        while True:
            monitor_region = get_window_region(GAME_TITLE)
            screenshot = sct.grab(monitor_region)
            img = np.array(screenshot)
            if img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                # Optionally save the screenshot for debugging
                # timestamp = time.strftime("%Y%m%d_%H%M%S")
                # cv2.imwrite(f"debug/debug_screenshot_{timestamp}.png", img)
                
            started_fishing = start_fishing_if_needed(img)
            if started_fishing:
                last_start_fishing = time.time()
                continue
            
            start_catching(img)
            
            catch_fish(img)
            
            if (fish_type_on_the_line_last_updated + 15) < time.time():
                print(f"Fish type on the line is {fish_type_on_the_line}, but it has not been updated for 15 seconds, resetting to unknown.")
                fish_type_on_the_line = "unknown"
                fish_type_on_the_line_last_updated = 0
            
            time.sleep(0.01)

if __name__ == "__main__":
    main()
