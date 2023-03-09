import numpy as np
import cv2
import glob

# Terminar quando pelo menos 9 pontos são encontrados
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
chessboardSize = (8,6)
frameSize = (1280,480)

# Preparar objeto de ponto de referência
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

size_of_chessboard_squares_mm = 25
objp = objp * size_of_chessboard_squares_mm

# Arrays para armazenar pontos do objeto e pontos da imagem
objpoints = [] # pontos 3D na coordenada do objeto
imgpoints_left = [] # pontos 2D na imagem esquerda
imgpoints_right = [] # pontos 2D na imagem direita

images_left = sorted(glob.glob('calibration_images\\left_images\\*.png'))
images_right = sorted(glob.glob('calibration_images\\right_images\\*.png'))

for imgLeft, imgRight in zip(images_left, images_right):
    img_left = cv2.imread(imgLeft)
    img_right = cv2.imread(imgRight)

    gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)

    # Encontrar as coordenadas do tabuleiro de xadrez
    ret_left, corners_left = cv2.findChessboardCorners(gray_left, (8,6), None)
    ret_right, corners_right = cv2.findChessboardCorners(gray_right, (8,6), None)

    # Adicionar pontos de objeto e pontos de imagem se o tabuleiro de xadrez foi encontrado
    if ret_left == True and ret_right == True:
        objpoints.append(objp)

        # Refinar as coordenadas do tabuleiro de xadrez
        corners2_left = cv2.cornerSubPix(gray_left,corners_left, (11,11), (-1,-1), criteria)
        corners2_right = cv2.cornerSubPix(gray_right,corners_right, (11,11), (-1,-1), criteria)
        imgpoints_left.append(corners2_left)
        imgpoints_right.append(corners2_right)

        # Desenhar e exibir as coordenadas do tabuleiro de xadrez na imagem
        img_left = cv2.drawChessboardCorners(img_left, (8,6), corners2_left, ret_left)
        img_right = cv2.drawChessboardCorners(img_right, (8,6), corners2_right, ret_right)
        cv2.imshow("IMG-LEFT", img_left)
        cv2.imshow("IMG-RIGHT", img_right)
        cv2.waitKey(1000)

cv2.destroyAllWindows()


############## CALIBRATION #######################################################

retL, cameraMatrixL, distL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints, imgpoints_left, frameSize, None, None)
heightL, widthL, channelsL = img_left.shape
newCameraMatrixL, roi_L = cv2.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

retR, cameraMatrixR, distR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints, imgpoints_right, frameSize, None, None)
heightR, widthR, channelsR = img_right.shape
newCameraMatrixR, roi_R = cv2.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))

print(cameraMatrixL)
print(newCameraMatrixL)

####################################################################################

########## Stereo Vision Calibration #############################################

flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC

criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv2.stereoCalibrate(objpoints, imgpoints_left, imgpoints_right, newCameraMatrixL, distL, newCameraMatrixR, distR, gray_left.shape[::-1], criteria_stereo, flags)


# Reprojection Error
mean_error = 0

for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecsL[i], tvecsL[i], newCameraMatrixL, distL)
    error = cv2.norm(imgpoints_left[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error


print("total error: {}".format(mean_error/len(objpoints)))


########## Stereo Rectification #################################################

rectifyScale= 1
rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R= cv2.stereoRectify(newCameraMatrixL, distL, newCameraMatrixR, distR, gray_left.shape[::-1], rot, trans, rectifyScale,(0,0))
print(Q)

stereoMapL = cv2.initUndistortRectifyMap(newCameraMatrixL, distL, rectL, projMatrixL, gray_left.shape[::-1], cv2.CV_16SC2)
stereoMapR = cv2.initUndistortRectifyMap(newCameraMatrixR, distR, rectR, projMatrixR, gray_right.shape[::-1], cv2.CV_16SC2)

print("Saving parameters!")
cv_file = cv2.FileStorage('stereoMap.xml', cv2.FILE_STORAGE_WRITE)

cv_file.write('stereoMapL_x',stereoMapL[0])
cv_file.write('stereoMapL_y',stereoMapL[1])
cv_file.write('stereoMapR_x',stereoMapR[0])
cv_file.write('stereoMapR_y',stereoMapR[1])
cv_file.write('q', Q)

cv_file.release()

###################################################################################

############################# UNDISTORT ###########################################

# Camera parameters to undistort and rectify images
cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

frame_left = cv2.imread('calibration_images\\left_images\\printL4.png')
frame_right = cv2.imread('calibration_images\\right_images\\printR4.png')

# Undistort and rectify images
#frame_right = cv2.remap(frame_right, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
#frame_left = cv2.remap(frame_left, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

undistorted_img_left = cv2.undistort(frame_left, cameraMatrixL, distL, None, newCameraMatrixL)
undistorted_img_right = cv2.undistort(frame_right, cameraMatrixR, distR, None, newCameraMatrixR)
                     
# Show the frames
cv2.imwrite("Und_right.png", frame_right) 
cv2.imwrite("Und_left.png", frame_left)

