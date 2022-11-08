
# this script imports the instruments table, and creates Person, Department, Room, Manufacturer, Purchase, Tag, Note and Asset objects

import pickle, re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Department, Person, Manufacturer, Purchase, Tag, Room, Note, Asset

# instrument fields
# ['AssetTag', 'InventoryDate', 'InstrumentName', 'Nickname', 'Manufacturer', 'Model', 'SerialNumber', 'PurchaseDate', 'Vendor', 
# 'PurchaseOrder', 'Cost', 'Department', 'Contact', 'Room', 'OldRoom', 'DecommissionDate', 'OperatorManual', 'ServiceManual', 'Notes', 
# 'RemovalReason', 'DBStatus']
instruments = {}

departments = {}
names = {}
dualnames = {}
manufacturers = {}
rooms = {}

rx_asset = re.compile(r"^(M/C X\d\d\d\d|OE-\d\d\d\d)$")
rx_job = re.compile(r"^\d\d-\d\d\d$")

def LoadPickles():
    global instruments, departments, names, dualnames, manufacturers, rooms
    instruments = pickle.load(open('/www/stss/db/instruments.p', 'rb'))
    departments = pickle.load(open('/www/stss/db/departments.p', 'rb'))
    names = pickle.load(open('/www/stss/db/names.p', 'rb'))
    dualnames = pickle.load(open('/www/stss/db/dualnames.p', 'rb'))
    manufacturers = pickle.load(open('/www/stss/db/manufacturers.p', 'rb'))
    rooms = pickle.load(open('/www/stss/db/rooms.p', 'rb'))

def DeleteAssets():
    for a in Asset.objects.all():
        a.delete()
        print(a.identifier, ' DELETED')

def ImportInstruments():
    if not User.objects.get(username='admin'): return
    for i in instruments.values():
        asset = GetAsset(i['AssetTag'])
        if not asset: continue
        AddNames(asset, i['InstrumentName'], i['Nickname'])
        AddModel(asset, i['Model'])
        AddSerial(asset, i['SerialNumber'])
        AddRoom(asset, i['Room'])
        AddInventoried(asset, i['InventoryDate'])
        AddManufacturer(asset, i['Manufacturer'])
        AddDepartment(asset, i['Department'])
        AddPurchase(asset, i)
        asset.status = GetStatus(asset, i['RemovalReason'])
        AddRemovalNote(asset, i['DecommissionDate'])
        AddContacts(asset, i['Contact'])
        AddTags(asset, i)
        AddNotes(asset, i['Notes'])
        asset.save()

def GetAsset(text):
    if rx_asset.match(text):
        asset, created = Asset.objects.get_or_create(identifier=text)
        return asset
    if not rx_job.match(text): print('Bad Asset Identifier:', text)

def AddNames(asset, name, nickname):
    if name and nickname:
        asset.name = name
        if nickname != name: asset.nickname = nickname
    elif nickname:
        asset.name = nickname
    elif name:
        asset.name = name

def AddModel(asset, text):
    if text: asset.model = text

def AddSerial(asset, text):
    if text: asset.serial = text

def AddRoom(asset, text):
    if not text: return
    if text.strip() in rooms:
        room = rooms[text.strip()]
        R, created = Room.objects.get_or_create(text=room)
        asset.room = R
    else:
        asset.location = ' --> '.join(text.splitlines())

def AddInventoried(asset, text):
    if text: asset.inventoried = text

def AddManufacturer(asset, text):
    if not text: return
    options = []
    for line in text.splitlines():
        for part in line.split('/'):
            m = manufacturers[part.strip()]
            if m: options.append(m)
    selected = SelectManufacturer(options)
    if selected:
        M, created = Manufacturer.objects.get_or_create(name=selected)
        asset.manufacturer = M

def SelectManufacturer(options):
    if len(options) == 1: return options[0]
    for i, option in enumerate(options): print(i, option)
    selected = input('select option or o for other > ')
    if not selected: return
    if selected != 'o': return options[int(selected)]
    selected = input('enter manufacturer > ')
    return selected

def AddDepartment(asset, text):
    if not text: return
    dept = text.strip()
    if dept in departments:
        D, created = Department.objects.get_or_create(name=departments[dept])
        asset.department = D
    else:
        print('UNKNOWN DEPARTMENT:', asset.identifier, dept)

def AddPurchase(asset, instrument):
    if not HasPurchase(instrument): return
    p = Purchase()
    p.date = instrument['PurchaseDate']
    p.vendor = instrument['Vendor']
    p.reference = instrument['PurchaseOrder']
    p.cost = instrument['Cost']
    p.save()
    asset.purchases.add(p)

def HasPurchase(instrument):
    if instrument['PurchaseDate']: return True
    if instrument['Vendor']: return True
    if instrument['PurchaseOrder']: return True
    if instrument['Cost']: return True

def GetStatus(asset, text):
    if not text: return 1
    if text == 'Discarded': return 2
    if text == 'Gifted': return 3
    if text == 'Parts Only': return 4
    if text == 'Faculty Left': return 5
    if text == 'Returned': return 6
    if text == 'lost at sea': return 7
    if text == 'Stolen': return 8
    print('UNRECOGNIZED RemovalReason:', asset.identifier, text)
    return 9

def AddRemovalNote(asset, text):
    if not text: return
    text = 'Date Removed From Service: ' + text
    AddNote(asset, text)

def AddNote(asset, text):
        n = Note()
        n.text = text
        n.contributor = User.objects.get(username='admin')
        n.save()
        asset.notes.add(n)

def AddContacts(asset, text):
    if not text: return
    if text in dualnames: text = dualnames[text]
    for part in text.split('/'):
        AddContact(asset, part.strip())

def AddContact(asset, text):
    if not text: return
    if text in names:
        first, last = names[text]
        person, created = Person.objects.get_or_create(first=first, last=last)
        asset.contacts.add(person)
    else:
        print("Not Found In Names Dictionary:", text)

def AddTags(asset, instrument):
    if instrument['OperatorManual']:
        T = Tag.objects.get_or_create(text='Operator Manual')
        asset.tags.add(T)
    if instrument['ServiceManual']:
        T = Tag.objects.get_or_create(text='Service Manual')
        asset.tags.add(T)

def AddNotes(asset, text):
    if text: AddNote(asset, text)

class Command(BaseCommand):

    def handle(self, *args, **options):
        LoadPickles()
        #DeleteAssets()
        ImportInstruments()