# imports
import picv
import cv2 as cv
import piececomparer as pc

comp = pc.piececomparer()

camera = picv.PiCV()
camera.connect('192.168.0.103')

foundgrid = False


# Dit uitvoeren na bewegen naar startpositie
print('Finding grid...')
grid = camera.TryFindGrid()
print('Grid found.')

cv.destroyAllWindows()

for i in range(0,8):
    for j in range(0, 8):
        pion, x, y, w, h = camera.GetSquare(i, j)
        color = comp.detectpiece(pion, i, j)
        if color == 'Red':
            cv.rectangle(grid, (x, y), (x+w, y+h), (0, 0, 255), 3)
        if color == 'Blue':
            cv.rectangle(grid, (x, y), (x+w, y+h), (255, 0, 0), 3)
        # this will loop over every single square

cv.imshow('grid', grid)

cv.waitKey(0)