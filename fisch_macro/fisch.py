
import pyautogui as pag
import time
from pynput import mouse
import cv2
import numpy as np
import time
import os
from PIL import Image as im
from multiprocessing import Process, Value

from img_detection import output_bw, find_image_on_screen, get_fishing_minigame_ss, start_scanning

size = pag.size()
height = size.height
width = size.width
startx = 435*width // 1470
bar_half_x = 1184*width // (1470 * 16)

def run(cmd):
    open("stdout.txt", "w").close()
    cmd = cmd.split("\n")[1:-1]
    
    output = "osascript "
    for i in cmd:
        output += " -e '"
        output+=i.lstrip()
        output+="'"
    os.system(output + " > stdout.txt 2> stderr.txt")


def playShakeMinigame():
    match_coordinates = find_image_on_screen("shake_button.png")
    while match_coordinates:
        pag.click(match_coordinates[0]//2, match_coordinates[1]//2)
        time.sleep(0.3)
        match_coordinates = find_image_on_screen("shake_button.png")
    #click every time
    playBarMinigame()
    
def playBarMinigame():

    #root, canvas = create_overlay_box()
    pag.click(width//2, height//2)
    #root.mainloop()
    #print(root, canvas)
    #canvas.create_rectangle(50, 50, 150, 150, fill="blue")
    #root.update()
    fish_id = None
    right_id = None
    left_id = None
    bar_id = None
    fish_x = Value("l", 0)
    bar_mid_x = Value("l", 0)
    clicking = Value("h", 0)
    held_down = Value("h", 0)
    fish_last_seen = Value("d", time.time())
    p = Process(target=start_scanning, args=(fish_last_seen, held_down, clicking, bar_mid_x, fish_x))
    p.start()
    while time.time() - fish_last_seen.value < 1.5:
        print(fish_x.value)
        print(bar_mid_x.value - bar_half_x/2)
        print(time.time() - fish_last_seen.value)
        if fish_x.value > bar_mid_x.value - bar_half_x/2:
            held_down.value = 1
            pag.mouseDown()
            time.sleep(0.05)
            pag.mouseUp()
            held_down.value = 0
            
            print("clicked")
        
        if abs(fish_x.value - bar_mid_x.value) < bar_half_x/2:
            time.sleep(0.2)
        elif fish_x.value - bar_mid_x.value > bar_half_x * 3:
            time.sleep(0.05)
        elif fish_x.value > bar_mid_x.value:
            time.sleep(0.15)
        else:
            time.sleep(0.1)
        
        #root.update()
    pag.mouseUp()
    p.join()
    #root.quit()
    #root.destroy()
        

def start_fish():
    pag.mouseDown()
    time.sleep(1.2)
    pag.mouseUp()
    time.sleep(2)
    playShakeMinigame()



# Coordinates of the white box (x1, y1, x2, y2)


#400, 800
#1000, 900


#create_overlay_box()
#playBarMinigame()
if __name__ == '__main__':
    cmd = """
tell application "System Events" to tell process "Roblox" to set frontmost to true
"""
    run(cmd)
    time.sleep(2)
    
    while True:
        start_fish()

