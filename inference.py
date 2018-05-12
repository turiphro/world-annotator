import time
import os
import mxnet as mx
import numpy as np
import cv2
from collections import namedtuple

DEFAULT_DATA_DIR = '~/data/'


def create(algorithm, data_dir=DEFAULT_DATA_DIR):
    if algorithm == 'dummy':
        return Dummy()
    elif algorithm == 'classify':
        return ResnetImagenet(data_dir=data_dir)


class Dummy():
    def fit(self, img):
        time.sleep(.3)
        return time.ctime()


class ResnetImagenet():
    mod = None

    def __init__(self, data_dir=DEFAULT_DATA_DIR):
        self.data_dir = os.path.expanduser(data_dir)

    def load(self):
        # download
        path = 'http://data.mxnet.io/models/imagenet-11k/'
        print("Downloading Resnet-152")
        mx.test_utils.download(
            path+'resnet-152/resnet-152-symbol.json', dirname=self.data_dir)
        mx.test_utils.download(path+'resnet-152/resnet-152-0000.params', dirname=self.data_dir)
        mx.test_utils.download(path+'synset.txt', dirname=self.data_dir)
        print("Downloaded!")

        # load model
        ctx = mx.cpu()
        fname = os.path.join(self.data_dir, 'resnet-152')
        sym, arg_params, aux_params = mx.model.load_checkpoint(fname, 0)
        self.mod = mx.mod.Module(symbol=sym, context=ctx, label_names=None)
        self.mod.bind(
            for_training=False, data_shapes=[('data', (1, 3, 224, 224))],
            label_shapes=self.mod._label_shapes)
        self.mod.set_params(arg_params, aux_params, allow_missing=True)
        with open(os.path.join(self.data_dir, 'synset.txt'), 'r') as f:
            self.labels = [l.rstrip() for l in f]

    def fit(self, img):
        """Resnet-152 pre-trained on the imagenet dataset

        Based on:
        https://github.com/apache/incubator-mxnet/blob/master/example/image-classification/README.md
        """
        if not self.mod:
            self.load()

        # data formatting
        img_mx = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_mx = cv2.resize(img_mx, (224, 224))
        img_mx = np.swapaxes(img_mx, 0, 2)
        img_mx = np.swapaxes(img_mx, 1, 2)
        img_mx = img_mx[np.newaxis, :]

        # predict
        Batch = namedtuple('Batch', ['data'])
        batch = Batch([mx.nd.array(img_mx)])
        self.mod.forward(batch) # 300ms
        prob = self.mod.get_outputs()[0].asnumpy()
        prob = np.squeeze(prob)
        a = np.argsort(prob)[::-1]

        # format result
        lines = ("{:.2f} {}".format(prob[i], ' '.join(self.labels[i].split()[1:]))
                 for i in a[0:3])
        labels = "\n".join(lines)
        return labels

