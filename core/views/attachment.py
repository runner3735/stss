import os
import core.ffutil as ff

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from ..models import *
from ..forms import *
from .other import get_instance

# Picture

def picture_detail(request, pk):
  picture = get_object_or_404(Picture, pk=pk)
  return render(request, 'picture.html', {'picture': picture})

def picture_modal_old(request, picture, model, pk):
  picture = get_object_or_404(Picture, pk=picture)
  linkable = get_instance(model, pk)
  return render(request, 'picture-modal.html', {'picture': picture, 'linkable': linkable})

def picture_modal(request, picture, model, pk):
  picture = get_object_or_404(File, pk=picture)
  linkable = get_instance(model, pk)
  return render(request, 'picture-modal.html', {'picture': picture, 'linkable': linkable})

@login_required
def picture_edit(request, pk):
  picture=get_object_or_404(Picture, pk=pk)
  next = picture.detail()
  if picture.contributor != request.user:
    return HttpResponseRedirect(next)
  if request.method == 'POST':
    form = PictureNameForm(request.POST, instance=picture)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(next)
  else:
    form = PictureNameForm(instance=picture)
  return render(request, 'picture-edit.html', {'form': form, 'picture': picture, 'next': next})

@login_required
def picture_rotate(request, pk, degrees):
  print('picture_rotate called')
  picture=get_object_or_404(Picture, pk=pk)
  if request.user == picture.contributor:
    picture.rotate(int(degrees))
  return HttpResponseRedirect(reverse('picture-edit', args=[pk]))

@login_required
def picture_delete(request, pk):
  picture=get_object_or_404(Picture, pk=pk)
  if picture.contributor == request.user:
    picture.delete()
  return HttpResponseRedirect(request.GET.get('next'))

def picture_remove_old(request, picture, model, pk):
  picture = get_object_or_404(Picture, pk=picture)
  if request.user != picture.contributor: return HttpResponse(status=204)
  linkable = get_instance(model, pk)
  linkable.pictures.remove(picture)
  return HttpResponse(status=204, headers={'HX-Trigger': 'pictureChanged'})

# Upload

@login_required
def upload(request, model="", pk=""):
  return render(request, 'upload.html', {'model': model, 'pk': pk})

@login_required
def file_upload_old(request):
  if request.method == 'POST':
    file = request.FILES.get('file')
    model = request.POST.get('model', None)
    pk = request.POST.get('pk', None)
    if model:
      attachable = get_instance(model, pk)
    else:
      attachable = None
    ext = os.path.splitext(file.name)[1]
    if model == 'purchase':
      create_document(request, file, attachable)
    elif ext.lower() in ['.jpg', '.gif', '.webp', '.png', '.jpeg']:
      create_picture(request, file, attachable)
    elif ext.lower() in ['.mp4', '.flv', '.webm', '.mkv', '.mov']:
      create_video(request, file, attachable)
    else:
      create_document(request, file, attachable)
    return HttpResponse('')
  print('ERROR: file_upload called not using post!')
  return JsonResponse({'post':'false'})

@login_required
def file_upload(request):
  if request.method == 'POST':
    upload = request.FILES.get('file')
    model = request.POST.get('model', None)
    pk = request.POST.get('pk', None)
    if model:
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
  print('created file', file.id)
  if attachable: attachable.files.add(file)

@login_required
def create_document(request, file, documentable):
  d = Document()
  d.contributor = request.user
  d.file = file
  d.name = os.path.splitext(file.name)[0]
  d.save()
  print('created document', d.id)
  if documentable: documentable.documents.add(d)

@login_required
def create_picture(request, file, picturable):
  p = Picture()
  p.contributor = request.user
  p.file = file
  p.name = os.path.splitext(file.name)[0]
  p.save()
  if not p.transpose():
    p.delete()
    return
  print('created picture', p.id)
  if picturable: picturable.pictures.add(p)

@login_required
def create_video(request, file, videoable):
  v = Video()
  v.contributor = request.user
  v.file = file
  v.name = os.path.splitext(file.name)[0]
  v.save()
  print('created video', v.id)
  ff.generate_thumb(v)
  if videoable: videoable.videos.add(v)

# Document

@login_required
def document_edit_name(request, pk):
  document = get_object_or_404(Document, pk=pk)
  form = DocumentNameForm(request.POST or None, instance=document)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'documentChanged'})
  return render(request, 'document-edit-name.html', {'form': form})



def document_remove(request, document, model, pk):
  document = get_object_or_404(Document, pk=document)
  if request.user != document.contributor: return HttpResponse(status=204)
  linkable = get_instance(model, pk)
  linkable.documents.remove(document)
  if linkable.documents.count(): return HttpResponse('')
  if model == 'purchase': return HttpResponse('', headers={'HX-Retarget': '#documents'})
  return HttpResponse('', headers={'HX-Retarget': '#document-table'})

def get_attachment(model, pk):
  if model == 'document':
    instance = get_object_or_404(Document, pk=pk)
  elif model == 'picture':
    instance = get_object_or_404(Picture, pk=pk)
  elif model == 'video':
    instance = get_object_or_404(Video, pk=pk)
  else:
    instance = None
  return instance

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
  return HttpResponse('') # lines below are used to clear the whole table if there are no files left, but this is a problem for the gallery view
  if linkable.files.count(): return HttpResponse('')
  if model == 'purchase': return HttpResponse('', headers={'HX-Retarget': '#files'})
  return HttpResponse('', headers={'HX-Retarget': '#file-table'})

@login_required
def picture_remove(request, file, model, pk):
  file = get_object_or_404(File, pk=file)
  user = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
  if user != file.contributor: return HttpResponse(status=204)
  linkable = get_instance(model, pk)
  linkable.files.remove(file)
  return HttpResponse(status=204, headers={'HX-Trigger': 'galleryChanged'})
