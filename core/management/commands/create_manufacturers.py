
# this command creates the manufacturers.p file, to map strings to manufacturer names

import pickle, re
from django.core.management.base import BaseCommand

rx_manufacturer = re.compile(r"^(.+?)( |,|\.|Co|Corp|Ltd|Inc)+$")

instruments = {} # ['Manufacturer']
oldmanufacturers = {}
manufacturers = {}

def LoadDatabase():
    global instruments
    instruments = pickle.load(open('/www/db/instruments.p', 'rb'))

def LoadManufacturers():
    global oldmanufacturers, manufacturers
    oldmanufacturers = pickle.load(open('/www/db/oldmanufacturers.p', 'rb'))
    manufacturers = pickle.load(open('/www/db/manufacturers.p', 'rb'))
    print('Oldmanufacturers Count:', len(oldmanufacturers))
    print('Manufacturers Count:', len(manufacturers))

def SaveManufacturers():
    pickle.dump(manufacturers, open('/www/db/manufacturers.p', 'wb'))
    print('Manufacturers Count:', len(manufacturers))

def CheckManufacturer(text): # parse text, which represents a single manufacturer, and create entry in manufacturers dictionary
    global manufacturers
    if text in manufacturers: return
    manufacturer = GetManufacturer(text)
    manufacturers[text] = manufacturer

def GetManufacturer(text):
    if text.lower() in ['tss', 'stss']: return ''
    text = text.replace(' - ', '-')
    m = rx_manufacturer.match(text)
    if m: text = m[1]
    if text in oldmanufacturers:
        text = oldmanufacturers[text]
    else:
        print('NOT FOUND:', text)
    if len(text) > 2: return text
    print()
    print(text)
    if input('Keep short manufacturer? [y] > '): return ''
    return text

def AddManufacturers():
    for i in instruments.values():
        text = i['Manufacturer']
        if not text: continue
        for line in text.splitlines():
            for part in line.split('/'):
                CheckManufacturer(part.strip())

def TestManufacturers():
    for i in instruments.values():
        text = i['Manufacturer']
        if not text: continue
        for line in text.splitlines():
            for part in line.split('/'):
                if part.strip() in manufacturers: continue
                print('Not Found:', part.strip())
    print('Test Complete!')

class Command(BaseCommand):

    def list_manufacturers(self): #helper function just to look at manufacturers pickle
        manufacturers = pickle.load(open('/www/db/manufacturers.p', 'rb'))
        for k in manufacturers.keys():
            if k != manufacturers[k]:
                print(k, ' --> ', manufacturers[k])
        print('Manufacturers:', len(manufacturers))

    def add_manufacturers(self):
        LoadDatabase()
        LoadManufacturers()
        AddManufacturers()
        SaveManufacturers()

    def test_manufacturers(self):
        LoadDatabase()
        LoadManufacturers()
        TestManufacturers()

    def handle(self, *args, **options):
        self.add_manufacturers()
