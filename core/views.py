
# import os, subprocess
# import physics.ytdlp as yt
# import physics.ffutil as ff

# from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404
# from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
# from django.urls import reverse

from .models import Department, Manufacturer, Purchase, Asset, Room, Note, Person, Tag, Video, Document, Picture
# from .forms import SetupForm, SetupNameForm, SetupDescriptionForm, SetupRoomForm, SetupLocationForm
# from .forms import DocumentForm, DocumentNameForm, PictureForm, PictureNameForm, ComponentForm, NoteForm, TagForm, CourseForm
# from .forms import VideoForm, YoutubeForm, VideoNameForm, VideoThumbnailForm

def home(request):
  context = {}
  context['assets'] = Asset.objects.all().count()
  context['jobs'] = 0
  context['customers'] = Person.objects.all().count()
  context['pictures'] = Picture.objects.all().count()
  context['documents'] = Document.objects.all().count()
  context['videos'] = Video.objects.all().count()
  return render(request, 'home.html', context)

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
            q = q.filter(Q(nickname__icontains=search) | Q(identifier__icontains=search) | Q(description__icontains=search))
        return q

    def get_context_data(self, **kwargs):
        context = super(AssetList, self).get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status', 'ALL')
        context['search'] = self.request.GET.get('search', '')
        context['statuses'] = {'In Service': '1', 'Discarded': '2', 'Gifted': '3', 'Parts Only': '4', 'Faculty Left': '5', 'Returned': '6', 'Lost': '7', 'Missing': '8', 'Unknown': '9' }
        return context

# # List View

# class DemoList(ListView):
#   model = Demo
#   paginate_by = 12
#   context_object_name = 'setups'
#   template_name = "physics/setups.html"

#   def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['title'] = 'Physics Demo List'
#     return context

# class VideoSelectDemo(LoginRequiredMixin, ListView):
#   model = Demo
#   paginate_by = 12
#   context_object_name = 'setups'
#   template_name = "physics/video-select-setup.html"

#   def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['video'] = get_object_or_404(Video, pk=self.kwargs['pk'])
#     context['title'] = 'Link A Demo'
#     return context

# class DemosByPicture(ListView):
#     queryset = Demo.objects.filter(picture__isnull=False)
#     paginate_by = 12
#     context_object_name = 'setups'
#     template_name ='physics/setups-with-picture.html'

# class ActivityList(ListView):
#   model = Activity
#   paginate_by = 12
#   context_object_name = 'setups'
#   template_name = "physics/setups.html"

#   def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['title'] = 'Physics Lab Activity List'
#     return context

# class ActivitiesByPicture(ListView):
#     queryset = Activity.objects.filter(picture__isnull=False)
#     paginate_by = 12
#     context_object_name = 'setups'
#     template_name ='physics/setups-with-picture.html'

# class CourseList(ListView):
#   model = Course
#   template_name = "physics/courses.html"

# class MyPictures(LoginRequiredMixin, ListView):
#     model = Picture
#     context_object_name = 'pictures'
#     template_name ='physics/pictures.html'
#     paginate_by = 12

#     def get_queryset(self):
#         return Picture.objects.filter(contributor=self.request.user)

#     def get_context_data(self, **kwargs):
#       context = super().get_context_data(**kwargs)
#       context['title'] = 'My Photos'
#       return context

# class Pictures(ListView):
#     queryset = Picture.objects.exclude(setups=None)
#     context_object_name = 'pictures'
#     template_name ='physics/pictures.html'
#     paginate_by = 12

#     def get_context_data(self, **kwargs):
#       context = super().get_context_data(**kwargs)
#       context['title'] = 'Photos'
#       return context

# class CourseVideos(ListView): # this function not used, but demonstrates how to use generic listview
#   model = Video
#   template_name ='physics/course-videos.html'
#   paginate_by = 10

#   def get_context_data(self, **kwargs):
#     context = super(CourseVideos, self).get_context_data(**kwargs)
#     context['course'] = Course.objects.get(pk=self.kwargs['pk'])
#     return context

#   def get_queryset(self):
#     pk = self.kwargs['pk']
#     return Video.objects.filter(courses__id=pk)

