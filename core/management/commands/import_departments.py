
import shelve
from django.core.management.base import BaseCommand
from ...models import Department

class Command(BaseCommand):

    def import_departments(self):
        with shelve.open('/mediafiles/db/stss-import.shelf') as db:
            departments = db['departments']
        names = set(departments.values())
        for name in names:
            d = Department()
            d.name = name
            d.save()
        print('Done importing departments.')

    def handle(self, *args, **options):
        self.import_departments()
