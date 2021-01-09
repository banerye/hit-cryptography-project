from django.urls import path
from users import views


urlpatterns = [
    path(r'register/', views.register, name='register'),  # user register front
    path(r'register_handle/', views.register_handle, name='register_handle'),  # deal with user register

    path(r'login/', views.login, name='login'),  # user login front
    path(r'login_handle/', views.login_handle, name='login_handle'),  # deal with user login

    path(r'logout/', views.logout, name='logout'),

    path(r'account/', views.check_account, name='check_account'),
    path(r'get_records/', views.get_records, name='get_records'),
    path(r'upload_publickey/', views.upload_publickey, name='upload_publickey'),
]