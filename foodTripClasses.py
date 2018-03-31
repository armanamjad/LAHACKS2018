import json

class FoodTrip:
    def __init__(self, jsonFile = None):
        self.jsonFile = jsonFile
        
        # duration is in seconds
        self.duration = jsonFile['routes'][0]['legs'][0]['duration']['value'];
        
        # distance is in meters
        self.totalDistance = jsonFile['routes'][0]['legs'][0]['distance']['value']
        
        # key = name of place, value = 
        self.places = [];
        
        self.startingPoint
        self.endingPoint
        
        self.htmlInstructions = None
        
    def insertPlace(self, name, address, score, category):
        newPlace = Place(name, address, score, category)
        self.places.add(Place)
        
    def printUpdates(self):
        print()
        
    def print(self):
        index = 0
        for place in self.places:
            print("Stop " + str(index) + " " + place.name)
            index += 1
    
class Place:
    def __init__(self, name, address, score = 0, category = ""):
        self.name = name
        self.address = address
        self.score = score
        self.category = category
        
    def print(self):
        print(self.name + " " + self.address)
        
