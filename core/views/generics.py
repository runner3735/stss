
from django.db.models import Q
from django.views.generic import ListView, DetailView

from ..models import *

# Detail

class PersonDetail(DetailView):
  model = Person
  context_object_name = 'person'
  template_name = 'person.html'

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

class TagDetail(DetailView):
  model = Tag
  context_object_name = 'tag'
  template_name = 'tag.html'

class AssetDetail(DetailView):
  model = Asset
  context_object_name = 'asset'
  template_name = 'asset.html'

class JobDetail(DetailView):
  model = Job
  context_object_name = 'job'
  template_name = 'job.html'

class PMIDetail(DetailView):
  model = PMI
  context_object_name = 'pmi'
  template_name = 'pmi.html'

class FileDetail(DetailView):
  model = File
  context_object_name = 'file'
  template_name = 'file.html'

# List

class RoomList(ListView):
    model = Room
    template_name = 'rooms.html'
    context_object_name = 'rooms'

class PMIList(ListView):
    model = PMI
    template_name = 'pmis.html'
    context_object_name = 'pmis'

class TagList(ListView):
    model = Tag
    template_name = 'tags.html'
    context_object_name = 'tags'

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

