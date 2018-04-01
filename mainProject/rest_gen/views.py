# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Restaurant, Way, Route
from .models import use
from .forms import LocationForm

# Create your views here.
def index(request):
    location = ""
    distance = 0
    if request.method == 'POST':
        input = ( request.POST.get('location', None), request.POST.get('distance', None) )

        return HttpResponseRedirect('results/')
    else:
        form = LocationForm()    
    context = {'location':location,'distance':distance,'form' : form }
    return render(request, 'rest_gen/index.html', context)

def loading(request):
    context = {}
    return render(request, 'rest_gen/loading.html', context)

def results(request):
    context = {}
    return render(request, 'rest_gen/results.html', context)

def detail(request, restaurant_id):
    r = Restaurant.objects.get(pk = restaurant_id)
    context = { 'name': r.m_name , 'address': r.m_address}
    return render(request, 'rest_gen/detail.html', context)
    
def selection(request, choicelist : list, maxDist, start):
    return 1



