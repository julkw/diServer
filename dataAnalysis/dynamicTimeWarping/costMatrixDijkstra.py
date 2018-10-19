from itertools import permutations
import heapq

# turn into global variables to prevent excessive copying
allDirections = []
sequences = []

def charDist(indices):
    global sequences
    chars = set(sequences[i][indices[i]] for i in range(len(sequences)))
    return len(chars) - 1

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
                nDist = currentPosition[0] + charDist(n)
                heapq.heappush(nextPosition, (nDist, n))
    
    path = []
    pathPosition = currentPosition[1]
    path.append(pathPosition)
    while pathPosition != start:
        pathPosition = predecessors[tuple(pathPosition)]
        path.append(pathPosition)
    
    return reversed(path)

    
