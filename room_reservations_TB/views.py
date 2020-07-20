from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import View
from datetime import datetime

from room_reservations_TB.models import Room, Reservation
from room_reservations_TB.forms import NewRoomForm, ReservationForm, SearchForm


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
            if room_name == '':
                text = '''
                        Conference room name cannot be empty!
                        <p><a href="/main/">Main menu</a></p>
                    '''
                return HttpResponse(text)
            name_to_check = Room.objects.filter(room_name=room_name)
            if name_to_check:
                text = '''
                        Conference room name already exists!
                        Choose another name!
                        <p><a href="/main/">Main menu</a></p>
                    '''
                return HttpResponse(text)
            room_capacity = form.cleaned_data['room_capacity']
            if room_capacity <= 0:
                text = '''
                        Conference room capacity invalid!
                        Choose capacity of people bigger than zero!
                        <p><a href="/main/">Main menu</a></p>
                    '''
                return HttpResponse(text)
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
        if not all_rooms:
            text = '''
                No conference rooms available!
                <p><a href="/main/">Main menu</a></p>
            '''
            return HttpResponse(text)
        today_reservations = Reservation.objects.filter(reservation_date=datetime.now())
        reservations = all_rooms.filter(pk__contains=today_reservations.values('room_id'))
        context['rooms'] = all_rooms
        context['reservations'] = reservations
        return render(request, 'room_list.html', context)


class RoomDetails(View):
    def get(self, request, room_id):
        context = {}
        room = Room.objects.get(pk=room_id)
        reservations = Reservation.objects.filter(room_id=room_id, reservation_date__gte=datetime.now())
        context['room'] = room
        context['reservations'] = reservations
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
            if room_name == '':
                text = '''
                        Conference room name cannot be empty!
                        <p><a href="/main/">Main menu</a></p>
                    '''
                return HttpResponse(text)
            name_to_check = Room.objects.filter(room_name=room_name).exclude(pk=room_id)
            if name_to_check:
                text = '''
                        Conference room name already exists!
                        Choose another name!
                        <p><a href="/main/">Main menu</a></p>
                    '''
                return HttpResponse(text)
            room_capacity = form.cleaned_data['room_capacity']
            if room_capacity <= 0:
                text = '''
                        Conference room capacity invalid!
                        Choose capacity of people bigger than zero!
                        <p><a href="/main/">Main menu</a></p>
                    '''
                return HttpResponse(text)
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


class RoomReservation(View):
    form = ReservationForm

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        reservations = Reservation.objects.filter(room_id=room_id)
        context = {"room_id": room.pk, "reservation_date": datetime.now(), 'room': room}
        return render(request, 'reserve_room.html', {'form': self.form(context), 'reservations': reservations})

    def post(self, request, room_id):  # TODO: clarify room_id being sent by post method
        data = request.POST
        form = self.form(data)
        text = 'Wrong input!'
        if form.is_valid():
            reservation_date = form.cleaned_data['reservation_date']
            if reservation_date < datetime.date(datetime.now()).today():  # TODO: Too complicated - simplify
                text = '''
                Date from past! Choose proper date!
                <p><a href="/main/">Main menu</a></p>
            '''
                return HttpResponse(text)
            date_to_check = Reservation.objects.filter(room_id=room_id, reservation_date=reservation_date)
            if date_to_check:
                text = '''
                Conference room is unavailable at selected date!
                Choose another date.
                <p><a href="/main/">Main menu</a></p>
            '''
                return HttpResponse(text)
            room_id = form.cleaned_data['room_id']
            reservation_comment = form.cleaned_data['reservation_comment']
            Reservation.objects.create(
                reservation_date=reservation_date,
                room_id=room_id,
                reservation_comment=reservation_comment,
            )
            return redirect('all_rooms')
        return HttpResponse(text)


class RoomSearch(View):
    form = SearchForm

    def get(self, request):
        return render(request, 'room_search.html', {'form': self.form()})

    def post(self, request):
        context = {}
        data = request.POST
        form = self.form(data)
        text = 'Wrong input!'
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            room_capacity = form.cleaned_data['room_capacity']
            room_projector = form.cleaned_data['room_projector']
            searched_rooms = Room.objects.filter(
                Q(room_name__icontains=room_name),
                Q(room_capacity__gte=room_capacity),
                Q(room_projector__exact=room_projector) | Q(room_projector__exact=True),
            )
            context['rooms'] = searched_rooms
            if searched_rooms:
                text = '''
                No conference rooms meeting your criteria!
                <p><a href="/main/">Main menu</a></p>
            '''
                return HttpResponse(text)
            return render(request, 'room_list.html', context)
        return HttpResponse(text)
