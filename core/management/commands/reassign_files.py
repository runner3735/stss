# this script finds files owned by admin, and reassigns them to the job technician or asset contact
# must be done after importing attachments

from django.core.management.base import BaseCommand
from ...models import Person, File, Asset, Job

admin = Person.objects.get(first='Database', last='Administrator')

def assign_asset_files():
    for asset in Asset.objects.all():
        if asset.files.count():
            contact = asset.contacts.first()
            if contact:
                files = asset.files.all()
                reassign(files, contact)

def assign_job_files():
    for job in Job.objects.all():
        if job.files.count():
            technician = job.technicians.first()
            if technician:
                files = job.files.all()
                reassign(files, technician)
                

def reassign(files, contributor):
    print('reassigning files to:', contributor.first, contributor.last)
    for file in files:
        if file.contributor == admin:
            file.contributor = contributor
            file.save()

class Command(BaseCommand):

    def handle(self, *args, **options):
        assign_asset_files()
        assign_job_files()



