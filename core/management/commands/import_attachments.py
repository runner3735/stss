# this script imports attachments
# must be done after importing assets and jobs

import hashlib, os
from datetime import datetime

from django.core.management.base import BaseCommand
from ...models import Person, File, Asset, Job

admin = Person.objects.get(first='Database', last='Administrator')

def GetStats(folder):
    print('statistics for:', folder)
    size = 0
    filecount = 0
    for root, dirs, files in os.walk(folder):
        for f in files:
            filepath = os.path.join(root, f)
            size += os.path.getsize(filepath)
            filecount += 1
            if f == 'Thumbs.db': print(filepath)
    print('total size:', size)
    print('files:', filecount)
    print()

def CheckAttachments(): # this function reveals 11 duplicate files
    paths = {}
    for root, dirs, files in os.walk('/www/attachments'):
        for f in files:
            filepath = os.path.join(root, f)
            ts = os.path.getmtime(filepath)
            relpath = datetime.utcfromtimestamp(ts).strftime('files/%Y/%m/') + f
            if relpath in paths:
                print(filepath, md5checksum(filepath))
                print(paths[relpath], md5checksum(paths[relpath]))
                print()
            else:
                paths[relpath] = filepath

def ImportAttachments():
    for asset_text in os.listdir('/www/attachments/Instruments'):
        identifier = 'M/C X' + asset_text[3:]
        asset = Asset.objects.get(identifier=identifier)
        asset_folder = os.path.join('/www/attachments/Instruments', asset_text)
        create_files(asset, asset_folder)
    for identifier in os.listdir('/www/attachments/Jobs'):
        job = Job.objects.get(identifier=identifier)
        job_folder = os.path.join('/www/attachments/Jobs', identifier)
        create_files(job, job_folder)

def create_files(attachable, folderpath):
    for f in os.listdir(folderpath):
        create_file(attachable, folderpath, f)

def create_file(attachable, folder, filename):
    if filename == 'Thumbs.db':
        print('ignoring Thumbs.db')
        return
    filepath = os.path.join(folder, filename)
    name, ext = os.path.splitext(filename)
    file = File()
    file.contributor = admin
    file.name = name
    file.hash = md5checksum(filepath)
    matching = File.objects.filter(hash=file.hash).first()
    if matching:
        print('duplicate:', filepath)
        os.unlink(filepath)
        file.content = matching.content
        if ext.lower() in ['.jpg', '.gif', '.webp', '.png', '.jpeg']: file.picture = matching.picture
    else:
        ts = os.path.getmtime(filepath)
        relfolder = datetime.utcfromtimestamp(ts).strftime('files/%Y/%m/')
        relpath = relfolder + filename
        file.content = relpath
        if ext.lower() in ['.jpg', '.gif', '.webp', '.png', '.jpeg']: file.picture = relpath
        newpath = file.filepath()
        newfolder = os.path.split(newpath)[0]
        os.makedirs(newfolder, exist_ok=True)
        try:
            os.rename(filepath, newpath)
        except:
            print('RENAME ERROR:', filepath, ' --> ', newpath)
    try:
        file.save()
        attachable.files.add(file)
    except:
        print('SAVE ERROR:', filepath, 'length:', len(filename))

def md5checksum(filepath):
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(8388608)
            if chunk:
                md5.update(chunk)
            else:
                return md5.hexdigest()

class Command(BaseCommand):

    def handle(self, *args, **options):
        GetStats('/www/attachments')
        ImportAttachments()


