
import os
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image, ImageOps
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

class Document(models.Model):
  name = models.CharField(max_length=200)
  file = models.FileField(upload_to='documents/%Y/%m/')
  contributor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta: 
    ordering = ["-created"]

  def __str__(self):
    return self.file.name

  def filename(self):
    return os.path.basename(self.file.name)

  def extension(self):
    return os.path.splitext(self.file.name)[1].lower()

  def delete(self, *args, **kwargs):
    if self.file: self.file.delete()
    super(Document, self).delete(*args, **kwargs)

class Picture(models.Model):
  name = models.CharField(max_length=200, blank=True, default="")
  file = models.ImageField(upload_to='pictures/%Y/%m/')
  contributor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  created = models.DateTimeField(auto_now_add=True)

  thumb300h = ImageSpecField(source='file', processors=[ResizeToFit(height=300, upscale=True)], format='JPEG', options={'quality': 60})
  thumb450h = ImageSpecField(source='file', processors=[ResizeToFit(height=450, upscale=False)], format='JPEG', options={'quality': 80})

  class Meta: 
    ordering = ["-created"]

  def detail(self):
    return reverse('picture', args=[str(self.id)])

  def __str__(self):
    return self.file.name

  def filename(self):
    return os.path.basename(self.file.name)

  def filepath(self):
    return os.path.join(settings.MEDIA_ROOT, self.file.name)



  def test(self):
    try:
      image = Image.open(self.file)
      image.close()
      return True
    except:
      print('ERROR:', self.filepath())

  def transpose(self):
    try:
      image = Image.open(self.file)
    except:
      print('ERROR:', self.filepath())
      return
    transposed = ImageOps.exif_transpose(image)
    transposed.save(self.filepath())
    return True

  def delete(self, *args, **kwargs):
    if self.file: self.file.delete()
    super(Picture, self).delete(*args, **kwargs)

class Video(models.Model):
  name = models.CharField(max_length=200, blank=True, default="")
  file = models.FileField(upload_to='videos/%Y/%m/', blank=True, null=True)
  contributor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  created = models.DateTimeField(auto_now_add=True)
  url = models.URLField(blank=True, null=True)
  thumbnail = models.ImageField(upload_to='videos/%Y/%m/', blank=True, null=True)

  thumb225h = ImageSpecField(source='thumbnail', processors=[ResizeToFit(height=225, upscale=True)], format='JPEG', options={'quality': 60})
  thumb450h = ImageSpecField(source='thumbnail', processors=[ResizeToFit(height=450, upscale=False)], format='JPEG', options={'quality': 80})

  class Meta: 
    ordering = ["-created"]

  def detail(self):
    return reverse('video', args=[self.id])

  def modeltype(self):
    return 'video'

  def __str__(self):
    return self.name

  def filename(self):
    if self.file:
      return os.path.basename(self.file.name)
    return ""

  def filepath(self):
    return os.path.join(settings.MEDIA_ROOT, self.file.name)

  def thumbname(self):
    return os.path.basename(self.thumbnail.name)

  def thumbpath(self):
    return os.path.join(settings.MEDIA_ROOT, self.thumbnail.name)

  def delete(self, *args, **kwargs):
    if self.file: self.file.delete()
    if self.thumbnail: self.thumbnail.delete()
    super(Video, self).delete(*args, **kwargs)