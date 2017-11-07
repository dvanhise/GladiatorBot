import random
from settings import MUT_AMOUNT


class Genome(dict):

    def mutate(self, gene):
        self[gene] += random.uniform(-MUT_AMOUNT, MUT_AMOUNT)
        self[gene] = min(1, self[gene])
        self[gene] = max(0, self[gene])

    # Uniform crossover
    def crossover(self, mate):
        for key in self.keys():
            self[key] = random.choice([self[key], mate[key]])

    def power(self, p):
        g = Genome()
        for key in self.keys():
            g[key] = self[key]**p
        return g
