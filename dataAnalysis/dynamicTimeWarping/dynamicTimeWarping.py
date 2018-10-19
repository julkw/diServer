import random, string
import costMatrixDijkstra as dij

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def addInsetions(word):
    number = random.randint(1, len(word))
    for _ in range(number):
        # don't change the first and the last character
        position = random.randint(1, len(word)-1)
        word = word[:position] + random.choice(string.ascii_lowercase) + word[position:]
    return word

def addDeletions(word):
    number = random.randint(1, len(word)-2)
    for _ in range(number):
        # don't change the first and the last character
        position = random.randint(1, len(word)-2)
        word = word[:position] + word[position + 1:]
    return word

def replaceCharacters(word):
    number = random.randint(1, len(word))
    for _ in range(number):
        position = random.randint(0, len(word)-1)
        word =  word[:position] + random.choice(string.ascii_lowercase) + word[position + 1:]
    return word

def printMatchedSequences(path, sequences):
    spacedSequences = []
    for x in range(len(sequences)):
        spacedSequences.append(sequences[x][0])
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

def main():
    originalSequence = randomword(20)
    print(originalSequence)
    numberOfSequences = 4
    sequences = [originalSequence]
    for _ in range(1, numberOfSequences):
        newSequence = addInsetions(originalSequence)
        #newSequence = addDeletions(originalSequence)
        newSequence = addDeletions(newSequence)
        sequences.append(newSequence)
        print(newSequence)

    print(' ')

    path = dij.timeWarpingPath(sequences)
    printMatchedSequences(path, sequences)

if __name__ == '__main__':
  main()
