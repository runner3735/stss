
import pickle
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def pickle_test(self):
        people = pickle.load(open('/mediafiles/db/people.p', 'rb'))
        for p in people.values(): print(p)
        print('Done with pickle test.')

    def handle(self, *args, **options):
        self.pickle_test()
