import os
import core.ffutil as ff

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from ..models import *
from ..forms import *
from .other import get_instance

# Picture

def picture_modal(request, picture, model, pk):
  picture = get_object_or_404(File, pk=picture)
  linkable = get_instance(model, pk)
  return render(request, 'picture-modal.html', {'picture': picture, 'linkable': linkable})

# Upload

@login_required
def upload(request, model="", pk=""):
  return render(request, 'upload.html', {'model': model, 'pk': pk})

@login_required
def file_upload(request):
  if request.method == 'POST':
    upload = request.FILES.get('file')
    model = request.POST.get('model', None)
    pk = request.POST.get('pk', None)
    if model and pk:
      attachable = get_instance(model, pk)
    else:
      attachable = None
    create_file(request, upload, attachable)
  return HttpResponse('')

@login_required
def create_file(request, upload, attachable):
  contributor = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
  name, ext = os.path.splitext(upload.name)
  file = File()
  file.contributor = contributor
  file.content = upload
  if ext.lower() in ['.jpg', '.gif', '.webp', '.png', '.jpeg']: file.picture = upload
  file.name = name
  file.save()
  if attachable: attachable.files.add(file)

# File

@login_required
def file_name_edit(request, pk):
  file = get_object_or_404(File, pk=pk)
  user = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
  if user != file.contributor: return HttpResponse(status=204)
  form = FileNameForm(request.POST or None, instance=file)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'fileChanged'})
  return render(request, 'file-name-edit.html', {'form': form})

@login_required
def file_remove(request, file, model, pk):
  file = get_object_or_404(File, pk=file)
  user = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
  if user != file.contributor: return HttpResponse(status=204)
  linkable = get_instance(model, pk)
  linkable.files.remove(file)
  if linkable.files.count(): return HttpResponse('')
  return HttpResponse(status=204, headers={'HX-Trigger': 'fileChanged'})

@login_required
def picture_remove(request, file, model, pk):
  file = get_object_or_404(File, pk=file)
  user = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
  if user != file.contributor: return HttpResponse(status=204)
  linkable = get_instance(model, pk)
  linkable.files.remove(file)
  return HttpResponse(status=204, headers={'HX-Trigger': 'galleryChanged'})