# class MyVideos(LoginRequiredMixin,ListView):
#     model = Video
#     template_name ='physics/my-videos.html'
#     paginate_by = 12
    
#     def get_queryset(self):
#         return Video.objects.filter(contributor=self.request.user)

# class Videos(ListView):
#     model = Video
#     context_object_name = 'videos'
#     template_name ='physics/videos.html'
#     paginate_by = 12

#     def get_queryset(self):
#         q1 = Video.objects.exclude(setups=None)
#         q2 = Video.objects.exclude(tags=None)
#         q3 = Video.objects.exclude(courses=None)
#         return q1 | q2 | q3

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Videos'
#         return context

# class MyDocuments(LoginRequiredMixin,ListView):
#     model = Document
#     template_name ='physics/my-documents.html'
#     paginate_by = 12
    
#     def get_queryset(self):
#         return Document.objects.filter(contributor=self.request.user)

# # Detail View

# class SetupDetail(DetailView):
#   model = Setup
#   context_object_name = 'setup'
#   template_name = "physics/setup.html"

# class CourseDetail(DetailView):
#   model = Course
#   template_name = "physics/course.html"

# class VideoDetail(DetailView):
#   model = Video
#   template_name = 'physics/video.html'

# class ComponentDetail(DetailView):
#   model = Component
#   template_name = 'physics/component.html'

# class TagDetail(DetailView):
#   model = Tag
#   template_name = 'physics/tag.html'

# # Demo

# @login_required
# def demo_new(request):
#   return setup_new(request, 'd')

# @login_required
# def activity_new(request):
#   return setup_new(request, 'a')

# # Setup

# def modal_test(request):
#   pictures = Picture.objects.all()
#   return render(request, 'physics/modal-test.html', {'pictures': pictures})

# @login_required
# def setup_new(request, setup_type):
#   if request.method == 'POST':
#     form = SetupForm(request.POST)
#     if form.is_valid():
#       setup = form.save()
#       setup.type = setup_type
#       setup.save()
#       return HttpResponseRedirect(setup.detail())
#   else:
#     form = SetupForm()
#   if setup_type == 'd': title = 'Create New Demo'
#   else: title = 'Create New Lab Activity'
#   return render(request, 'physics/setup-new.html', {'form': form, 'title': title})

# @login_required
# def setup_edit_name(request, pk):
#   setup=get_object_or_404(Setup, pk = pk)
#   if request.method == 'POST':
#     form = SetupNameForm(request.POST, instance=setup)
#     if form.is_valid():
#       form.save()
#       response = HttpResponse(status=204)
#       response['HX-Trigger'] = 'setupNameChanged'
#       return response
#   else:
#     form = SetupNameForm(instance=setup)
#   return render(request, 'physics/setup-edit-name.html', {'form': form, 'setup': setup})

# def setup_name(request, pk):
#   s=get_object_or_404(Setup, pk = pk)
#   return HttpResponse('<strong>' + s.name + '</strong>')

# @login_required
# def setup_edit_room(request, pk):
#   setup=get_object_or_404(Setup, pk = pk)
#   if request.method == 'POST':
#     form = SetupRoomForm(request.POST, instance=setup)
#     if form.is_valid():
#       form.save()
#       return HttpResponseRedirect(reverse('setup', args=[pk]))
#   else:
#     form = SetupRoomForm(instance=setup)
#   return render(request, 'physics/setup-edit-room.html', {'form': form, 'setup': setup})

# @login_required
# def setup_edit_location(request, pk):
#   setup=get_object_or_404(Setup, pk = pk)
#   if request.method == 'POST':
#     form = SetupLocationForm(request.POST, instance=setup)
#     if form.is_valid():
#       form.save()
#       return HttpResponseRedirect(reverse('setup', args=[pk]))
#   else:
#     form = SetupLocationForm(instance=setup)
#   return render(request, 'physics/setup-edit-location.html', {'form': form, 'setup': setup})

# @login_required
# def setup_select_picture(request, pk):
#   setup=get_object_or_404(Setup, pk = pk)
#   selected = request.GET.get('selected')
#   if not selected:
#     return render(request, 'physics/setup-select-picture.html', {'setup': setup})
#   picture=get_object_or_404(Picture, pk = selected)
#   setup.picture = picture
#   setup.save()
#   return HttpResponseRedirect(setup.detail())

