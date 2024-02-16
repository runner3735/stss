# this script creates authenticated user objects for the stss website
# superuser with username 'admin' must already exist

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Person

def UpdateAdmin():
    admin = User.objects.get(username='admin')
    admin.first_name = 'Database'
    admin.last_name = 'Administrator'
    admin.save()
    Person.objects.get_or_create(first='Database', last='Administrator')

def CreateUser(username, first, last):
    email = username + '@middlebury.edu'
    User.objects.create_user(username=username, email=email, password='mystss77', first_name=first, last_name=last)
    print('first:', first, '\tlast:', last, '\tusername:', username, '\temail:', email, '\tpassword: mystss77')
    Person.objects.get_or_create(first=first, last=last)

class Command(BaseCommand):

    def handle(self, *args, **options):
        UpdateAdmin()
        CreateUser('lritchie', 'Lance', 'Ritchie')
        CreateUser('jodys', 'Jody', 'Smith')
        CreateUser('cdonohue', 'Carrie', 'Donohue')
        CreateUser('cacarr', 'Caitlin', 'Carr')
        CreateUser('ejmcmahon', 'Eamon', 'McMahon')
        CreateUser('kbooth', 'Kevin', 'Booth')
        CreateUser('twicklan', 'Tim', 'Wickland')
        CreateUser('cekstrom', 'Cathy', 'Ekstrom')

