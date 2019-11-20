import io
import socket
import struct
import cv2 as cv
import numpy as np
import math
import copy

class PiCV:
    connection = None

    def __init__(self):
        pass


    def connect(self):
        server_socket = socket.socket()
        server_socket.bind(('192.168.0.100', 8002))
        server_socket.listen(0)
        print('listening')

        # Accept a single connection and make a file-like object out of it
        self.connection = server_socket.accept()[0].makefile('rb')


    def getFrame(self):
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            return None
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(self.connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)

        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        img = cv.imdecode(file_bytes, cv.IMREAD_COLOR)

        return img


    def TryFindGrid(self, img):
        imgcpy = copy.copy(img)

        # make grayscale version
        zwartwit = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # make binary threshold
        tresh = cv.adaptiveThreshold(zwartwit, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 111, 6)

        # edge detection on the binary threshold
        edges = cv.Canny(tresh, 100, 800)

        # find lines
        lines = cv.HoughLines(edges, 0.55, np.pi / 175, 75)

        hor, vert = self.divideHorizontalVerticalLines(lines)

        hor, vert = self.filterDoubles(hor, vert)

        hor, vert = self.filterHighest(hor, vert)

        self.drawlines(hor, (255, 0, 0), imgcpy)
        self.drawlines(vert, (0, 0, 255), imgcpy)

        # finding all line intersects
        intersects = self.find_intersects(hor, vert)

        for i in intersects:
            if i[0] != float('inf') or i[1] != float('inf'):
                cv.circle(imgcpy, (int(i[0]), int(i[1])), 5, (0, 255, 0))

        return self.CheckLineCount(hor, vert, imgcpy), imgcpy


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

        for l1 in vert:
            for l2 in hor:
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


    def CheckLineCount(self, hor, vert, img):
        if len(hor) == 9 and len(vert) == 9:
            return True

        return False
