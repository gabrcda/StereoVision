import cv2 as cv

class StereoCam:

    #Construtor: Instância um objeto de captura e seta as definições de captura.
    def __init__(self):
        self.stereo_cam = cv.VideoCapture(0)
        self.stereo_cam.set(cv.CAP_PROP_FRAME_HEIGHT, 1920.0)
        self.stereo_cam.set(cv.CAP_PROP_FRAME_WIDTH, 1080.0)


    #Retorna as configurações da câmera(resolução e fps).
    def settings_cam_running(self):
        width = self.stereo_cam.get(cv.CAP_PROP_FRAME_WIDTH)
        height = self.stereo_cam.get(cv.CAP_PROP_FRAME_HEIGHT)
        fps = self.stereo_cam.get(cv.CAP_PROP_FPS)
        print(width, height, fps)

    #Implementar calibração da câmera.
    def cam_calibrate():
        pass

    #Inicia uma captura de frames e salva o último frame capturado.
    def frames_capture(self):
        conductor = True

        while conductor:
            status, frame = self.stereo_cam.read()

            if not status or cv.waitKey(1) & 0xff == ord('q'):
                cv.imwrite("frame_captured\\print.png", frame)
                conductor = False
                

            cv.imshow("Camera", frame)