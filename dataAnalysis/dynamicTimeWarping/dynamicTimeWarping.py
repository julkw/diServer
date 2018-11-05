import random, string
import costMatrixDijkstra as dij
import sequenceUtils as su
import time

def collectStatistics(wordLength, repetitions, wordNumber):
    filename = "../../data/testData_wl" + str(wordLength) + "_wn" + str(wordNumber) + ".txt"
    file = open(filename, "a+")
    for _ in range(repetitions):
        originalSequence = su.randomword(wordLength)
        sequences = []
        for _ in range(wordNumber):
            newSequence = su.addInsetions(originalSequence)
            newSequence = su.addDeletions(newSequence)
            sequences.append(newSequence)
        path = dij.timeWarpingPath(sequences)
        result = su.extractOriginal(path, sequences)
        file.write(originalSequence + ",")
        file.write(result + "\n") 
    file.close()

def compareAlgorithms(dataFilename, resultFilename):
    dataFile = open(dataFilename, "r")
    resultFile = open(resultFilename, "a+")
    lines = dataFile.readlines()
    for line in lines:
        sequences = line.split(",")
        # Dijkstra
        before = time.time()
        path = dij.timeWarpingPath(sequences[1:])
        after = time.time()
        duration = after - before
        result = su.extractOriginal(path, sequences[1:])
        resultFile.write("Dijkstra: " + sequences[0] + "->" + result + "," + str(duration) + "\n")         
        print("Dijkstra: " + sequences[0] + "->" + result + "," + str(duration) + "\n")

        # A*
        before = time.time()
        path = dij.timeWarpingPathAStar(sequences[1:])
        after = time.time()
        duration = after - before
        result = su.extractOriginal(path, sequences[1:])
        resultFile.write("A*: " + sequences[0] + "->" + result + "," + str(duration) + "\n")
        print("A*: " + sequences[0] + "->" + result + "," + str(duration) + "\n")
    
    dataFile.close()
    resultFile.close()

def generateTestData(repetitions, wordLength, numberOfSequences, error, filename):
    file = open(filename, "a+")
    for _ in range(repetitions):
        originalSequence = su.randomword(wordLength)
        sequences = [originalSequence]
        for _ in range(numberOfSequences):
            newSequence = su.insertErrors(error, originalSequence)
            sequences.append(newSequence)
        file.write(",".join(sequences) + "\n")
        
    file.close()

def main():
    dataFilename = "../../data/errorStringTestData.txt"
    resultFilename = "../../data/algorithmComparison.txt"
    
    generateTestData(20, 20, 5, 0.3, dataFilename)
    compareAlgorithms(dataFilename, resultFilename)
    
    return
    
    originalSequence = su.randomword(20)
    numberOfSequences = 5
    for _ in range(numberOfSequences):
        newSequence = su.insertErrors(0.3, originalSequence)
        sequences.append(newSequence)
        print(newSequence)
    print(' ')
    # sequences = ['ngtinhzeongsfxsaet', 'bnjintztbonskfxvsbpt', 'bhzehosfyxdssbvt']
    path = dij.timeWarpingPathAStar(sequences)
    result = su.extractOriginal(path, sequences)
    print(' ')
    print('original: ' + originalSequence)
    print('newGuess: ' + result)

if __name__ == '__main__':
  main()
