
# this script imports the people table, and creates Person, Department, and Room objects

import pickle
from django.core.management.base import BaseCommand
from ...models import Department, Person, Room

people = {} # ['Name', 'Department', 'Phone', 'Office', 'Email', 'DBStatus']
departments = {}
names = {}
dualnames = {}
rooms = {}

def LoadPickles():
    global people, departments, names, dualnames, rooms
    people = pickle.load(open('/www/db/people.p', 'rb'))
    departments = pickle.load(open('/www/db/departments.p', 'rb'))
    names = pickle.load(open('/www/db/names.p', 'rb'))
    dualnames = pickle.load(open('/www/db/dualnames.p', 'rb'))
    rooms = pickle.load(open('/www/db/rooms.p', 'rb'))

def ImportPeople():
    for p in people.values():
        person = GetPerson(p['Name'])
        if not person: continue
        AddEmail(person, p['Email'])
        AddPhone(person, p['Phone'])
        AddDepartments(person, p['Department'])
        AddOffice(person, p['Office'])
        person.save()

def GetPerson(text):
    if not text: return
    first, last = names[text]
    person, created = Person.objects.get_or_create(first=first, last=last)
    return person

def AddEmail(person, text):
    if not text: return
    if '@' in text: person.email = text
    else: person.email = text + '@middlebury.edu'

def AddPhone(person, text):
    if not text: return
    person.phone = text

def AddDepartments(person, text):
    if not text: return
    for part in text.split('/'):
        dept = departments[part.strip()]
        D, created = Department.objects.get_or_create(name=dept)
        person.departments.add(D)

def AddOffice(person, text):
    if text in ['Left', 'Retired', 'Student']: return
    person.status = 5
    if not text: return
    room = rooms.get(text,"")
    if room:
        R, created = Room.objects.get_or_create(text=room)
        person.office = R
    else:
        print('Ignoring Office text:', text)

class Command(BaseCommand):

    def import_people(self):
        LoadPickles()
        ImportPeople()

    def handle(self, *args, **options):
        self.import_people()
