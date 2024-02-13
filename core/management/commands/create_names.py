
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
    people = pickle.load(open('/www/db/people.p', 'rb'))
    instruments = pickle.load(open('/www/db/instruments.p', 'rb'))
    jobs = pickle.load(open('/www/db/jobs.p', 'rb'))
    return
    for j in jobs.values():
        for k in j.keys(): print(k)
        break

def AnalyzeJobs():
    types = set()
    categories = set()
    statuses = set()
    values = set()
    for j in jobs.values():
        values.add(j['Budget'])
        types.add(j['Type'])
        categories.add(j['Category'])
        statuses.add(j['Status'])
        if j['Technician']:
            if '&' in j['Technician']:
                print('Technician: ', j['Technician'])
        if j['Customer']:
            if '&' in j['Customer']:
                print('Customer: ', j['Customer'])
        #if j['Status'] in ['Delayed', 'Deleted']: print(j['ID'], j['Status'])
    #PrintSet('types', types)
    #PrintSet('categories', categories)
    #PrintSet('statuses', statuses)
    #PrintSet('values', values)
    
def PrintSet(name, s):
    print(name, 'count:', len(s))
    for entry in s: print('   ', entry)

def LoadNames():
    global lastnames, names, dualnames, oldnames
    dualnames = pickle.load(open('/www/db/dualnames.p', 'rb'))
    oldnames = pickle.load(open('/www/db/oldnames.p', 'rb'))
    names = pickle.load(open('/www/db/names.p', 'rb'))
    lastnames = pickle.load(open('/www/db/lastnames.p', 'rb'))
    print('Dualnames Count:', len(dualnames))
    print('Oldnames Count:', len(oldnames))
    print('Lastnames Count:', len(lastnames))
    print('Names Count:', len(names))
    print()
    todelete = []
    for name in names:
        first, last = names[name]
        if first or last: continue
        todelete.append(name)
    for name in todelete:
        print('unmapping:', name)
        del names[name]

def SaveNames():
    print('Dualnames Count:', len(dualnames))
    print('Lastnames Count:', len(lastnames))
    print('Names Count:', len(names))
    if input('Save changes to disk? [n] > '):
        pickle.dump(dualnames, open('/www/db/dualnames.p', 'wb'))
        pickle.dump(lastnames, open('/www/db/lastnames.p', 'wb'))
        pickle.dump(names, open('/www/db/names.p', 'wb'))
        print('data saved!')

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
    for j in jobs.values():
        text = j['Technician']
        if not text: continue
        if text in dualnames: text = dualnames[text]
        for part in text.split('/'):
            CheckName(part.strip())
    for j in jobs.values():
        text = j['Customer']
        if not text: continue
        if text in dualnames: text = dualnames[text]
        for part in text.split('/'):
            CheckName(part.strip())

def CheckName(text): # parse text, which represents a single person, and create entry in names dictionary
    global names
    if text in names: return
    namepair = GetFirstLast(text)
    if not namepair: return
    if namepair in oldnames: namepair = oldnames[namepair]
    names[text] = namepair

def GetFirstLast(name):
    namepair = ParseName(name)
    if not namepair: return
    first, last = namepair
    if first: first = first[0].upper() + first[1:]
    if last: last = last[0].upper() + last[1:]
    return first, last

def ParseName(name):
    global lastnames, dualnames
    name = name.strip()
    m = rx2.match(name)
    if m: return m[2].strip(), m[1].strip()
    m = rx3.match(name)
    if m: return m[1], m[2]
    m = rx1.match(name)
    if m and name in lastnames:
        return lastnames[name], name
    if m:
        PrintNamepairsContaining(name)
        print('Last Name:', name)
        first = input("Enter First Name (or 'm' for manual or 'd' for dual) [no first name]:")
        if not first:
            return first, name
        if first == 'm':
            first = input("Enter First Name: ")
            last = input("Enter Last Name: ")
            if first or last: return first, last
            return
        if first != 'd':
            lastnames[name] = first
            return first, name
    print('PARSE ERROR: ' + name)
    fixed = input("Enter Parseable Name Field Text: ")
    dualnames[name] = fixed

def PrintNamepairsContaining(text): # print list of people with similar names
    text = text.lower()
    for name in names:
        if text in name.lower():
            print('***', names[name])

class Command(BaseCommand):

    def list_names(self): #helper function just to look at names pickle
        d = pickle.load(open('/www/db/names.p', 'rb'))
        for k in d.keys(): print(k, ' --> ', d[k])

    def list_manufacturers(self): #helper function just to look at names pickle
        manufacturers = pickle.load(open('/www/db/oldmanufacturers.p', 'rb'))
        for k in manufacturers.keys():
            if k != manufacturers[k]:
                print(k, ' --> ', manufacturers[k])
        print('Manufacturers:', len(manufacturers))

    def add_names(self):
        LoadDatabase()
        LoadNames()
        #AnalyzeJobs()
        AddNames()
        SaveNames()

    def handle(self, *args, **options):
        #self.list_names()
        #self.list_manufacturers()
        self.add_names()
