import itertools as it

import matplotlib.pyplot as plt


def collectAverages():
    filename = "data/moreThan3Reps.txt" 
    file = open(filename, "r") 
    data = []
    lines = file.readlines()
    threeCount = 0
    scoreSum = 0
    timeSum = 0
    for line in lines:
        line = line.replace('\n', '')
        words = line.split(',')
        
        users = int(words[0])
        stringLength = int(words[1])
        errorProbability = float(words[2])
        original = words[3]
        result = words[4]
        time = float(words[5])
        score = float(words[6])
        
        if threeCount == 0:
            timeSum = 0
            scoreSum = 0
        
        timeSum += time
        scoreSum += score
        
        if threeCount == 2:
            data.append([users, stringLength, errorProbability, timeSum/3.0, scoreSum/3.0])
        
        threeCount += 1
        threeCount %= 3
    return data

def plot(xIndex, yIndex, aggregateIndex, data, xLabel = '', yLabel = '', aggregateLable = '', figureNumber = 0):
    if figureNumber > 0:
        plt.figure(figureNumber)
    distinctAggregateValues = set(line[aggregateIndex] for line in data)
    for dv in distinctAggregateValues:
        valuePairs = list((line[xIndex], line[yIndex]) for line in data if line[aggregateIndex] == dv)
        valuePairs.sort()
        xList = []
        yList = []
        for xValue, yValues in it.groupby(valuePairs, lambda x: x[0]):
            xList.append(xValue)
            sum = 0
            divisor = 0
            for value in yValues:
                sum += value[1]
                divisor += 1
            yList.append(sum / divisor)

        line = plt.plot(xList, yList, label = str(dv))
        plt.legend(title=aggregateLable)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

def main():
    data = collectAverages()
    
    userNumberIndex = 0
    stringLengthIndex = 1
    errorProbabilityIndex = 2
    timeIndex = 3
    scoreIndex = 4

    plot(userNumberIndex, timeIndex, errorProbabilityIndex, data, "number of users", "time", "error probability", 1)
    plot(userNumberIndex, timeIndex, stringLengthIndex, data, "number of users", "time", "string length", 2)
    plot(stringLengthIndex, timeIndex, errorProbabilityIndex, data, "length of string", "time", "error probability", 3)
    plot(stringLengthIndex, timeIndex, userNumberIndex, data, "length of string", "time", "number of users", 4)
    plot(userNumberIndex, scoreIndex, errorProbabilityIndex, data, "number of users", "rating of result, normalized by string length", "error probability", 5)
    plt.show()    

if __name__ == '__main__':
  main()
