import time, sys
import argparse
import cv2

import inputs


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_type', default='webcam')
    parser.add_argument('-l', '--location', default=0)
    parser.add_argument('-r', '--resolution', nargs=2, type=int)
    parser.add_argument('-f', '--fullscreen', default=False)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    frames = inputs.create(args.input_type,
                           location=args.location,
                           resolution=args.resolution)

    for img in frames:
        if args.fullscreen:
            cv2.namedWindow('stream', cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty('stream', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('stream', img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