# @login_required
# def setup_edit_description(request, pk):
#   setup=get_object_or_404(Setup, pk = pk)
#   if request.method == 'POST':
#     form = SetupDescriptionForm(request.POST, instance=setup)
#     if form.is_valid():
#       form.save()
#       return HttpResponseRedirect(reverse('setup', args=[pk]) + '?tab=description')
#   else:
#     form = SetupDescriptionForm(instance=setup)
#   return render(request, 'physics/setup-edit-description.html', {'form': form, 'setup': setup})

# @login_required
# def setup_remove_document(request, pk, document):
#   setup=get_object_or_404(Setup, pk = pk)
#   setup.documents.remove(document)
#   return HttpResponseRedirect(reverse('setup', args=[pk]) + '?tab=documents')

# # Picture

# def picture_detail(request, pk):
#   picture = get_object_or_404(Picture, pk = pk)
#   return render(request, 'physics/picture.html', {'picture': picture})

# @login_required
# def setup_add_picture(request, pk):
#   setup=get_object_or_404(Setup, pk = pk)
#   next = setup.detail('pictures')
#   return add_picture(request, next, setup)

# @login_required
# def picture_new(request):
#   next = reverse('my-pictures')
#   return add_picture(request, next)

# @login_required
# def add_picture(request, next, picturable=None):
#   picture=Picture()
#   picture.contributor = request.user
#   if request.method == 'POST':
#     form = PictureForm(request.POST, request.FILES, instance=picture)
#     if form.is_valid():
#       form.save()
#       picture.transpose()
#       if picturable: picturable.pictures.add(picture)
#       return HttpResponseRedirect(next)
#   else:
#     form = PictureForm(instance=picture)
#   return render(request, 'physics/picture-new.html', {'form': form, 'picture': picture, 'next': next, 'fileform': True})

# @login_required
# def picture_edit(request, pk):
#   picture=get_object_or_404(Picture, pk = pk)
#   next = picture.detail()
#   if picture.contributor != request.user:
#     return HttpResponseRedirect(next)
#   if request.method == 'POST':
#     form = PictureNameForm(request.POST, instance=picture)
#     if form.is_valid():
#       form.save()
#       return HttpResponseRedirect(next)
#   else:
#     form = PictureNameForm(instance=picture)
#   return render(request, 'physics/picture-edit.html', {'form': form, 'picture': picture, 'next': next})

# @login_required
# def picture_rotate(request, pk, degrees):
#   print('picture_rotate called')
#   picture=get_object_or_404(Picture, pk=pk)
#   if request.user == picture.contributor:
#     picture.rotate(int(degrees))
#   return HttpResponseRedirect(reverse('picture-edit', args=[pk]))

# @login_required
# def picture_delete(request, pk):
#   picture=get_object_or_404(Picture, pk = pk)
#   if picture.contributor == request.user:
#     picture.delete()
#   return HttpResponseRedirect(request.GET.get('next'))

# # Video

# @login_required
# def video_upload(request):
#   next = reverse('my-videos')
#   return upload_video(request, None, next)

# @login_required
# def setup_add_video(request, pk):
#   setup=get_object_or_404(Setup, pk = pk)
#   next = setup.detail('videos')
#   return upload_video(request, setup, next)

# @login_required
# def upload_video(request, videoable, next):
#   video = Video()
#   video.contributor = request.user
#   if request.method == 'POST':
#     form = VideoForm(request.POST, request.FILES, instance=video)
#     if form.is_valid():
#       form.save()
#       if videoable: videoable.videos.add(video)
#       return HttpResponseRedirect(next)
#   else:
#     form = VideoForm(instance=video)
#   return render(request, 'physics/video-upload.html', {'form': form, 'video': video, 'next': next, 'fileform': True})

# @login_required
# def youtube_new(request):
#   next = reverse('my-videos')
#   if request.method == 'POST':
#     form = YoutubeForm(request.POST)
#     if form.is_valid():
#       video = form.save(commit=False)
#       if video.url:
#         video.contributor = request.user
#         yt.GetInfo(video.url, video)
#         yt.Download(video)
#         return render(request, 'physics/youtube-submitted.html', {'video': video, 'next': next})
#   else:
#     form = YoutubeForm()
#   return render(request, 'physics/youtube-new.html', {'form': form, 'next': next})

