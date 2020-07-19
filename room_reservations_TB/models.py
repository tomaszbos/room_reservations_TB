from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    room_capacity = models.PositiveIntegerField()
    room_projector = models.BooleanField()
    room_description = models.TextField(blank=True)

    def __str__(self):
        return self.room_name, self.room_capacity, self.room_projector
