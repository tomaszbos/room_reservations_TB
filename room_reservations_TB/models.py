from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    room_capacity = models.IntegerField()
    room_projector = models.BooleanField()

    def __str__(self):
        return self.room_name, self.room_capacity, self.room_projector