# @login_required
# def video_edit_name(request, pk):
#   video=get_object_or_404(Video, pk = pk)
#   if request.method == 'POST':
#     form = VideoNameForm(request.POST, instance=video)
#     if form.is_valid():
#       form.save()
#       response = HttpResponse(status=204)
#       response['HX-Trigger'] = 'videoNameChanged'
#       return response
#   else:
#     form = VideoNameForm(instance=video)
#   return render(request, 'physics/video-edit-name.html', {'form': form, 'video': video})

# def video_name(request, pk):
#   video=get_object_or_404(Video, pk = pk)
#   return HttpResponse('<strong>' + video.name + '</strong>')

# @login_required
# def video_edit_thumbnail(request, pk):
#   video=get_object_or_404(Video, pk = pk)
#   next = video.detail()
#   if video.contributor != request.user:
#     return HttpResponseRedirect(next)
#   if request.method == 'POST':
#     form = VideoThumbnailForm(request.POST, request.FILES, instance=video)
#     if form.is_valid():
#       form.save()
#       return HttpResponseRedirect(next)
#   else:
#     form = VideoThumbnailForm(instance=video)
#   return render(request, 'physics/video-edit-thumbnail.html', {'form': form, 'video': video, 'next': next, 'fileform': True})

# @login_required
# def video_add_setup(request, pk, setup):
#   video=get_object_or_404(Video, pk = pk)
#   video.setups.add(setup)
#   return HttpResponseRedirect(video.detail())

# @login_required
# def video_delete(request, pk):
#   video=get_object_or_404(Video, pk = pk)
#   if video.contributor == request.user: video.delete()
#   return HttpResponseRedirect(reverse('my-videos'))

# @login_required
# def video_select_thumbnail(request, pk):
#   video = get_object_or_404(Video, pk = pk)
#   selected = request.GET.get('selected')
#   if not selected:
#     ff.generate_thumbs(video.filepath())
#     thumbs = ff.get_thumbs()
#     return render(request, 'physics/video-select-thumbnail.html', {'video': video, 'thumbs': thumbs})
#   ff.set_thumbnail(video, selected)
#   ff.delete_temp()
#   return HttpResponseRedirect(video.detail())

# # Document

# @login_required
# def setup_add_document(request, pk):
#   setup=get_object_or_404(Setup, pk = pk)
#   next = setup.detail('documents')
#   return add_document(request, setup, next)

# @login_required
# def course_add_document(request, pk):
#   course=get_object_or_404(Course, pk = pk)
#   next = course.detail('documents')
#   return add_document(request, course, next)

# @login_required
# def add_document(request, documentable, next):
#   document=Document()
#   document.contributor = request.user
#   if request.method == 'POST':
#     form = DocumentForm(request.POST, request.FILES, instance=document)
#     if form.is_valid():
#       form.save()
#       print('Created Document:', document.id)
#       documentable.documents.add(document)
#       return HttpResponseRedirect(next)
#   else:
#     form = DocumentForm(instance=document)
#   return render(request, 'physics/document-new.html', {'form': form, 'document': document, 'next': next, 'fileform': True})

# @login_required
# def document_edit(request, pk):
#   document=get_object_or_404(Document, pk = pk)
#   next = request.GET.get('next')
#   if request.user != document.contributor:
#     return HttpResponseRedirect(next)
#   if request.method == 'POST':
#     form = DocumentNameForm(request.POST, instance=document)
#     if form.is_valid():
#       form.save()
#       return HttpResponseRedirect(next)
#   else:
#     form = DocumentNameForm(instance=document)
#   return render(request, 'physics/document-edit.html', {'form': form, 'document': document})

# @login_required
# def document_delete(request, pk):
#   document=get_object_or_404(Document, pk=pk)
#   related = []
#   for s in document.setups.all():
#     related.append(('setup', s.id, s.name))
#   for c in document.courses.all():
#     related.append(('course', c.id, c.name))
#   if not related: return delete(request, 'document', pk)
#   return render(request, 'physics/delete-confirm.html', {'model': 'document', 'pk': pk, 'related': related})

