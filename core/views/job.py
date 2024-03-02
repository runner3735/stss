import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import AnonymousUser

from ..models import *
from ..forms import *

def job_find(request):
  next = request.GET.get('next', '')
  form = JobIdentifierForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      return HttpResponseRedirect(reverse('job-get', args=[form.cleaned_data['identifier']]))
  return render(request, 'job-find.html', {'form': form, 'next': next})

def job_get(request, identifier):
  job = get_object_or_404(Job, identifier=identifier)
  return render(request, 'job.html', {'job': job})

def jobs(request):
  form = JobSearchForm()
  return render(request, 'jobs.html', {'form': form})

def job_page(request):
  context = jobs_get_context(request)
  return render(request, 'job-page.html', context)

def job_table(request):
  context = jobs_get_context(request)
  return render(request, 'job-table.html', context)

def jobs_get_context(request):
  page = request.GET.get('page', '1')
  status = request.GET.get('status','1')
  search = request.GET.get('search', '')
  sortby = request.GET.get('sortby', '-id')
  searchin = request.GET.get('searchin', 'N')
  q = Job.objects.all()
  if status: q = q.filter(status=status)
  if search:
    if searchin == 'N': #name
      q = q.filter(name__icontains=search)
    elif searchin == 'D': #details
      q = q.filter(details__icontains=search)
    elif searchin == 'B': #budget
      q = q.filter(budget__icontains=search)
    elif searchin == 'C': #course
      q = q.filter(course__icontains=search)
    elif searchin == 'L': #location
      q = q.filter(location__icontains=search)
    elif searchin == 'Y': #year
      q = q.filter(year=search)
  q = q.order_by(sortby)
  paginator = Paginator(q, 20)
  try:
    return {'jobs': paginator.page(page)}
  except EmptyPage:
    return {'jobs': []}

def job_name(request, pk):
  j = get_object_or_404(Job, pk=pk)
  return HttpResponse('<strong>' + j.name + '</strong>')

def job_budget(request, pk):
  j = get_object_or_404(Job, pk=pk)
  return HttpResponse('<strong>' + j.budget + '</strong>')

def job_course(request, pk):
  j = get_object_or_404(Job, pk=pk)
  return HttpResponse('<strong>' + j.course + '</strong>')

def job_location(request, pk):
  j = get_object_or_404(Job, pk=pk)
  return HttpResponse('<strong>' + j.location + '</strong>')

def job_status(request, pk):
  j = get_object_or_404(Job, pk=pk)
  if j.status: return HttpResponse('<strong>' + j.get_status_display() + '</strong>')
  return HttpResponse('')

def job_category(request, pk):
  j = get_object_or_404(Job, pk=pk)
  if j.category: return HttpResponse('<strong>' + j.get_category_display() + '</strong>')
  return HttpResponse('')

def job_kind(request, pk):
  j = get_object_or_404(Job, pk=pk)
  if j.kind: return HttpResponse('<strong>' + j.get_kind_display() + '</strong>')
  return HttpResponse('')

def job_opened(request, pk):
  j=get_object_or_404(Job, pk=pk)
  if j.opened: return HttpResponse('<strong>' + j.opened.strftime('%B %-d, %Y') + '</strong>')
  return HttpResponse('')

def job_deadline(request, pk):
  j=get_object_or_404(Job, pk=pk)
  if j.deadline: return HttpResponse('<strong>' + j.deadline.strftime('%B %-d, %Y') + '</strong>')
  return HttpResponse('')

def job_closed(request, pk):
  j=get_object_or_404(Job, pk=pk)
  if j.closed: return HttpResponse('<strong>' + j.closed.strftime('%B %-d, %Y') + '</strong>')
  return HttpResponse('')

def job_name_edit(request, pk):
  if not request.user.is_authenticated: return HttpResponse(status=204)
  j = get_object_or_404(Job, pk=pk)
  if request.method == 'POST':
    form = JobNameForm(request.POST, instance=j)
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobNameChanged'})
  else:
    form = JobNameForm(instance=j)
  return render(request, 'job-name-edit.html', {'form': form})

def job_budget_edit(request, pk):
  if not request.user.is_authenticated: return HttpResponse(status=204)
  j = get_object_or_404(Job, pk=pk)
  if request.method == 'POST':
    form = JobBudgetForm(request.POST, instance=j)
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobBudgetChanged'})
  else:
    form = JobBudgetForm(instance=j)
  return render(request, 'job-budget-edit.html', {'form': form})

