import time
import os
import cv2

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except ModuleNotFoundError:
    pass # Silently ignore. Using pycamera will throw errors.


def create(name, location=None, resolution=None):
    if name == 'image':
        return image_stream(location=location)
    elif name == 'video':
        return video_stream(location=str(location))
    elif name == 'webcam':
        return video_stream(location=int(location))
    elif name == 'picamera':
        return picamera_stream(resolution=resolution)
    else:
        raise ValueError("Unknown input type: {}".format(name))


def image_stream(location):
    """Yield a single image indefinitely"""
    if not location:
        raise ValueError("Image stream needs a file location")
    if not os.path.exists(location):
        raise ValueError("Can't find image file: {}".format(location))

    img = cv2.imread(location)
    while True:
        yield img


def video_stream(location=0):
    """Yield frames from a webcam (location as int) or video file (location as str)"""
    if isinstance(location, str) and not os.path.exists(location):
        raise ValueError("Can't find video file: {}".format(location))

    capture = cv2.VideoCapture(location)
    while True:
        ret, frame = capture.read()
        yield frame


def picamera_stream(resolution):
    """Yield frames from a raspberry pi webcam"""
    # No need for cv2.VideoCapture (which requires more pi drivers)
    camera = PiCamera()
    camera.framerate = 32
    camera.resolution = resolution
    rawCapture = PiRGBArray(camera, size=resolution)
    time.sleep(0.1)

    for frame in camera.capture_continuous(
            rawCapture, format='bgr', use_video_port=True):
        img = frame.array
        img = cv2.flip(img, -1) # flip both
        yield img
        rawCapture.truncate(0) # clear stream for next frame

