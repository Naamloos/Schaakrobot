import io
import socket
import struct
import cv2 as cv
import numpy as np
import math
import copy
import random


class piececomparer:
    def __init__(self):
        pass


    def detectpiece(self, imginput, x, y):
        #hsv = cv.cvtColor(imginput, cv.COLOR_BGR2HSV)

        blue_low = (50, 50, 50)
        blue_high = (255, 80, 50)
        blue = 255 in cv.inRange(imginput, blue_low, blue_high)

        red_low = (0, 0, 150)
        red_high = (77, 77, 255)
        red = 255 in cv.inRange(imginput, red_low, red_high)

        #cv.imshow('t' + str(x) + "t" + str(y), hsv)

        color = 'None'

        if red:
            color = 'Red'
        if blue:
            color = 'Blue'

        return color

