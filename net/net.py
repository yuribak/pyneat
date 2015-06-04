__author__ = 'yurib'

import numpy as np
from scipy.special import expit

class NN(object):

    def __init__(self, layers, seed=None, zeros=False):

        if seed:
            np.random.seed(seed)

        matrix = np.zeros if zeros else np.random.random
        self.weight = [matrix((ins, outs)) for ins, outs in zip(layers[:-1], layers[1:])]
        self.bias = [matrix((1, cols)) for cols in layers[1:]]
        self.layers = layers

    def activate(self, ins):
        assert len(ins) == self.layers[0]

        outs = self.sigmoid(np.array(ins[:]).reshape((1, self.layers[0])))
        for w, b in zip(self.weight, self.bias):
            outs = self.sigmoid(outs.dot(w) + b)
        return outs

    sigmoid = np.vectorize(expit)

    def __repr__(self):
        return 'layers:\n%s\nweights:\n%s\nbiases:\n%s\n' % (self.layers,self.weight,self.bias)


if __name__ == '__main__':
    net = NN([2, 1])
    print net
    print 'output:\n', net.activate([3, 2])
