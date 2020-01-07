import io
import socket
import struct
import cv2 as cv
import numpy as np
import math
import copy
import random


class piececomparer:
    shapes = {}

    def __init__(self):
        pass


    def loadshapes(self):
        self.shapes['pion'] = cv.imread("Pion.png", cv.IMREAD_GRAYSCALE)
        self.shapes['toren'] = cv.imread("Toren.png", cv.IMREAD_GRAYSCALE)
        self.shapes['paard'] = cv.imread("Paard.png", cv.IMREAD_GRAYSCALE)
        self.shapes['koning'] = cv.imread("Koning.png", cv.IMREAD_GRAYSCALE)
        self.shapes['koningin'] = cv.imread("Koningin.png", cv.IMREAD_GRAYSCALE)
        self.shapes['loper'] = cv.imread("Loper.png", cv.IMREAD_GRAYSCALE)


    def detectpiece(self, imginput):

        gs = cv.cvtColor(imginput, cv.COLOR_BGR2GRAY)
        #rz = cv.resize(gs, (500, 500), interpolation=cv.INTER_CUBIC)
        #img = cv.adaptiveThreshold(gs, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 1111, 4)
        name = str(random.randint(0, 200))
        #cv.imshow(name, rz)
        cv.imwrite("img" + name + ".png", gs)


        shapename = "empty"

        match = None

        # for key in self.shapes:
        #     ret = cv.matchTemplate(img, self.shapes[key], cv.TM_SQDIFF)
        #     if match is None or len(ret) > match:
        #         shapename = key
        #         match = len(ret)

        #res = cv.drawMatches(img, kp1, template, kp2, match[:10], None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        #cv.imshow('test', res)

        #cv.waitKey(0)

        if match is not None:
            return match, shapename
        return None, shapename