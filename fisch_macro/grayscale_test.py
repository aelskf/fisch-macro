from PIL import Image as im
import numpy as np
import pyautogui as pag
import cv2
from img_detection import output_bw, find_image_on_screen
size = pag.size()
height = size.height
width = size.width
startx = 435*width // 1470



grayscale_test = np.array(im.open("grayscale_test.png"))
grayscale_test = cv2.cvtColor(grayscale_test, cv2.COLOR_RGB2BGR)
grayscale_test = cv2.cvtColor(grayscale_test, cv2.COLOR_BGR2GRAY)
grayscale_test = output_bw(grayscale_test)
im.fromarray(grayscale_test).save("grayscale_bw.png")

grayscale_test2 = np.array(im.open("grayscale_test2.png"))
grayscale_test2 = cv2.cvtColor(grayscale_test2, cv2.COLOR_RGB2BGR)
grayscale_test2 = cv2.cvtColor(grayscale_test2, cv2.COLOR_BGR2GRAY)
grayscale_test2 = output_bw(grayscale_test2)
im.fromarray(grayscale_test2).save("grayscale2_bw.png")

for_testing_purposes = np.array(im.open("for_testing_purposes.png"))
for_testing_purposes = for_testing_purposes[1630:1675 , 876:2060]
#for_testing_purposes = cv2.cvtColor(for_testing_purposes, cv2.COLOR_RGB2BGR)
#for_testing_purposes = cv2.cvtColor(for_testing_purposes, cv2.COLOR_BGR2GRAY)
for_testing_purposes = output_bw(for_testing_purposes)
im.fromarray(for_testing_purposes).save("testing.png")

for_testing_2 = np.array(im.open("for_testing2.png"))
for_testing_2 = for_testing_2[1630:1675 , 876:2060]
#for_testing_purposes = cv2.cvtColor(for_testing_purposes, cv2.COLOR_RGB2BGR)
#for_testing_purposes = cv2.cvtColor(for_testing_purposes, cv2.COLOR_BGR2GRAY)
for_testing_2 = output_bw(for_testing_2)
im.fromarray(for_testing_2).save("testing2.png")


x, y = find_image_on_screen("left.png", 0.3, screenshot_gray=for_testing_2)
left = cv2.imread("left.png", cv2.IMREAD_UNCHANGED)
print(x, y)
_, w, h = left.shape[::-1]
print(w, h)
#for_testing_purposes2 = cv2.rectangle(for_testing_2, (x-(w//4), y-(h//4)), (x-(w//4), y-(h//4)), [133,0,133], 1)

cv2.rectangle(for_testing_2, (x, y), (x+w, y+h), [0,255,255], 1)

