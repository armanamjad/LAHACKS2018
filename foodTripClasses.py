import json

class foodTrip:
    def __init__(self, jsonFile):
        self.jsonFile = jsonFile
        
        # duration is in seconds
        self.duration = jsonFile['routes'][0]['legs'][0]['duration']['value'];
        
        # key = name of place, value = 
        self.places = [];
        self.htmlInstructions
        
    def insertPlace(self, name, address):
        newPlace = place()
        self.places.add(place)
        
    def printUpdates(self):
        print()
        
    def print(self):
        index = 0
        for place in self.places:
            print("Stop " + str(index) + " " + place.name)
            index += 1
    
class place:
    def __init__(self, name, address, score):
        self.name = name
        self.address = address
        self.score = score
        
