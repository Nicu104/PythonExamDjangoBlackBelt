

from django.urls import path, include

urlpatterns = [
    path('', include(('apps.mainapp.urls', 'users'), namespace='users')),
]
