# imports
import picv
import cv2 as cv

camera = picv.PiCV()

camera.connect()

foundgrid = False


# Dit uitvoeren na bewegen naar startpositie
print('Finding grid...')
grid = camera.TryFindGrid()
print('Grid found.')

cv.destroyAllWindows()
cv.imshow('grid', grid)

for i in range(0, 8):
    for j in range(0, 8):
        ig = camera.GetSquare(i, j)
        cv.imshow(str(i + 1) + "x" + str(j + 1), ig)

#cv.imshow('s', m)

cv.waitKey(0)