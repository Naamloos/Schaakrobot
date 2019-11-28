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
        rz = cv.resize(gs, (500, 500), interpolation=cv.INTER_LINEAR)
        img = cv.adaptiveThreshold(rz, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 1111, 2)
        cv.imshow(str(random.randint(0, 200)), img)

        shapename = "empty"

        match = None

        for key in self.shapes:
            template = cv.resize(self.shapes[key], (750, 750))
            ret, thresh = cv.threshold(img, 127, 255, 0)
            ret, thresh2 = cv.threshold(self.shapes[key], 127, 255, 0)
            contours, hierarchy = cv.findContours(thresh, 2, 1)
            cnt1 = contours[0]
            contours, hierarchy = cv.findContours(thresh2, 2, 1)
            cnt2 = contours[0]
            ret = cv.matchShapes(cnt1, cnt2, cv.CONTOURS_MATCH_I2, 0.0)
            if match is None or ret > match:
                shapename = key
                match = ret

        #res = cv.drawMatches(img, kp1, template, kp2, match[:10], None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        #cv.imshow('test', res)

        #cv.waitKey(0)

        if match is not None:
            return match, shapename
        return None, shapename