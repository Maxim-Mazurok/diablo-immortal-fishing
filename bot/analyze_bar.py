import cv2
import numpy as np

def analyze_bar(img, visualize=False):
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
        print(f"Column {x}: Filled ratio = {filled_ratio * 100:.2f}%")
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
        cv2.imshow("Red & Green Masks Highlighted", mask_vis)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if cv2.countNonZero(green_mask) > cv2.countNonZero(red_mask):
        # More green than red
        return "wait"
    elif cv2.countNonZero(red_mask) > 50:
        return "click"
    else:
        return "wait"

# # Example use:
# img = cv2.imread("test-cases/wait-5.png")
# # Define crop parameters
# top = 123
# left = 575
# height = 24
# width = 755
# # Crop: y1:y2, x1:x2
# crop = img[top:top+height, left:left+width]
# print(analyze_bar(crop))
