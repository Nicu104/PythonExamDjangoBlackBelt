from django.urls import re_path
from . import views

urlpatterns = [
    # re_path('', views.index, name=''),
    re_path('^travels$', views.travel, name='travel'),
    
    re_path('^destination/(?P<id>\d+)$', views.destination, name='destination'),
    
    #pathway to form that creates a new trip
    re_path('^travels/addtrip$', views.addtrip, name='addtrip'),
    
    #pathway to method that takes data from form and creates a ne trip
    re_path('^createtrip$', views.createtrip, name='createtrip'),
    
    re_path('^travels/join/(?P<id>\d+)/$', views.jointrip, name='jointrip'),
    
    re_path('^travels/logout$', views.logout, name='logout'),       
    
    re_path('^createuser$', views.createuser, name='createuser'),
    
    re_path('^login$', views.login, name='login'),
    
    re_path('^$', views.index, name='home'),
]