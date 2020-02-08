import io
import socket
import struct
import threading

import cv2 as cv
import numpy as np
import math
import copy

class PiCV:
    connection = None
    intersects = None
    horlines = None
    vertlines = None
    viewgrid = False

    def __init__(self):
        self.frameworking = False
        pass

    def toggleGrid(self):
        self.viewgrid = not self.viewgrid


    def connect(self, ip):
        server_socket = socket.socket()
        server_socket.bind((ip, 8002))
        server_socket.listen(0)
        print('listening')

        # Accept a single connection and make a file-like object out of it
        self.connection = server_socket.accept()[0].makefile('rb')
        self.frameworking = False


    def getFrame(self, connection):
        while self.frameworking:
            pass

        self.frameworking = True

        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            return
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)

        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        img = cv.imdecode(file_bytes, cv.IMREAD_COLOR)

        self.frameworking = False
        return img


    def TryFindGrid(self):
        found = False
        conn = self.connection
        while not found:
            img = self.getFrame(conn);
            imgcpy = copy.copy(img)

            # make grayscale version
            zwartwit = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # make binary threshold
            tresh = cv.adaptiveThreshold(zwartwit, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 1111, 7)

            # edge detection on the binary threshold
            edges = cv.Canny(tresh, 100, 300)

            # find lines
            lines = cv.HoughLines(edges, 0.55, np.pi / 180, 95)

            hor, vert = self.divideHorizontalVerticalLines(lines)

            hor, vert = self.filterDoubles(hor, vert)

            hor, vert = self.filterHighest(hor, vert)

            self.drawlines(hor, (0, 255, 0), imgcpy)
            self.drawlines(vert, (0, 255, 0), imgcpy)

            # finding all line intersects
            intersects = self.find_intersects(hor, vert)

            self.horlines = hor
            self.vertlines = vert
            self.intersects = intersects

            self.DrawIntersects(imgcpy)

            found = self.CheckLineCount(hor, vert)
            pass

        return imgcpy


    def drawlines(self, lines, color, img):
        if lines is not None:
            for i in range(0, len(lines)):
                cv.line(img, lines[i][0], lines[i][1], color, 3, cv.LINE_AA)


    def divideHorizontalVerticalLines(self, lines):
        linepts = self.getLinePoints(lines)

        hor = []
        vert = []
        for line in linepts:
            if np.abs(line[0][0] - line[1][0]) > np.abs(line[0][1] - line[1][1]):

                hor.append(line)
            else:
                vert.append(line)

        return hor, vert


    def filterDoubles(self, hor, vert):
        newhor = []
        for i in range(0, len(hor)):
            if not any(abs(hor[i][0][1] - h[0][1]) < 30 for h in newhor):
                newhor.append(hor[i])

        newvert = []
        for i in range(0, len(vert)):
            if not any(abs(vert[i][0][0] - h[0][0]) < 30 for h in newvert):
                newvert.append(vert[i])

        return newhor, newvert


    def filterHighest(self, hor, vert):
        returnvert = vert
        returnhor = hor

        if (any(hor)):
            highy = max(hor, key=lambda l: l[0][1])[0][1]
            returnhor = list(filter(lambda l: l[0][1] != highy, hor))

            lowy = min(hor, key=lambda l: l[0][1])[0][1]
            returnhor = list(filter(lambda l: l[0][1] != lowy, returnhor))

        if (any(vert)):
            highx = max(vert, key=lambda l: l[0][0])[0][0]
            returnvert = list(filter(lambda l: l[0][0] != highx, vert))

            lowx = min(vert, key=lambda l: l[0][0])[0][0]
            returnvert = list(filter(lambda l: l[0][0] != lowx, returnvert))

        return returnhor, returnvert


    def getLinePoints(self, lines):
        linepts = []
        for i in range(0, len(lines)):
            # determining line start and end
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            linepts.append((pt1, pt2))
        return linepts

    def find_intersects(self, hor, vert):
        # Looping through all lines

        intersects = []
        for l1 in hor:
            for l2 in vert:
                # loop through all lines and find intersections
                # line intersect point == f(x) = g(x)
                # f(x) = ax + b
                # f(x) = y
                intersects.append(self.get_intersect(l1[0], l1[1], l2[0], l2[1]))

        return intersects

    # https://stackoverflow.com/questions/3252194/numpy-and-line-intersections
    def get_intersect(self, a1, a2, b1, b2):
        """
        Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
        a1: [x, y] a point on the first line
        a2: [x, y] another point on the first line
        b1: [x, y] a point on the second line
        b2: [x, y] another point on the second line
        """
        s = np.vstack([a1, a2, b1, b2])  # s for stacked
        h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
        l1 = np.cross(h[0], h[1])  # get first line
        l2 = np.cross(h[2], h[3])  # get second line
        x, y, z = np.cross(l1, l2)  # point of intersection
        if z == 0:  # lines are parallel
            return (float('inf'), float('inf'))
        return (x / z, y / z)


    def CheckLineCount(self, hor, vert):
        if len(hor) == 9 and len(vert) == 9:
            return True

        return False

    def get_pointgrid(self, intersects, gridsize):
        tlist = list(intersects)

        gridwidth = gridsize[0]
        gridheight = gridsize[1]

        grid = list()

        for i in range(0, gridwidth):
            arr = list()
            for j in range(0, gridheight):
                arr.append(intersects[i + (gridheight * j)])
            arr.sort(key=lambda s: s[1])
            grid.append(arr)

        grid.sort(key= lambda s: s[0][0])

        return grid

    def GetSquare(self, hor, vert):
        frame = self.getFrame(self.connection)
        i = self.get_pointgrid(self.intersects, (9, 9))

        p1 = i[hor][vert]
        p2 = i[hor + 1][vert]
        p3 = i[hor][vert + 1]

        x = int(p1[0])
        y = int(p1[1])
        w = abs(int(p1[0] - p2[0]))
        h = abs(int(p1[1] - p3[1]))

        cutout = frame[y:y+h, x:x+w]

        return cutout, x, y, w, h

    def GetSquareIndices(self, hor, vert):
        i = self.get_pointgrid(self.intersects, (9, 9))

        p1 = i[hor][vert]
        p2 = i[hor + 1][vert]
        p3 = i[hor][vert + 1]

        x = int(p1[0])
        y = int(p1[1])
        w = abs(int(p1[0] - p2[0]))
        h = abs(int(p1[1] - p3[1]))

        return x, y, w, h


    def DrawOverlay(self, img):
        self.OverlayLines(img)
        self.DrawIntersects(img)


    def OverlayLines(self, img):
        self.drawlines(self.horlines, (0, 255, 0), img)
        self.drawlines(self.vertlines, (0, 255, 0), img)


    def DrawIntersects(self, img):
        for i in self.intersects:
            if i[0] != float('inf') or i[1] != float('inf'):
                cv.circle(img, (int(i[0]), int(i[1])), 5, (0, 0, 0))

    def convertPosition(self, input):
        hor = ["a", "b", "c", "d", "e", "f", "g", "h"]
        vert = ["8", "7", "6", "5", "4", "3", "2", "1"]

        horchar = str(input[0])
        vertchar = str(input[1])

        return hor.index(horchar), vert.index(vertchar)



    def GetColor(self, hor, vert):
        imginput = self.getFrame(self.connection)

        x, y, w, h = self.GetSquareIndices(hor, vert)

        blue_low = (50, 50, 50)
        blue_high = (255, 80, 50)
        blue = 255 in cv.inRange(imginput, blue_low, blue_high)[y:y+h, x:x+w]

        red_low = (0, 0, 150)
        red_high = (77, 77, 255)
        red = 255 in cv.inRange(imginput, red_low, red_high)[y:y+h, x:x+w]


        color = 'None'
        if red:
            color = 'Red'
        if blue:
            color = 'Blue'

        return color, x, y, w, h


    def updatePreview(self):
        img = self.getFrame(self.connection)
        self.DrawOverlay(img)
        cv.imshow('preview', img)

    def startLivestream(self):
        self.thread = threading.Thread(target=self.streamframe)
        self.thread.start()

    def streamframe(self):
        cv.namedWindow('Stream', cv.WINDOW_NORMAL)
        cv.resizeWindow('Stream', 950, 950)
        while True:
            frame = self.getFrame(self.connection)

            if self.viewgrid:
                self.DrawOverlay(frame)

            cv.imshow('Stream', frame)
            cv.waitKey(1)
