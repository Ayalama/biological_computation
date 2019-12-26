import random
import operator
import numpy as np

# set default parameters
ELITISM = 0.1
RECOMBINATION_P = 0.7
# mutation should be bigger
MUTATION_P = 0.15
DEFAULT_OBSTACLES = 0


class GeneticAlg:
    Directions = ['U', 'D', 'L', 'R']

    def __init__(self, pop_size, grid_size, src, dst,
                 obstacles_share=DEFAULT_OBSTACLES):
        """
        create the genetic algorithem object with required initializations
        :param pop_size: size of initial population
        :param grid_size: size of 2d grid
        :param src: starting (x,y) position
        :param dst: target (x,y) position
        :param obstacles_share: % of required squares in the grid, can be 0 if no obstacles are in the grid
        """
        self.elitism_cnt = int(pop_size * ELITISM)
        self.grid_size = grid_size
        self.src = src
        self.dst = dst
        self.population_size = pop_size
        self.chromosome_len = int(2.5 * grid_size)
        print("Chromosome length: " + str(self.chromosome_len))

        # initialize a chromosome representation for each instance in the population, in the size of chromosome_len
        self.initial_population = [[random.choice(self.Directions) for i in range(self.chromosome_len)]
                                   for j in range(pop_size)]

        # initialize obstacles on the grid
        self.obstacles_len = int(obstacles_share * (grid_size ** 2))
        self.obstacles = [(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)) for i in
                          range(self.obstacles_len)]

        # make sure src  and dst are'nt an obstacle
        if self.obstacles.count(self.src) > 0:
            self.obstacles.remove(self.src)
        if self.obstacles.count(self.dst) > 0:
            self.obstacles.remove(self.dst)

        print("Random population:")
        print(self.initial_population)
        self.cur_gen_population = self.initial_population[:]
        self.cur_gen_fitness = []
        self.best_fitness = []
        self.worst_fitness = []
        self.average_fitness = []
        self.prev_best_path = []
        self.cur_best_path = []
        self.cur_generation = 0
        self.cur_best_location = src
        self.cur_best_length = 0
        self.cur_worst_location = src
        self.cur_worst_length = 0
        self.best_possible_len = self.l1_distance(src)
        print("Best possible length: " + str(self.best_possible_len))
        self.is_optimal = src == dst
        self.cur_worst_distance = 0
        self.cur_best_distance = 0
        self.update_statistics(self.fitness())

    def l1_distance(self, location):
        """
        return the manhatten distance between input location and the destination
        :param location: input location
        :return: distance between input location and the destination (self.dst)
        """
        return abs(int(location[0]) - self.dst[0]) + abs(int(location[1]) - self.dst[1])

    def make_step(self, position, step):
        obs_panalty = 0
        if step == 'U' and position[0] > 0:
            if self.obstacles.count((position[0] - 1, position[1])) > 0:
                obs_panalty = 5
            else:
                return (position[0] - 1, position[1]), obs_panalty
        if step == 'D' and position[0] < self.grid_size - 1:
            if self.obstacles.count((position[0] + 1, position[1])) > 0:
                obs_panalty = 5
            else:
                return (position[0] + 1, position[1]), obs_panalty
        if step == 'L' and position[1] > 0:
            if self.obstacles.count((position[0], position[1] - 1)) > 0:
                obs_panalty = 5
            else:
                return (position[0], position[1] - 1), obs_panalty
        if step == 'R' and position[1] < self.grid_size - 1:
            if self.obstacles.count((position[0], position[1] + 1)) > 0:
                obs_panalty = 5
            else:
                return (position[0], position[1] + 1), obs_panalty
        return position, obs_panalty

    def calc_chromosom_dst(self, chromosom):
        """
        base on chromosom pate, make all path steps to get it's final destination on the grid
        :param chromosom: representation of the path on the grid
        :return: destination point on the grid and the final path length
        """
        position = self.src
        path_len = 0
        penalty = 0
        for step in chromosom:
            if position == self.dst:
                break

            path_len += 1
            path_len += penalty
            next_step, penalty = self.make_step(position, step)
            if position == next_step:
                path_len -= 1
                path_len += penalty
            position = next_step
        return position, path_len

    def fitness(self):
        """
        calculate the fitness of all chromosoms in the generation, and the summed fitness for the entire generation population
        :return: 
        chromo_dst_tup- fitness for each chromosom
        """
        chromo_dst_tup = []
        for i in range(len(self.cur_gen_population)):
            chromo_dst = self.calc_chromosom_dst(self.cur_gen_population[i])
            print(chromo_dst)
            chromo_dst_tup.append(chromo_dst)

        # fitness is 1/[distance from algo destination + number of steps]
        fitness = [1 / (3*self.l1_distance(chromo_dst[0]) + chromo_dst[1]) for chromo_dst in
                   chromo_dst_tup]
        s = sum(fitness)
        self.cur_gen_fitness = [f / s for f in fitness]

        return chromo_dst_tup

    def get_path(self, directions):
        cur = self.src
        path = []
        for direction in directions:
            next_step, penalty = self.make_step(cur, direction)
            path.append(next_step)
            if next_step == self.dst:
                break
            cur = next_step
        return path

    def update_statistics(self, chromopath_dest_len):
        """
        updated required statistics regarding current generation, given each chromosome destination and path length.
        :param chromopath_dest_len:
        :return:
        """
        best_fitness_idx = np.argmax(self.cur_gen_fitness)
        worst_fitness_idx = np.argmin(self.cur_gen_fitness)

        self.best_fitness.append(self.cur_gen_fitness[best_fitness_idx])
        self.worst_fitness.append(self.cur_gen_fitness[worst_fitness_idx])
        self.average_fitness.append(np.mean(self.cur_gen_fitness))

        if chromopath_dest_len is not None:
            self.cur_best_location = chromopath_dest_len[best_fitness_idx][0]
            self.cur_best_length = chromopath_dest_len[best_fitness_idx][1]

            self.cur_worst_location = chromopath_dest_len[worst_fitness_idx][0]
            self.cur_worst_length = chromopath_dest_len[worst_fitness_idx][1]

            self.cur_best_distance = self.l1_distance(chromopath_dest_len[best_fitness_idx][0])
            self.cur_worst_distance = self.l1_distance(chromopath_dest_len[worst_fitness_idx][0])

        self.prev_best_path = self.cur_best_path[:]
        self.cur_best_path = self.get_path(self.cur_gen_population[best_fitness_idx])
        self.is_optimal = self.cur_best_location == self.dst and self.cur_best_length <= self.best_possible_len

    def generate_chromosome(self, cur_gen_probability):
        """
        create new generation chromosome based on 2 parants selection from previous generation population.
        parants are selected based on given probabilities.
        :param cur_gen_probability:
        :return: new generation son that is a combination of 2 parants, or a copy of one of them
        """
        parent_index1, parent_index2 = np.random.choice(self.population_size, 2, p=cur_gen_probability)
        parent1, parent2 = self.cur_gen_population[parent_index1], self.cur_gen_population[parent_index2]

        # create combined sons in probability RECOMBINATION_P, or reproduce parants in probability 1 - RECOMBINATION_P
        should_recombine = np.random.choice([True, False], 1,
                                            p=[RECOMBINATION_P, 1 - RECOMBINATION_P])
        if should_recombine:
            cutidx=random.randint(0, self.chromosome_len - 1)
            son1 = parent1[:cutidx]
            son1.extend(parent2[cutidx:])
            son2 = parent2[:cutidx]
            son2.extend(parent1[cutidx:])
        else:
            son1, son2 = parent1, parent2
        son_index = np.random.choice(2)
        return son1 if son_index == 1 else son2

    def mutate_chromosome(self, chromosome):
        """
        for each cell in the chromozon, make a selection if to mutaste it in MUTATION_P probability.
        if mutation is required, and new direction value will be randomly selected for this cell
        :param chromosome:
        :return:
        """
        mutated_chromosome = chromosome[:]
        should_mutate_chromosome = np.random.choice([True, False], self.chromosome_len,
                                                    p=[MUTATION_P, 1 - MUTATION_P])
        for i in range(self.chromosome_len):
            if should_mutate_chromosome[i]:
                mutated_chromosome[i] = random.choice(self.Directions)
        return mutated_chromosome

    def new_generation(self):
        """
        initiate the selection process and creation of a new generation.
        select population for next generation based on elitism_cnt parameter defined in the initialization.
        take top previous generation chromosomes that are with the highest fitness value.
        to generate a generation that is with equal size to population_size we use mutation.
        
        :return: 
        """
        self.cur_generation += 1
        elitism = zip(self.cur_gen_fitness[:], self.cur_gen_population[:])
        ig = operator.itemgetter(0)
        elitism = sorted(elitism, key=ig, reverse=True)
        next_gen_population = [zipped_item[1] for zipped_item in elitism[0:self.elitism_cnt]]

        # mutate new chromosomes to next generation population
        while len(next_gen_population) < self.population_size:
            chromosome = self.generate_chromosome(self.cur_gen_fitness)
            chromosome = self.mutate_chromosome(chromosome)
            next_gen_population.append(chromosome)

        self.cur_gen_population = next_gen_population
        self.update_statistics(self.fitness())
