from itertools import permutations
import heapq
import datetime
import math

# turn into global variables to prevent excessive copying
allDirections = []
sequences = []

def distHeuristic(indices):
    global sequences
    stepsLeft = list(len(sequences[i]) - indices[i] for i in range(len(sequences)))
    maxLeft = max(stepsLeft)
    spaces = 0
    for sl in stepsLeft:
        spaces += maxLeft - sl
        
    return spaces

def charDist(indices):
    global sequences
    chars = set(sequences[i][indices[i]] for i in range(len(sequences)))
    return len(chars) - 1

def spaceDist(lastPosition, nextPosition):
    global sequences
    charList = list(sequences[i][nextPosition[i]] for i in range(len(sequences)) if nextPosition[i] > lastPosition[i])
    spaces = len(sequences) - len(charList)
    return len(set(charList)) - 1 + spaces

def standardDeviation(timestamps):
    referenceTS = timestamps[0]
    allDists = datetime.timedelta(0,0)
    for ts in timestamps:
        allDists += ts - referenceTS
    averageTime = referenceTS + allDists/len(timestamps)
    standardDev = datetime.timedelta(0,0)
    for ts in timestamps:
        standardDev += math.pow(ts - averageTime, 2)
    standardDev /= len(ts)
    return standardDev

def withTimeDist(lastPosition, nextPosition, noMatchTimePenalty):
    global sequences
    eventDist = spaceDist(lastPosition, nextPosition)
    timestamps = list(sequences[i][nextPosition[i]][1] for i in range(len(sequences)) if nextPosition[i][1] > lastPosition[i][1])
    timePenalty = standardDeviation(timestamps) + (len(sequences) - len(timestamps)) * noMatchTimePenalty
    return timePenalty + eventDist

def initializeDirections(dimensions):
    allDirections = []
    for d in range(dimensions):
        dir = list(0 for _ in range(d)) + list(1 for _ in range(d, dimensions))
        allDirections += set(permutations(dir))
    return allDirections

def neighbours(currentPosition):
    global sequences
    global allDirections

    neighbours = []
    for d in allDirections:
        outOfBounds = False
        for i in range(len(d)):
            outOfBounds = outOfBounds or (currentPosition[i] + d[i] >= len(sequences[i]))
        if not outOfBounds:
            neighbours.append(list(sum(x) for x in zip(currentPosition, d)))
    return neighbours

def timeWarpingPathWithTimestamps(eventSequence):
    # initialize global variables
    global allDirections
    global sequences
    allDirections = initializeDirections(len(eventSequence))
    sequences = eventSequence

    # Dijkstra
    predecessors = {}
    nextPosition = []

    start = list(0 for _ in range(len(sequences)))
    stop = list(len(s) - 1 for s in sequences)

    # this will not impact the path, just the end cost
    startTimestamps = list(s[0][1] for s in sequences)
    startDist = standardDeviation(startTimestamps) + withTimeDist(start, start, 0)
    # currentPosition = (startDist, start)
    currentPosition = (0, start)
    heapq.heappush(nextPosition, currentPosition)

    while currentPosition[1] != stop:
        currentPosition = heapq.heappop(nextPosition)
        for n in neighbours(currentPosition[1]):
            if tuple(n) not in predecessors:
                predecessors[tuple(n)] = currentPosition[1]
                nDist = currentPosition[0] + withTimeDist(currentPosition[1], n, 0)
                # nDist = currentPosition[0] + charDist(n)
                heapq.heappush(nextPosition, (nDist, n))
    
    path = []
    pathPosition = currentPosition[1]
    path.append(pathPosition)
    while pathPosition != start:
        pathPosition = predecessors[tuple(pathPosition)]
        path.append(pathPosition)
    
    return reversed(path)

def timeWarpingPath(localSequences):
    # initialize global variables
    global allDirections
    global sequences
    allDirections = initializeDirections(len(localSequences))
    sequences = localSequences

    # Dijkstra
    predecessors = {}
    nextPosition = []

    start = list(0 for _ in range(len(sequences)))
    stop = list(len(s) - 1 for s in sequences)

    currentPosition = (charDist(start), start)
    heapq.heappush(nextPosition, currentPosition)

    while currentPosition[1] != stop:
        currentPosition = heapq.heappop(nextPosition)
        for n in neighbours(currentPosition[1]):
            if tuple(n) not in predecessors:
                predecessors[tuple(n)] = currentPosition[1]
                nDist = currentPosition[0] + spaceDist(currentPosition[1], n)
                # nDist = currentPosition[0] + charDist(n)
                heapq.heappush(nextPosition, (nDist, n))
    
    path = []
    pathPosition = currentPosition[1]
    path.append(pathPosition)
    while pathPosition != start:
        pathPosition = predecessors[tuple(pathPosition)]
        path.append(pathPosition)
    
    return reversed(path)

def timeWarpingPathAStar(localSequences):
    # initialize global variables
    global allDirections
    global sequences
    allDirections = initializeDirections(len(localSequences))
    sequences = localSequences

    # Dijkstra
    predecessors = {}
    nextPosition = []

    start = list(0 for _ in range(len(sequences)))
    stop = list(len(s) - 1 for s in sequences)

    currentPosition = (0, start, charDist(start)) # dist with heuristic, position, actualDist
    heapq.heappush(nextPosition, currentPosition)

    while currentPosition[1] != stop:
        currentPosition = heapq.heappop(nextPosition)
        for n in neighbours(currentPosition[1]):
            if tuple(n) not in predecessors:
                predecessors[tuple(n)] = currentPosition[1]
                nDist = currentPosition[2] + spaceDist(currentPosition[1], n)
                # heapq.heappush(nextPosition, (nDist, n))
                heapq.heappush(nextPosition, (nDist + distHeuristic(n), n, nDist))
    
    path = []
    pathPosition = currentPosition[1]
    path.append(pathPosition)
    while pathPosition != start:
        pathPosition = predecessors[tuple(pathPosition)]
        path.append(pathPosition)
    
    return reversed(path)

    
