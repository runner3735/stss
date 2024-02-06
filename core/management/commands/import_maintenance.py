
# this script imports the people table, and creates Person, Department, and Room objects

import pickle
from django.core.management.base import BaseCommand
from ...models import Department, Person, Room

maintenance = {} # ['ID', 'Frequency', 'Creator']
people = {}
departments = {}
names = {}
dualnames = {}
rooms = {}

def LoadPickles():
    global maintenance
    maintenance = pickle.load(open('/www/db/maintenance.p', 'rb'))

def ImportMaintenance():
    for m in maintenance.values():
        print(m)
        break

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
    if text in ['Left', 'Retired']: return
    person.status = 5
    if not text: return
    room = rooms[text]
    if room:
        R, created = Room.objects.get_or_create(text=room)
        person.office = R
    else:
        print('Ignoring Office text:', text)

class Command(BaseCommand):

    def import_maintenance(self):
        LoadPickles()
        ImportMaintenance()

    def import_people(self):
        LoadPickles()
        ImportPeople()

    def handle(self, *args, **options):
        self.import_maintenance()
