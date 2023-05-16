from threading import Thread
import tkinter
from ga import GA
from queue import Queue


class GaThread(Thread):

    def __init__(self, queue, user_pop_size, user_tournament_size, user_gen, ref_list, n_intervals):
        super().__init__()

        self.n_intervals = n_intervals
        self.ref_list = ref_list
        self.queue = queue
        self.user_pop_size = user_pop_size = 50
        self.user_tournament_size = user_tournament_size = 8
        self.user_gen = user_gen = 5

    def run(self):
        my_ga = GA(self.ref_list, self.n_intervals)
        init_pop = my_ga.create_population(int(self.user_pop_size))
        fitness_list = my_ga.calculate_fitness(init_pop)

        for x in range(self.user_gen):
            crossed_population = my_ga.crossover(fitness_list, init_pop, self.user_tournament_size)
            new_population = my_ga.mutate(0.04, crossed_population)
            fitness_list = my_ga.calculate_fitness(new_population)
            init_pop[:] = [[i for i in j] for j in new_population]

        optimal = new_population[fitness_list.index(max(fitness_list))]
        self.queue.put(optimal)

