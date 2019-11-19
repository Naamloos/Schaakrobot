# imports
import cv2 as cv
import numpy as np
import math
import copy


# functions
def find_intersects(hor, vert):
    # Looping through all lines

    intersects = []
    for l1 in hor:
        for l2 in vert:
            # loop through all lines and find intersections
            # line intersect point == f(x) = g(x)
            # f(x) = ax + b
            # f(x) = y
            intersects.append(get_intersect(l1[0], l1[1], l2[0], l2[1]))

    for l1 in vert:
        for l2 in hor:
            # loop through all lines and find intersections
            # line intersect point == f(x) = g(x)
            # f(x) = ax + b
            # f(x) = y
            intersects.append(get_intersect(l1[0], l1[1], l2[0], l2[1]))

    return intersects


def get_lines_points(lines):
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


# https://stackoverflow.com/questions/3252194/numpy-and-line-intersections
def get_intersect(a1, a2, b1, b2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return (float('inf'), float('inf'))
    return (x/z, y/z)


def divide_hor_vert(lines):
    linepts = get_lines_points(lines)

    hor = []
    vert = []
    for line in linepts:
            if np.abs(line[0][0] - line[1][0]) > np.abs(line[0][1] - line[1][1]):

                hor.append(line)
            else:
                vert.append(line)

    return hor, vert


def get_pointgrid(intersects, gridsize):
    tlist = list(intersects)
    tlist = list(dict.fromkeys(tlist))
    tlist.sort(key=lambda s: s[0])

    gridwidth = gridsize[0]
    gridheight = gridsize[1]

    grid = list()

    for i in range(0, gridwidth):
        arr = []
        for j in range(0, gridheight):
            arr.append(intersects[i + (gridheight * j)])
        arr.sort(key=lambda s: s[1])
        grid.append(arr)

    return grid


def drawlines(lines, color, img):
    if lines is not None:
        for i in range(0, len(lines)):
            cv.line(img, lines[i][0], lines[i][1], color, 3, cv.LINE_AA)


def filter_highest(hor, vert):
    highy = max(hor, key=lambda l: l[0][1])[0][1]
    returnhor = list(filter(lambda l: l[0][1] != highy, hor))

    lowy = min(hor, key=lambda l: l[0][1])[0][1]
    returnhor = list(filter(lambda l: l[0][1] != lowy, returnhor))

    highx = max(vert, key=lambda l: l[0][0])[0][0]
    returnvert = list(filter(lambda l: l[0][0] != highx, vert))

    lowx = min(vert, key=lambda l: l[0][0])[0][0]
    returnvert = list(filter(lambda l: l[0][0] != lowx, returnvert))

    return returnhor, returnvert


def get_all_blocks_grid(pointgrid, img):
    blocs = []

    #sort
    pointgrid.sort(key=lambda l: l[0][1])
    for i in range(0, len(pointgrid) - 1, 1):
        pointgrid[i].sort(key=lambda l: l[1])

    x = pointgrid[0][0][0]
    xx = pointgrid[1][0][0]
    wh = int(pointgrid[1][0][0] - pointgrid[0][0][0])

    for i in range(0, len(pointgrid) - 1, 1):
        blocrow = []
        for j in range(0, len(pointgrid[i]) - 1, 1):
            x1 = int(pointgrid[i][j][0])
            y1 = int(pointgrid[i][j][1])
            blocrow.append(img[y1:y1+wh, x1:x1+wh])
        blocs.append(blocrow)

    return blocs;


# End functions

# load image and make a copy to draw on
img = cv.imread('schaakbord.jpg')
imgcpy = copy.copy(img)

# make grayscale version
zwartwit = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# make binary threshold
tresh = cv.adaptiveThreshold(zwartwit, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 111, 6)

# edge detection on the binary threshold
edges = cv.Canny(tresh, 100, 800)

# find lines
lines = cv.HoughLines(edges, 0.85, np.pi / 175, 130)

hor, vert = divide_hor_vert(lines)

hor, vert = filter_highest(hor, vert)

# drawing lines
drawlines(hor, (255, 0, 0), imgcpy)
drawlines(vert, (0, 0, 255), imgcpy)

# finding all line intersects
intersects = find_intersects(hor, vert)

for i in intersects:
    if i[0] != float('inf') or i[1] != float('inf'):
        cv.circle(imgcpy, (int(i[0]), int(i[1])), 5, (0,255,0))

# get points in 2 dimensional array
grid = get_pointgrid(intersects, (9,9))

blocks = get_all_blocks_grid(grid, img)

# print all img versions
cv.imshow('Original Image', img)
cv.imshow('Black/White image', zwartwit)
cv.imshow('Threshholded image', tresh)
cv.imshow('Image with edge detection', edges)
cv.imshow('Image with lines filled + dots', imgcpy)

# wait for key press then destroy
cv.waitKey()
cv.destroyAllWindows()
