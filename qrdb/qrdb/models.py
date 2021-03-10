from django.db import models

# Buildings -> Staircase -> Room -> Review <- User
class Building(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

class Staircase(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    building = models.ForeignKey(Staircase, on_delete=models.PROTECT)

class Room(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    staircase = models.ForeignKey(Staircase, on_delete=models.PROTECT)

class User(models.Model):
    crsid = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    register_time = models.DateTimeField()

class Year(models.Model):
    name = models.CharField(max_length=50)

# Reviews made between 2007 and 2014
class Review_v1(models.Model):
    crsid = models.CharField(max_length=10)
    year = models.ForeignKey(Year, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)

    number = models.IntegerField() # no idea what this is
    storage = models.IntegerField()
    size = models.IntegerField()
    bathroom = models.IntegerField()
    kitchen = models.IntegerField()
    noise = models.IntegerField()
    comments = models.TextField(blank=True)
    rentcomment = models.TextField(blank=True)

    rent_vary = models.IntegerField()
    light = models.IntegerField()
    furniture = models.IntegerField()
    moderated = models.BooleanField()

    class Meta:
        unique_together = ('crsid', 'room')

# New reviews
class Review_v2(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    year = models.ForeignKey(Year, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    year 

    # todo...
    class Meta:
        unique_together = ('crsid', 'room')


