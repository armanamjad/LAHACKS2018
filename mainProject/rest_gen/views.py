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
        m = []
        form = LocationForm(request.POST)
        if(form.is_valid()):
            m = form.cleaned_data
        input = ( m )
        request.session['data'] = input
        return HttpResponseRedirect('loading/')
    else:
        form = LocationForm()    
    context = {'location':location,'distance':distance,'form' : form }
    return render(request, 'rest_gen/index.html', context)

def loading(request):
    data = request.session['data']
    context = {'data':data}
    #restaurants = request.session['rest']
    return render(request, 'rest_gen/loading.html', context)

def results(request):
   # restList = request.session['rest']
    context = {}
    return render(request, 'rest_gen/results.html', context)

def detail(request, restaurant_id):
    r = Restaurant.objects.get(pk = restaurant_id)
    context = { 'name': r.m_name , 'address': r.m_address}
    return render(request, 'rest_gen/detail.html', context)
    
def selection(request, choicelist : list, maxDist, start):
    return 1



