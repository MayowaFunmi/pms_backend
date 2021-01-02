from django.db import models

# Create your models here.
class Building(models.Model):
    building_number = models.SmallIntegerField()


class Floor(models.Model):
    building_no = models.OneToOneField(Building, on_delete=models.CASCADE)
    floor_number = models.SmallIntegerField()


class Room(models.Model):
    building_no = models.OneToOneField(Building, on_delete=models.CASCADE)
    floor_no = models.OneToOneField(Floor, on_delete=models.CASCADE)
    ROOM_TYPE = [
        ('Standard', 'Standard'),
        ('Single', 'Single')
    ]

    room_type = models.CharField(choices=ROOM_TYPE, max_length=50)