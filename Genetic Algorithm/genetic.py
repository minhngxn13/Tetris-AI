import random
import functools
import math
import statistics
import time
from operator import itemgetter
from game import TetrisApp
import sys
from sys import stdout


def createIndividual(size):
    result = []
    for i in range(0, size):
        result.append(random.uniform(-10, 10))
    return result

def individualFromDistribution(average, std):
    result = []
    for i in range(0, size):
        result.append(random.normalvariate(average[i], std[i]))
    return result

def createGeneration(number, size):
    results = []
    for i in range(0, number):
        tmp = createIndividual(size)
        results.append(tmp)
    return results

def generationFromDistribution(number, size, average, std):
    results = []
    for i in range(0, number):
        tmp = individualFromDistribution(average, std)
        results.append(tmp)
    return results

def selectBestIndividuals(scores, number):
    bests = list(reversed(sorted(scores, key=itemgetter(0))))[0:number]
    return list(map(lambda x: x[1], bests))

def fitness(individual, seeds, pieceLimit):
    score = []
    lines = []
    for seed in seeds:
        run = TetrisApp(False, seed).run(indiv, pieceLimit)
        score.append(run[0])
        lines.append(run[1])
    return [int(sum(score)/len(score)), int(sum(lines)/len(lines))]

def computeAverage(population):
    result = list(functools.reduce(lambda i1, i2: [a+b for a,b in zip(i1, i2)], population))
    result = list(map(lambda x: x/len(population), result))
    return result

def computeStandardDeviation(population):
    average = computeAverage(population)
    results = [[] for _ in range(0, len(population[0]))]
    for individual in population:
        for index, weight in enumerate(individual):
            results[index].append(weight)
    result = list(map(lambda weights: statistics.stdev(weights), results))
    return result

survivors_rate = 0.2
pieceLimit = 1000
number = 50
batch = 100
size = 34

generation = createGeneration(50, 34)

with open('CapstoneProjectTetris/GeneticAlgorithm/Logs/logs_v1.txt', 'w') as file_out:
    sys.stdout = file_out

    for iteration in range(0, batch):
        start_time = time.time()
        seeds = [random.randint(0, 100000000) for _ in range(5)]

        print("\n\n--- Generation " + str(iteration) + " ---\n")
        scores = []
        for index, indiv in enumerate(generation):
            message = "\rindiv. " + str(index) + "/" + str(len(generation))
            sys.stdout.write(message)
            sys.stdout.flush()
            scores.append([fitness(indiv, seeds, pieceLimit), indiv])
        print("\n")
        for value in (list(reversed(sorted(scores, key=itemgetter(0))))):
            print(value)
        survivors = selectBestIndividuals(scores, int(len(scores) * survivors_rate))
        print(len(survivors))
        generation = survivors

        average = computeAverage(survivors)
        extra_var_multiplier = max((1.0 - iteration / float(batch / 2)), 0)
        std = list(map(lambda std: std + 0.001 * extra_var_multiplier, computeStandardDeviation(survivors)))

        print("\ntime elapsed: ", time.time() - start_time)
        print("average: ", average)
        print("std: ", std, "\n")

        for individual in generationFromDistribution(number - len(generation), size, average, std):
            generation.append(individual)

sys.stdout = sys.__stdout__