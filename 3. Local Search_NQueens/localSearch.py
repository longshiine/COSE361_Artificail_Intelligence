from NQueens import *
import random
import math, sys

verbose = False

# ==================================================================
# This section contains an implementation of straightforward
# Hill Climbing. It requires a state class that creates objects
# that implement the following methods: getValue, getMaxValue,
# allNeighbors, randomNeighbors, and that are printable

# todo: hillclimb
def hillClimb(startState, maxRounds=1000):
    """performs hill climbing algorithm, given start state and maximum number of rounds and
    return a best state until solution is found of local maxima is reached"""
    curr = startState
    value = startState.getValue()
    maxValue = startState.getMaxValue()
    count = 0
    if verbose:
        print("=====================START======================")
    while value < maxValue and count < maxRounds:
        if verbose:
            print("------------------ Count = ", count, "------------------")
            print(curr)
        neighs = curr.allNeighbors()
        bestNeigh = findBestNeighbor(neighs)
        nextValue = bestNeigh.getValue()
        if nextValue >= value:
            if verbose:
                print("Best neighbor:")
                print(bestNeigh)
            curr = bestNeigh
            value = nextValue
        else:
            break
        count += 1
    if verbose:
        print("=================FINAL STATE====================")
        print(curr)
        print("         Number of steps=", count)
        if value == maxValue:
            print("    Fount perfect solution")
    return value, maxValue, count

# todo: findBestNeighbor
def findBestNeighbor(neighbors):
    """Given a list of neighbors, find and return a neighbor with the best value.
    If there are multiple neighbors with same value, a random one is chosen."""
    startBest = neighbors[0]
    bestValue = startBest.getValue()
    bestNeighs = [startBest]
    for neigh in neighbors:
        value = neigh.getValue()
        if value > bestValue:
            bestNeighs = [neigh]
            bestValue = value
        elif value == bestValue:
            bestNeighs.append(neigh)
    bestNeigh = random.choice(bestNeighs)
    return bestNeigh


# ==================================================================
# This section contains an implementation of stochastic
# Hill Climbing. Similar to the basic hill-climbing, this function
# generates a fixed number of neighbors, not all, and takes the best
# one

# todo: 실습과제
def stochHillClimb(startState, numNeighs = 10, maxRounds = 1000):
    """performs stochastic hill climbing algorithm, given start state and 
    maximum number of rounds and return a best state until solution is found 
    of local maxima is reached. """
    curr = startState
    value = startState.getValue()
    maxValue = startState.getMaxValue()
    count = 0
    if verbose:
        print("=====================START======================")
    while value < maxValue and count < maxRounds:
        if verbose:
            print("------------------ Count = ", count, "------------------")
            print(curr)
        neighs = curr.randomNeighbors(numNeighs)
        bestNeigh = stochFindBestNeighbor(neighs, value)
        if bestNeigh:
            curr = bestNeigh
            value = bestNeigh.getValue()
        if verbose:
            print("Best or Selected neighbor:")
            print(curr)
        count += 1
    if verbose:
        print("=================FINAL STATE====================")
        print(curr)
        print("         Number of steps=", count)
        if value == maxValue:
            print("    Fount perfect solution")
    return value, maxValue, count

def stochFindBestNeighbor(neighbors, currValue):
    """Given a list of neighbors and current state's value, find and return a neighbor 
    which has higher value than current state. when finding best neighbor it uses rouletteSelect,
    high-value entities have the highest probability of being selected, but low-value entities 
    have some probability of being selected."""
    
    bestNeighs = []
    for neigh in neighbors:
        value = neigh.getValue()
        if value >= currValue:
            bestNeighs.append(neigh)
    if len(bestNeighs) == 0:
        return False
    deltaValues = [neigh.getValue() - currValue for neigh in bestNeighs]
    bestpos = rouletteSelect(deltaValues)
    return bestNeighs[bestpos]



# ==================================================================
# This section contains an implementation of simulated annealing.  This
# algorithm randomly generates a move from the current state.  If the randomly
# generated move is better than the current one, then it makes that move.  If
# it is worse, then it decides stochastically whether to take the move or not.
# This involves both the difference in value, and also the current temperature.
# The states involved here need to implement the same set of methods as before,
# Plus a makeRandomMove method, that returns a new state one off from the
# previous one."""

