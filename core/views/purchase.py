
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

from ..models import *
from ..forms import *
from .other import get_instance

# Purchase

def purchase_documents(request, pk):
  purchase = get_object_or_404(Purchase, pk=pk)
  documents = purchase.documents.all()
  return render(request, 'document-list.html', {'documents': documents, 'linkable': purchase})

def purchases(request):
  form = PurchaseSearchForm()
  return render(request, 'purchases.html', {'form': form})

def purchase_table(request):
  context = purchases_get_context(request)
  return render(request, 'purchase-table.html', context)

def purchase_page(request):
  context = purchases_get_context(request)
  return render(request, 'purchase-page.html', context)

def purchases_get_context(request):
  page = request.GET.get('page', '1')
  method = request.GET.get('method', '')
  search = request.GET.get('search', '')
  sortby = request.GET.get('sortby', '-id')
  searchin = request.GET.get('searchin', 'R')
  q = Purchase.objects.all()
  if method: q = q.filter(method=method)
  if search:
    if searchin == 'V': #vendor
      q = q.filter(vendor__name__icontains=search)
    elif searchin == 'R': #reference
      q = q.filter(Q(reference__icontains=search) | Q(vreference__icontains=search))
    elif searchin == 'D': #date
      q = q.filter(date__contains=search)
    elif searchin == 'P': #purchaser
      q = q.filter(purchaser__last__istartswith=search)
  q = q.order_by(sortby)
  paginator = Paginator(q, 16)
  try:
    return {'purchases': paginator.page(page)}
  except EmptyPage:
    return {'purchases': []}
 
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
  return render(request, 'purchase-add-asset.html', {'form': form, 'purchase': purchase})

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

@login_required
def purchase_new(request):
  form = PurchaseForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      p = form.save()
      vendor = request.POST.get('vendor').strip()
      if vendor:
        v, created = Vendor.objects.get_or_create(name=vendor)
        p.vendor = v
        purchaser, created = Person.objects.get_or_create(first=request.user.first_name, last=request.user.last_name)
        p.purchaser = purchaser
        p.save()
      return HttpResponseRedirect(reverse('purchases'))
  vendors = Vendor.objects.values_list('name', flat=True)
  return render(request, 'purchase-new.html', {'form': form, 'vendors': vendors})

@login_required
def purchase_edit(request, pk):
  purchase = get_object_or_404(Purchase, pk=pk)
  form = PurchaseEditForm(request.POST or None, instance=purchase)
  form.fields["purchaser"].queryset = Person.objects.filter(status=6)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return redirect('purchase', pk)
  return render(request, 'purchase-edit.html', {'purchase': purchase, 'form': form})

def document_remove(request, document, model, pk):
  document = get_object_or_404(Document, pk=document)
  if request.user != document.contributor: return HttpResponse(status=204)
  linkable = get_instance(model, pk)
  linkable.documents.remove(document)
  if linkable.documents.count(): return HttpResponse('')
  if model == 'purchase': return HttpResponse('', headers={'HX-Retarget': '#documents'})
  return HttpResponse('', headers={'HX-Retarget': '#document-table'})

