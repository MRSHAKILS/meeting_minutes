from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('minutes/', views.minutes, name='minutes'),
    path("logout/", views.logout, name="logout"),
    path('minutes/<int:pk>/delete/', views.delete_minutes, name='delete_minutes'),

    path('edit/<int:pk>/', views.edit_minutes, name='edit_minutes'),
    path("minutes/<int:pk>/", views.minutes_detail, name="minutes_detail"),
]
