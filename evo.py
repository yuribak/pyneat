__author__ = 'yuri'

from operator import itemgetter
import random
import string
from itertools import starmap

class Evo(object):
    def __init__(self, generator, pop_size, fitness, crossover, mutator):

        self.crossover = crossover
        self.fitness = fitness
        self.mutator = mutator
        self.generator = generator

        self.population = [generator() for _ in range(pop_size)]
        self.population = self.evaluate(self.population)

    def evaluate(self, inds):
        fitness = map(self.fitness, inds)
        return sorted(zip(inds, fitness), key=itemgetter(1), reverse=True)

    def select(self, inds_fits):
        tournament_size = 5
        fathers = [max(random.sample(inds_fits, tournament_size), key=itemgetter(1))[0] for _ in range(len(inds_fits))]
        mothers = [max(random.sample(inds_fits, tournament_size), key=itemgetter(1))[0] for _ in range(len(inds_fits))]
        return zip(fathers,mothers)

    def mutate(self, inds):
        mutation_probability = 0.0
        return [self.mutator(i) if random.random() < mutation_probability else i for i in inds]

    def step(self):
        parents = self.select(self.population)
        offsprings = starmap(self.crossover, parents)
        self.population = self.mutate(offsprings)
        self.population = self.evaluate(self.population)


def random_string():
    return random.sample(string.ascii_lowercase+' ', 20)

def fitness(s):
    target = 'the grey fox wooopty'
    return sum(x == y for x, y in zip(s, target))/float(len(target))

def crossover(f,m):
    r = random.randint(0, len(f))
    c = f[:r]+m[r:]
    return c

def mutator(s):
    r = random.randint(0,len(s)-1)
    temp = s[0]
    s[0] = s[r]
    s[r] = temp
    return s

if __name__ == '__main__':
    evo = Evo(random_string, 2000, fitness, crossover, mutator)

    gens = 1000
    g = gens
    while True:
        best, f = evo.population[0]
        print gens-g, ''.join(best), f
        if f < 1 and g:
            evo.step()
            g -= 1
        else:
            break



