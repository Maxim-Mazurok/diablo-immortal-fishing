import cv2
import numpy as np

# rare: 193px between edges of bars
# legendary: 179px
# mythic: 164px

def analyze_bar(img, visualize=False, visualize_to_file=False):
    current_time = cv2.getTickCount()
    timestamp = int(current_time)
    
    # Save image with current time in name
    cv2.imwrite(f"ab/ab_{timestamp}.png", img)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v_channel = hsv[:, :, 2]

    # Step 1: Threshold by brightness to detect filled vs unfilled
    brightness_mask = cv2.inRange(v_channel, 100, 255)

    # Step 2: Find fill boundary by scanning columns
    fill_boundary = None
    dark_streak = 0
    for x in range(brightness_mask.shape[1]):
        column = brightness_mask[:, x]
        filled_ratio = np.count_nonzero(column) / column.shape[0]
        # print(f"Column {x}: Filled ratio = {filled_ratio * 100:.2f}%")
        if filled_ratio < 0.1:  # Threshold for "dark"
            dark_streak += 1
            if dark_streak >= 3:
                fill_boundary = x - 2  # Start of the streak
                break
        else:
            dark_streak = 0
    if fill_boundary is None:
        fill_boundary = brightness_mask.shape[1]  # Fully filled

    # Erase the colored (filled) part of the bar for later color checks
    hsv[:, :fill_boundary, :] = 0
        
    if visualize:
        # Visualize the filled vs non-filled boundary
        vis_img = img.copy()
        cv2.line(vis_img, (fill_boundary, 0), (fill_boundary, vis_img.shape[0]-1), (255, 0, 255), 2)
        if visualize_to_file:
            cv2.imwrite(f"ab/ab_{timestamp}_vis1.png", vis_img)
        else:
            cv2.imshow("Filled Boundary Visualization", vis_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    # Step 3: Color masks
    red1 = cv2.inRange(hsv, np.array([0, 70, 50]), np.array([10, 255, 255]))
    red2 = cv2.inRange(hsv, np.array([160, 70, 50]), np.array([180, 255, 255]))
    red_mask = red1 | red2
    green_mask = cv2.inRange(hsv, np.array([35, 70, 50]), np.array([85, 255, 255]))
    
    if visualize:
        # Visualize red and green masks
        # Create a copy for visualization
        mask_vis = img.copy()
        # Highlight red mask pixels in pure red
        mask_vis[red_mask > 0] = [0, 0, 255]
        # Highlight green mask pixels in pure red as well
        mask_vis[green_mask > 0] = [0, 255, 0]
        if visualize_to_file:
            cv2.imwrite(f"ab/ab_{timestamp}_vis2.png", mask_vis)
        else:
            cv2.imshow("Red & Green Masks Highlighted", mask_vis)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
    # Step 4: Edge detection
    # Define crop parameters
    top = 0
    left = 0
    height = 18
    width = 742
    # Crop: y1:y2, x1:x2
    crop = img[top:top+height, left:left+width]
    # Convert the cropped image to grayscale
    # Increase brightness by 50%
    brighter_crop = cv2.convertScaleAbs(crop, alpha=1.5, beta=0)
    gray_crop = cv2.cvtColor(brighter_crop, cv2.COLOR_BGR2GRAY)
    # Apply maximum contrast: threshold to get only black and white
    _, bw_crop = cv2.threshold(gray_crop, 127, 255, cv2.THRESH_BINARY)

    # Measure distance from left to first black pixel (0)
    left_distance = None
    for x in range(bw_crop.shape[1]):
        column = bw_crop[:, x]
        if np.any(column == 0):
            left_distance = x
            break
    if left_distance is None:
        left_distance = bw_crop.shape[1]

    # Measure distance from right to first white pixel (255)
    right_distance = None
    for x in range(bw_crop.shape[1] - 1, -1, -1):
        column = bw_crop[:, x]
        if np.any(column == 255):
            right_distance = bw_crop.shape[1] - 1 - x
            break
    if right_distance is None:
        right_distance = bw_crop.shape[1]

    if visualize:
        if visualize_to_file:
            cv2.imwrite(f"ab/ab_{timestamp}_bw.png", bw_crop)
        else:
            cv2.imshow("Maximum Contrast (Black & White)", bw_crop)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    width = bw_crop.shape[1] - left_distance - right_distance
    print(f"Left to black: {left_distance}; Right white: {right_distance}; Width: {width}")
    
    type = "unknown"
    if 164-5 < width < 164+5:
        type = "mythic"
    elif 179-5 < width < 179+5:
        type = "legendary"
    elif 194-5 < width < 194+5:
        type = "rare"

    action = "wait"
    if cv2.countNonZero(green_mask) > cv2.countNonZero(red_mask):
        # More green than red - wait
        action = "wait"
    elif cv2.countNonZero(red_mask) > 50:
        action = "click"

    return [type, action]

# # Example use:
# img = cv2.imread("debug-legendary\debug_screenshot_20250624_015347.png")
# #mystic = 164
# #legendary = 179
# #rare = 194

# # Define crop parameters
# top = 123
# left = 575
# height = 24
# width = 755
# # Crop: y1:y2, x1:x2
# crop = img[top:top+height, left:left+width]
# print(analyze_bar(crop, visualize=True, visualize_to_file=True))
