"""
URL configuration for flightReservation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from flightApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("add-flight/",views.add_flight),
    path("view-flights/",views.fetch_filghts),
    path("update-flight/<int:pk>",views.update_fight),
    path("delete-flight/<int:pk>",views.delete_filght),
    path("add-passenger/",views.add_passenger),
    path("view-passengers/",views.fetch_passengers),
    path("update-passenger/<int:pk>",views.update_passenger),
    path("delete-passenger/<int:pk>",views.delete_passenger),
    path("book-flight/",views.book_flight),
    path("cancel-flight/",views.cancel_flight),
    
]


