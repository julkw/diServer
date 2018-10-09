import pymongo  
from flask import jsonify


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
            insertEvent(document)
      else: 
            diDatabase[collectionName].insert_one(document)
       