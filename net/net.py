__author__ = 'yurib'

import networkx as nx
import numpy as np
import random

from scipy.special import expit

from commons import WEIGHT, BIAS




class MatrixNN(object):

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


class Neuron(object):
    sigmoid = expit
    def __init__(self,id,g,activation=sigmoid):
        self.activation = activation
        self.graph = g
        self.output = None
        self.id = id

    def activate(self):

        ins = self.graph.in_edges(self)
        if not ins:
            return
        vs = [s.output for s,_ in ins]
        ws = [self.graph[s][t][WEIGHT] for s,t in ins]
        bs = [self.graph[s][t][BIAS] for s,t in ins]

        self.output = self.activation(sum(v*w+b for v,w,b in zip(vs,ws,bs)))
        return self.output

class NN(object):

    def __init__(self, g, inputs, outputs):

        self.graph = g.copy()

        # map graph nodes to neurons
        nodes = {n:Neuron(n,self.graph) for n in self.graph.nodes()}
        nx.relabel_nodes(self.graph,nodes,copy=False)

        # remember input and output nodes
        self.inputs = [nodes[n] for n in inputs]
        self.outputs = [nodes[n] for n in outputs]

        # assign random weights and bias if they don't exist
        for s,t in self.graph.edges():
            if WEIGHT not in self.graph[s][t]:
                self.graph[s][t][WEIGHT] = random.random()
            if BIAS not in self.graph[s][t]:
                self.graph[s][t][BIAS] = random.random()

    def activate(self,inputs):

        assert len(self.inputs) == len(inputs)

        topo_nodes = nx.topological_sort(self.graph)
        for node, input in zip(self.inputs,inputs):
            node.output = input

        for node in topo_nodes:
            node.activate()

        return [n.output for n in self.outputs]


if __name__ == '__main__':


    g = nx.DiGraph()
    g.add_nodes_from(range(5))
    g.add_edges_from([(0,3),(1,3),(2,4)])
    net = NN(g,[0,1,2],[3,4])

    print net
    print 'output:\n', net.activate([5,1,2])
