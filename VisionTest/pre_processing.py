import cv2 as cv
from matplotlib import pyplot as plt

class PreProcessing:

    #Separa as imagens capturadas pela lente da esquerda e da direita.
    def crop_images(self):
        img = cv.imread("frame_captured\\print.png")
        printL = img[0:480, 0:640]
        printR = img[0:480, 640:1280]
        cv.imwrite("test_images\\printL.png", printL)
        cv.imwrite("test_images\\printR.png", printR)

    #Calcula e plota a disparidade entre as imagens.
    def plot_diparity(self):
        imgL = cv.imread("test_images\\printL.png", cv.IMREAD_GRAYSCALE)
        imgR = cv.imread("test_images\\printR.png", cv.IMREAD_GRAYSCALE)
        stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
        disparity = stereo.compute(imgL,imgR)
        plt.imshow(disparity)
        plt.show()