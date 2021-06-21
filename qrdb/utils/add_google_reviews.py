import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'qrdb.settings')
sys.path.append('../')
from qrdb import setup
setup()

import pandas as pd
import re
from qrdb import models, CONFIG

from PIL import ImageOps

# pip install gdown
import gdown
from PIL import Image
import io

if len(sys.argv) not in [2, 3]:
    print('Usage: python add_google_reviews.py [EXCEL_FILE] [commit?]')
    # print("""Excel file must contain ONE SHEET with the following columns:
# 
    # """)
    quit()

df = pd.read_excel(sys.argv[1])
print(df)
print(f'Loaded {len(df)} rooms, columns: {df.columns}')


reviews = []
for i, row in df.iterrows():
    room_number = row['What was your room number? (eg. EE4, W8, K12, OCB16)'].upper().strip()
    crsid = row["What's your crsID? (e.g. mb2345)"].split('@')[0].strip()

    # Unique per review, this means we don't re-add the same one twice
    hash_id = str(row['Timestamp']) + crsid
    if models.Review_v2.objects.filter(hash_id=hash_id):
        print('Review already in DB, skipping!')
        continue

    # e.g. "W7" = 1, "OCB13" = 3
    staircase_size = sum(c.isalpha() for c in room_number)
    # This allows us to normalise e.g. "W07" -> "W7"
    room_normalized = room_number[:staircase_size] + room_number[staircase_size:].lstrip("0")

    try:
        room_object = models.Room.objects.get(name=room_normalized)
    except:
        print('Skipping', room_number, 'room not in database')
        continue

    
    year = int(row['Year of occupancy'].split('-')[0]) + 1

    room_rating_overall = CONFIG.RATING_CHOICES.index(row["Rate your room on these points! [📊 Overall]"])
    room_rating_light = CONFIG.RATING_CHOICES.index(row["Rate your room on these points! [💡 Light]"])
    room_rating_view = CONFIG.RATING_CHOICES.index(row["Rate your room on these points! [🗻 View]"])
    room_rating_quiet = CONFIG.RATING_CHOICES.index(row["Rate your room on these points! [🔊 Quiet]"])
    room_rating_size = CONFIG.RATING_CHOICES.index(row["Rate your room on these points! [🏰 Size ]"])
    room_rating_storage = CONFIG.RATING_CHOICES.index(row["Rate your room on these points! [📦 Storage]"])
    room_rating_bathroom = CONFIG.RATING_CHOICES.index(row["Rate your room on these points! [🛁 Bathroom]"])
    room_rating_heating = CONFIG.RATING_CHOICES.index(row["Rate your room on these points! [🔥 Heating/Temp]"])
    room_rating_repair = CONFIG.RATING_CHOICES.index(row["Rate your room on these points! [State of repair]"])
    room_rating_furniture = CONFIG.RATING_CHOICES.index(row["Rate your room on these points! [🪑 Desk/furniture]"])
    room_rating_gyp = CONFIG.RATING_CHOICES.index(row["Rate your room on these points! [🔪 Gyp room]"])
    if not pd.isnull(row["Rate your room on these points! [📶 WiFi]"]):
        room_rating_wifi = CONFIG.RATING_CHOICES.index(row["Rate your room on these points! [📶 WiFi]"])
    else:
        room_rating_wifi = -1

    if not pd.isnull(row["How many did you share your bathroom with? (roughly)"]):
        bathroom_sharing = int(row["How many did you share your bathroom with? (roughly)"])
    else:
        bathroom_sharing = -1
    if not pd.isnull(row["How many did you share your gyp with? (roughly)"]):
        gyp_sharing = int(row["How many did you share your gyp with? (roughly)"])
    else:
        gyp_sharing = -1

    room_review = row['Review: What was good and bad about your room?']
    room_tips = row['Any tips for the person staying in your room next year?']
    room_feedback = row['Feedback: Any issues/complaints/suggestions you have you want to let the JCR or the College know about?']


    review_object = models.Review_v2(crsid=crsid, year=year, room=room_object, hash_id=hash_id,
    room_rating_overall=room_rating_overall, room_rating_light=room_rating_light,
    room_rating_view=room_rating_view, room_rating_quiet=room_rating_quiet,
    room_rating_size=room_rating_size, room_rating_storage=room_rating_storage,
    room_rating_bathroom=room_rating_bathroom, room_rating_heating=room_rating_heating,
    room_rating_repair=room_rating_repair, room_rating_furniture=room_rating_furniture,
    room_rating_gyp=room_rating_gyp, room_rating_wifi=room_rating_wifi,
    bathroom_sharing=bathroom_sharing, gyp_sharing=gyp_sharing,
    room_review = row['Review: What was good and bad about your room?'],
    room_tips = row['Any tips for the person staying in your room next year?'],
    room_feedback = row['Feedback: Any issues/complaints/suggestions you have you want to let the JCR or the College know about?'],
    )

    print(review_object)

    reviews.append(review_object)

    # Process images!
    photos_links = row['Do you have any photos of your room? 📷 (optional, *highly recommended*!)']
    if not pd.isnull(photos_links):
        for photo_link in photos_links.split(','):
            gdown.download(photo_link.replace('open?', 'uc?'), 'temp-image', quiet=True)

            img = Image.open('temp-image')
            img = img.convert('RGB')

            img = ImageOps.exif_transpose(img)
            img.thumbnail([1200, 1200], Image.ANTIALIAS)

            with io.BytesIO() as output:
                img.save(output, format="JPEG", optimize=True, quality=60)
                contents = output.getvalue()
                print('Image size:', len(contents))

            os.remove('temp-image')

            photo_object = models.ReviewImage(review=review_object, image=contents)
            reviews.append(photo_object)

print(f'Have {len(reviews)} reviews/images.')

if len(sys.argv[2]) and sys.argv[2] == 'commit':
    for review in reviews:
        try:
            review.save()
        except Exception as e:
            print('Failed to save a review because', e)