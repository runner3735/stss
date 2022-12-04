
import os, datetime, time
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
from django.core.paginator import Paginator, EmptyPage

from .models import Department, Manufacturer, Purchase, Asset, Room, Note, Person, Tag, Video, Document, Picture, LineItem, Vendor
from .forms import AssetNameForm, AssetNicknameForm, AssetLocationForm, TagForm, NoteForm, PictureNameForm, PurchaseForm, AssetNumberForm, AssetIdentifierForm
from .forms import TextForm, AssetModelForm, AssetSerialForm, AssetStatusForm, AssetInventoriedForm, AssetInfoForm, AssetCloneForm
from .forms import PersonPhoneForm, PersonEmailForm, DepartmentForm, PersonStatusForm, PersonNewForm, PeopleSearchForm, AssetSearchForm, PurchaseSearchForm

def home(request):
  context = {}
  context['assets'] = Asset.objects.all().count()
  context['jobs'] = 0
  context['people'] = Person.objects.all().count()
  context['pictures'] = Picture.objects.all().count()
  context['documents'] = Document.objects.all().count()
  context['videos'] = Video.objects.all().count()
  return render(request, 'home.html', context)

def people(request):
  context = people_get_context(request)
  context['form'] = PeopleSearchForm(request.GET or None)
  return render(request, 'people.html', context)

def people_list(request):
  context = people_get_context(request)
  return render(request, 'people-list.html', context)

def people_get_context(request):
  page = request.GET.get('page', '1')
  status = request.GET.get('status', '')
  search = request.GET.get('search', '')
  q = Person.objects.all()
  if not status: q = q.exclude(status=0)
  elif status != 5: q=q.filter(status=status)
  if search: q = q.filter(Q(last__icontains=search) | Q(first__icontains=search))
  paginator = Paginator(q, 16)
  try:
    return {'people': paginator.page(page), 'status': status, 'search': search}
  except EmptyPage:
    return {'people': [], 'status': status, 'search': search}
  
def assets(request):
  context = assets_get_context(request)
  context['form'] = AssetSearchForm(request.GET or None)
  return render(request, 'assets.html', context)

def assets_list(request):
  context = assets_get_context(request)
  return render(request, 'assets-list.html', context)

def assets_get_context(request):
  page = request.GET.get('page', '1')
  status = request.GET.get('status','1')
  search = request.GET.get('search', '')
  q = Asset.objects.all()
  if status: q = q.filter(status=status)
  if search: q = q.filter(Q(nickname__icontains=search) | Q(identifier__icontains=search) | Q(name__icontains=search))
  paginator = Paginator(q, 16)
  try:
    return {'assets': paginator.page(page), 'status': status, 'search': search}
  except EmptyPage:
    return {'assets': [], 'status': status, 'search': search}

def vendors(request):
  q = Vendor.objects.all()
  paginator = Paginator(q, 18)
  context = {'vendors': paginator.page(1)}
  return render(request, 'vendors.html', context)

def vendor_list(request, page):
  q = Vendor.objects.all()
  method = request.POST.get('method','')
  search = request.POST.get('search', '')
  if search and method == '1': q = q.filter(name__istartswith=search)
  elif search: q = q.filter(name__icontains=search)
  paginator = Paginator(q, 18)
  try:
    vendors = paginator.page(page)
  except EmptyPage:
    vendors = []
  context = {'vendors': vendors}
  return render(request, 'vendor-list.html', context)

class RoomList(ListView):
    model = Room
    template_name = 'rooms.html'
    context_object_name = 'rooms'

def purchases(request):
  context = purchases_get_context(request)
  context['form'] = PurchaseSearchForm(request.GET or None)
  return render(request, 'purchases.html', context)

def purchases_list(request):
  context = purchases_get_context(request)
  return render(request, 'purchases-list.html', context)

def purchases_get_context(request):
  page = request.GET.get('page', '1')
  method = request.GET.get('method','')
  search = request.GET.get('search', '')
  q = Purchase.objects.all()
  if method: q =  q = q.filter(method=method)
  if search: q = q.filter(Q(vendor__name__icontains=search) | Q(reference__icontains=search))
  paginator = Paginator(q, 16)
  try:
    return {'purchases': paginator.page(page), 'method': method, 'search': search}
  except EmptyPage:
    return {'purchases': [], 'method': method, 'search': search}

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

class PersonDetail(DetailView):
  model = Person
  context_object_name = 'person'
  template_name = 'person.html'

