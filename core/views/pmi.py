
import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from ..models import *
from ..forms import *

@login_required
def pmi_new(request):
  form = PMIForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      pmi = form.save()
      pmi.creator = Person.objects.get(first=request.user.first_name, last=request.user.last_name)
      if pmi.last_job:
        job = Job.objects.get(identifier=pmi.last_job)
        pmi.name = job.name
        pmi.details = job.details
        pmi.location = job.location
        pmi.customers.set(job.customers.all())
        pmi.departments.set(job.departments.all())
        pmi.rooms.set(job.rooms.all())
        pmi.files.set(job.files.all())
        pmi.assets.set(job.assets.all())
        if job.closed:
          pmi.last = job.closed
          pmi.next = job.closed + datetime.timedelta(days=pmi.frequency)
        else:
          pmi.last_job = ''
          pmi.next = job.deadline
          pmi.job = job
      pmi.save()
      return HttpResponseRedirect(reverse('pmi', args=[pmi.pk]))
  return render(request, 'pmi-new.html', {'form': form})

# Display

def pmi_frequency(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  return HttpResponse(pmi.frequency)

def pmi_name(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  return HttpResponse(pmi.name)

def pmi_location(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  return HttpResponse(pmi.location)

def pmi_next(request, pk):
  pmi=get_object_or_404(PMI, pk=pk)
  if pmi.next: return HttpResponse(pmi.next.strftime('%B %-d, %Y'))
  return HttpResponse('')

@login_required
def pmi_name_edit(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  form = PMINameForm(request.POST or None, instance=pmi)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'pmiNameChanged'})
  return render(request, 'job-name-edit.html', {'form': form})

@login_required
def pmi_frequency_edit(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  if request.method == 'POST':
    form = PMIFrequencyForm(request.POST, instance=pmi)
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'pmiFrequencyChanged'})
  else:
    form = PMIFrequencyForm(instance=pmi)
  return render(request, 'pmi-frequency-edit.html', {'form': form})

@login_required
def pmi_location_edit(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  form = PMILocationForm(request.POST or None, instance=pmi)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'pmiLocationChanged'})
  return render(request, 'job-location-edit.html', {'form': form})

def pmi_files(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  return render(request, 'file-list.html', {'linkable': pmi})

def pmi_assets(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  return render(request, 'asset-list.html', {'linkable': pmi})

# Edit

@login_required
def pmi_next_edit(request, pk):
  pmi=get_object_or_404(PMI, pk=pk)
  form = PMINextForm(request.POST or None, instance=pmi)
  if request.method == 'POST':
    if 'today' in request.POST:
      pmi.next = datetime.date.today()
      pmi.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'pmiNextChanged'})
    if 'clear' in request.POST:
      pmi.next = None
      pmi.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'pmiNextChanged'})
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'pmiNextChanged'})
  return render(request, 'pmi-next-edit.html', {'form': form})

@login_required
def pmi_asset_add(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  form = AssetIdentifierForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      asset_tag = 'M/C X' + str(form.cleaned_data['identifier']).zfill(4)
      asset = Asset.objects.filter(identifier=asset_tag).first()
      if not asset: return HttpResponse(status=204)
      pmi.assets.add(asset)
      return HttpResponse(status=204, headers={'HX-Trigger': 'assetsChanged'})
  return render(request, 'form-asset-add.html', {'form': form})

@login_required
def pmi_completed(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  if pmi.job and pmi.job.closed and pmi.job.status == 3:
    pmi.last_job = pmi.job.identifier
    pmi.last = pmi.job.closed
    pmi.next = pmi.job.closed + datetime.timedelta(days=pmi.frequency)
    pmi.job = None
    pmi.save()
    return HttpResponseRedirect(reverse('pmis'))
  return HttpResponse(status=204)

def pmi_departments(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  departments = pmi.departments.all()
  return render(request, 'department-tags.html', {'departments': departments})

def pmi_rooms(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  rooms = pmi.rooms.all()
  return render(request, 'room-tags.html', {'rooms': rooms})

@login_required
def pmi_rooms_edit(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  form = RoomForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      room = form.cleaned_data['room']
      if 'add' in request.POST:
        pmi.rooms.add(room)
      elif 'remove' in request.POST:
        pmi.rooms.remove(room)
      return HttpResponse(status=204, headers={'HX-Trigger': 'roomsChanged'})
  return render(request, 'rooms-edit.html', {'form': form})

@login_required
def pmi_departments_edit(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  form = DepartmentForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      department = form.cleaned_data['department']
      if 'add' in request.POST:
        pmi.departments.add(department)
      elif 'remove' in request.POST:
        pmi.departments.remove(department)
      return HttpResponse(status=204, headers={'HX-Trigger': 'departmentsChanged'})
  return render(request, 'departments-edit.html', {'form': form})

@login_required
def pmi_details_edit(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  form = PMIDetailsForm(request.POST or None, instance=pmi)
  if request.method == 'POST':    
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(pmi.detail())
  return render(request, 'pmi-details-edit.html', {'form': form, 'pmi': pmi})