def job_course_edit(request, pk):
  if not request.user.is_authenticated: return HttpResponse(status=204)
  j = get_object_or_404(Job, pk=pk)
  if request.method == 'POST':
    form = JobCourseForm(request.POST, instance=j)
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobCourseChanged'})
  else:
    form = JobCourseForm(instance=j)
  return render(request, 'job-course-edit.html', {'form': form})

def job_location_edit(request, pk):
  if not request.user.is_authenticated: return HttpResponse(status=204)
  j = get_object_or_404(Job, pk=pk)
  if request.method == 'POST':
    form = JobLocationForm(request.POST, instance=j)
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobLocationChanged'})
  else:
    form = JobLocationForm(instance=j)
  return render(request, 'job-location-edit.html', {'form': form})

def job_opened_edit(request, pk):
  if not request.user.is_authenticated: return HttpResponse(status=204)
  j=get_object_or_404(Job, pk=pk)
  form = JobOpenedForm(request.POST or None, instance=j)
  if request.method == 'POST':
    if 'today' in request.POST:
      j.opened = datetime.date.today()
      j.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobOpenedChanged'})
    if 'clear' in request.POST:
      j.opened = None
      j.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobOpenedChanged'})
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobOpenedChanged'})
  return render(request, 'job-opened-edit.html', {'form': form})

def job_deadline_edit(request, pk):
  if not request.user.is_authenticated: return HttpResponse(status=204)
  j=get_object_or_404(Job, pk=pk)
  form = JobDeadlineForm(request.POST or None, instance=j)
  if request.method == 'POST':
    if 'today' in request.POST:
      j.deadline = datetime.date.today()
      j.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobDeadlineChanged'})
    if 'clear' in request.POST:
      j.deadline = None
      j.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobDeadlineChanged'})
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobDeadlineChanged'})
  return render(request, 'job-deadline-edit.html', {'form': form})

def job_closed_edit(request, pk):
  if not request.user.is_authenticated: return HttpResponse(status=204)
  job=get_object_or_404(Job, pk=pk)
  if not job.closed and job.status < 3: return HttpResponse(status=204)
  form = JobClosedForm(request.POST or None, instance=job)
  if request.method == 'POST':
    if 'today' in request.POST:
      job.closed = datetime.date.today()
      job.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobClosedChanged'})
    if 'clear' in request.POST:
      if not job.closed: return HttpResponse(status=204)
      job.closed = None
      job.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobClosedChanged'})
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobClosedChanged'})
  return render(request, 'job-closed-edit.html', {'form': form})

def job_status_edit(request, pk):
  if not request.user.is_authenticated: return HttpResponse(status=204)
  job = get_object_or_404(Job, pk=pk)
  form = JobStatusForm(request.POST or None, instance=job)
  if request.method == 'POST':
    if form.is_valid():
      if job.closed and form.cleaned_data['status'] < 3: return HttpResponse(status=204)
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobStatusChanged'})
  return render(request, 'job-status-edit.html', {'form': form})

def job_category_edit(request, pk):
  if not request.user.is_authenticated: return HttpResponse(status=204)
  job = get_object_or_404(Job, pk=pk)
  form = JobCategoryForm(request.POST or None, instance=job)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobCategoryChanged'})
  return render(request, 'job-category-edit.html', {'form': form})

def job_kind_edit(request, pk):
  if not request.user.is_authenticated: return HttpResponse(status=204)
  job = get_object_or_404(Job, pk=pk)
  form = JobKindForm(request.POST or None, instance=job)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'jobKindChanged'})
  return render(request, 'job-kind-edit.html', {'form': form})

@login_required
def job_details_edit(request, pk):
  job = get_object_or_404(Job, pk=pk)
  if request.method == 'POST':
    form = JobDetailsForm(request.POST, instance=job)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(job.detail())
  else:
    form = JobDetailsForm(instance=job)
  return render(request, 'job-details-edit.html', {'form': form, 'job': job})

def job_departments(request, pk):
  job = get_object_or_404(Job, pk=pk)
  departments = job.departments.all()
  return render(request, 'department-tags.html', {'departments': departments})

def job_rooms(request, pk):
  job = get_object_or_404(Job, pk=pk)
  rooms = job.rooms.all()
  return render(request, 'room-tags.html', {'rooms': rooms})

@login_required
def edit_technicians(request, pk):
  job = get_object_or_404(Job, pk=pk)
  return render(request, 'edit-technicians.html', {'job': job})

