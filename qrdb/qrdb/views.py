from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic

from . import models, CONFIG

def index(request):
    feed_dict = {}
    feed_dict['room_count'] = models.Room.objects.count()
    feed_dict['review_count'] = models.Review_v1.objects.count() + models.Review_v2.objects.count()
    feed_dict['photo_count'] = models.ReviewImage.objects.count()
    return render(request, "index.html", feed_dict)

@login_required
def view_map(request):
    print(request.user)
    feed_dict = {}
    feed_dict['buildings'] = models.Building.objects.all()
    return render(request, "map.html", feed_dict)

@login_required
def view_staircase(request, staircase_name):
    feed_dict = {}

    print(staircase_name)
    staircase = models.Staircase.objects.get(name=staircase_name)

    rooms = staircase.room_set.all()
    by_floor = []
    floor_names = CONFIG.FLOOR_NAMES
    floors = [f for f, _ in floor_names]
    for f, name in floor_names:
        floor_rooms = [r for r in rooms if r.floor == f]
        if len(floor_rooms) > 0:
            by_floor.append((name, floor_rooms))

    assert len([r for r in rooms if r.floor not in floors]) == 0, f"Some rooms in staircase {staircase_name} have unknown floor!"

    feed_dict['staircase'] = staircase
    feed_dict['rooms'] = staircase.room_set.all() 
    feed_dict['by_floor'] = by_floor
    return render(request, "staircase.html", feed_dict)


@login_required
def view_room(request, room_name):
    feed_dict = {}

    room = models.Room.objects.get(name=room_name)
    reviews = room.review_v1_set.all()
    
    for review in reviews:
        review.annotate()
    
    reviews = sorted(reviews, key=lambda x: x.year, reverse=True)
    

    reviews_v2 = room.review_v2_set.all()

    for review in reviews_v2:
        # Create array of attributes
        ratings = []
        for f in review._meta.get_fields():
            if f.name.startswith("room_rating"):
                value = CONFIG.RATING_CHOICES[f.value_from_object(review)]
                color = CONFIG.RATING_COLORS[value]
                ratings.append((f.name.split('_')[-1].capitalize(), value, color))
        review.ratings_array = ratings

    reviews_v2 = sorted(reviews_v2, key=lambda x: x.year, reverse=True)

    feed_dict['room'] = room
    feed_dict['reviews_v1'] = reviews
    feed_dict['reviews_v2'] = reviews_v2
    return render(request, "room.html", feed_dict)

@login_required
def view_image(request, image_id):
    image = models.ReviewImage.objects.get(id=image_id)

    return HttpResponse(image.image, content_type="image/jpeg")

class AddReviewView(generic.TemplateView):
    template_name = "addreview.html"

    def get_context_data(self, **kwargs):
        return {
            "rooms": models.Room.objects.values("name")
        }

    def post(self, request):
        # TODO: handle uploaded files
        form = forms.ReviewForm(request.POST)
        print(request.POST)
        if not form.is_valid():
            # TODO: display these errors
            print(form.errors)
            return self.get(request)
        # TODO: save review to database with current user
        # form.save()
        # TODO: redirect somewhere, maybe with flash message?
        return HttpResponse("yay!")

from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from . import forms, settings
import os

class AddReviewWizard(SessionWizardView):
    form_list = [forms.AddReviewForm1, forms.AddReviewForm2, forms.AddReviewForm3]
    template_name = 'form.html'

    # NOTE: These files may accumulate over time
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'tmp'))
    def done(self, form_list, **kwargs):
        print('wizard!!!o')
        return redirect('/')