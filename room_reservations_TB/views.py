from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from room_reservations_TB.models import Room
from room_reservations_TB.forms import NewRoomForm


def main_page(request):
    return render(request, 'main_page.html', {})


#     po wejściu metodą POST:
#         sprawdzić, czy nazwa sali, nie jest pusta,
#         sprawdzić, czy sala o podanej nazwie, nie istnieje już w bazie danych,
#         sprawdzić, czy pojemność sali jest liczbą dodatnią;
#         jeśli dane są poprawne, zapisać nową salę do bazy i przekierować użytkownika na stronę główną,
#         jeśli są niepoprawne, powinien wyświetlić użytkownikowi odpowiedni komunikat.
#
# Pamiętaj, żeby dodać odpowiedni wpis do pliku urls.py. Uzupełnij też odpowiedni link w szablonie bazowym.
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
            Room.objects.create(
                room_name=room_name,
                room_capacity=room_capacity,
                room_projector=room_projector,
            )
            text = f'Room {room_name} with capacity of {room_capacity} people and projector availability as {room_projector} added.'
        return HttpResponse(text)


class AllRooms(View):
    def get(self, request):
        context = {}
        all_rooms = Room.objects.all()
        context['rooms'] = all_rooms
        return render(request, 'room_list.html', context)
