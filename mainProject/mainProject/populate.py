import os
from rest_gen.models import Restaurant, Route, Way

def populate(rest_list):
    for i in len(rest_list):
        cur = rest_list[i]
        add_restaurant(cur.getName(), cur.getAddress(), cur.getScore())

def add_restaurant(name, address, score, image):
    r = Restaurant.objects.get_or_create(m_name = name, m_address=address, m_score = score)
    return r