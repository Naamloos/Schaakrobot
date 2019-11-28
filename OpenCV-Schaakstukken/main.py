# imports
import picv
import cv2 as cv
import piececomparer as pc

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

pion = camera.GetSquare(1, 1)
match, shapename = comp.detectpiece(pion)

print('1,1 is ' + shapename)

pion = camera.GetSquare(0, 0)
match, shapename = comp.detectpiece(pion)

print('0,0 is ' + shapename)

pion = camera.GetSquare(1, 0)
match, shapename = comp.detectpiece(pion)

print('0,1 is ' + shapename)

# for x in range(0,3):
#     for y in range(0,3):
#         pion = camera.GetSquare(x, y)
#         match, shapename, matchcount = comp.detectpiece(pion)
#         print(str(x) + 'x' + str(y) + 'y: ' + str(matchcount))

cv.waitKey(0)