import datetime
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

def _generate_parent(length, geneSet, get_fitness): # length = 10개 
    chromosome_list = []
    average = 0
    for i in range(0, 10): # 10놈
        genes = []
        while len(genes) < length:
            sampleSize = min(length - len(genes), len(geneSet))
            genes.extend(random.sample(geneSet, sampleSize))
        fitness = get_fitness(genes)
        average += fitness
        chromosome_list.append(Chromosome(genes, fitness))
    return chromosome_list, average/length

def _mutate(parent, geneSet, get_fitness): # 10자리중에서 한자리를 무조건 돌연변이 시킨다.
    childGenes = parent.Genes[:]
    index = random.randrange(0, len(parent.Genes))
    newGene, alternate = random.sample(geneSet, 2)
    childGenes[index] = alternate if newGene == childGenes[index] else newGene
    fitness = get_fitness(childGenes)
    return Chromosome(childGenes, fitness)

def proportional_selection(parent_list):
    child_list = []
    fitness_percent_list = []
    fitness_accum_list = []
    fitness_sum = 0
    for parent in parent_list:
        fitness_sum += parent.Fitness

    for parent in parent_list:
        fitness_percent_list.append(parent.Fitness / fitness_sum)

    fitness_sum = 0
    for fitness_percent in fitness_percent_list:
        fitness_sum += fitness_percent
        fitness_accum_list.append(fitness_sum)

    for i in range(0, 10):
        rand = random.random()
        before = 0
        for j in range(0, len(fitness_accum_list)):
            if rand > before and rand <= fitness_accum_list[j]:
                child_list.append(copy.deepcopy(parent_list[j]))
                break
            before = fitness_accum_list[j]
    return child_list

def tournament_selection(parent_list, k):
    child_list = []
    for i in range(0, 10):
        sample_index = random.sample(range(0,10), k)
        max_fitness = 0
        max_index = sample_index[0]
        for j in sample_index:
            if parent_list[j].Fitness > max_fitness:
                max_fitness = parent_list[j].Fitness
                max_index = j
        winner_chromosome = parent_list[max_index]
        child_list.append(copy.deepcopy(winner_chromosome))
    return child_list


def _generate_child(parent_list, geneSet, get_fitness, select_type, k=3):
    child_list = []

    # Selection
    if select_type == 'proportionate': # proportionate Selection
        child_list = proportional_selection(parent_list)
    elif select_type == 'tournament': # tournament Selection
        child_list = tournament_selection(parent_list, k)
    ## error
    else:
        print("Invalid Select Type!")
        return []

    # Crossover (Single Point Crossover 사용, Crossover point: 5)
    crossover_rate = 0.20
    crossover_point = 5
    selected = None
    for i in range(0, len(child_list)):
        rand = random.random()
        if rand < crossover_rate:
            if selected is None:
                selected = i
            else:
                child_list[selected].Genes[crossover_point:], child_list[i].Genes[crossover_point:] = child_list[i].Genes[crossover_point:], child_list[selected].Genes[crossover_point:]
                selected = None

        # update
        child_list[i].Fitness = get_fitness(child_list[i].Genes)

    # mutate
    mutate_rate = 0.20
    for i in range(0, len(child_list)):
        rand = random.random()
        if rand < mutate_rate:
            child = _mutate(child_list[i], geneSet, get_fitness)
            del child_list[i]
            child_list.append(child)
    return child_list


def get_answer(get_fitness, targetLen, optimalFitness, geneSet, display, select_type):
    random.seed()

    # genration count, maximum_average, fit_history
    gen_count = 0
    maximum_average = 0
    avg_fitness_hist = []

    # 1. Generate Parent
    bestParentList, average = _generate_parent(targetLen, geneSet, get_fitness) # 최초 generation, 그리고 그놈들의 각각의 fitness 값
    avg_fitness_hist.append(average)
    print("Generation : {},\t Average_Fitness: {}".format(gen_count, average))
    display(bestParentList)

    while True:
        gen_count += 1
        child_list = _generate_child(bestParentList, geneSet, get_fitness, select_type)

        fitness_sum = 0
        for child in child_list:
            fitness_sum += child.Fitness

        average = fitness_sum / 10
        avg_fitness_hist.append(average)
        print("Generation : {}, Average_Fitness: {}".format(gen_count, average))
        if average > maximum_average:
            bestParentList = child_list
            maximum_average = average

        if average >= optimalFitness:
            return child_list, avg_fitness_hist

class Chromosome:
    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness

def get_fitness(guess, target):
    fitness = 0
    for expected, actual in zip(target, guess):
        if expected == actual:
            fitness += 1
    return fitness

def display(candidate, target, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("{}\t{}\t\t{}".format(''.join(candidate.Genes),candidate.Fitness,timeDiff))

def display_list(candidate_list, target, startTime):
    fitness_sum = 0
    print("{}\t\t{}\t\t{}".format('Answer', 'Fitness','Time'))
    for candidate in candidate_list:
        display(candidate, target, startTime)
        fitness_sum += candidate.Fitness
    # print("average fitness : {}".format(fitness_sum / len(candidate_list)))

def generate_answer(length, is_duplicate_allowed):
    # 중복이 허용되거나, length가 4 넘을 때 (1234 인데 길이 4가 넘으면 중복은 당연히 허용)
    if is_duplicate_allowed is True or length > 4:
        return ''.join(random.choice("1234") for _ in range(length))

    answer_list = []
    num = random.randrange(1, 4)
    for i in range(length):
        while str(num) in answer_list:
            num = random.randrange(1, 4)
        answer_list.append(str(num))
    
    target = ''.join(answer_list)
    print("Target Answer: {}".format(target))

    return target

def english_test(target, select_type):
    geneset = "1234"
    startTime = datetime.datetime.now()

    def fnGetFitness(genes):
        return get_fitness(genes, target)

    def fnDisplay(candidate_list):
        display_list(candidate_list, target, startTime)

    optimalFitness = len(target) * 1
    child_list, avg_fitness_hist = get_answer(fnGetFitness, len(target), optimalFitness, geneset, fnDisplay, select_type)

    print("{} Selection, time: {}".format(select_type, datetime.datetime.now() - startTime))
    return avg_fitness_hist


def plot_result(values, title, legend, xlabel, ylabel):
    for value in values:
        plt.plot(range(0,len(value)), value)
    plt.title(title)
    plt.legend(legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


if __name__ == '__main__':
    target = generate_answer(10, True)

    proportionate_fit_hist = english_test(target,'proportionate')
    tournament_fit_hist = english_test(target, 'tournament')

    # plot_result(
    #     [proportionate_fit_hist,tournament_fit_hist],
    #     'Fitness graph of each selection type',
    #     ['proportional_selection', 'tournament_selection'],
    #     'Generation',
    #     'Fitness Value')