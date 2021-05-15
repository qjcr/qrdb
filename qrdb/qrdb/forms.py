from django import forms
from . import CONFIG, models


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review_v2
        exclude = ("crsid",)

class AddReviewForm1(forms.Form):
    room_number = forms.CharField(max_length=10)
    year = forms.ChoiceField(choices=[(c, c) for c in CONFIG.AVAILABLE_YEARS])

class AddReviewForm2(forms.Form):
    # TODO: Add sliders

    bathroom_sharing = forms.IntegerField(min_value=1, max_value=18)

    image = forms.ImageField(required=False)

    room_tips = forms.TextInput()
    room_review = forms.TextInput()
    room_feedback = forms.TextInput()

class AddReviewForm3(forms.Form):
    # TODO: Add sliders

    gyp_cooking_space = forms.ChoiceField(choices=[(c, c) for c in CONFIG.GYP_FREQUENCY_CHOICES])
    gyp_fridge_space = forms.ChoiceField(choices=[(c, c) for c in CONFIG.GYP_FREQUENCY_CHOICES])
    gyp_cupboard_space = forms.ChoiceField(choices=[(c, c) for c in CONFIG.GYP_FREQUENCY_CHOICES])

    if CONFIG.ENABLE_GYP_FREEZER_QUESTION:
        freezer = forms.ChoiceField(choices=[(c, c) for c in CONFIG.GYP_FREEZER_QUESTION_CHOICES])

    # TODO: Rest of questions, i cba