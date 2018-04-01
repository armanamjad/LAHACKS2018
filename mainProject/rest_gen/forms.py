from django import forms

class LocationForm (forms.Form):
    location = forms.CharField(label='location', max_length = 100)
    distance = forms.IntegerField( label = 'distance' )
    b = forms.ChoiceField(choices={(1, 'Breakfast')} , widget=forms.RadioSelect(), label = 'b')
    l = forms.ChoiceField(choices={(2, 'Lunch')}, widget=forms.RadioSelect(),label = 'l')
    d = forms.ChoiceField(choices={(3, 'Dinner')}, widget=forms.RadioSelect(),label = 'd')
    