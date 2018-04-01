import json
import urllib.parse
import urllib.request
import zomato_data
import random
from foodTripClasses import FoodTrip
from foodTripClasses import Place
from _random import Random
apiKey = "key=AIzaSyCR0MK8AsrhicE-TGn366RDbuKkQ1RgVRg"
googleMapImgApi = "key=AIzaSyB72MtN4g3WeFk6WNH3fM08_M_nGCAmYsk"
_testing = False


def createUrl(org: str, dest: str, wayPoints: list = []):
    # Formatting
    org = org.replace(" ", "+")
    dest = dest.replace(" ", "+")
    
    # declaring strings that will make up the url
    url = "https://maps.googleapis.com/maps/api/directions/json?"
    origin = "origin=" + org
    destination = "destination=" + dest
    waypts = "waypoints="
    
    if len(wayPoints) == 0:
        return url + origin + "&" + destination + "&" + apiKey
    else:
        for waypoint in wayPoints:
            waypts += ":via"
            waypts += waypoint.address.replace(" ", "+")
            waypts += "|"
        
        waypts = waypts[:-1]
        return url + origin + "&" + destination + "&" + waypts + "&" + apiKey
    
def createMapImgUrl(org: str, dest: str, wayPoints: list = []):
    org = org.replace(" ", "+")
    dest = dest.replace(" ", "+")
    
    url = "https://www.google.com/maps/embed/v1/directions?" + googleMapImgApi
    origin = "origin=" + org
    destination = "destination=" + dest
    waypts = "waypoints="
    
    if len(wayPoints) == 0:
        return url + origin + "&" + destination + "&" + apiKey
    else:
        for waypoint in wayPoints:
            waypts += waypoint.address.replace(" ", "+")
            waypts += waypoint.address.replace("Avenue", "Ave")
            waypts += "|"
        
        waypts = waypts[:-1]
        return url + "&" + origin + "&" + destination + "&" + waypts
    
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
def processListData(data: list, origin, randomStartingPoint = False, filterDuration = False, 
                    duration = 0, filterMiles = False, miles = 0):

    places = []
    # randomly generates an index so that starting place will be random
    index = 0
    if randomStartingPoint:
        index = random.randrange(0, len(data[0]))
    places.append(data[0][index])
    recentPlace = data[0][index]
    data.remove(data[0])
    for listOfPlaces in data:
        # gets closest place to the most recent place added to places
        closestPlace = findClosestDestination(listOfPlaces, recentPlace, places)
        places.append(closestPlace)
        recentPlace = closestPlace
    return places

# convert meters to miles
def convertMetersToMiles(meters):
    return meters / 1609.34

# convert seconds to days hours minutes
def convertSecondsToDHM(seconds):
    days = int(seconds/86400)
    remaining = seconds%86400
    hours = int(remaining/3600)
    remaining = remaining%3600
    minutes = int(remaining/60)
    return days, hours, minutes

def getFullTripStats(places: list, originAddress: str):
    # gets rid of beginning and ending of the places list
    copyOfPlaces = []
    for num in range(0, len(places) - 1):
        copyOfPlaces.append(places[num])
#     copyOfPlaces.pop(len(copyOfPlaces) - 1)
    jsonFile = getResult(createUrl(originAddress, places[len(places) - 1].address, copyOfPlaces))
    time = 0
    for leg in jsonFile['routes'][0]['legs']:
        time += int(leg['duration']['value'])
    distance = 0
    for leg in jsonFile['routes'][0]['legs']:
        distance += int(leg['distance']['value'])
    
#     print(json.dumps(jsonFile))
    foodTrip = FoodTrip(jsonFile)
    mapImgUrl = createMapImgUrl(originAddress, places[len(places) - 1].address, copyOfPlaces)
    return time, distance, mapImgUrl

def getLatLng(address):
    tempjsonFile = getResult(createUrl(address, address))
#     print(json.dumps(tempjsonFile))
    latLng = tempjsonFile['routes'][0]['legs'][0]['steps'][0]['start_location']
    return latLng["lat"], latLng["lng"]

def _test():
#     jsonFile = getResult("https://maps.googleapis.com/maps/api/directions/json?origin=Boston,MA&destination=Concord,MA&waypoints=Charlestown,MA|Lexington,MA&key=")
    org = Place("1", "5507 Don Rodolfo Ct, San Jose, CA 95123")
    place1 = Place("2", "140 E San Carlos St, San Jose, CA 95112")
    place2 = Place("3", "302 S Market St, San Jose, CA 95113")
    dest = Place("4", "505 E San Carlos St, San Jose, CA 95112")
    print(createUrl(org.address, dest.address, 
                                   [place1, place2]))
    jsonFile = getResult(createUrl(org.address, dest.address, 
                                   [place1, place2]))
