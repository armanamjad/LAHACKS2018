from django import forms

class LocationForm (forms.Form):
    location = forms.CharField(label='location', max_length = 100)
    distance = forms.IntegerField( label = 'distance' )
    