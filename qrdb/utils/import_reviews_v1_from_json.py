import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'qrdb.settings')
sys.path.append('../')
from qrdb import setup
setup()

import pandas as pd
import re
from qrdb import models
import json5

# survey.json comes from PHPMyAdmin
reviews = json5.load(open('survey.json', 'r'))
print(f'Loaded {len(reviews)} reviews')

# Delete all existing reviews
input('Deleting existing reviews, press enter to proceed...')
models.Review_v1.objects.all().delete()

review_objs = []
unique_constraint = set()
for review in reviews:
    # print(review)

    room = review['staircase'] + str(int(float(review['number'])))
    # print(room)
    try:
        room_object = models.Room.objects.get(name=room)
    except KeyboardInterrupt:
        raise
    except: #models.DoesNotExist:
        print(f'Skipping review for {room}, room does not exist')

    if review['crsid']:
        if (review['crsid'], room, review['year']) in unique_constraint:
            print('WARNING: Review duplicated, allowing anyway...')
            print((review['crsid'], room, review['year']))
        unique_constraint.add((review['crsid'], room, review['year']))
    else:
        print('Review has no crsid, allowing...')
    # if review['crsid'] == 

    review_obj = models.Review_v1(crsid=review['crsid'], year=review['year'], room=room_object,
                                storage=review['storage'], size=review['size'], bathroom=review['bathroom'], 
                                kitchen=review['kitchen'], noise=review['noise'], comments=review['comments'],
                                rentcomment=review['rentcomment'], rent_vary=review['rent_vary'], light=review['light'],
                                furniture=review['furniture'], moderated=review['moderated'],
                                old_id=review['id'])
    
    review_objs.append(review_obj)

print(f'Got {len(review_objs)} reviews.')

# Commit
for review in review_objs:
    review.save()