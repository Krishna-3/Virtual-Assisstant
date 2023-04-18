from time import sleep
import hand as h
import pyautogui as pag
import numpy as np
######################################################
frame_width, frame_height = 640, 480
frameR = 100
prevX, prevY = 0, 0
curX, curY = 0, 0
smooth = 2

click_r = False
click_i = False

finger_tips = [4, 8, 12, 16, 20]

screen_width, screen_height = pag.size()

hand = h.HandLandmarks()
######################################################
while True:
    img, hand_list = hand.handDetector(click_i, click_r)
    click_r, click_i = False, False

    if len(hand_list) != 0:
        x1, y1 = hand_list[8][1:]
        x2, y2 = hand_list[12][1:]
        x3, y3 = hand_list[16][1:]
        x4, y4 = hand_list[20][1:]
        x0, y0 = hand_list[0][1:]

        fingers = h.fingerUp(hand_list, finger_tips)

        if len(fingers) == 5:
            if fingers == [0, 1, 1, 1, 0]:
                length = hand.distance(x1, y1, x3, y3)
                if length < 60:
                    pag.scroll(-50)
                    click_r = True
            elif fingers == [0, 1, 1, 0, 0]:
                length = hand.distance(x1, y1, x2, y2)
                if(length < 40):
                    pag.click()
                    click_i = True
                    sleep(0.3)
            elif fingers == [0, 1, 0, 0, 0]:
                cx = np.interp(x1, (frameR, frame_width-frameR),
                               (0, screen_width))
                cy = np.interp(y1, (frameR, frame_height-frameR),
                               (0, screen_height))
                curX = prevX+(cx-prevX)//smooth
                curY = prevY+(cy-prevY)//smooth
                pag.moveTo(curX, curY)
                prevX, prevY = curX, curY
            elif fingers == [1, 1, 1, 1, 1]:
                length = hand.distance(x0, y0, x1, y1)
                if(length < 190):
                    hand.selfie(img)
