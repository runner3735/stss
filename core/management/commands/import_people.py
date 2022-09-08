
import pickle, re, shelve
from django.core.management.base import BaseCommand
from ...models import Department, Person, Room

rx1 = re.compile(r"^['A-Za-z-]+$")
rx2 = re.compile(r"^([ 'A-Za-z-]+),([ 'A-Za-z-]+)\.?$")
rx3 = re.compile(r"^(['A-Za-z-]+)\.? (['A-Za-z-]+)$")
rx_room = re.compile(r"^(MBH|MBH |)(\d\d\d[A-Z]?|R0\d)$")

people = {} # ['Name', 'Department', 'Phone', 'Office', 'Email', 'DBStatus']
departments = {}
names = {}
dualnames = {}
manufacturers = {}

def LoadPickles():
    global people, departments, names, dualnames, manufacturers
    people = pickle.load(open('/mediafiles/db/people.p', 'rb'))
    departments = pickle.load(open('/mediafiles/db/departments.p', 'rb'))
    names = pickle.load(open('/mediafiles/db/names.p', 'rb'))
    dualnames = pickle.load(open('/mediafiles/db/dualnames.p', 'rb'))
    manufacturers = pickle.load(open('/mediafiles/db/manufacturers.p', 'rb'))

def SavePickles():
    #pickle.dump(departments, open('/mediafiles/db/departments.p', 'wb'))
    pickle.dump(names, open('/mediafiles/db/names.p', 'wb'))
    #pickle.dump(dualnames, open('/mediafiles/db/dualnames.p', 'wb'))
    #pickle.dump(manufacturers, open('/mediafiles/db/manufacturers.p', 'wb'))
    print('pickles saved')

def GetNamePairs(text): # returns a list of first, last tuples
    global names
    if text in dualnames: text = dualnames[text]
    namepairs = []
    for name in text.split('/'):
        namepair = GetFirstLast(name)
        if namepair in names:
            namepair = names[namepair]
        else:
            print('New Namepair:', namepair)
            names[namepair] = namepair
        namepairs.append(namepair)
    return namepairs

def GetFirstLast(name):
    first, last = ParseName(name)
    if first: first = first[0].upper() + first[1:]
    if last: last = last[0].upper() + last[1:]
    return first, last

def ParseName(name):
    name = name.strip()
    m = rx2.match(name)
    if m: return m[2].strip(), m[1].strip()
    m = rx3.match(name)
    if m: return m[1], m[2]
    m = rx1.match(name)
    if m:
        print('Last Name:', name)
        first = input("Enter First Name:")
        return first, name
    print('PARSE ERROR: ' + name)
    first = input("Enter First Name:")
    last = input("Enter Last Name:")
    return first, last

def GetPeopleInfo():
    peopleinfo = {}
    for p in people.values():
        namepairs = GetNamePairs(p['Name'])
        assert len(namepairs) == 1, "Text in Name field of People table mapped to more than one person!"
        namepair = namepairs[0]
        depts = GetDepartments(p['Department'])
        if p['Office'] in ['Left', 'Retired']: office = ''
        else: office = GetOffice(p['Office'])
        peopleinfo[namepair] = depts, p['Phone'], office, p['Email']
    return peopleinfo

def GetDepartments(text):
    depts = []
    if not text: return depts
    for dept in text.split('/'):
        depts.append(departments[dept.strip()])
    return depts

def GetOffice(text):
    if not text: return
    m = rx_room.match(text.upper())
    if m: return m[2]
    print('Room Parse Error:', text)
    return input('Enter Room Number: ')

def AddPeopleInfo(p, info):
    depts, phone, office, email = info
    for dept in depts:
        D = Department.objects.get(name=dept)
        p.departments.add(D)
    if phone: p.phone = phone
    if office:
        R, created = Room.objects.get_or_create(text=office)
        p.office = R
    if email and '@' in email: p.email = email
    elif email: p.email = email + '@middlebury.edu'
    p.save()

class Command(BaseCommand):

    def import_people(self):
        peopleinfo = GetPeopleInfo()
        namepairs = set(names.values())
        print('namepairs:', len(namepairs))
        for namepair in namepairs:
            P, created = Person.objects.get_or_create(first=namepair[0], last=namepair[1])
            if namepair in peopleinfo: AddPeopleInfo(P, peopleinfo[namepair])
        print('Done importing people.')

    def handle(self, *args, **options):
        LoadPickles()
        self.import_people()
        SavePickles()
