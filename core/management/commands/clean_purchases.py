# this script sets the method and cleans up the reference fields for Purchase objects
# must import people and purchases first

import re
from django.core.management.base import BaseCommand
from ...models import Purchase, Person

rx_po = re.compile(r"^P[O\.# ]*(\d{4,7})$")
rx_po2 = re.compile(r"^MD-PO-\d+$")
rx_po3 = re.compile(r"^\d+$")
rx_cc = re.compile(r"^(CC|cc|credit card|Credit Card|Card)[-# ]*(.*)$")
rx_cc2 = re.compile(r"^(CD|JM|JS|CE|CC|MM)[-# ]*(\d+)$")

def SplitReferences():
    count = 0
    for purchase in Purchase.objects.all():
        if '/' in purchase.reference:
            parts = purchase.reference.split('/')
            if len(parts) != 2:
                print('TOO MANY PARTS:', purchase.reference)
                continue
            purchase.reference = parts[0].strip()
            purchase.vreference = parts[1].strip()
            purchase.save()
            count += 1
    print('Split References:', count)

def GetPurchasers():
    purchasers = {}
    purchasers['CD'] = Person.objects.get_or_create(first='Carrie', last='Donohue')[0]
    purchasers['JM'] = Person.objects.get_or_create(first='Judy', last='Mayer')[0]
    purchasers['JS'] = Person.objects.get_or_create(first='Joanna', last='Shipley')[0]
    purchasers['CE'] = Person.objects.get_or_create(first='Cathy', last='Ekstrom')[0]
    purchasers['CC'] = Person.objects.get_or_create(first='Catherine', last='Combelles')[0]
    purchasers['MM'] = Person.objects.get_or_create(first='Michelle', last='Matot')[0]
    for purchaser in purchasers.values():
        purchaser.status = 6
        purchaser.save()
    return purchasers

def CleanPurchases():
    purchasers = GetPurchasers()
    noreference = 0
    nomatch = 0
    pos = []
    ccs = []
    for purchase in Purchase.objects.filter(method__isnull=True):
        if not purchase.reference:
            noreference += 1
            continue
        m = rx_po.match(purchase.reference)
        if m:
            purchase.method = 2
            purchase.reference = 'P' + m[1].zfill(7)
            purchase.save()
            if purchase.reference != m[0]:
                pos.append(m[0] + ' --> ' + purchase.reference)
            else:
                pos.append(m[0])
            continue
        m = rx_po2.match(purchase.reference)
        if m:
            purchase.method = 2
            purchase.save()
            if purchase.reference != m[0]:
                pos.append(m[0] + ' --> ' + purchase.reference)
            else:
                pos.append(m[0])
            continue
        m = rx_po3.match(purchase.reference)
        if m:
            number = int(purchase.reference)
            if number > 4007 and number < 37869:
                purchase.method = 2
                purchase.reference = 'P' + purchase.reference.zfill(7)
                purchase.save()
                if purchase.reference != m[0]:
                    pos.append(m[0] + ' --> ' + purchase.reference)
                else:
                    pos.append(m[0])
                continue
        m = rx_cc2.match(purchase.reference)
        if m:
            purchase.method = 1
            purchase.reference = m[1] + m[2]
            purchase.purchaser = purchasers[m[1]]
            purchase.save()
            if purchase.reference != m[0]:
                ccs.append(m[0] + ' --> ' + purchase.reference)
            else:
                ccs.append(m[0])
            continue
        m = rx_cc.match(purchase.reference)
        if m:
            purchase.method = 1
            purchase.reference = m[2]
            purchase.save()
            if purchase.reference != m[0]:
                ccs.append(m[0] + ' --> ' + purchase.reference)
            else:
                ccs.append(m[0])
            continue
        nomatch += 1
        print('No Match:', purchase.reference)
    with open('/www/purchase_orders.txt', 'w') as f: f.write('\n'.join(pos))
    with open('/www/credit_card_orders.txt', 'w') as f: f.write('\n'.join(ccs))
    print('No Reference:', noreference)
    print('Purchase Orders Identified:', len(pos))
    print('Credit Card Orders Identified:', len(ccs))
    print('No Match:', nomatch)

class Command(BaseCommand):

    def handle(self, *args, **options):
        SplitReferences()
        CleanPurchases()