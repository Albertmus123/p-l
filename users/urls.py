from django.urls import path,re_path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('login', CustomLoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout') ,  
    path('sign-up', create_user, name="create_user"),
    path('dashboard',dashboard, name="dashboard"),
    path('password_reset/', forget_password, name='password_reset'),
    re_path(r'^password_reset_form/(?P<token>[-a-zA-Z0-9_.]+)/$',reset_form, name='password_reset_form')
]