def person_tab(request, pk, tab):
  person = get_object_or_404(Person, pk=pk)
  #time.sleep(2)
  if tab == 'assets':
    return render(request, 'person-assets.html', {'person': person})
  if tab == 'jobs':
    return render(request, 'person-jobs.html', {'person': person})
  if tab == 'tasks':
    return render(request, 'person-tasks.html', {'person': person})

def asset_notes(request, pk):
  asset = get_object_or_404(Asset, pk=pk)
  #notes = Note.objects.get(asset=pk)
  notes = asset.notes.all()
  return render(request, 'note-list.html', {'notes': notes})

def asset_pictures(request, pk):
  asset = get_object_or_404(Asset, pk=pk)
  pictures = asset.pictures.all()
  return render(request, 'picture-list.html', {'pictures': pictures})

def asset_documents(request, pk):
  asset = get_object_or_404(Asset, pk=pk)
  documents = asset.documents.all()
  return render(request, 'document-list.html', {'documents': documents})

def asset_videos(request, pk):
  asset = get_object_or_404(Asset, pk=pk)
  videos = asset.videos.all()
  return render(request, 'video-list.html', {'videos': videos})

def asset_purchases(request, pk):
  asset = get_object_or_404(Asset, pk=pk)
  return render(request, 'purchase-list.html', {'asset': asset})
  
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

class RoomDetail(DetailView):
  model = Room
  context_object_name = 'room'
  template_name = 'room.html'

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
      if created:
        asset.status = 1
        asset.inventoried = datetime.date.today()
        asset.save()
      return HttpResponseRedirect(asset.detail())
  else:
    form = AssetIdentifierForm()
  manufacturers = Manufacturer.objects.values_list('name', flat=True)
  return render(request, 'asset-new.html', {'form': form, 'manufacturers': manufacturers})

@login_required
def person_new(request):
  form = PersonNewForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      person = form.save(commit=False)
      person.status = 1
      person.save()
      return HttpResponseRedirect(person.detail())
  return render(request, 'person-new.html', {'form': form})

@login_required
def asset_clone(request, pk):
  original = get_object_or_404(Asset, pk=pk)
  form = AssetCloneForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      asset_tag = 'M/C X' + str(form.cleaned_data['identifier']).zfill(4)
      asset, created = Asset.objects.get_or_create(identifier=asset_tag)
      if created:
        asset.manufacturer = original.manufacturer
        asset.model = original.model
        asset.name =  original.name
        asset.serial = form.cleaned_data['serial']
        asset.status = 1
        asset.inventoried = datetime.date.today()
        if form.cleaned_data['room']: asset.room = original.room
        if form.cleaned_data['department']: asset.department = original.department
        if form.cleaned_data['contacts'] and original.contacts:
          for contact in original.contacts.all(): asset.contacts.add(contact)
        if form.cleaned_data['tags'] and original.tags:
          for tag in original.tags.all(): asset.tags.add(tag)
        asset.save()
        return HttpResponseRedirect(asset.detail())
      else:
        form.add_error('identifier', 'That asset tag number is already in use.')
  return render(request, 'asset-clone.html', {'form': form, 'asset': original})

