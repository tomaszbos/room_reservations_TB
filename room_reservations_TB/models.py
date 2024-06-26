from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    room_capacity = models.PositiveIntegerField()
    room_projector = models.BooleanField()
    room_description = models.TextField(blank=True)

    def __str__(self):
        return self.room_name


class Reservation(models.Model):
    reservation_date = models.DateField()
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    reservation_comment = models.TextField(blank=True)

    class Meta:  # TODO: How Meta works?
        unique_together = ('room_id', 'reservation_date')

    def __str__(self):
        return str(self.reservation_date)

# desccryptor klasowy # TODO: check
# meta klasy
# admin.py TODO: learn admin functionalioty
