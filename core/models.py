
import hashlib, os
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image, ImageOps
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.core.validators import RegexValidator

# independent models

class Department(models.Model):
    name = models.CharField(max_length=128, unique=True)
    acronym = models.CharField(max_length=4, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Room(models.Model):
  text = models.CharField(max_length=8)

  class Meta: 
    ordering = ["text"]

  def detail(self):
    return reverse('room-detail', args=[str(self.id)])
  
  def __str__(self):
    return self.text

class Manufacturer(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Tag(models.Model):
  text = models.CharField(max_length=128, unique=True)

  class Meta: 
    ordering = ["text"]

  def detail(self):
    return reverse('tag', args=[str(self.id)])

  def __str__(self):
    return self.text

class Note(models.Model):
    text = models.TextField(max_length=4096)
    contributor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ["-created"]

    def __str__(self):
        return self.text.splitlines()[0]

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

  def rotate(self, degrees):
    try:
      image = Image.open(self.file)
    except:
      return
    image = image.rotate(degrees, expand=True)
    image.save(self.filepath())
    checksum_rename(self)

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

def checksum_rename(obj):
  folder, filename = os.path.split(obj.file.name)
  folderpath = os.path.join(settings.MEDIA_ROOT, folder)
  ext = os.path.splitext(filename)[1]
  oldpath = os.path.join(folderpath, filename)
  newname = md5checksum(oldpath) + ext
  newpath = os.path.join(folderpath, newname)
  os.rename(oldpath, newpath)
  obj.file = os.path.join(folder, newname)
  obj.save()

def md5checksum(filepath):
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(8388608)
            if chunk:
                md5.update(chunk)
            else:
                return md5.hexdigest()

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

# dependent models

class Person(models.Model):
    rxphone = RegexValidator(regex=r'^(\d{4}|\d{10})$', message="Phone number must be either 4 or 10 digits")
    status_choices=[(0, 'Inactive'), (1, 'Technician'), (2, 'Faculty'), (3, 'Staff'), (4, 'Student'), (5, 'Other'), (6, 'Purchaser')]

    first = models.CharField(max_length=128)
    last = models.CharField(max_length=128)
    phone = models.CharField(validators=[rxphone], max_length=10, blank=True)
    email = models.EmailField(max_length=128, blank=True)
    status = models.SmallIntegerField(choices=status_choices, default=0)

    office = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True, editable=False)
    departments = models.ManyToManyField(Department, related_name='people', editable=False)

    class Meta:
        ordering = ["last"]
        constraints = [models.UniqueConstraint(fields=['first', 'last'], name='unique full name')]

    def detail(self):
      return reverse('person', args=[self.id])

    def modeltype(self):
      return 'person'

    def __str__(self):
        return self.first + ' ' + self.last

class Purchase(models.Model):
    method_choices = [(1, 'Credit Card'), (2, 'Purchase Order'), (3, 'Invoice')]
    funding_choices = [(1, 'Grant Funded'), (2, 'Capital Equipment'), (3, 'Start-up')]
    
    date = models.DateField(blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True)
    purchaser = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True)
    method = models.SmallIntegerField(choices=method_choices, blank=True, null=True)
    reference = models.CharField(max_length=128, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipping = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    documents = models.ManyToManyField(Document, related_name='purchases', editable=False)
    vreference = models.CharField(max_length=128, blank=True)
    funding = models.SmallIntegerField(choices=funding_choices, blank=True, null=True)
    edorda = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ["-id"]

    def modeltype(self):
      return 'purchase'

    def __str__(self):
        return str(self.date)

class Asset(models.Model):
    rxidentifier = RegexValidator(regex=r'^(M/C X\d\d\d\d|OE-\d\d\d\d)$', message="Asset Tag is not in the correct format")
    status_choices=[(1, 'In Service'), (2, 'Discarded'), (3, 'Gifted'), (4, 'Parts Only'), (5, 'Faculty Left'), (6, 'Returned'), (7, 'Lost'), (8, 'Missing'), (9, 'Unknown')]

    identifier = models.CharField(validators=[rxidentifier], max_length=16, unique=True)
    nickname = models.CharField(max_length=128, blank=True)
    name = models.CharField(max_length=128, blank=True)
    model = models.CharField(max_length=128, blank=True)
    serial = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=64, blank=True)
    inventoried = models.DateField(blank=True, null=True)
    status = models.SmallIntegerField(choices=status_choices, blank=True, null=True)

    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True, editable=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, editable=False)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, editable=False)
    contacts = models.ManyToManyField(Person, related_name='assets', editable=False)
    tags = models.ManyToManyField(Tag, related_name='assets', editable=False)
    notes = models.ManyToManyField(Note, related_name='assets', editable=False)
    documents = models.ManyToManyField(Document, related_name='assets', editable=False)
    pictures = models.ManyToManyField(Picture, related_name='assets', editable=False)
    videos = models.ManyToManyField(Video, related_name='assets', editable=False)
    purchases = models.ManyToManyField(Purchase, related_name='assets', editable=False, through='LineItem')

    class Meta: 
        ordering = ["-id"]

    def detail(self):
      return reverse('asset', args=[self.id])

    def modeltype(self):
      return 'asset'

    def __str__(self):
        if self.nickname: return self.nickname
        return self.name

class LineItem(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.cost

class Job(models.Model):
    kind_choices=[(1, 'None'), (2, 'Class'), (3, 'High Priority'), (4, 'Research'), (5, 'Low Priority'), (6, 'Other')]
    category_choices=[(1, 'None'), (2, 'Activity Support'), (3, 'Machining/Welding/Cutting'), (4, 'Instrument Maintenance/Repair'), (5, 'Preventative Maintenance Schedule'), (6, 'MBH Building Support'), (7, 'Custom Fabrication'), (8, 'Apparatus Maintenance/Repair')]
    status_choices=[(1, 'Pending'), (2, 'In Progress'), (3, 'Complete'), (4, 'Cancelled')]

    identifier = models.CharField(max_length=8, unique=True, null=True)
    name = models.CharField(max_length=128, blank=True)
    details = models.TextField(max_length=4096, blank=True)
    budget = models.CharField(max_length=128, blank=True)
    course = models.CharField(max_length=128, blank=True)
    location = models.CharField(max_length=128, blank=True)
    kind = models.SmallIntegerField(choices=kind_choices, blank=True, null=True)
    category = models.SmallIntegerField(choices=category_choices, blank=True, null=True)
    status = models.SmallIntegerField(choices=status_choices, blank=True, null=True)
    year = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    opened = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    closed = models.DateField(blank=True, null=True)

    customers = models.ManyToManyField(Person, related_name='jobs_as_customer', editable=False)
    technicians = models.ManyToManyField(Person, related_name='jobs_as_technician', editable=False)
    rooms = models.ManyToManyField(Room, related_name='jobs', editable=False)
    departments = models.ManyToManyField(Department, related_name='jobs', editable=False)
    assets = models.ManyToManyField(Asset, related_name='jobs', editable=False)
    notes = models.ManyToManyField(Note, related_name='jobs', editable=False)
    documents = models.ManyToManyField(Document, related_name='jobs', editable=False)
    pictures = models.ManyToManyField(Picture, related_name='jobs', editable=False)
    videos = models.ManyToManyField(Video, related_name='jobs', editable=False)
    
    class Meta: 
        ordering = ["-id"]

    def detail(self):
        return reverse('job', args=[self.id])

    def modeltype(self):
        return 'job'

    def __str__(self):
        return self.name

class Work(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    technician = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True)
    summary = models.CharField(max_length=1024, blank=True)
    hours = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

