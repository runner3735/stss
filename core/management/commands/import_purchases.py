
# this script imports the instruments table, and creates Person, Department, Room, Manufacturer, Purchase, Tag, Note and Asset objects

import pickle, re
from django.core.management.base import BaseCommand
from ...models import Purchase, Asset, Vendor

# instrument fields
# ['AssetTag', 'InventoryDate', 'InstrumentName', 'Nickname', 'Manufacturer', 'Model', 'SerialNumber', 'PurchaseDate', 'Vendor', 
# 'PurchaseOrder', 'Cost', 'Department', 'Contact', 'Room', 'OldRoom', 'DecommissionDate', 'OperatorManual', 'ServiceManual', 'Notes', 
# 'RemovalReason', 'DBStatus']

rx_asset = re.compile(r"^(M/C X\d\d\d\d|OE-\d\d\d\d)$")
rx_job = re.compile(r"^\d\d-\d\d\d$")

instruments = {}
vendors = {}

def LoadPickles():
    global instruments, vendors
    instruments = pickle.load(open('/www/stss/db/instruments.p', 'rb'))
    vendors = pickle.load(open('/www/stss/db/vendors.p', 'rb'))

def DeletePurchases():
    deleted = 0
    for p in Purchase.objects.all():
        p.delete()
        deleted += 1
    print('DELETED', deleted, 'Purchase objects')

def ImportPurchases():
    for i in instruments.values():
        asset = GetAsset(i['AssetTag'])
        if not asset: continue
        AddPurchase(asset, i)

def GetAsset(text):
    if rx_asset.match(text):
        asset, created = Asset.objects.get_or_create(identifier=text)
        if created: print('Created Asset:', text)
        return asset
    if not rx_job.match(text): print('Bad Asset Identifier:', text)

def AddPurchase(asset, instrument):
    if not HasPurchase(instrument): return
    p = Purchase()
    p.date = instrument['PurchaseDate']
    if instrument['Vendor']:
        text = instrument['Vendor'].strip()
        text = vendors[text]
        v, created = Vendor.objects.get_or_create(name=text)
        p.vendor = v
    if instrument['PurchaseOrder']: p.reference = instrument['PurchaseOrder']
    p.total = instrument['Cost']
    p.save()
    asset.purchases.add(p, through_defaults={'cost': p.total})

def HasPurchase(instrument):
    if instrument['PurchaseDate']: return True
    if instrument['Vendor']: return True
    if instrument['PurchaseOrder']: return True
    if instrument['Cost']: return True

class Command(BaseCommand):

    def handle(self, *args, **options):
        LoadPickles()
        #DeletePurchases()
        ImportPurchases()