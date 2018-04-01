from django import forms
from django.forms import widgets

class LocationForm (forms.Form):
    location = forms.CharField(label='location', max_length = 100)
    distance = forms.IntegerField( label = 'distance')
    meal = forms.MultipleChoiceField(choices = {('Lunch','Lunch'),('Breakfast','Breakfast'),('Dinner','Dinner')}, label = 'meals', widget = widgets.CheckboxSelectMultiple())
        
    cuisine = forms.MultipleChoiceField(
        choices = { ('American','American'),('Asian','Asian'),('Desserts','Desserts'),
        ('Bubble Tea','Boba'),('Italian','Italian'),('Mexican','Mexican'),('Indian','Indian') }
        , label = 'cuisine', widget = widgets.CheckboxSelectMultiple())

    