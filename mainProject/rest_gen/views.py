# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Restaurant, Way, Route
from .models import use
from .forms import LocationForm
from .main import generatePlaces


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
        return HttpResponseRedirect('results/')
    else:
        form = LocationForm()    
    context = {'location':location,'distance':distance,'form' : form }
    return render(request, 'rest_gen/index.html', context)

#5507 Don Rodolfo Ct, San Jose, CA 95123

def results(request):
    dat = request.session['data']
    #turn into normal list
    data = [0,0,0,0]
    data[0]= dat['location'] 
    data[1]=dat['distance'] 
    data[2]=dat['meal'] 
    data[3]=dat['cuisine'] 
    places = generatePlaces(data)
    nameList = []
    addressList = []
    urls = []
    # 1 is breakfast, 2 is lunch, 3 is dinner
    for i in range(0,2):
        nameList.append(places[i].name)
        addressList.append(places[i].address)
        urls.append(places[i].imageUrl)

    context = { 'name' : nameList, 'address' : addressList, 'url' : urls }
    return render(request, 'rest_gen/results.html', context)



