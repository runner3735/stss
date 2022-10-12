
import hashlib, os, subprocess

MEDIA_ROOT = os.getenv('MEDIA_ROOT', '')
MEDIA_URL = '/media/'

def get_duration(folder, filename):
    base, ext = os.path.splitext(filename)
    if not ext in ['.mkv','.avi','.mp4','.vob','.wmv','.flv','.mpg','.mov','.m4v','.asf','.3gp','.asx','.rm']: return 0
    filepath = os.path.join(folder, filename)
    args = ['mediainfo','--Inform=General;%Duration%',filepath]
    mediainfo = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = mediainfo.communicate()
    try:
        milliseconds = int(output)
        seconds = int(output[:-4])
    except:
        print('ERROR FINDING DURATION:', filepath)
    minutes, seconds = divmod(seconds, 60)
    return minutes

def duration(filepath):
    args = ['mediainfo','--Inform=General;%Duration%',filepath]
    mediainfo = subprocess.run(args, stdout=subprocess.PIPE)
    try:
        return int(mediainfo.stdout[:-4])
    except:
        print('ERROR FINDING DURATION:', filepath)
        return

# ffmpeg -ss 120 -i /mediafiles/videos/2022/03/QO3XT1tpgQY.webm -vf select="eq(pict_type\,I)" -frames:v 1 /mediafiles/temp/2minb.png

def generate_thumb(video): # generates thumbnail from video, and sets thumbnail
    filepath = video.filepath()
    temppath = os.path.join(MEDIA_ROOT, 'temp', 'thumbnail.jpg')
    temppath = filepath + '.jpg'
    args = ['ffmpeg', '-i', filepath, '-vf', 'scale=-1:450', '-frames:v', '1', temppath]
    #subprocess.run(args)
    ffmpeg = subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if ffmpeg.returncode == 0:
        videodir = os.path.dirname(video.file.name)
        thumbname = os.path.join(videodir, md5checksum(temppath) + '.jpg')
        thumbpath = os.path.join(MEDIA_ROOT, thumbname)
        if os.path.exists(thumbpath):
            os.unlink(temppath)
        else:
            os.rename(temppath, thumbpath)
        video.thumbnail = thumbname
        video.save()
    else:
        print('ERROR:', ffmpeg.args)

def generate_thumbs(filepath): # generates 12 thumbnails from video at filepath, and puts them in temp folder
    d = duration(filepath)
    args = ['ffmpeg', '-ss', '', '-i', filepath, '-vf', 'select=eq(pict_type\,I),scale=-1:450', '-frames:v', '1', '' ]
    for i in range(12):
        t = int((i + 0.5) * d / 12 )
        args[2] = str(t)
        args[9] = os.path.join(MEDIA_ROOT, 'temp', str(i) + '.jpg')
        ffmpeg = subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if ffmpeg.returncode == 0: continue
        print('ERROR:', ffmpeg.args)

def md5checksum(filepath):
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(8388608)
            if chunk:
                md5.update(chunk)
            else:
                return md5.hexdigest()

def get_thumbs():
    thumbs = {}
    thumbdir = os.path.join(MEDIA_ROOT, 'temp')
    for f in os.listdir(thumbdir):
        id, ext = os.path.splitext(f)
        if ext == '.jpg':
            url = os.path.join(MEDIA_URL, 'temp', f)
            thumbs[id] = url
    return thumbs

def set_thumbnail(video, selected):
    oldpath = os.path.join(MEDIA_ROOT, 'temp', selected + '.jpg')
    thumbname = os.path.splitext(video.file.name)[0] + selected + '.jpg'
    newpath = os.path.join(MEDIA_ROOT, thumbname)
    if not os.path.isfile(oldpath): return
    if os.path.isfile(newpath): os.unlink(newpath)
    os.rename(oldpath, newpath)
    video.thumbnail = thumbname
    video.save()
    print('Thumbnail:', thumbname)

def delete_temp():
    tempdir = os.path.join(MEDIA_ROOT, 'temp')
    for f in os.listdir(tempdir):
        filepath = os.path.join(tempdir, f)
        os.unlink(filepath)

# generate_thumbs('/mediafiles/videos/2022/03/QO3XT1tpgQY.webm')

def test():
    args = ['ffmpeg', '-ss', '60', '-i', '/mediafiles/videos/2022/03/QO3XT1tpgQY.webm', '-vf', 'select=eq(pict_type\,I)', '-frames:v', '1', 'test6.jpg']
    #ffmpeg = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ffmpeg = subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #output, errors = ffmpeg.communicate()
    print(ffmpeg)

#test()


