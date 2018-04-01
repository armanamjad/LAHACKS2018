from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:restaurant_id>/', views.detail, name = 'detail'),
    path( 'loading/', views.loading, name = 'loading' )
]
