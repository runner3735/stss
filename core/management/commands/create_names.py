
# this command creates the names.p file, to map strings to (first, last) name pairs

import pickle, re
from django.core.management.base import BaseCommand

rx1 = re.compile(r"^['A-Za-z-]+$")
rx2 = re.compile(r"^([ 'A-Za-z-]+),([ 'A-Za-z-]+)\.?$")
rx3 = re.compile(r"^(['A-Za-z-]+)\.? (['A-Za-z-]+)$")

people = {} # ['Name']
instruments = {} # ['Contact']
jobs = {} # ['Technician', 'Customer']
dualnames = {}
oldnames = {}
names = {}
lastnames = {}

def LoadDatabase():
    global people, instruments, jobs
    people = pickle.load(open('/www/stss/db/people.p', 'rb'))
    instruments = pickle.load(open('/www/stss/db/instruments.p', 'rb'))
    jobs = pickle.load(open('/www/stss/db/jobs.p', 'rb'))

def LoadNames():
    global lastnames, names, dualnames, oldnames
    dualnames = pickle.load(open('/www/stss/db/dualnames.p', 'rb'))
    oldnames = pickle.load(open('/www/stss/db/oldnames.p', 'rb'))
    names = pickle.load(open('/www/stss/db/names.p', 'rb'))
    lastnames = pickle.load(open('/www/stss/db/lastnames.p', 'rb'))
    print('Dualnames Count:', len(dualnames))
    print('Oldnames Count:', len(oldnames))
    print('Lastnames Count:', len(lastnames))
    print('Names Count:', len(names))

def SaveNames():
    pickle.dump(names, open('/www/stss/db/names.p', 'wb'))
    print('Names Count:', len(names))

def CheckName(text): # parse text, which represents a single person, and create entry in names dictionary
    global names
    if text in names: return
    namepair = GetFirstLast(text)
    if namepair in oldnames: namepair = oldnames[namepair]
    names[text] = namepair

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
    if m and name in lastnames:
        return lastnames[name], name
    if m:
        NameLookup(name)
        print('Last Name:', name)
        first = input("Enter First Name (or 'm' to create manual entries):")
        if first != 'm': return first, name
    print('PARSE ERROR: ' + name)
    first = input("Enter First Name:")
    last = input("Enter Last Name:")
    return first, last

def NameLookup(text):
    text = text.lower()
    for name in names:
        if text in name.lower():
            print(names[name])

def AddNames():
    for p in people.values():
        text = p['Name']
        if not text: continue
        CheckName(text.strip())
    for i in instruments.values():
        text = i['Contact']
        if not text: continue
        if text in dualnames: text = dualnames[text]
        for part in text.split('/'):
            CheckName(part.strip())

class Command(BaseCommand):

    def list_names(self): #helper function just to look at names pickle
        names = pickle.load(open('/www/stss/db/names.p', 'rb'))
        for k in names.keys(): print(k, ' --> ', names[k])

    def list_manufacturers(self): #helper function just to look at names pickle
        manufacturers = pickle.load(open('/www/stss/db/oldmanufacturers.p', 'rb'))
        for k in manufacturers.keys():
            if k != manufacturers[k]:
                print(k, ' --> ', manufacturers[k])
        print('Manufacturers:', len(manufacturers))

    def add_names(self):
        LoadDatabase()
        LoadNames()
        AddNames()
        SaveNames()

    def handle(self, *args, **options):
        #self.list_names()
        #self.list_manufacturers()
        self.add_names()
