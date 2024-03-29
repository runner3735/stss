
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

from ..models import *
from ..forms import *

# Home

def home(request):
  context = {}
  context['assets'] = Asset.objects.all().count()
  context['jobs'] = Job.objects.all().count()
  context['people'] = Person.objects.all().count()
  context['files'] = File.objects.all().count()
  context['pmis'] = PMI.objects.all().count()
  return render(request, 'home.html', context)

# Vendor

def vendors(request):
  q = Vendor.objects.all()
  paginator = Paginator(q, 18)
  context = {'vendors': paginator.page(1)}
  return render(request, 'vendors.html', context)

def vendor_list(request, page):
  q = Vendor.objects.all()
  method = request.POST.get('method','')
  search = request.POST.get('search', '')
  if search and method == '1': q = q.filter(name__istartswith=search)
  elif search: q = q.filter(name__icontains=search)
  paginator = Paginator(q, 18)
  try:
    vendors = paginator.page(page)
  except EmptyPage:
    vendors = []
  context = {'vendors': vendors}
  return render(request, 'vendor-list.html', context)

# Room

@login_required
def edit_room(request, model, pk):
  roomable = get_instance(model, pk)
  rooms = Room.objects.all()
  return render(request, 'edit-room.html', {'roomable': roomable, 'rooms': rooms})

@login_required
def select_room(request, model, pk, room):
  roomable = get_instance(model, pk)
  room = get_object_or_404(Room, pk=room)
  if model == 'asset':
    roomable.room = room
  else:
    roomable.office = room
  roomable.save()
  return HttpResponseRedirect(roomable.detail())

# Note

@login_required
def add_note(request, model, pk):
  notable = get_instance(model, pk)
  next = notable.detail()
  form = NoteForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      author = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
      note = form.save()
      note.author = author
      note.save()
      notable.notes.add(note)
      return HttpResponseRedirect(next)
  return render(request, 'note-new.html', {'form': form, 'next': next})

@login_required
def note_edit(request, pk):
  note=get_object_or_404(Note, pk=pk)
  editor = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
  if editor != note.author: return HttpResponse(status=204)
  form = NoteForm(request.POST or None, instance=note)
  if request.method == 'POST':
    if 'deleted' in request.POST:
      note.delete()
      return HttpResponse(status=204, headers={'HX-Trigger': 'noteChanged'})
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'noteChanged'})
  return render(request, 'note-edit.html', {'form': form, 'note': note})

# Tag

@login_required
def tags_edit(request, model, pk):
  taggable = get_instance(model, pk)
  if request.method == 'POST':
    tag = Tag()
    form = TagForm(request.POST, instance=tag)
    if form.is_valid():
      form.save()
      taggable.tags.add(tag)
      form = TagForm()
  else:
    form = TagForm()
  tags = Tag.objects.all()
  return render(request, 'tags-edit.html', {'form': form, 'taggable': taggable, 'tags': tags})

@login_required
def tag_add(request, model, pk, tag):
  taggable = get_instance(model, pk)
  taggable.tags.add(tag)
  return HttpResponseRedirect(reverse('edit-tags', args=[model, pk]))

@login_required
def tag_remove(request, model, pk, tag):
  taggable = get_instance(model, pk)
  taggable.tags.remove(tag)
  return HttpResponseRedirect(reverse('edit-tags', args=[model, pk]))

# Work

@login_required
def work_new(request, pk):
  job = get_object_or_404(Job, pk=pk)
  technician = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
  form = WorkForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      work = form.save()
      work.job = job
      work.technician = technician
      work.save()
      return HttpResponseRedirect(job.detail())
  return render(request, 'work-new.html', {'form': form, 'job': job})

@login_required
def work_edit(request, pk):
  work = get_object_or_404(Work, pk=pk)
  requester = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
  if work.technician != requester: return HttpResponseRedirect(work.job.detail())
  form = WorkForm(request.POST or None, instance=work)
  if request.method == 'POST':
    if 'delete' in request.POST:
      work.delete()
      return HttpResponseRedirect(work.job.detail())
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(work.job.detail())
  return render(request, 'work-edit.html', {'form': form, 'job': work.job})

# Development

def do_nothing(request, **kwargs):
  print(kwargs)
  return HttpResponse(status=204)

# Helper

def get_instance(model, pk): # this function is imported into several other view files
  if model == 'job':
    instance = get_object_or_404(Job, pk=pk)
  elif model == 'asset':
    instance = get_object_or_404(Asset, pk=pk)
  elif model == 'person':
    instance = get_object_or_404(Person, pk=pk)
  elif model == 'purchase':
    instance = get_object_or_404(Purchase, pk=pk)
  elif model == 'pmi':
    instance = get_object_or_404(PMI, pk=pk)
  else:
    instance = None
  return instance

