"""room_reservations_TB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from room_reservations_TB import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', views.main_page, name='main'),
    path('room/new/', views.NewRoom.as_view(), name='new_room'),
    path('room/', views.AllRooms.as_view(), name='all_rooms'),
    path('room/<int:room_id>/', views.RoomDetails.as_view(), name=f'room'),
    path('room/modify/<int:room_id>/', views.RoomEdit.as_view(), name=f'edit_room'),
    path('room/delete/<int:room_id>/', views.RoomDelete.as_view(), name=f'delete_room'),
    path('room/reserve/<int:room_id>/', views.RoomReservation.as_view(), name=f'reserve_room'),
    path('room/search/', views.RoomSearch.as_view(), name='search_rooms'),
]
