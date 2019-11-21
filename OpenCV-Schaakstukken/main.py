# imports
import picv
import cv2 as cv

camera = picv.PiCV()

camera.connect()

frame = camera.getFrame()

foundgrid = False

while not foundgrid:
    frame = camera.getFrame()
    cv.imshow('video', frame)
    foundgrid, grid = camera.TryFindGrid(frame)

cv.imshow('grid', grid)

while True:
    cv.imshow('video', frame)
