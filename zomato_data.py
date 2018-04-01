import json
import urllib.parse
import requests
import math
from foodTripClasses import Place

ZOMATO_API_KEY = 'bc2be972d9dca5ccff701e7d84b7a221'
BASE_ZOMATO_URL = 'https://developers.zomato.com/api/v2.1'

#Returns json dictionary with data for categories
def get_category_data():
    url = BASE_ZOMATO_URL + '/categories'
    data = None
    new_request = requests.get(url, headers={'user-key' : ZOMATO_API_KEY})
    if new_request.ok:
        data = new_request.json()
    return data

#Returns list of all the categories on zomato
def get_category_list():
    data = get_category_data()
    return [c['categories']['name'] for c in data['categories']]

#Returns dictionary with keys of cuisines on zomato whose values are the id's
def get_cuisine_dict(city_name):
    data = None
    query_parameters = [('city_id', get_city_id(city_name))]
    url = BASE_ZOMATO_URL + '/cuisines?'+ urllib.parse.urlencode(query_parameters)
    new_request = requests.get(url, headers={'user-key' : ZOMATO_API_KEY})
    if new_request.ok:
        data = new_request.json()
    return {c['cuisine']['cuisine_name']: c['cuisine']['cuisine_id'] for c in data['cuisines']}

#Returns id number of given category name
def get_category_id(category: str):
    data = get_category_data()
    for c in data['categories']:
        if(category == c['categories']['name']):
            return c['categories']['id']
    return -1

#Returns id number of given city name
def get_city_id(city_name: str):
    data = None
    query_parameters = [('q', city_name)]
    url = BASE_ZOMATO_URL + '/cities?'+ urllib.parse.urlencode(query_parameters)
    new_request = requests.get(url, headers={'user-key' : ZOMATO_API_KEY})
    if new_request.ok:
        data = new_request.json()
    return data['location_suggestions'][0]['id']

#Calculates the distance between two latlong pairs
def latlng_to_distance(lat1, lng1, lat2, lng2):
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lng1 = math.radians(lng1)
    lng2 = math.radians(lng2)
    a = math.pow(math.sin((lat1-lat2)/2), 2) + math.cos(lat1)*math.cos(lat2)* math.pow(math.sin((lng1 - lng2)/2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371 * c

#Removes all restaurants farther than the radius
def rm_far_restaurants(restaurants: list, lat, lng, radius: int):
    new_list = [[]]
    i = 0
    for rl in restaurants:
        for r in rl:
            if(latlng_to_distance(lat, lng, r.lat, r.lng) < radius):
                new_list[i].append(r)
        i+=1
        new_list.append([])
    new_list.pop(len(new_list)-1)
    return new_list

def get_city_name(address: str):
    for i in range(len(address)):
        if address[i] == ',':
            break
    city = ''
    for j in range(i+2, len(address)):
        if address[j].isdigit():
            break
        else:
            city += address[j]
    city = city[:-4]
    return city

#Returns list of lists of restaurants, one list per category
def get_restaurants_in_city(city: str, categories: list, sort = "rating", order = 'desc', cuisines = []):
    cuis_ids = []
    if len(cuisines) != 0:
        cuis_dict = get_cuisine_dict(city)
        for c in cuisines:
            cuis_ids.append(str(cuis_dict[c]))
    cuisine = ','.join(cuis_ids)
    cat_ids = []
    for c in categories:
        cat_ids.append(str(get_category_id(c)))
    restaurants_list = []
    for c in cat_ids:
        data = None
        if(sort == "cost"):
            order = "asc"
        query_parameters = [('entity_id', get_city_id(city)), ('entity_type', 'city'), ('category', c), ('sort', sort), ('count', 20), ('order', order), ('cuisines', cuisine)]
        url = BASE_ZOMATO_URL + '/search?'+ urllib.parse.urlencode(query_parameters)
        new_request = requests.get(url, headers={'user-key' : ZOMATO_API_KEY})
        if new_request.ok:
            data = new_request.json()
        restaurants = []
        for r in [restaurant['restaurant'] for restaurant in data['restaurants']]:
            score = int(float(r['user_rating']['aggregate_rating']) * 10)
            restaurants.append(Place(r['name'], r['location']['address'], score, lat = float(r['location']['latitude']), lng = float(r['location']['longitude']), imageUrl = r['thumb']))
        restaurants_list.append(restaurants)
    return restaurants_list

#tests
'''
restaurants = get_restaurants_in_city('San Jose', ['Breakfast', 'Lunch', 'Dinner'])
for rl in restaurants:
    for r in rl:
        print('name:\t' + r.name + '\taddress:\t' + r.address + '\tscore:\t' + str(r.score))
    print()
    print()
'''
#print(get_category_list())
'''
for k, v in get_cuisine_dict('Stockton').items():
    print(k, v)
    '''
