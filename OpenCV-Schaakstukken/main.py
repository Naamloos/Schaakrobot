# imports
import picv
import cv2 as cv
import piececomparer as pc
import RedOrBlue

comp = pc.piececomparer()
comp.loadshapes()

camera = picv.PiCV()
camera.connect('192.168.0.103')

foundgrid = False


# Dit uitvoeren na bewegen naar startpositie
print('Finding grid...')
grid = camera.TryFindGrid()
print('Grid found.')

cv.destroyAllWindows()

cv.imshow('grid', grid)

for i in range(0,8):
    for j in range(0, 8):
        pion = camera.GetSquare(i, j)
        # this will loop over every single square

cv.waitKey(0)