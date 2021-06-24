from django.db import models
from functools import cache

# Buildings -> Staircase -> Room -> Review <- User
class Building(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

class Staircase(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    building = models.ForeignKey(Building, on_delete=models.PROTECT)

    def get_room_count(self):
        return len(self.room_set.all())

class Room(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    staircase = models.ForeignKey(Staircase, on_delete=models.PROTECT)
    floor = models.CharField(max_length=1)

    view = models.CharField(max_length=20, blank=True)
    room_type = models.CharField(max_length=25, blank=True)

    bathroom = models.CharField(max_length=25, blank=True) # One of ['Shared', 'En-suite', 'Private']

    # cache means these answers are memoized - speeding up performance
    # This assumes room reviews do not change while running - this is currently true since we dont add reviews through the system

    @cache
    def get_review_count(self):
        return len(self.review_v1_set.all()) + len(self.review_v2_set.all())

    @cache
    def get_review_v2_count(self):
        return len(self.review_v2_set.all())

    @cache
    def reviews_have_comments(self):
        return any([r.comments for r in self.review_v1_set.all()]) or any([r.room_review for r in self.review_v2_set.all()])

    @cache
    def reviews_have_photos(self):
        return any([r.reviewimage_set.count() for r in self.review_v2_set.all()])

# Not currently used for reviews, we just have crsid string
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
class Review_v2(models.Model):
#     user = models.ForeignKey(User, on_delete=models.PROTECT)
    crsid = models.CharField(max_length=20)
    # year = models.ForeignKey(Year, on_delete=models.PROTECT)
    # Year is the _last_ year, so 2019-2020 is in the DB as 2020
    year = models.CharField(max_length=20)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    hash_id = models.CharField(max_length=100) # Prevents duplicate reviews, generate this somehow while updating database

    # Room rating sliders
    room_rating_overall = models.IntegerField()
    room_rating_light = models.IntegerField()
    room_rating_view = models.IntegerField()
    room_rating_quiet = models.IntegerField()
    room_rating_size = models.IntegerField()
    room_rating_storage = models.IntegerField()
    room_rating_bathroom = models.IntegerField()
    room_rating_heating = models.IntegerField()
    room_rating_repair = models.IntegerField()
    room_rating_furniture = models.IntegerField()
    room_rating_gyp = models.IntegerField()
    room_rating_wifi = models.IntegerField()

    # How many people shared this bathroom?
    bathroom_sharing = models.IntegerField(blank=True)
    gyp_sharing = models.IntegerField(blank=True)

    room_tips = models.TextField(blank=True)
    room_review = models.TextField(blank=True)

    # NOTE: This is for JCR/College, not for public view
    room_feedback = models.TextField(blank=True)

    # gyp_rating = models.IntegerField()
    # # 1-4, annotated with: never, rarely, usually, almost always, always
    # gyp_cooking_space = models.IntegerField(blank=True)
    # gyp_fridge_space = models.IntegerField(blank=True)
    # gyp_cupboard_space = models.IntegerField(blank=True)

    # 0-2, annotated with: [Yes, No, No but I want one]
    # freezer = models.IntegerField(blank=True)

    # gyp_sharing = models.IntegerField(blank=True)

    # gyp_usage = models.IntegerField(blank=True)
    # gyp_review = models.TextField(blank=True)

    # NOTE: Once again private
    # gyp_feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ('crsid', 'room', 'year')

class ReviewImage(models.Model):
    review = models.ForeignKey(Review_v2, on_delete=models.CASCADE) # !!!
    # image = models.ImageField(upload_to='images/')

    # We store images in the database (max size 250KB)
    # This may be a bad decision for performance, but it makes the DB very portable
    image = models.BinaryField(max_length=256_000)