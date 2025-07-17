from django.contrib import admin
from django.urls import path, include
from clinicapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('clinicapp.urls')),
]
