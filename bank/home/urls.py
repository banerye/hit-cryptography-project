from django.urls import path
from home import views


urlpatterns = [
    path(r'', views.index, name='index'),  # index front
]