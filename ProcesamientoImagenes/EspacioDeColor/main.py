import csv2 as cv 
import numpy as np


cap = cv.VideoCapture(0)

while(1):
    #Take each frame
    _, frame = cap.read()
    
    #Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    #Define range of blue color in HSV
    lower_blue = np.array([50,50,50])
    upper_blue = np.array([130,255,255])

    #THreshold the HSV image to get only blue colors from
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    res = cv.bitwise_and(frame, frame, mask = mask)

    cv.imshow("frame", frame)
    cv.imshow("mask", mask)
    cv.imshow("res", res)
    k = cv.wait_key(5) & 0xff
    if k == 27:
        break

cv.destroyAllWindows()

