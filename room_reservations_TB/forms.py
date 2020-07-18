from django import forms


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
        required=True,
        label='Conference Room Projector Available',
    )
