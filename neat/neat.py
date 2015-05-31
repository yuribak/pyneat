__author__ = 'yurib'
import random
from itertools import product
from net.net import NN

class Link(object):

    def __init__(self, in_node, out_node, hmarker, weight=None, enabled=True):
        self.in_node = in_node
        self.out_node = out_node
        self.hmarker = hmarker
        self.weight = weight or random.random()
        self.enabled = enabled

    def __repr__(self):
        return 'in:%d, out:%d, hmarker:%d, weight:%.2f, enabled:%s' % (self.in_node,self.out_node,self.hmarker,self.weight,self.enabled)

    @staticmethod
    def random_links(layers, link_prob=1.0):
        """generate links between nodes of adjacent layers with probability link_prob"""
        assert 0 <= link_prob <= 1
        layer_nodes = [range(sum(layers[:i]), sum(layers[:i]) + layers[i]) for i in range(len(layers))]

        links = []
        for prev,cur in zip(layer_nodes[:-1], layer_nodes[1:]):
            for p,c in product(prev, cur):
                if random.random() < link_prob:
                    # hmarker == 0 ???
                    links.append(Link(p, c, 0))

        return links

class Genome(object):
    def __init__(self, layers, links=None):
        self.layers = layers
        self.links = links or Link.random_links(layers)

    def to_nn(self):
        net = NN(self.layers)
        for link in self.links:
            # TODO: set enabled flag for the link
            (in_layer, in_node), (out_layer, out_node) = map(self._node_id_abs_to_layer_coords,
                                                             [link.in_node, link.out_node])
            net.weight[in_layer][in_node][out_node] = link.weight if link.enabled else 0
        return net

    def _node_id_abs_to_layer_coords(self, n):
        for i,l in enumerate(self.layers):
            if sum(self.layers[:i+1]) > n:
                return i, n - sum(self.layers[:i])
        raise ValueError('node id outside of range')

    def __repr__(self):
        return 'layers:%s\nlinks:%s' % (self.layers, self.links)


if __name__ == '__main__':

    g = Genome([2,3,2])
    print g
    net = g.to_nn()
    print net
