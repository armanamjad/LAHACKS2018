# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from .models import Restaurant, Way, Route
# Create your views here.
def index(request):
    index = 1
    #restList refers to the full list of restaurants that the user wants to visit
    restList = Restaurant.objects.all()
    # routeList is the routes corresponding to each restaurant from the user's current location
    # each route is made up of individual Ways stored as one to many in the database
    # the ways are sorted in order by their pk
    routeList = Route.objects.all()
    wayList = []
    curRoute = Route.objects.get(pk = index)

    context = {'restList':restList, }
    return render(request, 'index.html', context)

