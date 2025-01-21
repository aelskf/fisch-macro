import tkinter as tk
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
bar_half_x = 1184*width // (1470 * 8)

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
    missed = 0
    prevx, prevy = 0,0
    while missed<5:
        match_coordinates = find_image_on_screen("shake_button.png")
        if match_coordinates:
            currx, curry = match_coordinates
            if not (abs(currx-prevx)<5 and abs(curry-prevy)<5):
                missed = 0
                pag.click(currx//2, curry//2)
                currx = prevx
                curry = prevy
                time.sleep(0.1)
            else:
                missed+=1
        else:
            missed +=1
    #click every time
    playBarMinigame()
    
def playBarMinigame():

    #root = tk.Tk()
    #root.attributes("-alpha", 0.5)
    #root.attributes("-topmost", 1)
    #root.geometry(f"{592}x{30}+{startx}+{840}")
    #canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    #canvas.pack(fill=tk.BOTH, expand=True)
    #root.update()
    #square = None
    #rectangle = None
    
    pag.click(width//2, height//2)
    fish_id = None
    right_id = None
    left_id = None
    bar_id = None
    fish_x = Value("l", 0)
    bar_mid_x = Value("l", 0)
    held_down = Value("h", 0)
    fish_last_seen = Value("d", time.time())
    p = Process(target=start_scanning, args=(fish_last_seen, held_down, bar_mid_x, fish_x))
    p.start()
    while time.time() - fish_last_seen.value < 1:
        
        if abs(fish_x.value - bar_mid_x.value) <= bar_half_x//2:
            held_down.value = 1
            pag.mouseDown()
            pag.sleep(0.045)
            pag.mouseUp()
            held_down.value = 0
            color = "green"
        elif fish_x.value - bar_mid_x.value > bar_half_x * 2:
            held_down.value = 1
            pag.mouseDown()
            color = "red"
        elif fish_x.value - bar_mid_x.value > bar_half_x //2:
            held_down.value = 1
            pag.mouseDown()
            pag.sleep(0.3)
            pag.mouseUp()
            held_down.value = 0
            color = "yellow"
        elif bar_mid_x.value - fish_x.value > bar_half_x * 2:
            pag.mouseUp()
            held_down.value = 0
            color = "red"
        else:
            held_down.value = 1
            pag.mouseDown()
            pag.sleep(0.07)
            pag.mouseUp()
            held_down.value = 0
            color = "yellow"
            pag.sleep(0.23)
            
        #if square:
        #    canvas.delete(square)
        #if rectangle:
        #    canvas.delete(rectangle)
        #rectangle = canvas.create_rectangle((bar_mid_x.value - bar_half_x)//2, 15, (bar_mid_x.value + bar_half_x)//2, 35, fill="blue")
        #square = canvas.create_rectangle(fish_x.value//2-10, 0, fish_x.value//2+10, 15, fill=color)
        #root.update()
        pag.sleep(0.07)
    
    #root.destroy()
    pag.mouseUp()
    p.join()
        

def start_fish():
    pag.mouseDown()
    time.sleep(1.2)
    pag.mouseUp()
    time.sleep(1)
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

