import os
from datetime import datetime
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from ..models import *
from ..forms import *
from .other import get_instance
from core.tasks import create_task, download_video, download_video_to, post_process
from celery.result import AsyncResult

# Youtube

@login_required
def youtube_new(request):
  form = DownloadForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      download = form.save(commit=False)
      download.downloader = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
      download.status = 'added to queue'
      download.status_date = datetime.datetime.now()
      download.save()
      #download_video(download.id)
      download_video.delay(download.id)
      return HttpResponseRedirect(reverse('my-downloads'))
  return render(request, 'youtube-new.html', {'form': form})

@login_required
def download_new(request):
  if request.method != 'POST': return HttpResponse(status=204)
  form = DownloadForm(request.POST)
  if form.is_valid():
    download = form.save(commit=False)
    download.downloader = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
    download.status = 'added to queue'
    download.status_date = datetime.datetime.now()
    download.save()
    #download_video(download.id)
    download_video.delay(download.id)
    form = DownloadForm()
    return render(request, 'download-form.html', {'form': form})
  return HttpResponse(status=204)

@login_required
def download_new_to(request, model, pk):
  if request.method != 'POST': return HttpResponse(status=204)
  form = DownloadForm(request.POST)
  if form.is_valid():
    download = form.save(commit=False)
    download.downloader = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
    download.status = 'added to queue'
    download.status_date = datetime.datetime.now()
    download.save()
    #download_video_to(download.id, model, pk)
    download_video_to.delay(download.id, model, pk)
    form = DownloadForm()
    return render(request, 'download-form.html', {'form': form})
  return HttpResponse(status=204)
   
@login_required
def download_delete(request, pk):
  download = get_object_or_404(Download, pk=pk)
  download.delete()
  return HttpResponse('')

@login_required
def downloads_delete(request):
  requester = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
  downloads = Download.objects.filter(downloader=requester)
  downloads.delete()
  return HttpResponseRedirect(reverse('my-downloads'))

def download_row(request, pk):
  download = get_object_or_404(Download, pk=pk)
  if download.status == 'downloading video': return render(request, 'download-pending.html', {'download': download})
  if download.status == 'added to queue': return render(request, 'download-pending.html', {'download': download})
  return render(request, 'download-finished.html', {'download': download})

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

# Upload

@login_required
def upload(request):
  form = DownloadForm()
  downlink = reverse('download-new')
  uplink = reverse('upload-file')
  next = reverse('my-files')
  return render(request, 'upload.html', {'downlink': downlink, 'uplink': uplink, 'next': next, 'form': form})

@login_required
def upload_to(request, model, pk):
  uplink = reverse('upload-file-to', args=[model, pk])
  next = reverse(model, args=[pk])
  if model == 'purchase': return render(request, 'upload.html', {'uplink': uplink, 'next': next})
  form = DownloadForm()
  downlink = reverse('download-new-to', args=[model, pk])
  return render(request, 'upload.html', {'downlink': downlink, 'uplink': uplink, 'next': next, 'form': form})

@login_required
def upload_file(request):
  if request.method == 'POST':
    upload = request.FILES.get('file')
    create_file(request, upload)
  return HttpResponse('')

@login_required
def upload_file_to(request, model, pk):
  if request.method == 'POST':
    upload = request.FILES.get('file')
    attachable = get_instance(model, pk)
    file = create_file(request, upload)
    attachable.files.add(file)
  return HttpResponse('')

@login_required
def create_file(request, upload):
  contributor = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
  name, ext = os.path.splitext(upload.name)
  file = File()
  file.contributor = contributor
  file.content = upload
  if ext.lower() in ['.jpg', '.gif', '.webp', '.png', '.jpeg']: file.picture = file.content
  file.name = name
  file.save()
  #post_process(file.id)
  post_process.delay(file.id)
  return file

# File

@login_required
def my_files(request):
   requester = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
   files = File.objects.filter(contributor=requester)
   return render(request, 'my-files.html', {'files': files})

@login_required
def my_downloads(request):
   requester = get_object_or_404(Person, first=request.user.first_name, last=request.user.last_name)
   downloads = Download.objects.filter(downloader=requester).order_by('-id')
   return render(request, 'my-downloads.html', {'downloads': downloads})

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

# Test

@csrf_exempt
def run_task(request):
    if request.POST:
        task_type = request.POST.get("type")
        task = create_task.delay(int(task_type))
        return JsonResponse({"task_id": task.id}, status=202)

@csrf_exempt
def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result, status=200)