# @login_required
# def document_convert(request, pk):
#   document=get_object_or_404(Document, pk = pk)
#   docpath = os.path.join(settings.MEDIA_ROOT, document.file.name)
#   if docpath.lower().endswith('.pdf'):
#     jpgpath = docpath[:-4] + '.jpg'
#     if not os.path.exists(jpgpath):
#       if convert_pdf(docpath, jpgpath):
#         picture = Picture()
#         picture.name = document.name
#         picture.file.name = document.file.name[:-4] + '.jpg'
#         picture.contributor = document.contributor
#         picture.created = document.created
#         picture.save()
#         for s in document.setups.all():
#           picture.setups.add(s)
#   return HttpResponseRedirect(request.GET.get('next'))

# def convert_pdf(pdfpath, jpgpath):
#   result = subprocess.call(['gs','-sDEVICE=jpeg','-dNOPAUSE','-dQUIET','-dBATCH','-r144','-sOutputFile=' + jpgpath,pdfpath])
#   if not result: return True

# @login_required
# def course_remove_document(request, pk, document):
#   course=get_object_or_404(Course, pk = pk)
#   course.documents.remove(document)
#   return HttpResponseRedirect(reverse('course', args=[pk]) + '?tab=documents')

# # Tag

# def tags(request):
#   if request.user.is_authenticated:
#     return tags_edit(request)
#   tags = Tag.objects.all()
#   return render(request, 'physics/tags.html', {'tags': tags})

# @login_required
# def tags_edit(request):
#   if request.method == 'POST':
#     tag = Tag()
#     form = TagForm(request.POST, instance=tag)
#     if form.is_valid():
#       form.save()
#       form = TagForm()
#   else:
#     form = TagForm()
#   tags = Tag.objects.all()
#   return render(request, 'physics/tags-edit.html', {'form': form, 'tags': tags})

# @login_required
# def tag_edit(request, tag):
#   tag=get_object_or_404(Tag, pk = tag)
#   if request.method == 'POST':
#     form = TagForm(request.POST, instance=tag)
#     if form.is_valid():
#       form.save()
#       return HttpResponseRedirect(reverse('tag', args=[tag.id]))
#   else:
#     form = TagForm(instance=tag)
#   return render(request, 'physics/tag-edit.html', {'form': form, 'tag': tag})

# @login_required
# def tag_delete(request, tag):
#   tag=get_object_or_404(Tag, pk = tag)
#   if tag.setups.count() == 0:
#     if tag.videos.count() == 0:
#       tag.delete()
#       return HttpResponseRedirect(reverse('tags'))
#   return HttpResponseRedirect(reverse('tag', args=[tag.id]))

# @login_required
# def edit_tags(request, model, pk):
#   taggable = get_instance(model, pk)
#   if request.method == 'POST':
#     tag = Tag()
#     form = TagForm(request.POST, instance=tag)
#     if form.is_valid():
#       form.save()
#       taggable.tags.add(tag)
#       form = TagForm()
#   else:
#     form = TagForm()
#   tags = Tag.objects.all()
#   return render(request, 'physics/edit-tags.html', {'form': form, 'taggable': taggable, 'tags': tags})

# def get_instance(model, pk):
#   if model == 'setup':
#     taggable=get_object_or_404(Setup, pk = pk)
#   elif model == 'video':
#     taggable=get_object_or_404(Video, pk = pk)
#   else:
#     taggable = None
#   return taggable

# @login_required
# def addtag(request, model, pk, tag):
#   taggable = get_instance(model, pk)
#   taggable.tags.add(tag)
#   return HttpResponseRedirect(reverse('edit-tags', args=[model, pk]))

# @login_required
# def untag(request, model, pk, tag):
#   taggable = get_instance(model, pk)
#   taggable.tags.remove(tag)
#   return HttpResponseRedirect(reverse('edit-tags', args=[model, pk]))

# def taggable_tags(request, taggable):
#   tags = taggable.tags.all()
#   return render(request, 'physics/taggable-tags.html', {'tags': tags})

