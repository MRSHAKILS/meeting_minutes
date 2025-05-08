from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('minutes/', views.minutes, name='minutes'),
    path("logout/", views.logout, name="logout"),
]
