import cv2 as cv

class StereoCam:

    #Construtor: Instância um objeto de captura e seta as definições de captura.
    def __init__(self):
        self.stereo_cam = cv.VideoCapture(0)
        self.stereo_cam.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        self.stereo_cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480) 


    #Retorna as configurações da câmera(resolução e fps).
    def settings_cam_running(self):
        width = self.stereo_cam.get(cv.CAP_PROP_FRAME_WIDTH)
        height = self.stereo_cam.get(cv.CAP_PROP_FRAME_HEIGHT)
        fps = self.stereo_cam.get(cv.CAP_PROP_FPS)
        print(width, height, fps)


    #Obtém as imagens para calibrar a câmera.
    def getImagesCalibrateCam(self):
        num = 1

        while num != 5:
            status, frame = self.stereo_cam.read()
                
            if not status or cv.waitKey(1) & 0xff == ord('s'):
                cv.imwrite('calibration_images\\two_images\\print' + str(num) + '.png', frame)
                img = cv.imread('calibration_images\\two_images\\print' + str(num) + '.png')
                printL = img[0:480, 0:640]
                printR = img[0:480, 640:1280]
                cv.imwrite("calibration_images\\left_images\\printL" +str(num)+ ".png", printL)
                cv.imwrite("calibration_images\\right_images\\printR" +str(num)+ ".png", printR)
                print('image save')
                num += 1
            

            cv.imshow("Camera", frame)


    def capFrame(self):
        num = 1
        while num != 3:
            succes, frame = self.stereo_cam.read()

            cv.imshow("frame", frame) 

            # Hit "q" to close the window
            if cv.waitKey(1) & 0xFF == ord('q'):
                num = 3
