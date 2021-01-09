from django.urls import path, re_path
from payment import views


urlpatterns = [
    re_path(r'^detail/(?P<ciphertext>.*)/$', views.detail, name='detail'),
    path(r'check/', views.check, name='check')
]