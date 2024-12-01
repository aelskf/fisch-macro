
import pyautogui as pag
import time
from pynput import mouse
import cv2
import numpy as np
import time
import tkinter as tk
import os
from PIL import Image as im


from img_detection import output_bw, find_image_on_screen, get_fishing_minigame_ss

size = pag.size()
height = size.height
width = size.width
startx = 435*width // 1470
bar_half_x = 1184*width // (1470 * 8)
def create_overlay_box():
    root = tk.Tk()
    root.title("Tkinter Overlay with Box")
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.7)
    root.configure(bg='white')

    # Set window size to screen size
    root.geometry(f"{600* width // 1470}x{50*height//956}+{startx}+{840*height//956}")
    #root.geometry(f"{width}x{height}+0+0")
    canvas = tk.Canvas(root, bg='white', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    #root.mainloop()
    root.update()
    return root, canvas


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
    threshold = 0.6
    fish_x = 0
    bar_mid_x = 0
    held_down = False
    
    fish_last_seen = time.time()
    while time.time() - fish_last_seen < 1:
        
        screenshot = get_fishing_minigame_ss()
        
        if held_down: match_right = find_image_on_screen("right.png",threshold, "fishing_minigame", screenshot)
        match_fish = find_image_on_screen("fish.png", threshold,"fishing_minigame", screenshot)
        if not held_down: match_left = find_image_on_screen("left.png", threshold,"fishing_minigame", screenshot)
        print(time.time() - fish_last_seen)
        #if fish_id:
        #    canvas.delete(fish_id)
        #    fish_id = None
        #if left_id:
        #    canvas.delete(left_id)
        #    left_id = None
        #if right_id:
        #    canvas.delete(right_id)
        #    right_id = None
        #if bar_id:
        #    canvas.delete(bar_id)
        
        if held_down and match_right:
            x, y = match_right
            bar_mid_x = x - bar_half_x
            #right_id = canvas.create_rectangle(x//2-10, 0, x//2+10, 20, fill="blue")
            
        if not held_down and match_left:
            x, y = match_left
            bar_mid_x = x + bar_half_x
            #left_id = canvas.create_rectangle(x//2-10, 0, x//2+10, 20, fill="red")
        if match_fish:
            fish_last_seen = time.time()
            x, y = match_fish
            fish_x = x
            #fish_id = canvas.create_rectangle(x//2-10, 0, x//2+10, 20, fill="green")
        #bar_id = canvas.create_rectangle((bar_mid_x -bar_half_x )// 2, 20, (bar_mid_x + bar_half_x) // 2, 40, fill="black")
        if bar_mid_x - bar_half_x//2<fish_x < bar_mid_x + bar_half_x//2:
            pag.mouseUp()
            for i in range(5):
                pag.click()
                time.sleep(0.1)
            held_down = False
        elif fish_x > bar_mid_x:
            held_down = True
            pag.mouseDown()
        else:
            held_down = False
            pag.mouseUp()
        
        #root.update()
    pag.mouseUp()
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

cmd = """
tell application "System Events" to tell process "Roblox" to set frontmost to true
"""
run(cmd)
time.sleep(2)
#create_overlay_box()
#playBarMinigame()
while True:
    start_fish()

