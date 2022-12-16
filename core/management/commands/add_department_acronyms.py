
# this script adds a 4-character acronym to the Department objects

import pickle
from django.core.management.base import BaseCommand
from ...models import Department

def AddAcronyms():
    departments = pickle.load(open('/www/stss/db/departments.p', 'rb'))
    acronyms = {}
    for acronym, name in departments.items():
        if len(acronym) == 4:
            acronyms[name] = acronym.upper()
    for department in Department.objects.all():
        if department.name in acronyms:
            department.acronym = acronyms[department.name]
        else:
            print('No Acronym:', department.name)
            department.acronym = 'NONE'
        department.save()

class Command(BaseCommand):

    def handle(self, *args, **options):
        AddAcronyms()

