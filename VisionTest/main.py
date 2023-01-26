from stereo_cam import StereoCam
from pre_processing import PreProcessing

camera = StereoCam()
camera.settings_cam_running()
camera.frames_capture()
pre_processing = PreProcessing()
pre_processing.crop_images()
pre_processing.plot_diparity()