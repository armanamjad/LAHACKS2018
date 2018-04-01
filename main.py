import json
import urllib.parse
import urllib.request
import zomato_data
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
# finds closest place by comparing duration
def findClosestDestination(places: list, origin: Place, visitedPlaces):
    placesNames = [place.name for place in visitedPlaces]
    closestPlace = None
    minDuration = None
    tempFoodTrip = None
    
    # loops through a list of places
    for place in places:
        if not place.name in placesNames:
            tempjsonFile = getResult(createUrl(origin.address, place.address))
            tempFoodTrip = FoodTrip(tempjsonFile)
            
            # compares duration of temporary trips
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
# def filterPlacesByDuration(places: list, origin: Place, duration: int):
#     newPlaces = []
#     
#     for place in places:
#         tempjsonFile = getResult(createUrl(origin.address, place.address))
#         tempFoodTrip = FoodTrip(tempjsonFile)
#         if tempFoodTrip.duration <= duration:
#             newPlaces.append(place)
#             
#     return newPlaces

# def filterPlacesByMiles(places: list, origin: Place, miles: int):
#     meters = miles * 1609.344
# #     print("total meters: " + str(meters))
#     newPlaces = []
#     
#     for place in places:
#         tempjsonFile = getResult(createUrl(origin.address, place.address))
#         tempFoodTrip = FoodTrip(tempjsonFile)
#          
# #         print("Trip meters from : " + str(origin.address) + " " + str(place.address) 
# #               + " " + str(tempFoodTrip.totalDistance))
#         
#         if tempFoodTrip.totalDistance <= meters:
#             newPlaces.append(place)
#     
#     return newPlaces
# filterDuration is a set with a bool and int seconds
# filterMiles is a set with a bool and int miles
# data is a list of lists of places
def processListData(data: list, origin, 
                    filterDuration = False, duration = 0, filterMiles = False, miles = 0):
#     refinedData = data
#     if filterDuration:
#         for l in data:
#             l = filterPlacesByDuration(l, origin, duration)
#     if filterMiles:
#         for l in data:
#             l = filterPlacesByMiles(l, origin, miles)
    places = []
    places.append(data[0][0])
    recentPlace = data[0][0]
    data.remove(data[0])
    for listOfPlaces in data:
        # gets closest place to the most recent place added to places
        closestPlace = findClosestDestination(listOfPlaces, recentPlace, places)
        places.append(closestPlace)
        recentPlace = closestPlace
    return places
    
def getLatLong(address):
    tempjsonFile = getResult(createUrl(address, address))
    tempFoodTrip = FoodTrip(tempjsonFile)
    latlong = tempjsonFile['routes'][0]['legs'][0]['steps'][0]['start_location']
    return latlong["lat"], latlong["lng"]

def _test():
    startingPlace = Place("Starting point", "Fresno, CA")
    place1 = Place("Location 1", "San Jose, CA")
    place2 = Place("Location 2", "Los Angeles, CA")
    place3 = Place("Location 3", "Irvine, CA")
     
    listOfPlaces = [place1, place2, place3]
    
#     filteredPlaces = filterPlacesByDuration(listOfPlaces, startingPlace, 30000)
#     filteredPlaces = filterPlacesByMiles(listOfPlaces, startingPlace, 353910/1609.344)
#     for place in filteredPlaces:
#         place.print()
#     print(findClosestDestination(listOfPlaces, startingPlace).name)
    
#     jsonFile = getResult(createUrl("Chicago,IL", "Los Angeles,CA"))
#     print(json.dumps(jsonFile))

def getRestaurants():
    categories = ["Breakfast", "Lunch", "Dinner"]
    listOflistOfPlaces = zomato_data.get_restaurants_in_city("Irvine", categories)
    startingPlace = Place("Location 1", "1043 West Peltason Dr Irvine, CA")
    return processListData(listOflistOfPlaces, startingPlace)

def main():
    if _testing:
        _test()
    
<<<<<<< HEAD
    refinedList = getRestaurants()
    for place in refinedList:
        print(place.name)
=======
#     categories = ["Breakfast", "Lunch", "Dinner"]
#     listOflistOfPlaces = zomato_data.get_restaurants_in_city("Orange County", categories)
#     startingPlace = Place("Location 1", 
#                                   "1043 West Peltason Dr Irvine, CA")
#     
#     refinedList = processListData(listOflistOfPlaces, startingPlace)
#     for place in refinedList:
#         print(place.name)
    lat, lng = getLatLong("5507 Don Rodolfo San Jose, CA")
    print(lat, lng)

>>>>>>> f9b8babcc43b947f44b924b44ee7d17731f714cb
    
main()
