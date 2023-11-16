from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('login', CustomLoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout') ,  
    path('sign-up', create_user, name="create_user"),
    path('dashboard',dashboard, name="dashboard"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')

]