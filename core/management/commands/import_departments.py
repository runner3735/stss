
import pickle
from django.core.management.base import BaseCommand
from ...models import Department

class Command(BaseCommand):

    def import_departments(self):
        departments = pickle.load(open('/mediafiles/db/departments.p', 'rb'))
        names = set(departments.values())
        for name in names:
            d = Department()
            d.name = name
            d.save()
        print('Done importing departments.')

    def handle(self, *args, **options):
        self.import_departments()
