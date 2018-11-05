from itertools import permutations
import heapq

# turn into global variables to prevent excessive copying
allDirections = []
sequences = []
maxLength = 0

def distHeuristic(indices):
    global sequences
    global maxLength
    spaces = 0
    for s in sequences:
        spaces += maxLength - len(s)
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
    global maxLength
    allDirections = initializeDirections(len(localSequences))
    sequences = localSequences
    maxLength = max(list(len(s) for s in sequences))

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

    
