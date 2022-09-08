
import pickle, re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Department, Person, Manufacturer, Purchase, Tag, Room, Note, Asset

# ['AssetTag', 'InventoryDate', 'InstrumentName', 'Nickname', 'Manufacturer', 'Model', 'SerialNumber', 'PurchaseDate', 'Vendor', 
# 'PurchaseOrder', 'Cost', 'Department', 'Contact', 'Room', 'OldRoom', 'DecommissionDate', 'OperatorManual', 'ServiceManual', 'Notes', 
# 'RemovalReason', 'DBStatus']
instruments = {}
departments = {}
names = {}
dualnames = {}
manufacturers = {}
lastnames = {}

rx1 = re.compile(r"^['A-Za-z-]+$")
rx2 = re.compile(r"^([ 'A-Za-z-]+),([ 'A-Za-z-]+)\.?$")
rx3 = re.compile(r"^(['A-Za-z-]+)\.? (['A-Za-z-]+)$")
rx_manufacturer = re.compile(r"^(.+?)( |,|\.|Co|Corp|Ltd|Inc)+$")
rx_asset = re.compile(r"^(M/C X\d\d\d\d|OE-\d\d\d\d)$")
rx_room = re.compile(r"^(MBH|MBH |)(\d\d\d[A-Z]?|R0\d)$")
rx_job = re.compile(r"^\d\d-\d\d\d$")

def LoadPickles():
    global instruments, departments, names, dualnames, manufacturers
    instruments = pickle.load(open('/mediafiles/db/instruments.p', 'rb'))
    departments = pickle.load(open('/mediafiles/db/departments.p', 'rb'))
    names = pickle.load(open('/mediafiles/db/names.p', 'rb'))
    dualnames = pickle.load(open('/mediafiles/db/dualnames.p', 'rb'))
    manufacturers = pickle.load(open('/mediafiles/db/manufacturers.p', 'rb'))

def SavePickles():
    #pickle.dump(departments, open('/mediafiles/db/departments.p', 'wb'))
    pickle.dump(names, open('/mediafiles/db/names.p', 'wb'))
    pickle.dump(lastnames, open('/mediafiles/db/lastnames.p', 'wb'))
    #pickle.dump(dualnames, open('/mediafiles/db/dualnames.p', 'wb'))
    #pickle.dump(manufacturers, open('/mediafiles/db/manufacturers.p', 'wb'))
    print('pickles saved')

def GetManufacturer(instrument):
    text = instrument['Manufacturer']
    if not text: return
    if text.lower() == 'n/a': return
    texts = []
    for m in text.split('/'):
        m = CleanManufacturer(m)
        m = manufacturers.get(m, m)
        if m.lower() in ['tss', 'stss']: m = ''
        if m: texts.append(m)
    if not texts: return
    return '/'.join(texts)

def CleanManufacturer(text):
    text = text.strip()
    text = text.replace(' - ', '-')
    m = rx_manufacturer.match(text)
    if m: return m[1]
    return text

def GetPeople(instrument):
    text = instrument['Contact']
    if not text: return []
    p_objects = []
    for first, last in GetNamePairs(text):
        p, created = Person.objects.get_or_create(first=first, last=last)
        if created: print('Created Person:', first, last)
        p_objects.append(p)
    return p_objects

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
    global lastnames
    name = name.strip()
    m = rx2.match(name)
    if m: return m[2].strip(), m[1].strip()
    m = rx3.match(name)
    if m: return m[1], m[2]
    m = rx1.match(name)
    if m:
        if name in lastnames:
            namepair = lastnames[name], name
            return names[namepair]
        NameLookup(name)
        print('Last Name:', name)
        first = input("Enter First Name:")
        lastnames[name] = first
        return first, name
    print('PARSE ERROR: ' + name)
    first = input("Enter First Name:")
    last = input("Enter Last Name:")
    return first, last

def GetDepartment(instrument):
    global departments
    text = instrument['Department']
    if not text: return
    depts = text.split('/')
    if len(depts) > 1: print('MULTIPLE DEPARTMENTS:', text)
    dept = depts[0].strip()
    if not dept in departments:
        print('UNKNOWN DEPARTMENT:', dept)
        departments[dept] = input('Enter Full Department Name > ')
    D, created = Department.objects.get_or_create(name=departments[dept])
    return D