# todo: 실습과제
def simAnnealing(startState, initTemp=100.0):
    """performs Simulated Annealing algorithm, given start state and 
    initial Temperature and return a best state when solution is 
    found of temperature is reached to zero or current state is optimal"""

    currTemp = initTemp
    currState = startState
    currState.setPrintMode(full=False)

    currValue = currState.getValue()
    maxValue = currState.getMaxValue()
    count = 0
    if verbose:
        print("=====================START======================")

    while round(currTemp, 2) > 0 and currValue < maxValue:
        if verbose:
            print("------------------ Count = ", count, "------------------")
            print(currState)
            print("current Temperature: ", currTemp)
        nextState = currState.makeRandomMove()
        nextValue = nextState.getValue()
        difference = nextValue - currValue
        if difference >= 0:
            currState = nextState
            currValue = nextValue
            if verbose:
                print("neighbor(Higher or Equal): ")
                print(nextState)
        else:
            threshold = math.exp(difference / currTemp)
            randomValue = random.random()
            if randomValue <= threshold:
                currState = nextState
                currValue = nextValue
                if verbose:
                    print("neighbor(Lower): ")
                    print(nextState)
        currTemp -= float(0.1)
        count += 1

    if verbose:
        print("=================FINAL STATE====================")
        print(currState)
        print("         Number of steps=", count)
        if currValue == maxValue:
            print("    Fount perfect solution")
    return currValue, maxValue, count

# ==================================================================
# This section contains an implementation of beam search.  This algorithm
# randomly generates n starting points.  It then generates all the successors
# of each of the n states, and puts them in one pool.  The top n successors
# are kept at each round.

# todo: 실습과제
def beamSearch(nqueenNum, numStates = 10, stopLimit=1000):
    """performs Beam Search algorithm, given nqueen number, num of states and stop 
    limitation, return a best state when optimal state is in current states list
    or is reached to maximum count """
    currStates = []
    for i in range(numStates):
        nextState = NQueens(nqueenNum)
        nextState.setPrintMode(full=False)
        currStates.append(nextState)
    maxValue = currStates[0].getMaxValue()
    sortByValue(currStates)

    count = 0
    foundOptimal = False
    if verbose:
        print("=====================START======================")
    while not foundOptimal and count < stopLimit:
        if verbose:
            print("------------------ Count = ", count, "------------------")
            print("< Current States(numStates) >")
            for state in currStates:
                print(state)
        bestNNeighs = []
        for nextState in currStates:
            neighs = nextState.allNeighbors()
            (bestNNeighs, foundOptimal) = keepBestNNeighbors(bestNNeighs, neighs, numStates, maxValue)
            if foundOptimal:
                break
        currStates = bestNNeighs
        if verbose:
            print("< Next states(numStates) >")
            for state in bestNNeighs:
                print(state)
            print("< Best Next state >")
            print(currStates[0])
        count += 1
        state = currStates[0]
    if verbose:
        print("=================FINAL STATE====================")
        print(state)
        print("         Number of steps=", count)
        if state.getValue() == maxValue:
            print("    Fount perfect solution")
    return state.getValue(), maxValue, count


# todo: 실습과제 - docstring 작성
def sortByValue(stateList):
    """Given a list of neighbors, return a list of neighbors. 
    it sortes the given list in decending order by value of states"""
    stateList.sort(key=lambda neigh: neigh.getValue(), reverse=True)

# todo: 실습과제 - docstring 작성
def keepBestNNeighbors(bestSoFar, neighs, n, maxVal):
    """When N best neighbor list, list of neighbors, number of states and maximum value
    is given, it returns updated N_best_neighbor_list and a foundOptimal value indicating 
    whether an optimal state was found in this state. When updating N_best_neighbor_list 
    it uses insertState function to properly insert the new state"""

    sortByValue(neighs)
    bestNeigh = neighs[0]
    if bestNeigh.getValue() == maxVal:  # if we have found an optimal solution
        return ([bestNeigh], True)
    else:
        i = 0
        while i < len(neighs):
            nextNeigh = neighs[i]
            if len(bestSoFar) == n:
                worstOfBest = bestSoFar[-1]
                if nextNeigh.getValue() < worstOfBest.getValue():
                    break
            insertState(bestSoFar, nextNeigh, n)
            i = i + 1
        return (bestSoFar, False)

# todo: 실습과제 - docstring 작성
def insertState(sortedList, newState, limit):
    """Given sorted N_best_neighbor_list, new state and number of states, it updates(returns) 
    N_best_neighbor_list by comparing value of new state and previous states. When
    the value of new state is greater than that of existing state it insert new state
    to the list"""

    i = 0
    for state in sortedList:
        if newState.getValue() > state.getValue():
            break
        i = i + 1
    sortedList.insert(i, newState)
    if len(sortedList) > limit:
        sortedList.pop(-1)


