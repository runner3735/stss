
# this script looks through the Department field in jobs.py, and allows manual adding of department mapping to departments.py

import pickle
from django.core.management.base import BaseCommand

def UpdateDepartments():
    departments = pickle.load(open('/www/db/departments.p', 'rb'))
    jobs = pickle.load(open('/www/db/jobs.p', 'rb'))
    print('Departments Count:', len(departments))
    for j in jobs.values():
        text = j['Department']
        if not text: continue
        for line in text.splitlines():
            for part in line.split('/'):
                if part.strip() in departments: continue
                AddDepartmentString(part.strip(), departments)
    print('Departments Count:', len(departments))
    if input('Save changes to disk? [n] > '):
        pickle.dump(departments, open('/www/db/departments.p', 'wb'))
        print('data saved!')

def AddDepartmentString(text, departments):
    print('UNKNOWN DEPARTMENT:', text)
    department = input('Enter Full Department Name: [ignore] > ')
    if department: departments[text] = department

class Command(BaseCommand):

    def handle(self, *args, **options):
        UpdateDepartments()
 