def GetPurchase(instrument):
    pd = instrument['PurchaseDate']
    v = instrument['Vendor']
    po = instrument['PurchaseOrder']
    c = instrument['Cost']
    if pd or v or po or c:
        p = Purchase()
        if pd: p.date = pd
        if v: p.vendor = v
        if po: p.reference = po
        if c: p.cost = c
        p.save()
        return p

def CreatePurchase():
    p = Purchase()
    p.date = '2017-02-14'
    p.vendor = 'Tech Core Supplies'
    p.method = 1
    p.reference = 'some text'
    p.cost = '1295.0'
    p.save()

def InstrumentStatus(instrument):
    text = instrument['RemovalReason']
    if not text: return 1
    if text == 'Discarded': return 2
    elif text == 'Gifted': return 3
    elif text == 'Parts Only': return 4
    elif text == 'Faculty Left': return 5
    elif text == 'Returned': return 6
    elif text == 'lost at sea': return 7
    elif text == 'Stolen': return 8
    print('UNRECOGNIZED RemovalReason:', text)
    return 9

def RemovalNote(instrument, admin):
    dd = instrument['DecommissionDate']
    rr = instrument['RemovalReason']
    if dd: dd = 'Date Removed From Service: ' + dd + '\n'
    else: dd = ''
    if rr: rr = 'Reason For Removal: ' + rr + '\n'
    else: rr = ''
    text = dd + rr
    if text: return CreateNote(text, admin)

def InstrumentNote(instrument, admin):
    text = instrument['Notes']
    if text: return CreateNote(text, admin)

def CreateNote(text, user):
        n = Note()
        n.text = text
        n.contributor = user
        n.save()
        return n

def GetRoom(instrument):
    text = instrument['Room']
    if not text: return
    m = rx_room.match(text.upper())
    if m: return m[2]

def CheckInstruments(): # for testing
    for identifier, instrument in instruments.items():
        text = instrument['Manufacturer']
        if not text: continue
        m = GetManufacturer(instrument)
        if not m: print(text)

def CheckRooms(): # for testing
    others = set()
    for identifier, instrument in instruments.items():
        text = instrument['Room']
        if not text: continue
        m = rx_room.match(text.upper())
        #if m: print(text, ' --> ', m[2])
        if not m: others.add(text)
    for t in others:
        lines = t.splitlines()
        print(' --> '.join(lines))

def NameLookup(text):
    text = text.lower()
    for name in names:
        if text in ' '.join(name).lower():
            print(names[name])

def DeleteAssets():
    for a in Asset.objects.all():
        a.delete()
        print(a.identifier, ' DELETED')

class Command(BaseCommand):

    def import_instruments(self):
        admin = User.objects.get(username='admin')
        oman = Tag.objects.get(text='Operator Manual')
        sman = Tag.objects.get(text='Service Manual')
        for identifier, instrument in instruments.items():
            if rx_job.match(identifier): continue
            if not rx_asset.match(identifier):
                print('Bad Identifier:', identifier)
                print(instrument)
                continue
            print('Importing:', identifier)
            a = Asset()
            a.identifier = identifier
            a.nickname = instrument['Nickname']
            if not a.nickname: a.nickname = ''
            a.description = instrument['InstrumentName']
            if not a.description: a.description = ''
            a.model = instrument['Model']
            if not a.model: a.model = ''
            a.serial = instrument['SerialNumber']
            if not a.serial: a.serial = ''
            room = GetRoom(instrument)
            a.location = ''
            if room:
                R, created = Room.objects.get_or_create(text=room)
                a.room = R
            elif instrument['Room']:
                lines = instrument['Room'].splitlines()
                a.location = ' --> '.join(lines)
            if instrument['InventoryDate']: a.inventoried = instrument['InventoryDate']
            a.save()
            m = GetManufacturer(instrument)
            if m:
                M, created = Manufacturer.objects.get_or_create(name=m)
                a.manufacturer = M
            d = GetDepartment(instrument)
            if d: a.department = d
            p = GetPurchase(instrument)
            if p: a.purchases.add(p)
            s = InstrumentStatus(instrument)
            if s: a.status = s
            n = RemovalNote(instrument, admin)
            if n: a.notes.add(n)
            for p in GetPeople(instrument):
                a.contacts.add(p)
            if instrument['OperatorManual']: a.tags.add(oman)
            if instrument['ServiceManual']: a.tags.add(sman)
            n = InstrumentNote(instrument, admin)
            if n: a.notes.add(n)
            a.save()

    def handle(self, *args, **options):
        LoadPickles()
        #CheckInstruments()
        #CheckRooms()
        #DeleteAssets()
        self.import_instruments()
        SavePickles()