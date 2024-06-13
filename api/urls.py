from django.urls import path
from home.views import *

urlpatterns = [
    path('index/', index,name='index'),
    path('person/', person,name='perosn'),
    path('classperson/',ClassPerson.as_view(),name='classperson'),
    path('register/',Register.as_view(),name='register'),
    path('login/',Login.as_view(),name='login'),
]
