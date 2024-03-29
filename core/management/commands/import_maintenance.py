
# this script imports the maintenance table, and creates PMI objects
# must import people and jobs first

import datetime, pickle
from django.core.management.base import BaseCommand
from ...models import Person, PMI, Job

maintenance = {} # ['ID', 'Frequency', 'Creator']

def LoadPickles():
    global maintenance
    maintenance = pickle.load(open('/www/db/maintenance.p', 'rb'))

def ImportMaintenance():
    PMI.objects.all().delete()
    for m in maintenance.values():
        username = m['Creator'][5:].lower()
        creator = GetPerson(username)
        reference = Job.objects.get(identifier=m['ID'])
        frequency = int(m['Frequency'])
        pmi = PMI()
        if reference.status == 3 and reference.closed:
            pmi.last_job = reference.identifier
            pmi.last = reference.closed
            pmi.next = reference.closed + datetime.timedelta(days=frequency)
        elif reference.status == 3:
            print('Import Error: reference job is complete, but there is no closed date!')
            print(reference.identifier)
            pmi.job = reference
        else:
            pmi.job = reference
        pmi.creator = creator
        pmi.frequency = frequency
        pmi.name = reference.name
        pmi.details = reference.details
        pmi.location = reference.location
        pmi.save()
        pmi.customers.set(reference.customers.all())
        pmi.departments.set(reference.departments.all())
        pmi.rooms.set(reference.rooms.all())
        pmi.assets.set(reference.assets.all())
        print('Imported:', reference)

def GetPerson(username):
    if username == 'jodys': return Person.objects.get(first='Jody', last='Smith')
    if username == 'goodrich': return Person.objects.get(first='Chris', last='Goodrich')
    if username == 'cdonohue': return Person.objects.get(first='Carrie', last='Donohue')
    if username == 'cacarr': return Person.objects.get(first='Caitlin', last='Carr')
    if username == 'ejmcmahon': return Person.objects.get(first='Eamon', last='McMahon')
    if username == 'kbooth': return Person.objects.get(first='Kevin', last='Booth')
    if username == 'twicklan': return Person.objects.get(first='Tim', last='Wickland')
    if username == 'cekstrom': return Person.objects.get(first='Cathy', last='Ekstrom')
    if username.endswith('\lance'): return Person.objects.get(first='Lance', last='Ritchie')
    if username == 'gsharon': return Person.objects.get(first='Greg', last='Sharon')
    print('Not Found:', username)

class Command(BaseCommand):

    def import_maintenance(self):
        LoadPickles()
        ImportMaintenance()

    def handle(self, *args, **options):
        self.import_maintenance()
