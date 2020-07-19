from django import forms

from room_reservations_TB.models import Room


class NewRoomForm(forms.Form):
    room_name = forms.CharField(
        required=True,
        label='Conference Room Name',
        widget=forms.TextInput(attrs={'placeholder': 'Conference Room Name'}),
    )
    room_capacity = forms.IntegerField(
        required=True,
        label='Conference Room Capacity',
        initial=0,
    )
    room_projector = forms.BooleanField(
        required=False,
        label='Conference Room Projector Available',
    )

    room_description = forms.CharField(
        required=False,
        label='Conference Room Description',
        widget=forms.Textarea(attrs={'placeholder': 'Conference Room Description'}),
    )


class ReservationForm(forms.Form):
    reservation_date = forms.DateField(
        required=True,
        label='Reservation Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    room_id = forms.ModelChoiceField(
        queryset=Room.objects.all(),
    )
    reservation_comment = forms.CharField(
        required=False,
        label='Reservation comment',
        widget=forms.Textarea(attrs={'placeholder': 'Reservation comment'}),
    )


class SearchForm(forms.Form):
    room_name = forms.CharField(
        required=False,
        label='Conference Room Name',
        widget=forms.TextInput(attrs={'placeholder': 'Conference Room Name'}),
    )
    room_capacity = forms.IntegerField(
        required=True,
        label='Conference Room Capacity',
        initial=0,
    )
    room_projector = forms.BooleanField(
        required=False,
        label='Conference Room Projector Available',
    )
