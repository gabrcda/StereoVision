import cv2 as cv
from matplotlib import pyplot as plt

class PreProcessing:

    #Separa as imagens capturadas pela lente da esquerda e da direita.
    def crop_images(self, file_path):
        img = cv.imread(file_path)
        printL = img[0:480, 0:640]
        printR = img[0:480, 640:1280]
        cv.imwrite("img_exL.png", printL)
        cv.imwrite("img_exR.png", printR)

    #Calcula e plota a disparidade entre as imagens.
    def plot_diparity(imgL, imgR):
        imgL = cv.imread(imgL, cv.IMREAD_GRAYSCALE)
        imgR = cv.imread(imgR, cv.IMREAD_GRAYSCALE)
        stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
        disparity = stereo.compute(imgL,imgR)
        plt.imshow(disparity)
        plt.show()