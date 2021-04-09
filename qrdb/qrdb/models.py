from django.db import models

# Buildings -> Staircase -> Room -> Review <- User
class Building(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

class Staircase(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    building = models.ForeignKey(Building, on_delete=models.PROTECT)

class Room(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    staircase = models.ForeignKey(Staircase, on_delete=models.PROTECT)
    floor = models.CharField(max_length=1)

    view = models.CharField(max_length=20, blank=True)
    room_type = models.CharField(max_length=25, blank=True)

    bathroom = models.CharField(max_length=25, blank=True) # One of ['Shared', 'En-suite', 'Private']

class User(models.Model):
    crsid = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    register_time = models.DateTimeField()

# class Year(models.Model):
#     name = models.CharField(max_length=50)

# Reviews made between 2007 and 2014
class Review_v1(models.Model):
    old_id = models.IntegerField()
    crsid = models.CharField(max_length=10)
    # year = models.ForeignKey(Year, on_delete=models.PROTECT)
    year = models.CharField(max_length=20)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)

    # number = models.IntegerField() # no idea what this is
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

    # Convert the numeric fields into strings for v1 reviews
    # Taken from legacy errata.php and survey-form.php
    def annotate(self):
        size_map = {0: "Small", 1: "Medium", 2: "Large", 3: "Fisher smaller", 4: "Fisher bigger"}
        bathroom_map = {0: "Ensuite", 1: "Private external", 2: "Corridor", 3: "Floor", 4: "Building", 5: "Other"}
        noise_map = {0: "Very", 1: "Fairly", 2: "Slightly", 3: "Not at all"}

        # Quality is used for storage, kitchen, light, furniture
        quality_map = {-1: "", 0: "Bad", 1: "Poor", 2: "Adequate", 3: "Good", 4: "Excellent"}

        self.size_string = size_map[self.size]
        self.bathroom_string = bathroom_map[self.bathroom]
        self.noise_string = noise_map[self.noise]

        self.storage_string = quality_map[self.storage]
        self.kitchen_string = quality_map[self.kitchen]
        self.light_string = quality_map[self.light]
        self.furniture_string = quality_map[self.furniture]

    # class Meta:
        # unique_together = ('crsid', 'room')

# New reviews
# class Review_v2(models.Model):
#     user = models.ForeignKey(User, on_delete=models.PROTECT)
#     year = models.ForeignKey(Year, on_delete=models.PROTECT)
#     room = models.ForeignKey(Room, on_delete=models.PROTECT)
#     year 

#     # todo...
#     class Meta:
#         unique_together = ('crsid', 'room')


