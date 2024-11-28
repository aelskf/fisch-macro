
from PIL import Image as im
import numpy as np
import pyautogui as pag
import cv2


size = pag.size()
height = size.height
width = size.width
startx = 438*width // 1470


def output_bw(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    for a in range(len(image)):
        for b in range(len(image[a])):
            if 125<=image[a][b]<=140 or 70<=image[a][b]<=80:
                image[a][b] = 0
            else:
                image[a][b] = 255
    return image
    
def get_fishing_minigame_ss():
    screenshot = pag.screenshot()
    image = np.array(screenshot)
    image = image[(1630*height//956):(1675*height//956), (startx*2):(startx*2 +1184*width // 1470)]
    return output_bw(image)
def find_image_on_screen(template_path, threshold=0.7, where="all", screenshot_gray = None):
    # Take a screenshot and convert to OpenCV format
    if screenshot_gray is None:
        screenshot = pag.screenshot()
        screenshot = np.array(screenshot)  # Convert to NumPy array
        if where == "fishing_minigame":
            screenshot = screenshot[(1630*height//956):(1675*height//956), (startx*2):(startx*2 +1184*width // 1470)]
            
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # Convert to BGR

        # Load the template image
        

        # Ensure both images are grayscale
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) if len(template.shape) == 3 else template
    
    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Check if match meets the threshold
    if max_val >= threshold:
        match_x, match_y = max_loc
        center_x = match_x + template.shape[1] // 2
        center_y = match_y + template.shape[0] // 2
        #if where == "fishing_minigame": im.fromarray(screenshot).save("testing.png")
        return (center_x, center_y)
    else:
        return False
