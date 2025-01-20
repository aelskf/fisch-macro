from multiprocessing import Process, Value
import time
from PIL import Image as im
import numpy as np
import pyautogui as pag
import cv2
import mss

size = pag.size()
height = size.height
width = size.width
startx = 438*width // 1470
bar_half_x = 1184*width // (1470 * 16)

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
    with mss.mss() as sct:
        monitor = {"top": (815*height//956), "left": (startx), "width": 592*width // 1470, "height": 45*height//(956*2)}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
        # Grab the data
        sct_img = sct.grab(monitor)
        
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        data = im.fromarray(img)
        #cv2.imshow("Image", img)
        #cv2.waitKey(0)  # Wait for a key press
        #cv2.destroyAllWindows()
        print("returning screenshot")
        return output_bw(img)
        
    #screenshot = pag.screenshot()
    #image = np.array(screenshot)
    #image = image[(1630*height//956):(1675*height//956), (startx*2):(startx*2 +1184*width // 1470)]
    #return output_bw(image)
    
    
    
def find_image_on_screen(template_path, threshold=0.7, where="all", screenshot_gray = None):
    # Take a screenshot and convert to OpenCV format
    if screenshot_gray is None:
        screenshot = pag.screenshot()
        screenshot = np.array(screenshot)  # Convert to NumPy array
        if where == "fishing_minigame":
            screenshot = screenshot[(1630*height//956):(1675*height//956), (startx*2):(startx*2 +1184*width // 1470)]
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
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

def start_scanning(fish_last_seen, held_down, clicking, bar_mid_x, fish_x):
    threshold = 0.6
    fish_last_seen.value = time.time()
    while time.time() - fish_last_seen.value< 1:
        print(time.time() - fish_last_seen.value)
        screenshot = get_fishing_minigame_ss()
        val_at_ss = held_down.value
        
        if val_at_ss: match_right = find_image_on_screen("right.png",threshold, "fishing_minigame", screenshot)
        else:
            match_left = find_image_on_screen("left.png", threshold,"fishing_minigame", screenshot)
        match_fish = find_image_on_screen("fish.png", threshold,"fishing_minigame", screenshot)
        
        
        if val_at_ss and match_right:
            x, y = match_right
            bar_mid_x.value = x - bar_half_x
        if not val_at_ss and match_left:
            x, y = match_left
            bar_mid_x.value = x + bar_half_x
        if match_fish:
            fish_last_seen.value = time.time()
            x, y = match_fish
            fish_x.value = x
        
        if fish_x.value > bar_mid_x.value:
            clicking.value = 0
        else:
            clicking.value = 1
    print(time.time() - fish_last_seen.value)
    print("exiting")
