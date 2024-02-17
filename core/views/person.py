
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

def person_assets(request, pk):
  person = get_object_or_404(Person, pk=pk)
  return render(request, 'person-assets.html', {'person': person})

def person_jobs(request, pk):
  person = get_object_or_404(Person, pk=pk)
  return render(request, 'job-list.html', {'jobs': person.jobs_as_customer.all()})

def person_tasks(request, pk):
  person = get_object_or_404(Person, pk=pk)
  return render(request, 'job-list.html', {'jobs': person.jobs_as_technician.all()})

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
def person_add(request, person, model, pk):
  linkable = get_instance(model, pk)
  if model == 'job': linkable.customers.add(person)
  elif model == 'pmi': linkable.customers.add(person)
  else: linkable.contacts.add(person)
  return HttpResponseRedirect(reverse('people-select', args=[model, pk]))

@login_required
def person_remove(request, person, model, pk):
  linkable = get_instance(model, pk)
  if model == 'job': linkable.customers.remove(person)
  elif model == 'pmi': linkable.customers.remove(person)
  else: linkable.contacts.remove(person)
  return HttpResponseRedirect(reverse('people-select', args=[model, pk]))

@login_required
def people_select(request, model, pk):
  linkable = get_instance(model, pk)
  return render(request, 'people-select.html', {'linkable': linkable})

def people_tags(request, model, pk):
  linkable = get_instance(model, pk)
  if model == 'asset': selected = linkable.contacts.all()
  else: selected = linkable.customers.all()
  choices = person_choices(request)
  if not choices: choices = selected
  return render(request, 'people-tags.html', {'linkable': linkable, 'choices': choices, 'selected': selected})

def person_choices(request):
  method = request.GET.get('method', '')
  search = request.GET.get('search', '')
  if not search: return
  if method == '1': return Person.objects.exclude(status=0).filter(last__istartswith=search)
  return Person.objects.exclude(status=0).filter(first__icontains=search)