# # Course

# @login_required
# def course_new(request):
#   if request.method == 'POST':
#     form = CourseForm(request.POST)
#     if form.is_valid():
#       form.save()
#       return HttpResponseRedirect(reverse('courses'))
#   else:
#     form = CourseForm()
#   return render(request, 'physics/course-new.html', {'form': form})

# @login_required
# def addcourse(request, model, pk, course):
#   courseable = get_instance(model, pk)
#   courseable.courses.add(course)
#   return HttpResponseRedirect(reverse('edit-courses', args=[model, pk]))

# @login_required
# def uncourse(request, model, pk, course):
#   courseable = get_instance(model, pk)
#   courseable.courses.remove(course)
#   return HttpResponseRedirect(reverse('edit-courses', args=[model, pk]))

# @login_required
# def edit_courses(request, model, pk):
#   courseable = get_instance(model, pk)
#   courses = Course.objects.all()
#   selected = courseable.courses.all()
#   return render(request, 'physics/edit-courses.html', {'courseable': courseable, 'courses': courses, 'selected': selected})

# # Component

# def components(request):
#   if request.user.is_authenticated:
#     return components_edit(request)
#   components = Component.objects.all()
#   return render(request, 'physics/components.html', {'components': components})

# @login_required
# def components_edit(request):
#   if request.method == 'POST':
#     component = Component()
#     form = ComponentForm(request.POST, instance=component)
#     if form.is_valid():
#       form.save()
#       form = ComponentForm()
#   else:
#     form = ComponentForm()
#   components = Component.objects.all()
#   return render(request, 'physics/components-edit.html', {'form': form, 'components': components})

# @login_required
# def component_edit(request, component):
#   component=get_object_or_404(Component, pk = component)
#   if request.method == 'POST':
#     form = ComponentForm(request.POST, instance=component)
#     if form.is_valid():
#       form.save()
#       return HttpResponseRedirect(reverse('component', args=[component.id]))
#   else:
#     form = ComponentForm(instance=component)
#   return render(request, 'physics/component-edit.html', {'form': form, 'component': component})

# @login_required
# def component_delete(request, component):
#   component=get_object_or_404(Component, pk = component)
#   if component.setups.count() == 0:
#     component.delete()
#     return HttpResponseRedirect(reverse('components'))
#   return HttpResponseRedirect(reverse('component', args=[component.id]))

# @login_required
# def setup_components(request, pk):
#   setup=get_object_or_404(Setup, pk = pk)
#   if request.method == 'POST':
#     component = Component()
#     form = ComponentForm(request.POST, instance=component)
#     if form.is_valid():
#       form.save()
#       setup.components.add(component)
#       form = ComponentForm()
#   else:
#     form = ComponentForm()
#   components = Component.objects.all()
#   return render(request, 'physics/setup-components.html', {'form': form, 'setup': setup, 'components': components})

# @login_required
# def setup_remove_component(request, setup, component):
#   setup=get_object_or_404(Setup, pk = setup)
#   component=get_object_or_404(Component, pk = component)
#   setup.components.remove(component)
#   return HttpResponseRedirect(reverse('setup-components', args=[setup.id]))

# @login_required
# def setup_add_component(request, setup, component):
#   setup=get_object_or_404(Setup, pk = setup)
#   component=get_object_or_404(Component, pk = component)
#   setup.components.add(component)
#   return HttpResponseRedirect(reverse('setup-components', args=[setup.id]))

# # Note

# @login_required
# def picture_add_note(request, pk):
#   picture=get_object_or_404(Picture, pk = pk)
#   next = picture.detail()
#   return notable_add_note(request, picture, next)

# @login_required
# def setup_add_note(request, pk):
#   setup=get_object_or_404(Setup, pk = pk)
#   next = setup.detail('notes')
#   return notable_add_note(request, setup, next)

# @login_required
# def video_add_note(request, pk):
#   video=get_object_or_404(Video, pk = pk)
#   next = video.detail()
#   return notable_add_note(request, video, next)

