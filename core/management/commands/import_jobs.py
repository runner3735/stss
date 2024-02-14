
# this script imports the jobs table, and creates Job, Work, Note, Room, Department, and Person objects
# should import people and assets first
# requires User object with username "admin"

# there are many jobs with no closed date, so check that later

import pickle, re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Department, Person, Room, Note, Asset, Job, Work

instruments = {}
jobs = {}
departments = {}
names = {}
dualnames = {}
rooms = {}
locations = {}
choices = {}

rx_asset = re.compile(r"^(M/C X\d\d\d\d|OE-\d\d\d\d)$")
rx_job = re.compile(r"^\d\d-\d\d\d$")

def LoadPickles():
    global instruments, jobs, departments, names, dualnames, rooms, locations
    instruments = pickle.load(open('/www/db/instruments.p', 'rb'))
    jobs = pickle.load(open('/www/db/jobs.p', 'rb'))
    departments = pickle.load(open('/www/db/departments.p', 'rb'))
    names = pickle.load(open('/www/db/names.p', 'rb'))
    dualnames = pickle.load(open('/www/db/dualnames.p', 'rb'))
    rooms = pickle.load(open('/www/db/rooms.p', 'rb'))
    locations = pickle.load(open('/www/db/locations.p', 'rb'))

def LoadChoices():
    global choices
    for option, name in Job.kind_choices:
        choices[name] = option
    for option, name in Job.category_choices:
        choices[name] = option
    for option, name in Job.status_choices:
        choices[name] = option
    choices['Canceled'] = 4
    choices['Deleted'] = 4
    choices['Carried Over'] = 3
    choices['Moved Forward'] = 3
    choices['Delayed'] = 3
    choices['Carried Over FY06'] = 3
    choices['Carried to Next FY'] = 3
    choices['Preventive Maintenance Schedule'] = 5

def DeleteJobs():
    print('Jobs records before deletion:', Job.objects.all().count())
    Job.objects.all().delete()
    print('Jobs records after deletion:', Job.objects.all().count())

def AnalyzeJobs():
    types = set()
    categories = set()
    statuses = set()
    for J in jobs.values():
        t = J['Type']
        if t: types.add(t)
        c = J['Category']
        if c: categories.add(c)
        s = J['Status']
        if s: statuses.add(s)
    for t in types: print('Type:', t)
    for c in categories: print('Category:', c)
    for s in statuses: print('Status:', s)

# Main Command
def ImportJobs():
    if not User.objects.get(username='admin'):
        print('admin user not found. aborting.')
        return
    ids = []
    newids = []
    for id in jobs:
        if id.startswith('99'): ids.append(id)
        else: newids.append(id)
    ids.sort()
    print("Jobs from 1999:", len(ids))
    newids.sort()
    ids.extend(newids)
    print("Begin Importing Jobs")
    print('Jobs:', Job.objects.all().count())
    for id in ids:
        J = jobs[id]
        job = GetJob(J['ID'])
        if not job: continue
        AddNameDetails(job, J['Tag'], J['Details'])
        AddOpenedDeadlineClosed(job, J['Opened'], J['Deadline'], J['Closed'])
        AddKindCategoryStatus(job, J['Type'], J['Category'], J['Status'])
        AddCourseBudget(job, J['Course'], J['Budget'])
        AddNote(job, J['Comments'])
        AddDepartments(job, J['Department'])
        AddAsset(job, J['Instrument'])
        AddRoomsLocation(job, J['Location'])
        AddCustomers(job, J['Customer'])
        AddTechnicians(job, J['Technician'])
        AddWork(job, J['Hours'])
        AddYear(job)
        job.save()
    print("Done Importing Jobs")
    print('Jobs:', Job.objects.all().count())

def GetJob(text):
    if rx_job.match(text):
        job, created = Job.objects.get_or_create(identifier=text)
        return job
    print('Bad Job ID:', text)

def AddNameDetails(job, tag, details):
    if tag: tag = tag.strip()
    else: tag = ''
    if details: details = details.strip()
    else: details = ''
    if tag.lower() == details.lower(): details = ''
    job.name = tag
    job.details = details
    if not tag: print("NO TAG:", job.identifier)

def AddCourseBudget(job, course, budget):
    if course: job.course = course.strip()
    if budget: job.budget = budget.strip()

def AddAsset(job, instrument):
    if not instrument: return
    if rx_asset.match(instrument):
        asset, created = Asset.objects.get_or_create(identifier=instrument)
        if created: print("ASSET NOT FOUND FOR JOB:", job.identifier, "CREATING EMPTY ASSET:", instrument)
        job.assets.add(asset)

