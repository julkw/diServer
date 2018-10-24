import math
import re
import random, string
import costMatrixDijkstra as dij
from collections import Counter
# import Levenshtein 

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def addInsetions(word):
    number = random.randint(1, len(word))
    for _ in range(number):
        # don't change the first and the last character
        position = random.randint(0, len(word)-1)
        word = word[:position] + random.choice(string.ascii_lowercase) + word[position:]
    return word

def addDeletions(word):
    removalRate = 0.5
    maxRemoval = len(word)-2
    number = random.randint(1, math.floor(maxRemoval * removalRate))
    for _ in range(number):
        # don't change the first and the last character
        position = random.randint(0, len(word)-1)
        word = word[:position] + word[position + 1:]
    return word

def replaceCharacters(word):
    number = random.randint(1, len(word))
    for _ in range(number):
        position = random.randint(0, len(word)-1)
        word =  word[:position] + random.choice(string.ascii_lowercase) + word[position + 1:]
    return word

def matchSequences(path, sequences):
    spacedSequences = []
    for _ in range(len(sequences)):
        spacedSequences.append('')
    lastPosition = list(-1 for _ in range(len(sequences)))
    for position in path:
        for i in range(len(position)):
            if position[i] != lastPosition[i]:
                spacedSequences[i] = spacedSequences[i] + sequences[i][position[i]]
            else:
                spacedSequences[i] = spacedSequences[i] + ' '
        lastPosition = position
    for s in spacedSequences:
        print(s)
    return spacedSequences

def extractOriginal(path, sequences):
    result = ''
    spacedSequences = matchSequences(path, sequences)
    index = 0
    lastLetters = list(s[0] for s in spacedSequences)
    while index < len(spacedSequences[0]):
        # decide on length on block
        stepLengths = []
        for s in spacedSequences:
            nextPosition = re.search(r'[^ ]', s[index:])
            steps = len(s[index:])
            if nextPosition != None:
                steps = nextPosition.span()[0]
            stepLengths.append(steps)
        blockLength = Counter(stepLengths).most_common()[0][0] + 1
        # decide on event
        events = ''
        
        # make sure every user's last entry is used
         #for sIndex in range(len(spacedSequences)):
         #    if spacedSequences[sIndex][index] == ' ':
         #        spacedSequences[sIndex] = spacedSequences[sIndex][:index] + lastLetters[sIndex] + spacedSequences[sIndex][index + 1:]
        # find most frequent entries in block
        for i in range(index, min(len(spacedSequences[0]), index + blockLength)):
            for sIndex in range(len(spacedSequences)):
                if spacedSequences[sIndex][i] != ' ':
                    events = events + spacedSequences[sIndex][i]
                    lastLetters[sIndex] = spacedSequences[sIndex][i]
        occuranceNumbers = Counter(events).most_common()
        # no clear solution -> star
        if len(occuranceNumbers) > 1 and occuranceNumbers[0][1] == occuranceNumbers[1][1]:
            result = result + '*'
        else:
            result = result + occuranceNumbers[0][0]

        index += blockLength
    return result

def collectStatistics(wordLength, repetitions, wordNumber):
    filename = "../../data/testData_wl" + str(wordLength) + "_wn" + str(wordNumber) + ".txt"
    file = open(filename, "a+")
    
    for _ in repetitions:
        originalSequence = randomword(wordLength)
        sequences = []
        for _ in range(wordNumber):
            newSequence = addInsetions(originalSequence)
            newSequence = addDeletions(newSequence)
            sequences.append(newSequence)
        path = dij.timeWarpingPath(sequences)
        result = extractOriginal(path, sequences)
        file.write(originalSequence + ",")
        file.write(result + "\n")
    
    file.close()

def main():
    collectStatistics(10, 50, 5)
    # collectStatistics(20, 50, 5)
    collectStatistics(10, 50, 6)
    collectStatistics(10, 50, 7)
    collectStatistics(10, 50, 8)
    collectStatistics(10, 50, 9)
    collectStatistics(10, 50, 10)
    # originalSequence = randomword(10)
    # numberOfSequences = 10
    # sequences = []
    # for _ in range(numberOfSequences):
    #     newSequence = addInsetions(originalSequence)
    #     #newSequence = addDeletions(originalSequence)
    #     newSequence = addDeletions(newSequence)
    #     sequences.append(newSequence)
    #     print(newSequence)

    # print(' ')
    # #sequences = ['xanxb','xab','xab','xbab','xbab']
    # path = dij.timeWarpingPath(sequences)
    # # matchSequences(path, sequences)
    # result = extractOriginal(path, sequences)
    # print(' ')
    # print('original: ' + originalSequence)
    # print('newGuess: ' + result)
    # # print('score: '+ str(Levenshtein.distance(originalSequence, result)))

if __name__ == '__main__':
  main()
