
from django.core.management.base import BaseCommand
from ...models import Tag

class Command(BaseCommand):

    def create_tags(self):
        t =Tag()
        t.text = 'Operator Manual'
        t.save()
        t =Tag()
        t.text = 'Service Manual'
        t.save()
        print("Tags created")
    
    def handle(self, *args, **options):
        self.create_tags()