def technician_list(request, pk):
  job = get_object_or_404(Job, pk=pk)
  selected = job.technicians.all()
  choices = Person.objects.filter(status=1)
  return render(request, 'technician-list.html', {'contactable': job, 'contacts': choices, 'selected': selected})

def job_details(request, pk):
  job = get_object_or_404(Job, pk=pk)
  return render(request, 'job-details.html', {'job': job})

def job_assets(request, pk):
  job = get_object_or_404(Job, pk=pk)
  return render(request, 'job-assets.html', {'job': job})

def job_works(request, pk):
  job = get_object_or_404(Job, pk=pk)
  if isinstance(request.user, AnonymousUser):
    requester = None
  else:
    requester = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
  return render(request, 'job-works.html', {'job': job, 'requester': requester})

def job_notes(request, pk):
  job = get_object_or_404(Job, pk=pk)
  notes = job.notes.all()
  return render(request, 'note-list.html', {'notes': notes})

def job_files(request, pk):
  job = get_object_or_404(Job, pk=pk)
  return render(request, 'file-list.html', {'linkable': job})

def job_gallery(request, pk):
  job = get_object_or_404(Job, pk=pk)
  pictures = job.files.exclude(picture='')
  return render(request, 'picture-list.html', {'pictures': pictures, 'linkable': job})

@login_required
def job_assets_edit(request, pk):
  job = get_object_or_404(Job, pk=pk)
  return render(request, 'job-assets-edit.html', {'job': job})

def job_assets_list(request, pk):
  job = get_object_or_404(Job, pk=pk)
  selected = job.assets.all()
  choices = job_assets_page(request)
  if not choices: choices = selected
  return render(request, 'job-assets-list.html', {'job': job, 'choices': choices, 'selected': selected})

def job_assets_page(request):
  search = request.GET.get('search', '')
  if len(search) < 3: return
  search = 'M/C X' + search
  q = Asset.objects.filter(identifier__startswith=search)
  return q

@login_required
def job_asset_add(request, pk, asset):
  job = get_object_or_404(Job, pk=pk)
  a = get_object_or_404(Asset, pk=asset)
  job.assets.add(asset)
  if a.location and job.location:
    if a.location != job.location:
      job_location = job.location + '; ' + a.location
      job.location = job_location[:128]
      job.save()
  elif a.location:
    job.location = a.location
    job.save()
  if a.room: job.rooms.add(a.room)
  return HttpResponseRedirect(reverse('job-assets-edit', args=[pk]))

@login_required
def job_asset_remove(request, pk, asset):
  job = get_object_or_404(Job, pk=pk)
  job.assets.remove(asset)
  return HttpResponseRedirect(reverse('job-assets-edit', args=[pk]))

@login_required
def job_new(request):
  job = job_create()
  if job: return HttpResponseRedirect(reverse('job-details-edit', args=[job.id]))
  return HttpResponse(status=204, headers={'HX-Trigger': 'jobNotCreated'})

@login_required
def pmi_schedule(request, pk):
  pmi = get_object_or_404(PMI, pk=pk)
  job = job_create()
  if not job: return HttpResponse(status=204, headers={'HX-Trigger': 'jobNotCreated'})
  job.name = pmi.name
  job.location = pmi.location
  job.details = pmi.details
  job.deadline = pmi.next
  job.category = 5
  job.customers.set(pmi.customers.all())
  job.departments.set(pmi.departments.all())
  job.rooms.set(pmi.rooms.all())
  job.files.set(pmi.files.all())
  job.assets.set(pmi.assets.all())
  job.save()
  pmi.job = job
  pmi.save()
  return HttpResponseRedirect(job.detail())

def job_create():
  now = datetime.date.today()
  fiscal_year = now.year
  if now.month > 6: fiscal_year += 1
  prefix = str(fiscal_year)[2:4] + '-'
  year_jobs = Job.objects.filter(year=fiscal_year).order_by('-identifier').values_list('identifier', flat=True)[:1]
  if year_jobs: suffix = str(int(year_jobs[0][-3:]) + 1).zfill(3)
  else: suffix = '001'
  next_identifier = prefix + suffix
  job, created = Job.objects.get_or_create(identifier=next_identifier)
  if not created: return
  job.year = fiscal_year
  job.status = 1
  job.opened = now
  job.save()
  return job

def job_rooms_edit(request, pk):
  if not request.user.is_authenticated: return HttpResponse(status=204)
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

def job_departments_edit(request, pk):
  if not request.user.is_authenticated: return HttpResponse(status=204)
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