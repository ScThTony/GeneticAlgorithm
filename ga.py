import itertools
import random
import xmlrpc.server

import unit
import tkinter.messagebox
from typing import *
import statistics


class GA:

    def __init__(self, ref_list: list[unit], int__num: int):
        self.ref_list = ref_list
        self.unit_num = len(self.ref_list)
        self.int_num = int__num
        self.ref_pool = [[] for i in range(self.unit_num)]
        self.create_pool()

    def create_pool(self):
        for i, station in enumerate(self.ref_list):
            indices_of_ones = tuple(itertools.combinations(list(range(self.int_num)), station.required_int))
            for pos in indices_of_ones:
                self.ref_pool[i].append(''.join(['1' if x in pos else '0' for x in range(self.int_num)]))

    def random_chromosome(self):
        chromo = []
        for i in range(self.unit_num):
            chromo.append(random.sample(self.ref_pool[i], 1)[0])
        return chromo

    def create_population(self, size: int) -> List[List[str]]:
        return [self.random_chromosome() for x in range(size)]

    def calculate_fitness(self, pop: List[List[str]]) -> List[float]:
        installed_capacity = sum([x.capacity for x in self.ref_list])
        pop_fitness = []
        list_total_available = []
        for chrom in pop:
            list_total_available.clear()
            for int_sched in zip(*chrom):
                total_down_per_interval = 0
                for u, unit_m in enumerate(int_sched):
                    if unit_m == '1':
                        total_down_per_interval += self.ref_list[u].capacity
                list_total_available.append(installed_capacity - total_down_per_interval)
            score = round(float(max(list_total_available)) / statistics.pstdev(list_total_available) * 100, 4)
            pop_fitness.append(score)
        return pop_fitness

    # returns the index of tournament winner.
    # Don't need to operate on actualy population. Just the fitness values and their indices suffice.
    # ensures only 1 unique winner
    def tournament(self, pop_fitness: List[float], tournament_size: int):
        tour = []
        while len(tour) < tournament_size:
            tour.append(random.sample(pop_fitness, 1)[0])
        return tour.index(max(tour))

    def crossover(self, fitness_pop: List[float], current_pop, tournament_size: int):
        cross_pop = []
        while len(cross_pop) < len(fitness_pop):
            pa_index1 = self.tournament(fitness_pop, tournament_size)
            pa_index2 = self.tournament(fitness_pop, tournament_size)
            parent1, parent2 = current_pop[pa_index1], current_pop[pa_index2]  # selected 2 parents to reproduce)
            point = random.randrange(len(parent1))
            if point == 0 or point == len(parent1) - 1:
                cross_pop.extend([parent1, parent2])
            else:
                child1 = parent1[:point + 1] + parent2[point + 1:]
                child2 = parent2[:point + 1] + parent1[point + 1:]
                cross_pop.extend([child1, child2])

        if len(cross_pop) - len(fitness_pop) == 1:
            del cross_pop[-1]

        return cross_pop

    def mutate(self, mu_rate: float, current_pop: List[List[str]]):

        for ind, c in enumerate(current_pop):
            if random.uniform(0, 1) < mu_rate:
                rand_index = random.randrange(self.unit_num)
                # Will not cause index error. Python will handle rand_index + 1 in a slice
                c[rand_index] = random.sample([i for i in self.ref_pool[rand_index] if i != c[rand_index]], 1)[0]
        return current_pop
