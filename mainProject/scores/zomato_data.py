import json
import urllib.parse
import requests
from foodTripClasses import Place

ZOMATO_API_KEY = 'a7067b73018e25cbaa491cb3964081c6'
BASE_ZOMATO_URL = 'https://developers.zomato.com/api/v2.1'

#Not using anymore
def get_result(url: str) -> dict:
    response = None
    try:
        response = urllib.request.urlopen(url)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)
    finally:
        if response != None:
            response.close()

#Returns json dictionary with data for categories
def get_category_data():
    url = BASE_ZOMATO_URL + '/categories'
    data = None
    new_request = requests.get(url, headers={'user-key' : ZOMATO_API_KEY})
    if new_request.ok:
        data = new_request.json()
    return data

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

#Returns list of lists of restaurants, one list per category
def get_restaurants_in_city(city: str, categories: list):
    cat_ids = []
    for c in categories:
        cat_ids.append(str(get_category_id(c)))
    restaurants_list = []
    for c in cat_ids:
        data = None
        query_parameters = [('entity_id', get_city_id(city)), ('entity_type', 'city'), ('category', c), ('sort', 'rating'), ('count', 5)]
        url = BASE_ZOMATO_URL + '/search?'+ urllib.parse.urlencode(query_parameters)
        new_request = requests.get(url, headers={'user-key' : ZOMATO_API_KEY})
        if new_request.ok:
            data = new_request.json()
        restaurants = []
        for r in [restaurant['restaurant'] for restaurant in data['restaurants']]:
            score = int(float(r['user_rating']['aggregate_rating']) * 10)
            restaurants.append(Place(r['name'], r['location']['address'], score))
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