# @login_required
# def notable_add_note(request, notable, next):
#   note=Note()
#   note.contributor = request.user
#   if request.method == 'POST':
#     form = NoteForm(request.POST, instance=note)
#     if form.is_valid():
#       form.save()
#       print('Created Note:', note.id)
#       notable.notes.add(note)
#       return HttpResponseRedirect(next)
#   else:
#     form = NoteForm(instance=note)
#   return render(request, 'physics/note-new.html', {'form': form, 'next': next})

# @login_required
# def note_edit(request, pk):
#   note=get_object_or_404(Note, pk=pk)
#   if request.user != note.contributor:
#     return HttpResponseRedirect(request.GET.get('next'))
#   elif request.method == 'POST':
#     form = NoteForm(request.POST, instance=note)
#     if form.is_valid():
#       form.save()
#       return HttpResponseRedirect(request.GET.get('next'))
#   else:
#     form = NoteForm(instance=note)
#   return render(request, 'physics/note-edit.html', {'form': form, 'note': note})

# @login_required
# def note_delete(request, pk):
#   note=get_object_or_404(Note, pk=pk)
#   if note.contributor == request.user:
#     note.delete()
#   return HttpResponseRedirect(request.GET.get('next'))

# # Upload

# @login_required
# def upload(request, model="", pk=""):
#   return render(request, 'physics/upload.html', {'model': model, 'pk': pk})

# @login_required
# def file_upload(request):
#   if request.method == 'POST':
#     print('POST:', request.POST)
#     file = request.FILES.get('file')
#     model = request.POST.get('model', None)
#     pk = request.POST.get('pk', None)
#     if model == 'setup':
#       obj = get_object_or_404(Setup, pk=pk)
#     else:
#       obj = None
#     ext = os.path.splitext(file.name)[1]
#     if ext.lower() in ['.jpg', '.gif', '.webp', '.png', '.jpeg']:
#       create_picture(request, file, obj)
#     elif ext.lower() in ['.mp4', '.flv', '.webm', '.mkv', '.mov']:
#       create_video(request, file, obj)
#     else:
#       create_document(request, file, obj)
#     return HttpResponse('')
#   print('ERROR: file_upload called not using post!')
#   return JsonResponse({'post':'false'})

# @login_required
# def create_document(request, file, documentable):
#   d = Document()
#   d.contributor = request.user
#   d.file = file
#   d.name = os.path.splitext(file.name)[0]
#   d.save()
#   print('created document', d.id)
#   if documentable:
#     documentable.documents.add(d)

# @login_required
# def create_picture(request, file, picturable):
# #  try:
# #    b = BytesIO(file.read())
# #    image = Image.open(b)
# #    image.close()
# #  except:
# #    print('ERROR: creating document instead')
# #    create_document(request, file, picturable)
#   p = Picture()
#   p.contributor = request.user
#   p.file = file
#   p.name = os.path.splitext(file.name)[0]
#   p.save()
#   if not p.transpose():
#     p.delete()
#     return
#   print('created picture', p.id)
#   if picturable:
#     picturable.pictures.add(p)

# @login_required
# def create_video(request, file, videoable):
#   v = Video()
#   v.contributor = request.user
#   v.file = file
#   v.name = os.path.splitext(file.name)[0]
#   v.save()
#   print('created video', v.id)
#   ff.generate_thumb(v)
#   if videoable:
#     videoable.videos.add(v)

# # Delete

# @login_required
# def delete(request, model, pk):
#   next = request.GET.get('next')
#   if model == 'document':
#     obj = get_object_or_404(Document, pk=pk)
#   else:
#     return HttpResponseRedirect(next)
#   if obj.contributor == request.user:
#     obj.file.delete()
#     obj.delete()
#   return HttpResponseRedirect(next)

# # Test

# @login_required
# def test(request):
#   if request.user.get_username() == 'lritchie':
#     check_paths()
#   return HttpResponseRedirect(reverse('home'))