def AddEquipmentNotes():
    for instrument in instruments:
        if rx_job.match(instrument):
            job = Job.objects.get(identifier=instrument)
            note = CreateEquipmentNote(instrument)
            job.notes.add(note)
    print("Done adding equipment notes")

def CreateEquipmentNote(instrument):
    info = instruments[instrument]
    lines = []
    lines.append("Equipment Information")
    lines.append("")
    if info['InstrumentName']: lines.append("Name: " + info['InstrumentName'])
    if info['Manufacturer']: lines.append("Manufacturer: " + info['Manufacturer'])
    if info['Model']: lines.append("Model: " + info['Model'])
    if info['SerialNumber']: lines.append("Serial Number: " + info['SerialNumber'])
    n = Note()
    n.text = '\n'.join(lines)
    n.contributor = User.objects.get(username='admin')
    n.save()
    return n

def AddRoomsLocation(job, text):
    if not text: return
    text = text.replace('&', '/')
    for line in text.splitlines():
        for part in line.split('/'):
            AddRoomOrLocation(job, part.strip())

def AddRoomOrLocation(job, text):
    if not text: return
    if text in rooms:
        for room in rooms[text].split('/'):
            R, created = Room.objects.get_or_create(text=room)
            job.rooms.add(R)
    elif text not in locations:
        print('BAD ROOM TEXT:', text, "FOR", job.identifier)
    elif job.location:
        job.location = job.location + ' ' + locations[text]
    else:
        job.location = locations[text]

def AddOpenedDeadlineClosed(job, opened, deadline, closed):
    if opened: job.opened = opened
    else: print("NO OPENED DATE:", job.identifier)
    if deadline: job.deadline = deadline
    if closed: job.closed = closed

def AddDepartments(job, text):
    if not text: return
    for part in text.split('/'):
        dept = departments[part.strip()]
        D, created = Department.objects.get_or_create(name=dept)
        job.departments.add(D)

def AddKindCategoryStatus(job, type, category, status):
    if not type: job.kind = 1
    elif type in choices: job.kind = choices[type]
    else: print('UNKNOWN TYPE:', type)
    if not category: job.category = 1
    elif category in choices: job.category = choices[category]
    else: print('UNKNOWN CATEGORY:', category)
    if not status: print('NO STATUS:', job.identifier)
    elif status in choices: job.status = choices[status]
    else: print('UNKNOWN STATUS:', status)

def AddNote(job, comments):
    if not comments: return
    comments = comments.strip()
    if not comments: return
    n = Note()
    n.text = comments
    n.contributor = User.objects.get(username='admin')
    n.save()
    job.notes.add(n)

def AddCustomers(job, text):
    if not text: return
    if text in dualnames: text = dualnames[text]
    for part in text.split('/'):
        AddCustomer(job, part.strip())

def AddCustomer(job, text):
    if not text: return
    if text in names:
        first, last = names[text]
        person, created = Person.objects.get_or_create(first=first, last=last)
        if created:
            if not first: print("CREATED PERSON WITH NO FIRST NAME:", last)
            if not last: print("CREATED PERSON WITH NO LAST NAME:", first)
        job.customers.add(person)
    else:
        print("**NOT FOUND IN NAMES DICTIONARY:", text)

def AddTechnicians(job, text):
    if not text: return
    if text in dualnames: text = dualnames[text]
    for part in text.split('/'):
        AddTechnician(job, part.strip())

def AddTechnician(job, text):
    if not text: return
    if text in names:
        first, last = names[text]
        person, created = Person.objects.get_or_create(first=first, last=last)
        if created: print("CREATED PERSON:", first, last)
        job.technicians.add(person)
    else:
        print("Not Found In Names Dictionary:", text)

def AddWork(job, hours):
    if not hours: return
    w = Work(job=job, hours=hours)
    if job.closed: w.date = job.closed
    if job.technicians.count() > 1:
        technician, created = Person.objects.get_or_create(first="All", last="Technicians")
    else:
        technician = job.technicians.first()
    if technician: w.technician = technician
    else: print("NO TECHNICIAN FOR JOB:", job.identifier)
    w.save()

def AddYear(job):
    year = int(job.identifier[:2])
    if year == 99: year = 1999
    else: year = 2000 + year
    job.year = year

class Command(BaseCommand):

    def handle(self, *args, **options):
        LoadPickles()
        LoadChoices()

        #DeleteJobs()
        #AnalyzeJobs()

        ImportJobs()
        AddEquipmentNotes() # run this only once after importing jobs
