# imports
import picv
import cv2 as cv
import piececomparer as pc

comp = pc.piececomparer()
comp.loadshapes()

camera = picv.PiCV()
camera.connect()

foundgrid = False


# Dit uitvoeren na bewegen naar startpositie
print('Finding grid...')
grid = camera.TryFindGrid()
print('Grid found.')

cv.destroyAllWindows()

cv.imshow('grid', grid)
cv.waitKey(0)

for i in range(0, 8):
    for j in range(0,8):
        pion = camera.GetSquare(7, 2)
        match, shapename = comp.detectpiece(pion)

        if match:
            print('found: ' + shapename)
        else:
            print('no matches')
        pass