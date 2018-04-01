from django.shortcuts import render

def index(request):
	return render(request, 'foodapp/index.html')

def loading(request):
	return render(request, 'foodapp/loading.html')

def results(request):
	return render(request, 'foodapp/results.html')