# def update_paths():
#   print()
#   for d in Document.objects.all():
#     if d.file:
#       oldname = d.file.name
#       newname = 'documents/' + d.created.strftime("%Y/%m") + '/' + d.filename()
#       newname = move_file(oldname, newname)
#       if newname:
#         d.file.name = newname
#         d.save()
#   for p in Picture.objects.all():
#     if p.file:
#       oldname = p.file.name
#       newname = 'pictures/' + p.created.strftime("%Y/%m") + '/' + p.filename()
#       newname = move_file(oldname, newname)
#       if newname:
#         p.file.name = newname
#         p.save()
#   for v in Video.objects.all():
#     if v.file:
#       oldname = v.file.name
#       newname = 'videos/' + v.created.strftime("%Y/%m") + '/' + v.filename()
#       newname = move_file(oldname, newname)
#       if newname:
#         v.file.name = newname
#         v.save()
#     if v.thumbnail:
#       oldname = v.thumbnail.name
#       newname = 'videos/' + v.created.strftime("%Y/%m") + '/' + v.thumbname()
#       newname = move_file(oldname, newname)
#       if newname:
#         v.thumbnail.name = newname
#         v.save()

# def move_file(oldname, newname):
#   if newname == oldname: return ""
#   oldpath = os.path.join(settings.MEDIA_ROOT, oldname)
#   if not os.path.isfile(oldpath):
#     print('NOT FOUND:', oldname)
#     return ""
#   newpath = os.path.join(settings.MEDIA_ROOT, newname)
#   if os.path.exists(newpath):
#     print('ALREADY EXISTS:', newname)
#     return ""
#   newdir = os.path.dirname(newpath)
#   if not os.path.isdir(newdir):
#     os.makedirs(newdir)
#   os.rename(oldpath, newpath)
#   print(oldname, ' --> ', newname)
#   return newname

# def check_paths():
#   print('\n*** CHECKING PATHS DOCUMENTS***')
#   for d in Document.objects.all():
#     if not file_exists(d.file):
#       print('Document', d.id)
#   print('\n*** CHECKING PATHS PICTURES***')
#   for p in Picture.objects.all():
#     if not file_exists(p.file):
#       print('Picture', p.id)
#   print('\n*** CHECKING PATHS VIDEOS***')
#   for v in Video.objects.all():
#     if not file_exists(v.file):
#       print('Video', v.id)
#     if not file_exists(v.thumbnail):
#       print('Video Thumbnail', v.id)
#   print('\n*** DONE CHECKING PATHS ***')

# def file_exists(ff):
#   if not ff:
#     print('FileField NOT DEFINED')
#     return
#   filepath = os.path.join(settings.MEDIA_ROOT, ff.name)
#   if os.path.isfile(filepath): return True
#   print('FILE NOT FOUND:', ff.name)

# def object_report():
#   print("\n *** OBJECT COUNTS *** ")
#   print("Courses:", Course.objects.count())
#   print("Rooms:", Room.objects.count())
#   print("Components:", Component.objects.count())
#   print("Tags:", Tag.objects.count())
#   print("Notes:", Note.objects.count())
#   print("Documents:", Document.objects.count())
#   print("Pictures:", Picture.objects.count())
#   print("Setups:", Setup.objects.count())
#   print("Videos:", Video.objects.count())
  
#   print("\n *** VIDEOS *** ")
#   for video in Video.objects.all():
#       print("Video", str(video.id).zfill(3), video.contributor)
#       for course in video.courses.all():
#         print("    ", course.text)
  
#   print("\n *** PICTURES *** ")
#   for picture in Picture.objects.all():
#     print("Picture", str(picture.id).zfill(2), picture.contributor)
#     for s in picture.setups.all():
#       print("    Setup", str(s.id).zfill(2))

#   print("\n *** NOTES *** ")
#   for note in Note.objects.all():
#     print("Note", str(note.id).zfill(2), note.contributor, '-->', note.text.strip().splitlines()[0][:150])
#     for s in note.setups.all():
#       print("    Setup", str(s.id).zfill(2))
#     for picture in note.pictures.all():
#       print("    Picture", str(picture.id).zfill(2))
#     for video in note.videos.all():
#       print("    Video", str(video.id).zfill(3))

#   print("\n *** DOCUMENTS *** ")
#   for d in Document.objects.all():
#     print("Document", str(d.id).zfill(2), d.contributor, '-->', d.filename())
#     for s in d.setups.all():
#       print("    Setup", str(s.id).zfill(2))

#   print("\n *** END OF OBJECT REPORT *** ")
