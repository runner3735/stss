
import os, datetime
# import subprocess
# import physics.ytdlp as yt
import core.ffutil as ff

# from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse

from .models import Department, Manufacturer, Purchase, Asset, Room, Note, Person, Tag, Video, Document, Picture, LineItem, Vendor
from .forms import AssetNameForm, AssetLocationForm, TagForm, NoteForm, PictureNameForm, PurchaseForm, AssetNumberForm, AssetIdentifierForm
from .forms import TextForm, AssetModelForm, AssetSerialForm, AssetStatusForm, AssetInventoriedForm

def home(request):
  context = {}
  context['assets'] = Asset.objects.all().count()
  context['jobs'] = 0
  context['people'] = Person.objects.all().count()
  context['pictures'] = Picture.objects.all().count()
  context['documents'] = Document.objects.all().count()
  context['videos'] = Video.objects.all().count()
  return render(request, 'home.html', context)

class PersonList(ListView):
    model = Person
    paginate_by = 15
    template_name = 'people.html'

    def get_queryset(self):
        status = self.request.GET.get('status', 'ALL')
        search = self.request.GET.get('search', '')
        q = Person.objects.all()
        # if status != 'ALL':
        #     q = q.filter(status=status)
        if search:
            q = q.filter(Q(last__icontains=search) | Q(first__icontains=search))
        return q

    def get_context_data(self, **kwargs):
        context = super(PersonList, self).get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status', 'ALL')
        context['search'] = self.request.GET.get('search', '')
        context['statuses'] = {'Active': '1', 'Inactive': '2' }
        return context

class VendorList(ListView):
    model = Vendor
    template_name = 'vendors.html'
    context_object_name = 'vendors'

class PurchaseList(ListView):
    model = Purchase
    paginate_by = 15
    template_name = 'purchases.html'

    def get_queryset(self):
        method = self.request.GET.get('method', 'ALL')
        search = self.request.GET.get('search', '')
        q = Purchase.objects.all()
        if method != 'ALL':
            q = q.filter(method=method)
        if search:
            q = q.filter(Q(vendor__name__icontains=search) | Q(reference__icontains=search))
        return q

    def get_context_data(self, **kwargs):
        context = super(PurchaseList, self).get_context_data(**kwargs)
        context['method'] = self.request.GET.get('method', 'ALL')
        context['search'] = self.request.GET.get('search', '')
        context['methods'] = {'Credit Card': '1', 'Purchase Order': '2'}
        return context

class AssetList(ListView):
    model = Asset
    paginate_by = 15
    template_name = 'assets.html'

    def get_queryset(self):
        status = self.request.GET.get('status', 'ALL')
        search = self.request.GET.get('search', '')
        q = Asset.objects.all()
        if status != 'ALL':
            q = q.filter(status=status)
        if search:
            q = q.filter(Q(nickname__icontains=search) | Q(identifier__icontains=search) | Q(name__icontains=search))
        return q

    def get_context_data(self, **kwargs):
        context = super(AssetList, self).get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status', 'ALL')
        context['search'] = self.request.GET.get('search', '')
        context['statuses'] = {'In Service': '1', 'Discarded': '2', 'Gifted': '3', 'Parts Only': '4', 'Faculty Left': '5', 'Returned': '6', 'Lost': '7', 'Missing': '8', 'Unknown': '9' }
        return context

class PersonDetail(DetailView):
  model = Person
  context_object_name = 'person'
  template_name = 'person.html'

def purchase_detail(request, pk): # this is an alternative to PurchaseDetail that adds items to the context
  purchase = get_object_or_404(Purchase, pk=pk)
  items = LineItem.objects.filter(purchase=purchase)
  return render(request, 'purchase.html', {'purchase': purchase, 'items': items})

def purchase_add_asset(request, pk):
  purchase = get_object_or_404(Purchase, pk=pk)
  if request.method == 'POST':
    form = AssetNumberForm(request.POST)
    if form.is_valid():
      asset_tag = 'M/C X' + str(form.cleaned_data['number']).zfill(4)
      asset_cost = form.cleaned_data['cost']
      asset = Asset.objects.get(identifier=asset_tag)
      purchase.assets.add(asset, through_defaults={'cost': asset_cost})
      return HttpResponseRedirect(reverse('purchase', args=[pk]))
  else:
    form = AssetNumberForm()
  return render(request, 'purchase-add-asset.html', {'form': form})

def purchase_update_total(request, pk):
  purchase = get_object_or_404(Purchase, pk=pk)
  items = LineItem.objects.filter(purchase=purchase)
  if purchase.shipping:
    total = purchase.shipping
  else:
    total = 0
  for item in items:
    if item.cost: total += item.cost
  purchase.total = total
  purchase.save()
  return HttpResponseRedirect(reverse('purchase', args=[pk]))

class PurchaseDetail(DetailView):
  model = Purchase
  context_object_name = 'purchase'
  template_name = 'purchase.html'

