# Main application
# Show image stream and annotation

import time, sys
import argparse
import threading
import queue
import cv2

import inputs
import inference


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_type', default='webcam',
                        help='Choose from image, webcam, picamera, video')
    parser.add_argument('-a', '--algorithm', default='dummy')
    parser.add_argument('-l', '--location', default=0)
    parser.add_argument('-r', '--resolution', nargs=2, type=int)
    parser.add_argument('-f', '--fullscreen', default=False)
    parser.add_argument('-d', '--datadir', default='~/data/')
    return parser.parse_args()


annotation = 'testing'


def annotate(q, infer):
    global annotation
    while True:
        img = q.get()
        if img is None:
            break
        annotation = infer.fit(img)
        print('------------')
        print(annotation)
        q.task_done()


def main(args):
    frames = inputs.create(args.input_type,
                           location=args.location,
                           resolution=args.resolution)
    infer = inference.create(args.algorithm,
                             data_dir=args.datadir)

    # Running inference is slow and happens at a lower framerate;
    # hence, we run it in a separate thread and occasionally
    # feed it need images
    # Note: the queue is suboptimal but at least thread-safe
    annotation_queue = queue.Queue()
    annotation_thread = threading.Thread(
        target=annotate, args=(annotation_queue, infer))
    annotation_thread.start()

    if args.fullscreen:
        cv2.namedWindow('stream', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('stream', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    for img in frames:
        if img is not None and not annotation_queue.unfinished_tasks:
            annotation_queue.put(img)

        font = cv2.FONT_HERSHEY_SIMPLEX
        for i, line in enumerate(annotation.split('\n')):
            cv2.putText(img, line, (10, 30+30*i), font, 1, (0, 0, 0), 1)
        cv2.imshow('stream', img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    annotation_queue.put(None)
    #annotation_thread.join()


if __name__ == '__main__':
    args = parse_args()
    main(args)
