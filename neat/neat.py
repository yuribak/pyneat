__author__ = 'yurib'

import random
import networkx as nx
from itertools import product
from commons import WEIGHT, BIAS

class Link(object):

    def __init__(self, in_node, out_node, hmarker, weight=None, enabled=True):
        self.in_node = in_node
        self.out_node = out_node
        self.hmarker = hmarker
        self.weight = weight or random.random()
        self.enabled = enabled

    def __repr__(self):
        return '(%d,%d), hmarker:%d, weight:%.2f, enabled:%s' % (self.in_node,self.out_node,self.hmarker,self.weight,self.enabled)

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

class Node(object):
    def __init__(self, id, hmarker):
        self.id = id
        self.hmarker = hmarker

class Genome(object):

    HMARKER = 0

    @staticmethod
    def hmarker():
        Genome.HMARKER += 1
        return Genome.HMARKER

    def __init__(self, layers, link_prob=0.0):

        # split nodes to layers
        agg_layers = [sum(layers[:i]) for i in range(len(layers)+1)]
        self.layers = [range(agg_layers[i-1], agg_layers[i]) for i in range(1, len(agg_layers))]
        self.nodes = {}

        self.links = {}
        # generate links
        for i, layer in enumerate(self.layers[:-1]):

            higher_nodes = sum(self.layers[i+1:], [])
            for node in layer:

                # at least one link to the next layer to ensure connectivity
                t = random.sample(self.layers[i+1], 1)[0]
                self.add_link(node, t)

                # links to nodes from higher layers with probability link_prob
                for t in higher_nodes:
                    if random.random() < link_prob:
                        self.add_link(node, t)

    def add_link(self,s,t):
        self.links[(s,t)] = Link(s,t,Genome.hmarker())

    def add_random_link(self, hmarker):
        while True:
            sl = random.sample(range(len(self.layers)-1), 1)[0]
            s = random.sample(self.layers[sl], 1)[0]
            t = random.sample(sum(self.layers[sl+1:],[]), 1)[0]
            if (s, t) not in self.links:
                break
        self.add_link(s,t,hmarker)

    def delete_link(self, s, t):
        del self.links[(s,t)]

    def layer_idx_by_node(self,node_id):
        for i, layer in enumerate(self.layers):
            if node_id in layer:
                return i
        raise ValueError('Unknown node id!')

    def add_random_node(self,hmarker):

        # choose link to split
        link = random.sample(self.links.values(), 1)[0]

        # choose layer for new node
        s, t = link.in_node, link.out_node
        s_layer, t_layer = map(self.layer_idx_by_node,[s,t])

        if t_layer - s_layer == 1:
            self.layers.insert(t_layer,[])
            new_node_layer = t_layer
        else:
            new_node_layer = s_layer + 1

        # add new node
        new_node = max(sum(self.layers,[])) + 1
        self.layers[new_node_layer].append(new_node)

        # delete old link and add new ones
        self.delete_link(s,t)
        self.add_link(s,new_node,hmarker)
        self.add_link(new_node,t,hmarker)

    def to_digraph(self):

        g = nx.DiGraph()

        for link in self.links.values():
            g.add_edge(link.in_node,link.out_node, weight=link.weight)

        return g,self.layers[0],self.layers[-1]

    def __repr__(self):
        return 'nodes:%s\nlayers:%s\nlinks: (%d)\n%s' % (self.layers,map(len,self.layers), len(self.links), '\n'.join(str(l) for l in self.links.values()))

def crossover(f,m):
    pass




if __name__ == '__main__':

    g = Genome([2,3,2], link_prob=0)
    print g
    f,ins,outs = g.to_digraph()
    print type(f),ins,outs,f.edges()
