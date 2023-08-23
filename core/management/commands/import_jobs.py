
# this script imports the instruments table, and creates Person, Department, Room, Manufacturer, Purchase, Tag, Note and Asset objects

import pickle, re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Department, Person, Manufacturer, Tag, Room, Note, Asset, Job

# instrument fields
# ['AssetTag', 'InventoryDate', 'InstrumentName', 'Nickname', 'Manufacturer', 'Model', 'SerialNumber', 'PurchaseDate', 'Vendor', 
# 'PurchaseOrder', 'Cost', 'Department', 'Contact', 'Room', 'OldRoom', 'DecommissionDate', 'OperatorManual', 'ServiceManual', 'Notes', 
# 'RemovalReason', 'DBStatus']
jobs = {}
departments = {}
names = {}
dualnames = {}
manufacturers = {}
rooms = {}

rx_asset = re.compile(r"^(M/C X\d\d\d\d|OE-\d\d\d\d)$")
rx_job = re.compile(r"^\d\d-\d\d\d$")

def LoadPickles():
    global jobs, departments, names, dualnames, manufacturers, rooms
    jobs = pickle.load(open('/www/db/jobs.p', 'rb'))
    departments = pickle.load(open('/www/db/departments.p', 'rb'))
    names = pickle.load(open('/www/db/names.p', 'rb'))
    dualnames = pickle.load(open('/www/db/dualnames.p', 'rb'))
    manufacturers = pickle.load(open('/www/db/manufacturers.p', 'rb'))
    rooms = pickle.load(open('/www/db/rooms.p', 'rb'))

def DeleteJobs():
    for j in Job.objects.all():
        j.delete()
        print(j.identifier, ' DELETED')

def CheckDepartments():
    print('Departments Count:', len(departments))
    for j in jobs.values():
        text = j['Department']
        if not text: continue
        for line in text.splitlines():
            for part in line.split('/'):
                if part.strip() in departments:
                    print(part.strip(), ' --> ', departments[part.strip()])
                else:
                    AddDepartmentString(part.strip())
    print('Departments Count:', len(departments))
    if input('Save changes to disk? [n] > '):
        pickle.dump(departments, open('/www/stss/db/departments.p', 'wb'))
        print('data saved!')

def AddDepartmentString(text):
    global departments
    print('UNKNOWN DEPARTMENT:', text)
    department = input('Enter Department Name: [ignore] > ')
    if department: departments[text] = department

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
    for J in jobs.values():
        job = GetJob(J['ID'])
        continue
        if not job: continue
        AddNames(job, J['InstrumentName'], J['Nickname'])
        AddModel(job, J['Model'])
        AddSerial(job, J['SerialNumber'])
        AddRoom(job, J['Room'])
        AddInventoried(job, J['InventoryDate'])
        AddManufacturer(job, J['Manufacturer'])
        AddDepartment(job, J['Department'])
        job.status = GetStatus(job, J['RemovalReason'])
        AddRemovalNote(job, J['DecommissionDate'])
        AddContacts(job, J['Contact'])
        AddTags(job, J)
        #AddEquipmentInfo(job) # this is to add equipment entries in instruments table as a note
        AddNotes(job, J['Notes'])
        job.save()

def GetJob(text):
    if rx_job.match(text):
        job, created = Job.objects.get_or_create(identifier=text)
        return job
    print('Bad Job ID:', text)

def AddNames(job, name, nickname):
    if name and nickname:
        job.name = name
        if nickname != name: job.nickname = nickname
    elif nickname:
        job.name = nickname
    elif name:
        job.name = name

def AddModel(job, text):
    if text: job.model = text

def AddSerial(job, text):
    if text: job.serial = text

def AddRoom(job, text):
    if not text: return
    if text.strip() in rooms:
        room = rooms[text.strip()]
        R, created = Room.objects.get_or_create(text=room)
        job.room = R
    else:
        job.location = ' --> '.join(text.splitlines())

def AddInventoried(job, text):
    if text: job.inventoried = text

def AddManufacturer(job, text):
    if not text: return
    options = []
    for line in text.splitlines():
        for part in line.split('/'):
            m = manufacturers[part.strip()]
            if m: options.append(m)
    if not options:
        print('Ignoring Manufacturer Text:', text)
        return
    selected = SelectManufacturer(options)
    if selected:
        M, created = Manufacturer.objects.get_or_create(name=selected)
        job.manufacturer = M

def SelectManufacturer(options):
    if len(options) == 1: return options[0]
    return ' / '.join(options) # I was always selecting the multiple option, so just make it automatic
    options.append(' / '.join(options))
    for i, option in enumerate(options): print(i, option)
    selected = input('select option or o for other > ')
    if not selected: return
    if selected != 'o': return options[int(selected)]
    selected = input('enter manufacturer > ')
    return selected

def AddDepartment(job, text):
    if not text: return
    dept = text.strip()
    if dept in departments:
        D, created = Department.objects.get_or_create(name=departments[dept])
        job.department = D
    else:
        print('UNKNOWN DEPARTMENT:', job.identifier, dept)

def GetStatus(job, text):
    if not text: return 1
    if text == 'Discarded': return 2
    if text == 'Gifted': return 3
    if text == 'Parts Only': return 4
    if text == 'Faculty Left': return 5
    if text == 'Returned': return 6
    if text == 'lost at sea': return 7
    if text == 'Stolen': return 8
    print('UNRECOGNIZED RemovalReason:', job.identifier, text)
    return 9

def AddRemovalNote(job, text):
    if not text: return
    text = 'Date Removed From Service: ' + text
    AddNote(job, text)

def AddNote(job, text):
        n = Note()
        n.text = text
        n.contributor = User.objects.get(username='admin')
        n.save()
        job.notes.add(n)

def AddContacts(job, text):
    if not text: return
    if text in dualnames: text = dualnames[text]
    for part in text.split('/'):
        AddContact(job, part.strip())

def AddContact(job, text):
    if not text: return
    if text in names:
        first, last = names[text]
        person, created = Person.objects.get_or_create(first=first, last=last)
        job.contacts.add(person)
    else:
        print("Not Found In Names Dictionary:", text)

def AddTags(job, instrument):
    if instrument['OperatorManual']:
        T, created = Tag.objects.get_or_create(text='Operator Manual')
        job.tags.add(T)
    if instrument['ServiceManual']:
        T, created = Tag.objects.get_or_create(text='Service Manual')
        job.tags.add(T)

def AddNotes(job, text):
    if text: AddNote(job, text)

class Command(BaseCommand):

    def handle(self, *args, **options):
        LoadPickles()
        #CheckDepartments()
        #DeleteJobs()
        AnalyzeJobs()
        #ImportJobs()