#     print(json.dumps(jsonFile))
    trip = FoodTrip(jsonFile)
    totalDistance = trip.totalDistance
    t = 0
    for leg in jsonFile['routes'][0]['legs']:
        t += int(leg['duration']['value'])
    time = convertSecondsToDHM(t)
    print("Total time of the trip is " + str(time[0]) + " days " + 
              str(time[1]) + " hours " + str(time[2]) + " minutes")
    print("Total distance in miles is " + str(convertMetersToMiles(totalDistance)))
#     startingPlace = Place("Starting point", "Fresno, CA")
#     place1 = Place("Location 1", "San Jose, CA")
#     place2 = Place("Location 2", "Los Angeles, CA")
#     place3 = Place("Location 3", "Irvine, CA")
#     place4 = Place("Location 4", "San Francisco, C             dc  cfx5r cfdcfdcfd cfdfdcdfgr454eA")
#      
#     wayPoints = [place1, place2, place3, place4]
#     totalTime, totalDistance = getFullTripStats(wayPoints, startingPlace.address)
#     time = convertSecondsToDHM(totalTime)
#     print("Total time of the trip is " + str(time[0]) + " days " + 
#               str(time[1]) + " hours " + str(time[2]) + " minutes")
#     print("Total distance in miles is " + str(convertMetersToMiles(totalDistance)))
    
    
#     filteredPlaces = filterPlacesByDuration(listOfPlaces, startingPlace, 30000)
#     filteredPlaces = filterPlacesByMiles(listOfPlaces, startingPlace, 353910/1609.344)
#     for place in filteredPlaces:
#         place.print()
#     print(findClosestDestination(listOfPlaces, startingPlace).name)
    
#     jsonFile = getResult(createUrl("Chicago,IL", "Los Angeles,CA"))
#     print(json.dumps(jsonFile))

def generatePlaces(info):
    startingAddress = info[0]
    distance = info[1]
    categories = info[2]
    category_info = [False, False, False]
    for c in categories:
        if c == 'Breakfast':
            category_info[0] = True
        elif c == 'Lunch':
            category_info[1] = True
        elif c == 'Dinner':
            category_info[2] = True
    cuisineList = info[3]
    city = zomato_data.get_city_name(startingAddress)
    
    startingPlace = Place("Starting place", startingAddress)
    startingPlace.lat, startingPlace.lng = getLatLng(startingPlace.address)
        
    listOflistOfPlaces = zomato_data.get_restaurants_in_city(city, categories, 
                                                             cuisines = cuisineList)
    listOflistOfPlaces = zomato_data.rm_far_restaurants(listOflistOfPlaces, 
                                                            startingPlace.lat, 
                                                            startingPlace.lng, distance)
    refinedList = processListData(listOflistOfPlaces, startingPlace, True)
    
    totalTime, totalDistance, mapImgUrl = getFullTripStats(refinedList, startingPlace.address)
    time = convertSecondsToDHM(totalTime)
    i = 0
    for x in range (category_info):
        if(category_info[x]):
            category_info[x] = refinedList[i]
            i+=1
        else:
            category_info[x] = None
    return category_info

def main():
    if _testing:
        _test()
    else:
        startingPlace = Place("Location 1", 
                                      "5507 Don Rodolfo Ct, San Jose, CA 95123")
        categories = ["Breakfast", "Lunch", "Dinner"]
        cuisineList = ["Pizza", "Mexican"]
         
        startingPlace.lat, startingPlace.lng = getLatLng(startingPlace.address)
         
        listOflistOfPlaces = zomato_data.get_restaurants_in_city("Los Angeles", categories,
                                                                 cuisines=cuisineList)
        listOflistOfPlaces = zomato_data.rm_far_restaurants(listOflistOfPlaces, 
                                                            startingPlace.lat, 
                                                            startingPlace.lng, 1000000000)
              
        refinedList = processListData(listOflistOfPlaces, startingPlace, True)
        for place in refinedList:
            if not place.imageUrl == "":
                print(place.address, place.imageUrl)
            else:
                print(place.name + " does not have an image")
           
        totalTime, totalDistance, mapImgUrl = getFullTripStats(refinedList, startingPlace.address)
        time = convertSecondsToDHM(totalTime)
        print("Total time of the trip is " + str(time[0]) + " days " + 
              str(time[1]) + " hours " + str(time[2]) + " minutes")
        print("Total distance in miles is " + str(convertMetersToMiles(totalDistance)))
    
# main()

