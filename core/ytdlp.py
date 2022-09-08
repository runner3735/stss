
import json, os, threading, yt_dlp
from datetime import datetime

MEDIA_ROOT = os.getenv('MEDIA_ROOT', '')

class MyLogger(object):

    def __init__(self):
        object.__init__(self)
        self.thumbnail = ''
        self.filename = ''
    
    def debug(self, msg):
        print('DEBUG:', msg)
        if 'Writing video thumbnail' in msg:
            i = msg.find(':')
            if i != -1:
                self.thumbnail = msg[i + 2:]
                print('THUMBNAIL:', msg[i + 2:])
        elif msg.startswith('[Merger] Merging formats into '):
            self.filename = msg[31:-1]
            print('FILENAME:', msg[31:-1])
    
    def info(self, msg):
        print('INFO:', msg)
    
    def warning(self, msg):
        print('WARNING:', msg)
    
    def error(self, msg):
        print('ERROR:', msg)

class Downloader(threading.Thread):

    def __init__(self, video):
        threading.Thread.__init__(self)
        self.opts = GetOpts()
        self.opts['progress_hooks'] = [self.my_hook]
        self.opts['logger'] = MyLogger()
        self.video = video
        self.filenames = {}

    def run(self):
        if not MEDIA_ROOT: return
        os.chdir(MEDIA_ROOT)
        print('\nSTARTED DOWNLOADING:', self.video.url)
        with yt_dlp.YoutubeDL(self.opts) as ydl:
            ydl.download([self.video.url])
        print('\nFINISHED DOWNLOADING:', self.video.url)
        self.video.thumbnail = self.opts['logger'].thumbnail
        print('Set video thumbnail to:', self.video.thumbnail)
        filename = self.check_filenames()
        if filename == 'error': return
        if self.opts['logger'].filename:
            self.video.file = self.opts['logger'].filename
        elif filename:
            self.video.file = filename
        else:
            return
        print('Set video file to:', self.video.file)
        self.video.save()

    def check_filenames(self):
        for filename, status in self.filenames.items():
            if status != 'finished': return 'error'
        if len(self.filenames) == 1: return filename

    def my_hook(self, d):
        if d['status'] == 'finished': print('Finished:', d['filename'])
        self.filenames[d['filename']] = d['status']

def GetInfo(link, video): # public function called in view
    opts = GetOpts()
    print('Getting info for:', link)
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(link, download=False)
    video.url = info['webpage_url']
    print('Set video url to:', video.url)
    video.name = info['title']
    print('Set video name to:', video.name)
    j = json.dumps(info, indent = 4)
    jsonpath = os.path.join(MEDIA_ROOT, 'youtube', info['id'] + '.json')
    with open(jsonpath, 'w') as f: f.write(j)
    return info

def GetOpts():
    opts = {}
    opts['format'] = 'bv*[height<=1080]+ba/b[height<=1080]'
    opts['outtmpl'] = 'videos/' + datetime.now().strftime("%Y/%m") + '/%(id)s.%(ext)s'
    opts['writethumbnail'] = True
    opts['no-embed-thumbnail'] = True
    opts['noplaylist'] = True
    #opts['merge_output_format'] = 'mp4'
    return opts

def Download(video): # public function called in view
    d = Downloader(video)
    d.start()
