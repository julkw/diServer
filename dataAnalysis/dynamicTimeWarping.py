# Python 2.7
import random
import string
import time

import costMatrixDijkstra as dij
import sequenceUtils as su
import timeSequenceUtils as tsu


def main():    

    # test without time
    originalSequence = su.randomword(15)
    numberOfSequences = 5
    sequences = []
    for _ in range(numberOfSequences):
        newSequence = su.insertErrors(0.3, originalSequence)
        sequences.append(newSequence)
    path = dij.timeWarpingPathAStar(sequences)
    result = su.extractOriginal(path, sequences)
    print(' ')
    print('original: ' + originalSequence)
    print('newGuess: ' + result)
    print('new Guess rating: ' + str(dij.sequenceRating(originalSequence, result)))
    print('userInputs and ratings:')
    for s in sequences:
        rating = dij.sequenceRating(result, s)
        print(s + ": " + str(rating))        
    return

    # test with Time
    originalSequence = tsu.randomSequenceWithTime(15, 3)
    numberOfSequences = 3
    sequences = []
    for _ in range(numberOfSequences):
        #newSequence = tsu.insertErrorsWithTime(originalSequence.copy(), 0.3, 1.5)
        newSequence = tsu.insertErrorsWithTime(list(originalSequence), 0.3, 1.5)
        sequences.append(newSequence)
    path = dij.aStarTimeWarpingPathWithTimestamps(sequences)
    resultSequence = tsu.extractOriginalWithTime(path, sequences)
    print('original')
    tsu.printTimeSequence(originalSequence)
    print(' ')
    print('guess')
    tsu.printTimeSequence(resultSequence)
    print(" ")
    print(' rating of result: ' + str(dij.sequenceRatingWithTime(originalSequence, resultSequence)))
    print('user ratings:')
    for s in sequences:
        rating = dij.sequenceRatingWithTime(resultSequence, s)
        print(str(rating))        
    return

if __name__ == '__main__':
  main()
