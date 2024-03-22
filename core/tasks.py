
import time
from celery import shared_task

import json, os, yt_dlp
from datetime import datetime

from core.models import Download, File, Person

MEDIA_ROOT = os.getenv('MEDIA_ROOT', '')
tempfolder = '/www/temp/'

def update_status(download, status):
    download.status_date = datetime.now()
    download.status = status
    download.save() 

def find_files(id):
    picture = ''
    video = ''
    for f in os.listdir(tempfolder):
        base, ext = os.path.splitext(f)
        if base != id: continue
        if ext.lower() in ['.jpg', '.gif', '.webp', '.png', '.jpeg']: picture = f
        elif ext.lower() in ['.webm', '.mp4', '.mkv']: video = f
    return picture, video

def existing_file(existing, download):
    update_status(download, 'using existing video')
    if existing.contributor == download.downloader: return existing
    file, created = File.objects.get_or_create(url=existing.url, contributor=download.downloader)
    if not created: return file
    file.name = existing.name
    file.content = existing.content
    file.picture = existing.picture
    file.save()
    return file

def valid_url(url):
    if 'youtube' in url and '/watch?' in url: return True

@shared_task
def download_video(download_id):
    download = Download.objects.get(pk=download_id)
    if not valid_url(download.url): return update_status(download, 'invalid url')
    update_status(download, 'downloading video')
    opts = ytdlp_options(download.quality)

    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            info = ydl.extract_info(download.url, download=False)
            info = ydl.sanitize_info(info)
        except:
            return update_status(download, 'no video info found')
        
    url = info['webpage_url']
    existing = File.objects.filter(url=url).first()
    if existing: return existing_file(existing, download)

    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            error_code = ydl.download([url])
            if error_code: return update_status(download, 'video download failed with error code:' + str(error_code))
        except:
            return update_status(download, 'video download failed')
    
    picture, video = find_files(info['id'])
    if not video: return update_status(download, 'no video downloaded')
    year = info['upload_date'][:4]
    month = info['upload_date'][4:6]
    write_json(info, year, month)
    move_file(video, year, month)
    move_file(picture, year, month)
    file = File()
    file.contributor = download.downloader
    file.name = info['title']
    file.url = url
    file.content = os.path.join('files', year, month, video)
    if picture: file.picture = os.path.join('files', year, month, picture)
    file.save()
    update_status(download, 'video download successful')
    return file

def write_json(info, year, month):
    folder = os.path.join(MEDIA_ROOT, 'files', year, month)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, info['id'] + '.json')
    j = json.dumps(info, indent=4)
    with open(filepath, 'w') as f: f.write(j)

def move_file(filename, year, month):
    if not filename: return
    oldpath = os.path.join(tempfolder, filename)
    newpath = os.path.join(MEDIA_ROOT, 'files', year, month, filename)
    os.rename(oldpath, newpath)
    print(oldpath, ' --> ', newpath)

def ytdlp_options(quality):
    opts = {}
    if quality == 0:
        opts['format'] = 'bv*[height<=720]+ba/b[height<=720]'
    elif quality == 1:
        opts['format'] = 'bv*[height<=1080]+ba/b[height<=1080]'
    else:
        opts['format'] = 'bv*[height<=720]+ba/b[height<=720]'
    #opts['outtmpl'] = '/www/temp/' + datetime.now().strftime("%Y/%m") + '/%(id)s.%(ext)s'
    opts['outtmpl'] = tempfolder + '%(id)s.%(ext)s'
    #opts['outtmpl'] = '%(id)s.%(ext)s'
    opts['writethumbnail'] = True
    opts['no-embed-thumbnail'] = True
    opts['noplaylist'] = True
    opts['merge_output_format'] = 'mp4'
    return opts

# Test

@shared_task
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True