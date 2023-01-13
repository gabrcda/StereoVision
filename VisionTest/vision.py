import cv2 as cv

camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_FRAME_HEIGHT, 1920.0)
camera.set(cv.CAP_PROP_FRAME_WIDTH, 1080.0)
width = camera.get(cv.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv.CAP_PROP_FRAME_HEIGHT)
fps = camera.get(cv.CAP_PROP_FPS)
print(width, height, fps)
rodando = True

while rodando:

    status, frame = camera.read()

    if not status or cv.waitKey(1) & 0xff == ord('q'):
        rodando = False

    cv.imshow("Camera", frame)