
# this command creates the rooms.p file, to map strings to room numbers

import pickle, re
from django.core.management.base import BaseCommand

rx_room = re.compile(r"^(MBH|BH|RM|)[ #]*(\d\d\d[A-Z]?|R0\d)$")
rx_number = re.compile(r"\d\d\d")
rx_num = re.compile(r"^\d+$")

people = {}
instruments = {}
jobs = {}
rooms = {}
locations = {}
locwords = {}

def LoadDatabase():
    global people, instruments, jobs
    people = pickle.load(open('/www/db/people.p', 'rb'))
    instruments = pickle.load(open('/www/db/instruments.p', 'rb'))
    jobs = pickle.load(open('/www/db/jobs.p', 'rb'))

def LoadRooms():
    global rooms, locations, locwords
    rooms = pickle.load(open('/www/db/rooms.p', 'rb'))
    print('Room Count:', len(rooms))
    #locations = pickle.load(open('/www/db/locations.p', 'rb'))
    print('Location Count:', len(locations))
    locwords = pickle.load(open('/www/db/locwords.p', 'rb'))
    print('Location Word Count:', len(locwords))

def SaveRooms():
    pickle.dump(rooms, open('/www/db/rooms.p', 'wb'))
    print('Room Count:', len(rooms))
    pickle.dump(locations, open('/www/db/locations.p', 'wb'))
    print('Location Count:', len(locations))
    pickle.dump(locwords, open('/www/db/locwords.p', 'wb'))
    print('Location Word Count:', len(locwords))

def AddRooms():
    print('SCANNING PEOPLE')
    for p in people.values():
        if not p['Office']: continue
        CheckText(p['Office'])
    print('SCANNING INSTRUMENTS')
    for i in instruments.values():
        if not i['Room']: continue
        for line in i['Room'].splitlines():
            for part in line.split('/'):
                CheckText(part.strip())
    print('SCANNING JOBS')
    for j in jobs.values():
        if not j['Location']: continue
        for line in j['Location'].splitlines():
            line = line.replace('&', '/')
            for part in line.split('/'):
                CheckText(part.strip())

def CheckText(text): # parse text, which represents a single room or location, and create entry in rooms or location dictionary
    if text in rooms: return
    if text in locations: return
    if CheckRoom(text): return
    CheckLocation(text)

def CheckLocation(text):
    global locations
    fixed = []
    for word in text.lower().split():
        if rx_num.match(word):
            fixed.append(word)
        else:
            AddLocationWord(word)
            fixed.append(locwords[word])
    location = ' '.join(fixed)
    locations[text] = location.title()

def AddLocationWord(word):
    global locwords
    if word in locwords: return
    new = input('Enter word [' + word + '] > ')
    if new: locwords[word] = new
    else: locwords[word] = word

def CheckRoom(text): # parse text, which represents a single room or location, and create entry in rooms dictionary
    global rooms
    m = rx_room.match(text.upper())
    if m:
        rooms[text] = m[2]
        return True
    numbers = rx_number.findall(text)
    if not numbers: return
    print('PART:', text)
    default = '/'.join(numbers)
    room = input('Enter Room Number [d = ' + default + '] > ')
    if room == 'd':
        rooms[text] = default
        return True
    if room:
        rooms[text] = room
        return True

def CreateLocwords():
    locwords = {}
    for k in locations:
        if rx_num.match(k): continue
        locwords[k] = locations[k]
    pickle.dump(locwords, open('/www/db/locwords.p', 'wb'))
    print('Location Word Count:', len(locwords))
    for k, v in rooms.items():
        if len(v) == 3 and rx_num.match(v): continue
        print(v)

class Command(BaseCommand):

    def list_locations(self):
        jobs = pickle.load(open('/www/db/jobs.p', 'rb'))
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
