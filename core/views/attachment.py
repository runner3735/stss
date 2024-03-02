import hashlib, os
import core.ffutil as ff
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()

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

def rotate(file, degrees):
  try: image = Image.open(file.picture)
  except: return
  image = image.rotate(degrees, expand=True)
  image.save(file.filepath())
  checksum_rename(file)

# Upload

@login_required
def upload(request, model="", pk=""):
  return render(request, 'upload.html', {'model': model, 'pk': pk})

@login_required
def upload_test(request):
  return render(request, 'upload-test.html')

@login_required
def file_upload(request):
  if request.method == 'POST':
    upload = request.FILES.get('file')
    model = request.POST.get('model', None)
    pk = request.POST.get('pk', None)
    if model and pk: attachable = get_instance(model, pk)
    else: attachable = None
    create_file(request, upload, attachable)
  return HttpResponse('')

@login_required
def create_file(request, upload, attachable):
  contributor = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
  name, ext = os.path.splitext(upload.name)
  file = File()
  file.contributor = contributor
  file.content = upload
  if ext.lower() in ['.jpg', '.gif', '.webp', '.png', '.jpeg']: file.picture = file.content
  file.name = name
  file.save()
  if attachable: attachable.files.add(file)
  path = file.filepath()
  checksum = md5checksum(path)
  matching = File.objects.filter(hash=checksum).first()
  if matching:
     os.unlink(path)
     file.content = matching.content
     if file.picture: file.picture = matching.content
  elif ext.lower() == '.heic':
     convert_image(file)
  file.hash = checksum
  file.save()

def convert_image(file):
  try:
      image = Image.open(file.content)
  except:
      print('unable to open:', file.content)
      return
  newpath = file.filepath() + '.jpg'
  if os.path.exists(newpath): 
    print('path already exists:', newpath)
    return
  image.save(newpath)
  file.picture = file.content.name + '.jpg'   

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

# Utility

def checksum_rename(file):
  folder, filename = os.path.split(file.content.name)
  folderpath = os.path.join(settings.MEDIA_ROOT, folder)
  ext = os.path.splitext(filename)[1]
  oldpath = os.path.join(folderpath, filename)
  newname = md5checksum(oldpath) + ext
  newpath = os.path.join(folderpath, newname)
  os.rename(oldpath, newpath)
  file.content = os.path.join(folder, newname)
  if file.picture: file.picture = os.path.join(folder, newname)
  file.save()

def md5checksum(filepath):
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(8388608)
            if chunk:
                md5.update(chunk)
            else:
                return md5.hexdigest()