import json
import urllib.parse
import urllib.request
from foodTripClasses import FoodTrip
from foodTripClasses import Place
apiKey = "key=AIzaSyCf6FC2ZTf-gFn3cvptcowZl_jwaGaZclY"
_testing = False


def createUrl(org: str, dest: str, wayPoints: list = None):
    # Formatting
    org = org.replace(" ", "+")
    dest = dest.replace(" ", "+")
    
    # declaring strings that will make up the url
    url = "https://maps.googleapis.com/maps/api/directions/json?"
    origin = "origin=" + org
    destination = "destination=" + dest
    waypoints = "waypoints=optimize:true|"
    
    
    
    if len(waypoints) == 0:
        return url + origin + "&" + destination + "&" + apiKey
    else:
        return url + origin + "&" + destination + "&" + waypoints + "&" + apiKey

def getResult(url):
    response = None
    
    try:
        response = urllib.request.urlopen(url)
        jsonText = response.read().decode(encoding = 'utf-8')
        return json.loads(jsonText)
    finally:
        if response != None:
            response.close()
            
def findClosestDestination(places: list, origin: Place):
    places = filterPlacesByDuration(places, origin, 10000)
    
    closestPlace = None
    minDuration = None
    tempFoodTrip = None
    for place in places:
        tempjsonFile = getResult(createUrl(origin.address, place.address))
        tempFoodTrip = FoodTrip(tempjsonFile)
        if minDuration == None:
            minDuration = tempFoodTrip.duration
            closestPlace = place
        elif tempFoodTrip.duration < minDuration:
            minDuration = tempFoodTrip.duration
            closestPlace = place
        elif tempFoodTrip == minDuration:
            print(place.name + "is as far away as " + closestPlace.name)
            
    return closestPlace

# removes locations that have a higher duration than duration passed   
def filterPlacesByDuration(places: list, origin: Place, duration: int):
    newPlaces = []
    
    for place in places:
        tempjsonFile = getResult(createUrl(origin.address, place.address))
        tempFoodTrip = FoodTrip(tempjsonFile)
        if tempFoodTrip.duration <= duration:
            newPlaces.append(place)
            
    return newPlaces

def filterPlacesByMiles(places: list, origin: Place, miles: int):
    meters = miles * 1609.344
#     print("total meters: " + str(meters))
    newPlaces = []
    
    for place in places:
        tempjsonFile = getResult(createUrl(origin.address, place.address))
        tempFoodTrip = FoodTrip(tempjsonFile)
         
#         print("Trip meters from : " + str(origin.address) + " " + str(place.address) 
#               + " " + str(tempFoodTrip.totalDistance))
        
        if tempFoodTrip.totalDistance <= meters:
            newPlaces.append(place)
    
    return newPlaces
# filterDuration is a set with a bool and int seconds
# filterMiles is a set with a bool and int miles
# data is a list of lists of places
def processListData(filterDuration = (False, None), filterMiles = (False, None), data: list,
                    origin):
    refinedData = data
    if filterDuration:
        refinedData = filterPlacesByDuration(refinedData, origin, filterDuration[1])
    if filterMiles:
        refinedData = filterPlacesByMiles(refinedData, origin, filterMiles[1])
    
    places = []
    
    index = 1
    for listOfPlaces in data:
        if not places:
            # starting place
            places.append(data[0][0])
        places.append(findClosestDestination(listOfPlaces, places[index]))
    return places
    

def _test():
    startingPlace = Place("Starting point", "Fresno, CA")
    place1 = Place("Location 1", "San Jose, CA")
    place2 = Place("Location 2", "Los Angeles, CA")
    place3 = Place("Location 3", "Irvine, CA")
     
    listOfPlaces = [place1, place2, place3]
    
#     filteredPlaces = filterPlacesByDuration(listOfPlaces, startingPlace, 30000)
    filteredPlaces = filterPlacesByMiles(listOfPlaces, startingPlace, 353910/1609.344)
    for place in filteredPlaces:
        place.print()
#     print(findClosestDestination(listOfPlaces, startingPlace).name)
    
#     jsonFile = getResult(createUrl("Chicago,IL", "Los Angeles,CA"))
#     print(json.dumps(jsonFile))

def main():
    if _testing:
        _test()
    
main()