def asset_nickname(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  return HttpResponse('<strong>' + asset.nickname + '</strong>')

@login_required
def asset_edit_nickname(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  if request.method == 'POST':
    form = AssetNicknameForm(request.POST, instance=asset)
    if form.is_valid():
      form.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'assetNicknameChanged'
      return response
  else:
    form = AssetNicknameForm(instance=asset)
  return render(request, 'asset-edit-nickname.html', {'form': form})

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





@login_required
def asset_edit_info(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  form = AssetInfoForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      manufacturer, created = Manufacturer.objects.get_or_create(name=form.cleaned_data['manufacturer'])
      if created: print('Created Manufacturer:', manufacturer.name)
      asset.manufacturer = manufacturer
      asset.model = form.cleaned_data['model']
      asset.name = form.cleaned_data['name']
      asset.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'assetInfoChanged'
      return response
  else:
    if asset.manufacturer: form.fields['manufacturer'].initial = asset.manufacturer.name
    form.fields['model'].initial = asset.model
    form.fields['name'].initial = asset.name
  manufacturers = Manufacturer.objects.values_list('name', flat=True)
  return render(request, 'asset-edit-info.html', {'form': form, 'manufacturers': manufacturers})

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

def last_names(request):
  last = request.GET.get('last')
  if last:
    options = Person.objects.filter(last__istartswith=last).order_by('last').distinct().values_list('last', flat=True)
  else:
    options = []
  return render(request, 'datalist-options.html', {'options': options})

def first_names(request):
  last = request.GET.get('last')
  if last:
    options = Person.objects.filter(last=last).order_by('first').distinct().values_list('first', flat=True)
  else:
    options = []
  return render(request, 'datalist-options.html', {'options': options})

def asset_model_options(request):
  manufacturer = request.GET.get('manufacturer')
  if manufacturer:
    options = Asset.objects.filter(manufacturer__name=manufacturer).order_by('model').distinct().values_list('model', flat=True)
  else:
    options = []
  return render(request, 'datalist-options.html', {'options': options})

def person_departments(request, pk):
  person = get_object_or_404(Person, pk=pk)
  departments = person.departments.all()
  return render(request, 'person-departments.html', {'departments': departments})

def asset_name_options(request):
  model = request.GET.get('model')
  if model:
    options = Asset.objects.filter(model=model).order_by('name').distinct().values_list('name', flat=True)
  else:
    options = []
  return render(request, 'datalist-options.html', {'options': options})

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
    models = Asset.objects.filter(manufacturer=asset.manufacturer).order_by('model').distinct().values_list('model', flat=True)
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

@login_required
def person_edit_department(request, pk):
  person = get_object_or_404(Person, pk=pk)
  form = DepartmentForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      department = form.cleaned_data['department']
      if 'add' in request.POST:
        person.departments.add(department)
      elif 'remove' in request.POST:
        person.departments.remove(department)
      return HttpResponse(status=204, headers={'HX-Trigger': 'departmentsChanged'})
  return render(request, 'person-edit-department.html', {'form': form})

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
  return render(request, 'edit-status.html', {'form': form})


def person_status(request, pk):
  person=get_object_or_404(Person, pk=pk)
  return HttpResponse('<strong>' + person.get_status_display() + '</strong>')

@login_required
def person_edit_status(request, pk):
  person = get_object_or_404(Person, pk=pk)
  form = PersonStatusForm(request.POST or None, instance=person)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'statusChanged'
      return response
  return render(request, 'edit-status.html', {'form': form})



def asset_inventoried(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  if asset.inventoried:
    return HttpResponse('<strong>' + asset.inventoried.strftime('%B %-d, %Y') + '</strong>')
  return HttpResponse('')

@login_required
def asset_edit_inventoried(request, pk):
  asset=get_object_or_404(Asset, pk=pk)
  form = AssetInventoriedForm(request.POST or None, instance=asset)
  if request.method == 'POST':
    if 'today' in request.POST:
      asset.inventoried = datetime.date.today()
      asset.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'assetInventoriedChanged'})
    if 'clear' in request.POST:
      asset.inventoried = None
      asset.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'assetInventoriedChanged'})
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'assetInventoriedChanged'})
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







def person_phone(request, pk):
  person=get_object_or_404(Person, pk=pk)
  return HttpResponse('<strong>' + person.phone + '</strong>')
  
@login_required
def person_edit_phone(request, pk):
  person=get_object_or_404(Person, pk=pk)
  form = PersonPhoneForm(request.POST or None, instance=person)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      response = HttpResponse(status=204)
      response['HX-Trigger'] = 'personPhoneChanged'
      return response
  return render(request, 'person-edit-phone.html', {'form': form})

def person_email(request, pk):
  person=get_object_or_404(Person, pk=pk)
  return HttpResponse('<strong>' + person.email + '</strong>')
  
@login_required
def person_edit_email(request, pk):
  person=get_object_or_404(Person, pk=pk)
  form = PersonEmailForm(request.POST or None, instance=person)
  if request.method == 'POST':
    username = request.POST.get('username')
    if username:
      form = PersonEmailForm({'email': username + '@middlebury.edu'}, instance=person)
    if form.is_valid():
      form.save()
      return HttpResponse(status=204, headers={'HX-Trigger': 'emailChanged'})
  return render(request, 'person-edit-email.html', {'form': form})


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

def picture_modal(request, pk):
  picture = get_object_or_404(Picture, pk=pk)
  return render(request, 'picture-modal.html', {'picture': picture})

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
  if model == 'asset':
    roomable.room = room
  else:
    roomable.office = room
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

