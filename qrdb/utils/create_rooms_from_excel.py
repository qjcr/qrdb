import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'qrdb.settings')
sys.path.append('../')
from qrdb import setup
setup()

import pandas as pd
import re
from qrdb import models

if len(sys.argv) not in [2, 3]:
    print('Usage: python create_rooms_from_excel.py [EXCEL_FILE] [commit?]')
    print("""Excel file must contain ONE SHEET with the following columns:
    Building:    e.g. "Old Court", "Erasmus"
    Room type:   one of "Twin", "Bedroom", "Set"
    Floor:       e.g. "G", "1", "2", "3", "4"
    Bathroom,    one of "Shared", "En-suite"
    View:        e.g. "Court", "Queens' Lane", "East"
    Room number: e.g. "K23", "E3a", "Q11"
    """)
    quit()

print('Loading excel file: ')
df = pd.read_excel(sys.argv[1])
print(df)
print(f'Loaded {len(df)} rooms, columns: {df.columns}')

# Finding buildings

buildings = {}
for i, row in df.iterrows():
    b = row['Building']
    if b not in buildings:
        buildings[b] = models.Building(name=b)
    
print(f'Found {len(buildings)} buildings: {buildings.keys()}')

# Finding staircases
staircases = {}
for i, row in df.iterrows():
    s = re.match("[A-Z]*", row['Room Number']).group(0)
    assert len(s), f"Empty staircase in row {row}"

    b = row['Building']
    if s not in staircases:
        staircases[s] = models.Staircase(building=buildings[b], name=s)
    
print(f'Found {len(staircases)} staircases: {staircases.keys()}')

# Finding rooms
rooms = {}
views = set()
floors = set()

for i, row in df.iterrows():
    s = re.match("[A-Z]*", row['Room Number']).group(0)
    r = row['Room Number']

    # shared = False
    # if r.endswith('a') or r.endswith('b'):
    #     print(f'Merging shared(?) room {r} -> {r[:-1]}, please check this is OK')
    #     r = r[:-1]
    #     shared = True

    floor = str(row['Floor'])
    view = row['View']
    room_type = row['Room type']
    bathroom = row['Bathroom']

    # These asserts are just to make sure that the data is uniform
    # They can be removed if you would like other room types/bathroom types to be supported, and the front-end will still work.
    assert room_type in ['Twin', 'Bedroom', 'Set'], f"Invalid room type value {room_type} for room {r}"
    assert bathroom in ['En-suite', 'Shared', 'Private'], f"Invalid bathroom value {bathroom} for room {r}"
    assert floor in ['G', '1', '2', '3', '4'], f"Invalid floor value {floor} for room {r}"

    floors.add(floor)
    views.add(view)

    # if shared and r in rooms:
    #     continue

    assert r not in rooms, f"Room {r} exists twice!"
    rooms[r] = models.Room(staircase=staircases[s], name=r, floor=floor, view=view, bathroom=bathroom, room_type=room_type)
    
print(f'Found {len(rooms)} rooms: {rooms.keys()}')
print(f'views: {views}')
print(f'floors: {floors}')

print('********')
print(f'READY TO COMMIT {len(buildings) + len(staircases) + len(rooms)} ITEMS')
if len(sys.argv) == 3 and sys.argv[2] == 'commit':
    for b in buildings.values():
        b.save()
    for s in staircases.values():
        s.save()
    for r in rooms.values():
        r.save()
    print('Done!')
else:
    print('Dry run ending. Run with "commit" to apply changes to DB')
