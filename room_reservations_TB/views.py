from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from room_reservations_TB.models import Room
from room_reservations_TB.forms import NewRoomForm


def main_page(request):
    return render(request, 'main_page.html', {})


class NewRoom(View):
    form = NewRoomForm

    def get(self, request):
        return render(request, 'new_room.html', {'form': self.form()})

    def post(self, request):
        data = request.POST
        form = self.form(data)
        text = 'Wrong input!'
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            room_capacity = form.cleaned_data['room_capacity']
            room_projector = form.cleaned_data['room_projector']
            room_description = form.cleaned_data['room_description']
            Room.objects.create(
                room_name=room_name,
                room_capacity=room_capacity,
                room_projector=room_projector,
                room_description=room_description,
            )
            return redirect('all_rooms')
        return HttpResponse(text)


class AllRooms(View):
    def get(self, request):
        context = {}
        all_rooms = Room.objects.all()
        context['rooms'] = all_rooms
        return render(request, 'room_list.html', context)


class RoomDetails(View):
    def get(self, request, room_id):
        context = {}
        room = Room.objects.get(pk=room_id)
        context['room'] = room
        return render(request, 'room_details.html', context)


class RoomEdit(View):
    form = NewRoomForm

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        context = {"room_name": room.room_name, "room_capacity": room.room_capacity,
                   "room_projector": room.room_projector, "room_description": room.room_description, 'room': room}
        return render(request, 'new_room.html', {'form': self.form(context)})

    def post(self, request, room_id):
        data = request.POST
        form = self.form(data)
        text = 'Wrong input!'
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            room_capacity = form.cleaned_data['room_capacity']
            room_projector = form.cleaned_data['room_projector']
            room_description = form.cleaned_data['room_description']
            Room.objects.filter(pk=room_id).update(
                room_name=room_name,
                room_capacity=room_capacity,
                room_projector=room_projector,
                room_description=room_description,
            )
            return redirect('all_rooms')
        return HttpResponse(text)


class RoomDelete(View):
    def get(self, request, room_id):
        Room.objects.filter(pk=room_id).delete()
        return redirect('all_rooms')
