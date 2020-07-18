from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from room_reservations_TB.models import Room
from room_reservations_TB.forms import NewRoomForm


def main_page(request):
    return render(request, 'main_page.html', {})



# Utwórz widok, pozwalający na dodanie nowej sali. Umieść go pod adresem /room/new/. Widok powinien:
#
#     po wejściu metodą GET wyświetlić formularz zawierający następujące pola:
#         nazwa sali – tekst,
#         pojemność sali – liczba,
#         dostępność rzutnika – checkbox.
#     po wejściu metodą POST:
#         sprawdzić, czy nazwa sali, nie jest pusta,
#         sprawdzić, czy sala o podanej nazwie, nie istnieje już w bazie danych,
#         sprawdzić, czy pojemność sali jest liczbą dodatnią;
#         jeśli dane są poprawne, zapisać nową salę do bazy i przekierować użytkownika na stronę główną,
#         jeśli są niepoprawne, powinien wyświetlić użytkownikowi odpowiedni komunikat.
#
# Pamiętaj, żeby dodać odpowiedni wpis do pliku urls.py. Uzupełnij też odpowiedni link w szablonie bazowym.
class NewRoom(View):
    def get(self, request):
        form = NewRoomForm()
        return render(request, 'new_room.html', {'form': form})

    def post(self, request):
        data = request.POST
        form = NewRoomForm(data)
        text = 'No data!'
        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            room_capacity = form.cleaned_data['room_capacity']
            room_projector = form.cleaned.data['room_projector']
            Room.objects.create(
                room_name=room_name,
                room_capacity=room_capacity,
                room_projector=room_projector,
            )
            text = f'Room {room_name} with capacity of {room_capacity} people and projector availability as {room_projector} added.'
        return HttpResponse(text)
