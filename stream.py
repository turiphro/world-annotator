from picamera.array import PiRGBArray
from picamera import PiCamera
import time, sys
import cv2

RESOLUTION = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) >= 3 else (640, 480)
FULLSCREEN = True

camera = PiCamera()
camera.resolution = RESOLUTION
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=RESOLUTION)

time.sleep(0.1)

# No need for cv2.VideoCapture (which requires more pi drivers)
for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    img = frame.array
    img = cv2.flip(img, -1) # flip both

    if FULLSCREEN:
        cv2.namedWindow('stream', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('stream', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('stream', img)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0) # clear stream for next frame

    if key == ord('q'):
        break


