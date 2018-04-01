from django import forms
from django.forms import widgets

class LocationForm (forms.Form):
    location = forms.CharField(label='location', max_length = 100)
    distance = forms.IntegerField( label = 'distance' )
    meal = forms.MultipleChoiceField(choices = {('1','Breakfast'),('2','Lunch'),('3','Dinner')}, label = 'meals', widget = widgets.CheckboxSelectMultiple())
    