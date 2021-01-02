from django.db import models

# Create your models here.
class Building(models.Model):
    building_number = models.SmallIntegerField()


class Floor(models.Model):
    building_no = models.OneToOneField(Building, on_delete=models.CASCADE)
    floor_number = models.SmallIntegerField()


class RoomCategory(models.Model):
    ROOM_TYPE = [
        ('Standard', 'Standard'),
        ('Single', 'Single')
    ]

    room_type = models.CharField(choices=ROOM_TYPE, max_length=50)
    rate = models.IntegerField()
    beds = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    size = models.CharField(max_length=59)

    def __str__(self):
        return f"{self.room_type} room costs N{self.rate}"


class Room(models.Model):
    room_category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    building_no = models.OneToOneField(Building, on_delete=models.CASCADE)
    floor_no = models.OneToOneField(Floor, on_delete=models.CASCADE)
    room_number = models.SmallIntegerField()
    availability = models.BooleanField(default=False)

    def __str__(self):
        return f"The room {self.room_number} {self.room_category} has a maximum of {self.room_category.capacity} person " \
               f"and cost {self.room_category.rate}/night "
