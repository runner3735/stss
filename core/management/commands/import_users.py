# this script creates authenticated user objects for the stss website

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

def CreateUser(username, first, last):
    email = username + '@middlebury.edu'
    user = User.objects.create_user(username=username, email=email, password='mystss77', first_name=first, last_name=last)
    print('first:', first, '\tlast:', last, '\tusername:', username, '\temail:', email, '\tpassword: mystss77')

class Command(BaseCommand):

    def handle(self, *args, **options):
        CreateUser('lritchie', 'Lance', 'Ritchie')
        CreateUser('jodys', 'Jody', 'Smith')
        CreateUser('cdonohue', 'Carrie', 'Donohue')
        CreateUser('cacarr', 'Caitlin', 'Carr')
        CreateUser('ejmcmahon', 'Eamon', 'McMahon')
        CreateUser('kbooth', 'Kevin', 'Booth')
        CreateUser('twicklan', 'Tim', 'Wickland')
        CreateUser('cekstrom', 'Cathy', 'Ekstrom')

