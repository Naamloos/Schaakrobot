# imports
import picv
import cv2 as cv
import time

camera = picv.PiCV()
camera.connect('192.168.0.103')

# Dit uitvoeren na bewegen naar startpositie
print('Finding grid...')
grid = camera.TryFindGrid()
print('Grid found.')

start_time = time.time()

x, y = camera.convertPosition('a8')
color, x, y, w, h = camera.GetColor(x, y)

for i in range(0,8):
    for j in range(0, 8):
        color, x, y, w, h = camera.GetColor(i, j)
        if color == 'Red':
            cv.rectangle(grid, (x, y), (x+w, y+h), (0, 0, 255), 3)
        if color == 'Blue':
            cv.rectangle(grid, (x, y), (x+w, y+h), (255, 0, 0), 3)
        # this will loop over every single square

cv.imshow('grid', grid)

end_time = time.time()

diff = end_time - start_time

print("execution time in seconds: " + str(diff))

cv.waitKey(0)