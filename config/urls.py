from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.conf.urls import handler404
from django.shortcuts import render
from django.http import Http404



def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

handler404 = custom_404_view