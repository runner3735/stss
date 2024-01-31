
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

from ..models import *
from ..forms import *
from .other import get_instance

# Person

def people(request):
  context = people_get_context(request)
  context['form'] = PeopleSearchForm(request.GET or None)
  return render(request, 'people.html', context)

def people_list(request):
  context = people_get_context(request)
  return render(request, 'people-list.html', context)

def people_get_context(request):
  page = request.GET.get('page', '1')
  status = request.GET.get('status', '')
  search = request.GET.get('search', '')
  q = Person.objects.all()
  if not status: q = q.exclude(status=0)
  elif status != 5: q=q.filter(status=status)
  if search: q = q.filter(Q(last__icontains=search) | Q(first__icontains=search))
  paginator = Paginator(q, 16)
  try:
    return {'people': paginator.page(page), 'status': status, 'search': search}
  except EmptyPage:
    return {'people': [], 'status': status, 'search': search}

def person_tab(request, pk, tab):
  person = get_object_or_404(Person, pk=pk)
  #time.sleep(2)
  if tab == 'assets':
    return render(request, 'person-assets.html', {'person': person})
  if tab == 'jobs':
    return render(request, 'person-jobs.html', {'person': person})
  if tab == 'tasks':
    return render(request, 'person-tasks.html', {'person': person})

@login_required
def person_new(request):
  form = PersonNewForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      person = form.save(commit=False)
      person.status = 1
      person.save()
      return HttpResponseRedirect(person.detail())
  return render(request, 'person-new.html', {'form': form})

def last_names(request):
  last = request.GET.get('last')
  if last:
    options = Person.objects.filter(last__istartswith=last).order_by('last').distinct().values_list('last', flat=True)
  else:
    options = []
  return render(request, 'datalist-options.html', {'options': options})

def first_names(request):
  last = request.GET.get('last')
  if last:
    options = Person.objects.filter(last=last).order_by('first').distinct().values_list('first', flat=True)
  else:
    options = []
  return render(request, 'datalist-options.html', {'options': options})

def person_phone(request, pk):
  person=get_object_or_404(Person, pk=pk)
  return HttpResponse('<strong>' + person.phone + '</strong>')
  
@login_required
def person_edit_phone(request, pk):
  person=get_object_or_404(Person, pk=pk)
  form = PersonPhoneForm(request.POST or None, instance=person)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'personPhoneChanged'
      return response
  return render(request, 'person-edit-phone.html', {'form': form})

def person_email(request, pk):
  person=get_object_or_404(Person, pk=pk)
  return HttpResponse('<strong>' + person.email + '</strong>')
  
@login_required
def person_edit_email(request, pk):
  person=get_object_or_404(Person, pk=pk)
  form = PersonEmailForm(request.POST or None, instance=person)
  if request.method == 'POST':
    username = request.POST.get('username')
    if username:
      form = PersonEmailForm({'email': username + '@middlebury.edu'}, instance=person)
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'emailChanged'})
  return render(request, 'person-edit-email.html', {'form': form})

def person_status(request, pk):
  person=get_object_or_404(Person, pk=pk)
  return HttpResponse('<strong>' + person.get_status_display() + '</strong>')

@login_required
def person_edit_status(request, pk):
  person = get_object_or_404(Person, pk=pk)
  form = PersonStatusForm(request.POST or None, instance=person)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'statusChanged'
      return response
  return render(request, 'edit-status.html', {'form': form})

def person_departments(request, pk):
  person = get_object_or_404(Person, pk=pk)
  departments = person.departments.all()
  return render(request, 'department-tags.html', {'departments': departments})

@login_required
def person_edit_department(request, pk):
  person = get_object_or_404(Person, pk=pk)
  form = DepartmentForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      department = form.cleaned_data['department']
      if 'add' in request.POST:
        person.departments.add(department)
      elif 'remove' in request.POST:
        person.departments.remove(department)
      return HttpResponse(status=204, headers={'HX-Trigger': 'departmentsChanged'})
  return render(request, 'departments-edit.html', {'form': form})

@login_required
def job_rooms_edit(request, pk):
  job = get_object_or_404(Job, pk=pk)
  form = RoomForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      room = form.cleaned_data['room']
      if 'add' in request.POST:
        job.rooms.add(room)
      elif 'remove' in request.POST:
        job.rooms.remove(room)
      return HttpResponse(status=204, headers={'HX-Trigger': 'roomsChanged'})
  return render(request, 'rooms-edit.html', {'form': form})

@login_required
def job_departments_edit(request, pk):
  job = get_object_or_404(Job, pk=pk)
  form = DepartmentForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      department = form.cleaned_data['department']
      if 'add' in request.POST:
        job.departments.add(department)
      elif 'remove' in request.POST:
        job.departments.remove(department)
      return HttpResponse(status=204, headers={'HX-Trigger': 'departmentsChanged'})
  return render(request, 'departments-edit.html', {'form': form})

@login_required
def add_technician(request, pk, technician):
  job = get_object_or_404(Job, pk=pk)
  job.technicians.add(technician)
  return HttpResponseRedirect(reverse('edit-technicians', args=[pk]))

@login_required
def remove_technician(request, pk, technician):
  job = get_object_or_404(Job, pk=pk)
  job.technicians.remove(technician)
  return HttpResponseRedirect(reverse('edit-technicians', args=[pk]))

@login_required
def addcontact(request, model, pk, contact):
  contactable = get_instance(model, pk)
  if model == 'job': contactable.customers.add(contact)
  else: contactable.contacts.add(contact)
  return HttpResponseRedirect(reverse('edit-contacts', args=[model, pk]))

@login_required
def uncontact(request, model, pk, contact):
  contactable = get_instance(model, pk)
  if model == 'job': contactable.customers.remove(contact)
  else: contactable.contacts.remove(contact)
  return HttpResponseRedirect(reverse('edit-contacts', args=[model, pk]))

@login_required
def edit_contacts(request, model, pk):
  contactable = get_instance(model, pk)
  return render(request, 'edit-contacts.html', {'contactable': contactable})

def contact_list(request, model, pk):
  contactable = get_instance(model, pk)
  if model == 'job': selected = contactable.customers.all()
  else: selected = contactable.contacts.all()
  choices = person_page(request)
  if not choices: choices = selected
  return render(request, 'contact-list.html', {'contactable': contactable, 'contacts': choices, 'selected': selected})

def person_page(request):
  q = Person.objects.exclude(status=0)
  page = request.GET.get('page','1')
  method = request.GET.get('method','')
  search = request.GET.get('search', '')
  if search and method == '1': q = q.filter(last__istartswith=search)
  elif search: q = q.filter(first__icontains=search)
  else: return
  paginator = Paginator(q, 20)
  try:
    return paginator.page(page)
  except EmptyPage:
    return