class VendorDetail(DetailView):
  model = Vendor
  context_object_name = 'vendor'
  template_name = 'vendor.html'

class AssetDetail(DetailView):
  model = Asset
  context_object_name = 'asset'
  template_name = 'asset.html'

@login_required
def asset_new(request):
  if request.method == 'POST':
    form = AssetIdentifierForm(request.POST)
    if form.is_valid():
      asset_tag = 'M/C X' + str(form.cleaned_data['identifier']).zfill(4)
      asset, created = Asset.objects.get_or_create(identifier=asset_tag)
      return HttpResponseRedirect(asset.detail())
  else:
    form = AssetIdentifierForm()
  manufacturers = Manufacturer.objects.values_list('name', flat=True)
  return render(request, 'asset-new.html', {'form': form, 'manufacturers': manufacturers})



def asset_nickname(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  return HttpResponse('<strong>' + asset.nickname + '</strong>')

def asset_notes(request, pk):
  asset = get_object_or_404(Asset, pk=pk)
  return render(request, 'notes.html', {'notable': asset})

def asset_name(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  return HttpResponse('<strong>' + asset.name + '</strong>')

@login_required
def asset_edit_name(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  if request.method == 'POST':
    form = AssetNameForm(request.POST, instance=asset)
    if form.is_valid():
      form.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'assetNameChanged'
      return response
  else:
    form = AssetNameForm(instance=asset)
  return render(request, 'asset-edit-name.html', {'form': form})













def asset_manufacturer(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  return HttpResponse('<strong>' + asset.manufacturer.name + '</strong>')
  
@login_required
def asset_edit_manufacturer(request, pk):
  if request.method == 'POST':
    form = TextForm(request.POST)
    if form.is_valid():
      asset=get_object_or_404(Asset, pk=pk)
      manufacturer, created = Manufacturer.objects.get_or_create(name=form.cleaned_data['text'])
      asset.manufacturer = manufacturer
      asset.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'assetManufacturerChanged'
      return response
  else:
    form = TextForm()
  manufacturers = Manufacturer.objects.values_list('name', flat=True)
  return render(request, 'asset-edit-manufacturer.html', {'form': form, 'manufacturers': manufacturers})

def asset_model(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  return HttpResponse('<strong>' + asset.model + '</strong>')
  
@login_required
def asset_edit_model(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  if request.method == 'POST':
    form = AssetModelForm(request.POST, instance=asset)
    if form.is_valid():
      form.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'assetModelChanged'
      return response
  else:
    form = AssetModelForm(instance=asset)
  if asset.manufacturer:
    models = Asset.objects.filter(manufacturer=asset.manufacturer).values_list('model', flat=True)
    models = list(set(models))
    models.sort()
  else:
    models = []
  return render(request, 'asset-edit-model.html', {'form': form, 'models': models})

def asset_serial(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  return HttpResponse('<strong>' + asset.serial + '</strong>')
  
@login_required
def asset_edit_serial(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  if request.method == 'POST':
    form = AssetSerialForm(request.POST, instance=asset)
    if form.is_valid():
      form.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'assetSerialChanged'
      return response
  else:
    form = AssetSerialForm(instance=asset)
  return render(request, 'asset-edit-serial.html', {'form': form})

def asset_department(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  return HttpResponse('<strong>' + asset.department.name + '</strong>')

@login_required
def asset_edit_department(request, pk):
  if request.method == 'POST':
    selected = request.POST.get('department')
    asset=get_object_or_404(Asset, pk=pk)
    department = Department.objects.get(name=selected)
    asset.department = department
    asset.save()
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'assetDepartmentChanged'
    return response
  departments = Department.objects.values_list('name', flat=True)
  return render(request, 'asset-edit-department.html', {'departments': departments})

def asset_status(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  if asset.status:
    return HttpResponse('<strong>' + asset.get_status_display() + '</strong>')
  else:
    return HttpResponse('')

@login_required
def asset_edit_status(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  if request.method == 'POST':
    form = AssetStatusForm(request.POST, instance=asset)
    if form.is_valid():
      form.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'assetStatusChanged'
      return response
  else:
    form = AssetStatusForm(instance=asset)
  return render(request, 'asset-edit-status.html', {'form': form})

def asset_inventoried(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  if asset.inventoried:
    return HttpResponse('<strong>' + asset.inventoried.strftime('%B %-d, %Y') + '</strong>')
  return HttpResponse('')

@login_required
def asset_edit_inventoried(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  if request.method == 'POST':
    form = AssetInventoriedForm(request.POST, instance=asset)
    if 'today' in request.POST:
      asset.inventoried = datetime.date.today()
      asset.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'assetInventoriedChanged'
      return response
    if form.is_valid():
      form.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'assetInventoriedChanged'
      return response
  else:
    form = AssetInventoriedForm(instance=asset)
  return render(request, 'asset-edit-inventoried.html', {'form': form})











@login_required
def asset_add_purchase(request, pk):
  asset = get_object_or_404(Asset, pk=pk)
  if request.method == 'POST':
    form = PurchaseForm(request.POST)
    if form.is_valid():
      purchase = form.save()
      asset.purchases.add(purchase)
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'PurchasesChanged'
      return response
  else:
    form = PurchaseForm()
  return render(request, 'asset-add-purchase.html', {'form': form})

@login_required
def purchase_new(request):
  if request.method == 'POST':
    form = PurchaseForm(request.POST)
    if form.is_valid():
      p = form.save()
      vendor = request.POST.get('vendor').strip()
      if vendor:
        v, created = Vendor.objects.get_or_create(name=vendor)
        if created: print("Created Vendor:", vendor)
        p.vendor = v
        p.save()
      return HttpResponseRedirect(reverse('purchases'))
  else:
    form = PurchaseForm()
  vendors = Vendor.objects.values_list('name', flat=True)
  return render(request, 'purchase-new.html', {'form': form, 'vendors': vendors})

def asset_location(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  return HttpResponse('<strong>' + asset.location + '</strong>')

@login_required
def asset_edit_location(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  if request.method == 'POST':
    form = AssetLocationForm(request.POST, instance=asset)
    if form.is_valid():
      form.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'assetLocationChanged'
      return response
  else:
    form = AssetLocationForm(instance=asset)
  return render(request, 'asset-edit-location.html', {'form': form})

@login_required
def note_edit(request, pk):
  note=get_object_or_404(Note, pk=pk)
  if request.user != note.contributor:
    return HttpResponse(status=204)
  elif request.method == 'POST':
    if 'deleted' in request.POST:
      note.delete()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'noteChanged'
      return response
    form = NoteForm(request.POST, instance=note)
    if form.is_valid():
      form.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'noteChanged'
      return response
  else:
    form = NoteForm(instance=note)
  return render(request, 'note-edit.html', {'form': form, 'note': note})

def picture_detail(request, pk):
  picture = get_object_or_404(Picture, pk=pk)
  return render(request, 'picture.html', {'picture': picture})

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

@login_required
def edit_room(request, model, pk):
  roomable = get_instance(model, pk)
  rooms = Room.objects.all()
  return render(request, 'edit-room.html', {'roomable': roomable, 'rooms': rooms})

@login_required
def select_room(request, model, pk, room):
  roomable = get_instance(model, pk)
  room = get_object_or_404(Room, pk=room)
  roomable.room = room
  roomable.save()
  return HttpResponseRedirect(roomable.detail())

@login_required
def edit_tags(request, model, pk):
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
  return render(request, 'edit-tags.html', {'form': form, 'taggable': taggable, 'tags': tags})

def get_instance(model, pk):
  if model == 'asset':
    instance = get_object_or_404(Asset, pk=pk)
  elif model == 'person':
    instance = get_object_or_404(Person, pk=pk)
  elif model == 'purchase':
    instance = get_object_or_404(Purchase, pk=pk)
  else:
    instance = None
  return instance

@login_required
def addtag(request, model, pk, tag):
  taggable = get_instance(model, pk)
  taggable.tags.add(tag)
  return HttpResponseRedirect(reverse('edit-tags', args=[model, pk]))

@login_required
def untag(request, model, pk, tag):
  taggable = get_instance(model, pk)
  taggable.tags.remove(tag)
  return HttpResponseRedirect(reverse('edit-tags', args=[model, pk]))

@login_required
def addcontact(request, model, pk, contact):
  contactable = get_instance(model, pk)
  contactable.contacts.add(contact)
  return HttpResponseRedirect(reverse('edit-contacts', args=[model, pk]))

@login_required
def uncontact(request, model, pk, contact):
  contactable = get_instance(model, pk)
  contactable.contacts.remove(contact)
  return HttpResponseRedirect(reverse('edit-contacts', args=[model, pk]))

@login_required
def edit_contacts(request, model, pk):
  contactable = get_instance(model, pk)
  contacts = Person.objects.all()
  selected = contactable.contacts.all()
  return render(request, 'edit-contacts.html', {'contactable': contactable, 'contacts': contacts, 'selected': selected})

@login_required
def add_note(request, model, pk):
  notable = get_instance(model, pk)
  next = notable.detail()
  note = Note()
  note.contributor = request.user
  if request.method == 'POST':
    form = NoteForm(request.POST, instance=note)
    if form.is_valid():
      form.save()
      notable.notes.add(note)
      return HttpResponseRedirect(next)
  else:
    form = NoteForm(instance=note)
  return render(request, 'note-new.html', {'form': form, 'next': next})

@login_required
def upload(request, model="", pk=""):
  return render(request, 'upload.html', {'model': model, 'pk': pk})

@login_required
def file_upload(request):
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

