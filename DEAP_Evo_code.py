import numpy as np
import random
import copy

from deap import base
from deap import creator
from deap import tools

"""
This is for testing 2a) - 2d) 
p1 = np.random.randint(2, size=68)

p2 = np.random.randint(2, size=68)

p3 = np.random.randint(2, size=68)

"""
game_matrix = [[[8, 8, 8], [6, 6, 7], [6, 7, 6], [5, 9, 9]],
               [[7, 6, 6], [9, 5, 9], [9, 9, 5], [0, 0, 0]]]

# 2a)


def payoff_to_ind1(individual1, individual2, individual3, game):
    if(len(individual1) == (len(individual2) and len(individual3))):
        payoff = []

        for i in range(len(individual1)):
            if individual1[i] == 0:
                if individual2[i] == 1 and individual3[i] == 1:
                    payoff.append(game[1][0][0])
                if individual2[i] == 1 and individual3[i] == 0:
                    payoff.append(game[1][1][0])
                if individual2[i] == 0 and individual3[i] == 1:
                    payoff.append(game[1][2][0])
                if individual2[i] == 0 and individual3[i] == 0:
                    payoff.append(game[1][3][0])

            if individual1[i] == 1:
                if individual2[i] == 1 and individual3[i] == 1:
                    payoff.append(game[0][0][0])
                if individual2[i] == 1 and individual3[i] == 0:
                    payoff.append(game[0][1][0])
                if individual2[i] == 0 and individual3[i] == 1:
                    payoff.append(game[0][2][0])
                if individual2[i] == 0 and individual3[i] == 0:
                    payoff.append(game[0][3][0])

    # Assuming mem_depth of 2, return the sum of the 2 games
    return sum(payoff[-2:])


# 2b)
def move_by_ind1(individual1, individual2, individual3, round):
    memory_depth = 2

    # Error checking
    if round < 0:
        print(f'ERROR: Round is less than 0. Must be > 0.')
        return []

    # Run default move if round is less than 2
    if round < 2:
        return individual1[len(individual1) - (2*memory_depth) + round]
    else:
        bit_list = []
        # Appending the first game
        bit_list.append(individual1[-2])
        bit_list.append(individual2[-2])
        bit_list.append(individual3[-2])

        # Appending the second game
        bit_list.append(individual1[-1])
        bit_list.append(individual2[-1])
        bit_list.append(individual3[-1])

        # Converting bits to binary string
        output = [str(x) for x in bit_list]
        binary = ''.join(output)
        # Convert to decimal
        decNo = int(binary, 2)

        # Use the decimal to find the move in the array
        return individual1[decNo]

# 2c)


def process_move(individual, move, m_depth):
    # Creating a copy of individual for later checking
    ind_temp = []

    for i in individual:
        ind_temp.append(i)

    # Grabbing the index of the oldest game, roughly 67th bit
    first_memBit_idx = len(individual) - m_depth

    # Removing the old game and push new game in the now empty 68th bit
    individual.pop(first_memBit_idx)
    individual.append(move)

    # Testing:
    # If length of individual remained the same,
    # individual's 1st memory bit is now its previous 2nd memory bit,
    # individual's last memory bit is now "move"

    if (len(individual) == len(ind_temp) and
        individual[first_memBit_idx] == ind_temp[first_memBit_idx + 1] and
            individual[len(individual) - 1] == move):

        return True
    else:
        print(
            f"ERROR: Player was {ind_temp} \n and player is {individual}, the process has a problem")
        return False

# 2d)


def eval_function(individual1, individual2, individual3, m_depth, n_rounds):
    score1 = 0

    for round in range(n_rounds):
        ind1Move = move_by_ind1(
            individual1, individual2, individual3, round)
        ind2Move = move_by_ind1(
            individual2, individual1, individual3, round)
        ind3Move = move_by_ind1(
            individual3, individual1, individual2, round)
        process_move(individual1, ind1Move, m_depth)
        process_move(individual2, ind2Move, m_depth)
        process_move(individual3, ind3Move, m_depth)

        # Calculating the payoff of individual 1 and adding it to the score integer to get the total for all rounds
        score1 += payoff_to_ind1(individual1,
                                 individual2, individual3, game_matrix)

    return score1

# 2e)


def fitness_tournament(pop, fitness, m_depth, n_rounds):
    scores = []
    for p1 in pop:
        scores1 = 0
        for p2 in pop:
            for p3 in pop:
                scores1 += eval_function(
                    p1, p2, p3, m_depth, n_rounds)

        scores.append(scores1)
    for indScore in scores:
        # Converts totalScore into a tuple
        fitness.append((indScore,))

    return fitness


def calculate_scaled_fitnesses(pop, raw_fitness):
    # updates the array raw_fitness with scaled values

    # There's a posibility that the offspring will all have the same payoff (at least while running the code)
    fits = []
    for fit in raw_fitness:
        fits.append(fit[0])

    raw_fitness = np.array(fits)

    # 0.9 to make sure the minimum not turning into 0 after scaling
    minimum = np.min(raw_fitness) * 0.9

    avg = np.mean(raw_fitness)
    a = avg/(avg - minimum)
    b = -minimum * (avg/(avg - minimum))

    scaled_fitness = []

    for fit in raw_fitness:
        scale = a*fit + b
        scaled_fitness.append((scale,))

    return scaled_fitness


def dev_toolbox(n_bits):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # Initialize the toolbox
    toolbox = base.Toolbox()

    # Generate attributes
    toolbox.register("attr_bool", random.randint, 0, 1)

    # Initialize structures
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_bool, n_bits)

    # Define the population to be a list of individuals
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Register the evaluation operator
    toolbox.register("evaluate", fitness_tournament)

    # Register the crossover operator
    toolbox.register("mate", tools.cxTwoPoint)

    # Register a mutation operator
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

    # Operator for selecting individuals for breeding
    toolbox.register("select", tools.selRoulette)

    #toolbox.register("hallOfFame", tools.HallOfFame)

    return toolbox


def main(m_depth, n_bits, n_rounds, pop_size, gen):

    random.seed(64)
    toolbox = dev_toolbox(n_bits)
    pop = toolbox.population(n=pop_size)

    # Initial fitnesses from the original players
    fitnesses = []
    fitnesses = fitness_tournament(pop, fitnesses, m_depth, n_rounds)

    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    fits = [ind.fitness.values for ind in pop]

    cross, mutate = 0.95, 0.01

    bestOverall = []

    for g in range(gen):
        print("\n===== Generation", g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))

        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            # Cross two individuals
            if random.random() < cross:
                toolbox.mate(child1, child2)

                # "Forget" the fitness values of the children
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation
        for mutant in offspring:
            # Mutate an individual
            if random.random() < mutate:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Populate the fitness with offspring
        pop = copy.deepcopy(offspring)

        fitnesses = []
        fitnesses = fitness_tournament(pop, fitnesses, m_depth, n_rounds)

        fitnesses = calculate_scaled_fitnesses(pop, fitnesses)

        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        # This part is for statistic display
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Best %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

        print("-- End of (successful) evolution --")

        best_ind = tools.selBest(pop, 1, fit_attr="fitness")[0]
        bestOverall.append(best_ind.fitness.values)
        print("Best individual is %s, %s" %
              (best_ind, best_ind.fitness.values))

    # Printing the best individual overall
    print("")
    bestOverall = np.array(bestOverall)
    best = np.max(bestOverall)
    print("The best individual is: %s" % best)

# print(fitnesses)


if __name__ == "__main__":
    # main(m_depth, n_bits, n_rounds, pop_size, gen):
    main(2, 68, 10, 10, 20)
