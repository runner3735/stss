# this script imports the instruments table, and creates Person, Department, Room, Manufacturer, Purchase, Tag, Note and Asset objects

import pickle, re
from django.core.management.base import BaseCommand
from ...models import Purchase

rx_po = re.compile(r"^P[O\.# ]*(\d{4,7})$")
rx_cc = re.compile(r"^(CC|cc|credit card|Credit Card|Card)[-# ]*(.*)$")

def CleanPurchases():
    pocount = 0
    cccount = 0
    unidentified = 0
    results = []
    for purchase in Purchase.objects.all():
        m = rx_po.match(purchase.reference)
        if m:
            purchase.method = 2
            purchase.reference = 'P' + m[1].zfill(7)
            purchase.save()
            results.append(m[0] + ' --> Method: Purchase Order, Internal Reference:' + purchase.reference)
            pocount += 1
            continue
        m = rx_cc.match(purchase.reference)
        if m:
            purchase.method = 1
            purchase.reference = m[2]
            purchase.save()
            results.append(m[0] + ' --> Method: Credit Card, Internal Reference:' + purchase.reference)
            cccount += 1
            continue
        unidentified += 1
    with open('/www/results.txt', 'w') as f: f.write('\n'.join(results))
    print('Purchase Orders Identified:', pocount)
    print('Credit Card Orders Identified:', cccount)
    print('Unmatched:', unidentified)

class Command(BaseCommand):

    def handle(self, *args, **options):
        CleanPurchases()