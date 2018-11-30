# Python 2.7
import random
import string
import time

import costMatrixDijkstra as dij
import sequenceUtils as su
import timeSequenceUtils as tsu


def main():    
    # test with Time
    originalSequence = tsu.randomSequenceWithTime(10, 3)
    print(originalSequence)
    numberOfSequences = 3
    sequences = []
    for _ in range(numberOfSequences):
        #newSequence = tsu.insertErrorsWithTime(originalSequence.copy(), 0.3, 1.5)
        newSequence = tsu.insertErrorsWithTime(list(originalSequence), 0.3, 1.5)
        sequences.append(newSequence)
    path = dij.aStarTimeWarpingPathWithTimestamps(sequences)
    resultSequence = tsu.extractOriginalWithTime(path, sequences)
    print('original')
    print(originalSequence)
    print('guess')
    print(resultSequence)
    return

    # test without time
    originalSequence = su.randomword(15)
    numberOfSequences = 5
    sequences = []
    for _ in range(numberOfSequences):
        newSequence = su.insertErrors(0.3, originalSequence)
        sequences.append(newSequence)
        print(newSequence)
    print(' ')
    path = dij.timeWarpingPathAStar(sequences)
    result = su.extractOriginal(path, sequences)
    print(' ')
    print('original: ' + originalSequence)
    print('newGuess: ' + result)

    return

if __name__ == '__main__':
  main()
