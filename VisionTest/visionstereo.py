import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
imgL = cv.imread('scene1.row3.col1.ppm', cv.IMREAD_GRAYSCALE)
imgR = cv.imread('scene1.row3.col2.ppm', cv.IMREAD_GRAYSCALE)
stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity, 'gray')
plt.show()