# ==================================================================
# This section contains an implementation of genetic algorithm search. This
# algorithm randomly generates n starting points.  It then chooses n "parents"
# from the population, based on roulette-wheel selection, which is based on
# the value/fitness of each state.  Another way to put this is that it samples
# with replacement from the probability distribution that corresponds to the
# amount of fitness the individual is responsible for. It crosses over parents
# with each other to create a new generation, and then continues.

# todo: geneticAlg
def geneticAlg(nqueenNum, popSize=30, maxGenerations=1000, crossPerc=0.5, mutePerc=0.05):
    if popSize % 2 == 1:
        print("Making population size even:")
        popSize += 1
    currStates = []
    for i in range(popSize):
        nextState = NQueens(nqueenNum)
        currStates.append(nextState)
    maxFit = currStates[0].getMaxValue()

    if verbose:
        print("=============== initial state =================")
        printNeighbors(currStates, False)
        print("===============================================")

    count = 0
    foundOptimal = False
    overallBest = currStates[0]

    while (not foundOptimal) and count < maxGenerations:
        count += 1
        if verbose:
            print("generation: ", count)
        fits = [state.getValue() for state in currStates]
        if maxFit in fits:
            pos = fits.index(maxFit)
            bestOne = currStates[pos]
            foundOptimal = True
        else:
            if verbose:
                print("Average fitness: ", sum(fits)/len(fits))
                print("max fitness: ", max(fits))
                print("min fitness: ", min(fits))
            bestLoc = fits.index(max(fits))
            bestOne = currStates[bestLoc]
            parentPool = selectParents(currStates, fits)
            currStates = mateParents(parentPool, crossPerc, mutePerc)
            if verbose:
                printNeighbors(currStates, False)
                print("=====================================")
        if bestOne.getValue() > overallBest.getValue():
            overallBest = bestOne
    if verbose:
        print("================= GOAL ==================")
        print("  Last generation best one:")
        print(bestOne)
        print("  Overall best discovered: ")
        print(overallBest)
        print("  Number of steps =", count)
    return bestOne.getValue(), maxFit, count



def selectParents(states, fitnesses):
    parents = []
    for i in range(len(states)):
        nextParentPos = rouletteSelect(fitnesses)
        parents.append(states[nextParentPos])
    return parents


def mateParents(parents, crossoverPerc, mutationPerc):
    newPop = []
    for i in range(0, len(parents), 2):
        p1 = parents[i]
        p2 = parents[i+1]
        doCross = random.random()
        if doCross < crossoverPerc:
            n1, n2 = p1.crossover(p2)
            newPop.append(n1)
            newPop.append(n2)
        else:
            newPop.append(p1.copyState())
            newPop.append(p2.copyState())
    for i in range(len(newPop)):
        nextOne = newPop[i]
        doMutate = random.random()
        if doMutate <= mutationPerc:
            newPop[i] = nextOne.makeRandomMove()
    return newPop


# ========================================================================
# This next section contains utility functions used by more than one of the algorithms


def rouletteSelect(valueList):
    """takes in a list giving the values for a set of entities. It randomly
    selects one of the positions in the list by treating the values as a kind of
    probability distribution and sampling from that distribution. Each entity gets
    a piece of a roulette wheel whose size is based on comparative value: high-value
    entities have the highest probability of being selected, but low-value entities have
    *some* probability of being selected."""
    totalValues = sum(valueList)
    pick = random.random() * totalValues
    s = 0
    for i in range(len(valueList)):
        s += valueList[i]
        if s >= pick:
            return i
    return len(valueList) - 1


def addNewRandomMove(state, stateList):
    """Generates new random moves (moving one queen within her column) until
    it finds one that is not already in the list of boards. If it finds one,
    then it adds it to the list. If it tries 100 times and doesn't find one,
    then it returns without changing the list"""
    nextNeigh = state.makeRandomMove()
    count = 0
    while alreadyIn(nextNeigh, stateList):
        nextNeigh = state.makeRandomMove()
        count += 1
        if count > 100:
            # if tried 100 times and no valid new neighbor, give up!
            return
    stateList.append(nextNeigh)


def alreadyIn(state, stateList):
    """Takes a state and a list of state, and determines whether the state
    already appears in the list of states"""
    for s in stateList:
        if state == s:
            return True
    return False


def printNeighbors(neighList, full = True):
    """Takes a list of neighbors and values, and prints them all out"""
    print("Neighbors:")
    for neigh in neighList:
        neigh.setPrintMode(full)
        print(neigh)
