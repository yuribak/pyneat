__author__ = 'yurib'

import random

def n_point(f,m,n=1):
    """
    :param f: parent 1
    :param m: parent 2
    :param n: points to performs corssover
    :return: 2 children (each with the first segment selected from a different parent)
    """

    assert n <= min(len(f), len(m)) - 1
    f_splits = [0] + sorted(random.sample(xrange(1, len(f)), n)) + [len(f)]
    if len(f) == len(m):
        m_splits = f_splits
    else:
        m_splits = [0] + sorted(random.sample(xrange(1, len(m)), n)) + [len(m)]

    cf,cm = [],[]

    for i in xrange(1,n+2):
        cf += f[f_splits[i-1]:f_splits[i]] if i%2 else m[m_splits[i-1]:m_splits[i]]
        cm += m[m_splits[i-1]:m_splits[i]] if i%2 else f[f_splits[i-1]:f_splits[i]]

    return cf,cm

def n_point_crossover(n, result=0):
    def g(f, m):
        children = n_point(f, m, n)
        return children if result == 'all' else children[result]
    return g

if __name__ == '__main__':
    print n_point('aa','bb')
    print n_point('aaaaaa', 'bbbbbb', 2)
    print n_point('aaaaa','bbb',2)