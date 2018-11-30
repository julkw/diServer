import pymongo  
from flask import jsonify
import datetime
import dataAnalysis.costMatrixDijkstra as dij
import dataAnalysis.timeSequenceUtils as tsu

client = pymongo.MongoClient("mongodb://localhost")

diDatabase = client["diDatabase"]

# collections 
competitions = diDatabase["competitions"]
athletes = diDatabase["athletes"]
teams = diDatabase["teams"]
events = diDatabase["events"]
users = diDatabase["users"]
apps = diDatabase["apps"]

def insertEvent(event):
      allNecessaryFields = 'userID' in event and 'appID' in event and 'timestamp' in event and 'competition' in event
      if not allNecessaryFields:
            return False
      events.insert_one(event)
      return True

def insertEvents(events):
      allInsertionsSuccessful = True
      for event in events:
            allInsertionsSuccessful = insertEvent(event) and allInsertionsSuccessful
      return allInsertionsSuccessful

def insertIntoCollection(collectionName, document):
      if collectionName == "events":
            return insertEvent(document)
      else: 
            return diDatabase[collectionName].insert_one(document)

def getCompetitionEvents(gameID):
      competition = competitions.find_one({"gameid": gameID})
      if competition == None:
            print("couldn't find the game")
            return None
      if "events" in competition:
            return competition["events"]
      # create events from user data
      userEvents = {}
      for event in events.find({"competition": gameID}):
            user = event["userID"]
            eventType = event["event"]
            timestamp = event["timestamp"]
            if user in userEvents:
                  userEvents[user].append((eventType, datetime.datetime.strptime(timestamp, '%H:%M:%S.%f')))
            else:
                  userEvents[user] = [(eventType, datetime.datetime.strptime(timestamp, '%H:%M:%S.%f'))]
      sequences = []
      for user in userEvents:
            sequences.append(userEvents[user])
      path = dij.aStarTimeWarpingPathWithTimestamps(sequences)
      resultSequence = tsu.extractOriginalWithTime(path, sequences)
      # add result events to game document
      jsonSequence = list({"event": str(s[0]), "timestamp":str(s[1])} for s in resultSequence)
      competition["events"] = jsonSequence
      competitions.update_one({"id:": gameID}, {"$set": competition}, upsert=False)
      return jsonSequence 