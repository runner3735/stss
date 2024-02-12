import datetime

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage

from ..models import *
from ..forms import *
from .other import get_instance

# Asset

def assets(request):
  form = AssetSearchForm()
  return render(request, 'assets.html', {'form': form})

def asset_page(request):
  context = assets_get_context(request)
  return render(request, 'asset-page.html', context)

def asset_table(request):
  context = assets_get_context(request)
  return render(request, 'asset-table.html', context)

def assets_get_context(request):
  page = request.GET.get('page', '1')
  status = request.GET.get('status','1')
  search = request.GET.get('search', '')
  sortby = request.GET.get('sortby', '-id')
  searchin = request.GET.get('searchin', 'N')
  q = Asset.objects.all()
  if status: q = q.filter(status=status)
  if search:
    if searchin == 'N': #name or nickname
      q = q.filter(Q(name__icontains=search) | Q(nickname__icontains=search))
    elif searchin == 'M': #manufacturer
      q = q.filter(manufacturer__name__icontains=search)
    elif searchin == 'L': #model
      q = q.filter(model__icontains=search)
    elif searchin == 'S': #serial
      q = q.filter(serial__icontains=search)
    elif searchin == 'I': #asset tag
      q = q.filter(identifier__icontains=search)
    elif searchin == 'D': #inventory date
      q = q.filter(inventoried__contains=search)
    elif searchin == 'T': #department
      q = q.filter(department__name__icontains=search)
  q = q.order_by(sortby)
  paginator = Paginator(q, 20)
  try:
    return {'assets': paginator.page(page)}
  except EmptyPage:
    return {'assets': []}

def asset_notes(request, pk):
  asset = get_object_or_404(Asset, pk=pk)
  notes = asset.notes.all()
  return render(request, 'note-list.html', {'notes': notes})

def asset_files(request, pk):
  linkable = get_object_or_404(Asset, pk=pk)
  return render(request, 'file-list.html', {'linkable': linkable})

def asset_gallery(request, pk):
  linkable = get_object_or_404(Asset, pk=pk)
  return HttpResponse(status=204)

def asset_purchases(request, pk):
  asset = get_object_or_404(Asset, pk=pk)
  return render(request, 'purchase-list.html', {'asset': asset})

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
 
def asset_model_options(request):
  manufacturer = request.GET.get('manufacturer')
  if manufacturer:
    options = Asset.objects.filter(manufacturer__name=manufacturer).order_by('model').distinct().values_list('model', flat=True)
  else:
    options = []
  return render(request, 'datalist-options.html', {'options': options})

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
      return HttpResponse(status=204, headers={'HX-Trigger': 'assetLocationChanged'})
  else:
    form = AssetLocationForm(instance=asset)
  return render(request, 'asset-edit-location.html', {'form': form})

def asset_remove(request, asset, model, pk):
  linkable = get_instance(model, pk)
  linkable.assets.remove(asset)
  if linkable.assets.count(): return HttpResponse('')
  #return HttpResponse('', headers={'HX-Retarget': '#assets'})
  return HttpResponse(status=204, headers={'HX-Trigger': 'assetsChanged'})

