from django.contrib import admin
from django.urls import path
from .views import signup_view, login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signup_view, name='home'),       
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
]
