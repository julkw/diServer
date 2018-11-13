import random
import string
import math
from collections import Counter
import re
import datetime
import sequenceUtils as su

def addTime(word, averageGap):
    events = []
    time = datetime.datetime.now()
    for letter in word:
        factor = random.uniform(0.0, 2.0)
        gap = averageGap * factor
        time += gap
        events.append((letter, time))
    return events

def randomSequenceWithTime(numberOfEvents, avgSecsBetweenEvents):
    word = su.randomword(numberOfEvents)
    averageGap = datetime.timedelta(0, avgSecsBetweenEvents)
    events = addTime(word, averageGap)
    return events
        
def insertTimeError(event, maxError, predecessorTime, successorTime):
    newTime = predecessorTime
    while newTime <= predecessorTime or newTime >= successorTime:
        factor = random.uniform(-0.5, 1.0)
        newTime = event[1] + factor * maxError
    event = (event[0], newTime)
    return event

#TODO: Replace by something that takes skew into consideration (higher likelyhood of pressing the button too late than too early)
def averageTime(timestamps):
    referenceTS = timestamps[0]
    allDists = datetime.timedelta(0,0)
    for ts in timestamps:
        allDists += ts - referenceTS
    averageTime = referenceTS + allDists/len(timestamps)
    return averageTime

def insertErrorsWithTime(events, errorProbability, maxTimeErrorInSecs):
    maxError = datetime.timedelta(0, maxTimeErrorInSecs)
    i = 0
    while i < len(events):
        # define the borders for the new time
        if i == 0:
            predTime = events[0][1] - maxError
        else:
            predTime = events[i-1][1]
        if i == len(events) - 1:
            succTime = events[i][1] + maxError
        else:
            succTime = events[i+1][1]
        
        # decide whether to insert an event error
        if random.uniform(0.0, 1.0) > errorProbability:
            events[i] = insertTimeError(events[i], maxError, predTime, succTime)
            i += 1
            continue

        # decide on kind of error
        change = random.choice(['delete', 'insert', 'replace'])
        if change == 'delete':
            del events[i]
            continue
        elif change == 'insert':
            # this is revisited in the next step as the insertion is in front of the current element
            # events[i] = insertTimeError(events[i], maxError, predTime, succTime)
            succTime = events[i][1]
            newEvent = events[i]
            newEvent = (random.choice(string.ascii_lowercase), predTime + (succTime - predTime)/2.0)  
            newEvent = insertTimeError(newEvent, maxError, predTime, succTime)
            events.insert(i, newEvent)            
        elif change == 'replace':
            newEvent = (random.choice(string.ascii_lowercase), events[i][1])
            events[i] = insertTimeError(newEvent, maxError, predTime, succTime)
        i += 1
    return events

def extractOriginalWithTime(path, timeSequences):
    # since spaces are penalized, step lengths don't make much sense anymore
    # therefore we can just follow the path and make a decision for every node
    result = []
    lastPosition = list(-1 for _ in range(len(timeSequences)))
    for position in path:
        # decide on event
        currentEvent = list(timeSequences[i][position[i]][0] for i in range(len(position)) if position[i] != lastPosition[i])
        noEvent = len(position) - len(currentEvent)
        occuranceNumbers = Counter(currentEvent).most_common()
        if noEvent > occuranceNumbers[0][1]:
            continue
        # no clear solution -> star
        elif len(occuranceNumbers) > 1 and occuranceNumbers[0][1] == occuranceNumbers[1][1]:
            resultEvent = '*'
        else:
            resultEvent = occuranceNumbers[0][0]

        #calculate time
        times = list(timeSequences[i][position[i]][1] for i in range(len(position)) if resultEvent == '*' or timeSequences[i][position[i]][0] == resultEvent)
        resultTime = averageTime(times)
        result.append((resultEvent, resultTime))
    return result
