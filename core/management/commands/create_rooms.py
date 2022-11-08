
# this command creates the rooms.p file, to map strings to room numbers

import pickle, re
from django.core.management.base import BaseCommand

rx_room = re.compile(r"^(MBH|MBH |BH|BH |)(\d\d\d[A-Z]?|R0\d)$")

people = {}
instruments = {}
jobs = {}
rooms = {}

def LoadDatabase():
    global people, instruments, jobs
    people = pickle.load(open('/www/stss/db/people.p', 'rb'))
    instruments = pickle.load(open('/www/stss/db/instruments.p', 'rb'))
    jobs = pickle.load(open('/www/stss/db/jobs.p', 'rb'))

def LoadRooms():
    global rooms
    rooms = pickle.load(open('/www/stss/db/rooms.p', 'rb'))
    print('Room Count:', len(rooms))

def SaveRooms():
    pickle.dump(rooms, open('/www/stss/db/rooms.p', 'wb'))
    print('Room Count:', len(rooms))

def AddRooms():
    for p in people.values():
        if not p['Office']: continue
        CheckRoom(p['Office'])
    for i in instruments.values():
        if not i['Room']: continue
        for line in i['Room'].splitlines():
            for part in line.split('/'):
                CheckRoom(part.strip())
#    for j in jobs.values():
#        CheckRoom(j['Location'])

def CheckRoom(text): # parse text, which represents a single room or location, and create entry in rooms dictionary
    global rooms
    if text in rooms: return
    m = rx_room.match(text.upper())
    if m:
        rooms[text] = m[2]
    else:
        print('Room Parse Error:', text)
        room = input('Enter Room Number: ')
        rooms[text] = room

class Command(BaseCommand):

    def list_locations(self):
        jobs = pickle.load(open('/www/stss/db/jobs.p', 'rb'))
        for k in jobs.keys():
            location = jobs[k]['Location']
            if location: print(location)

    def add_rooms(self):
        LoadDatabase()
        LoadRooms()
        AddRooms()
        SaveRooms()

    def handle(self, *args, **options):
        self.add_rooms()
