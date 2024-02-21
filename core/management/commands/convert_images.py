# this script generates a jpg picture for each heic file
# must be done after importing attachments

import os
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

from django.core.management.base import BaseCommand
from ...models import File

def jobs_with_heic():
    jobs = set()
    for file in File.objects.all():
        if file.extension() == '.heic':
            print(file.content)
            for job in file.jobs.all(): jobs.add(job.identifier)
    print(jobs)
    print()

def convert_images():
    for file in File.objects.all():
        if file.extension() == '.heic':
            try:
                image = Image.open(file.content)
            except:
                print('unable to open:', file.content)
                continue
            newpath = file.filepath() + '.jpg'
            if not os.path.exists(newpath): image.save(newpath)
            else: print('path already exists:', newpath)
            file.picture = file.content.name + '.jpg'
            file.save()

class Command(BaseCommand):

    def handle(self, *args, **options):
        jobs_with_heic()
        convert_images()


