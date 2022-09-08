
from django.urls import path
from . import views

urlpatterns = [
  # Home
  path('', views.home, name='home'),

#   # Course
#   path('course/new/', views.course_new, name='course-new'),
#   path('courses/', views.CourseList.as_view(), name='courses'),
#   path('course/<int:pk>/', views.CourseDetail.as_view(), name='course'),
#   path('uncourse/<str:model>/<int:pk>/<int:course>/', views.uncourse, name='uncourse'),
#   path('addcourse/<str:model>/<int:pk>/<int:course>/', views.addcourse, name='addcourse'),
#   path('courses/<str:model>/<int:pk>/', views.edit_courses, name='edit-courses'),

#   # Asset
#   path('demos/', views.DemoList.as_view(), name='demos'),
#   path('demosbypicture/', views.DemosByPicture.as_view(), name='demos-by-picture'),
#   path('demo/new/', views.demo_new, name='demo-new'),

#   # Setup
#   path('setup/<int:pk>/', views.SetupDetail.as_view(), name='setup'),
#   path('setup/<int:pk>/name/edit/', views.setup_edit_name, name='setup-edit-name'),
#   path('setup/<int:pk>/name/', views.setup_name, name='setup-name'),
#   path('setup/<int:pk>/room/', views.setup_edit_room, name='setup-edit-room'),
#   path('setup/<int:pk>/location/', views.setup_edit_location, name='setup-edit-location'),
#   path('setup/<int:pk>/description/', views.setup_edit_description, name='setup-edit-description'),
#   path('setup/<int:pk>/select/picture/', views.setup_select_picture, name='setup-select-picture'),
  
#   # Activity
#   path('activities/', views.ActivityList.as_view(), name='activities'),
#   path('activitiesbypicture/', views.ActivitiesByPicture.as_view(), name='activities-by-picture'),
#   path('activity/new/', views.activity_new, name='activity-new'),

#   # Tag
#   path('tags/', views.tags, name='tags'),
#   path('tag/<int:pk>/', views.TagDetail.as_view(), name='tag'),
#   path('tag/<int:tag>/edit/', views.tag_edit, name='tag-edit'),
#   path('tag/<int:tag>/delete/', views.tag_delete, name='tag-delete'),
#   path('untag/<str:model>/<int:pk>/<int:tag>/', views.untag, name='untag'),
#   path('addtag/<str:model>/<int:pk>/<int:tag>/', views.addtag, name='addtag'),
#   path('tags/<str:model>/<int:pk>/', views.edit_tags, name='edit-tags'),

#   # Component
#   path('components/', views.components, name='components'),
#   path('component/<int:pk>/', views.ComponentDetail.as_view(), name='component'),
#   path('component/<int:component>/edit/', views.component_edit, name='component-edit'),
#   path('component/<int:component>/delete/', views.component_delete, name='component-delete'),
#   path('setup/<int:pk>/components/', views.setup_components, name='setup-components'),
#   path('setup/<int:setup>/component/<int:component>/add/', views.setup_add_component, name='setup-add-component'),
#   path('setup/<int:setup>/component/<int:component>/remove/', views.setup_remove_component, name='setup-remove-component'),
  
#   # Picture
#   path('picture/new/', views.picture_new, name='picture-new'),
#   path('pictures/', views.Pictures.as_view(), name='pictures'),
#   path('mypictures/', views.MyPictures.as_view(), name='my-pictures'),
#   path('picture/<int:pk>/', views.picture_detail, name='picture'),
#   path('picture/<int:pk>/edit/', views.picture_edit, name='picture-edit'),
#   path('picture/<int:pk>/rotate/<int:degrees>/', views.picture_rotate, name='picture-rotate'),
#   path('picture/<int:pk>/delete/', views.picture_delete, name='picture-delete'),
#   path('setup/<int:pk>/picture/', views.setup_add_picture, name='setup-add-picture'),

#   # Video
#   path('myvideos/', views.MyVideos.as_view(), name='my-videos'),
#   path('videos/', views.Videos.as_view(), name='videos'),
#   path('video/<int:pk>/', views.VideoDetail.as_view(), name='video'),
#   path('video/upload/', views.video_upload, name='video-upload'),
#   path('youtube/new/', views.youtube_new, name='youtube-new'),
#   path('video/<int:pk>/name/edit', views.video_edit_name, name='video-edit-name'),
#   path('video/<int:pk>/name/', views.video_name, name='video-name'),
#   path('video/<int:pk>/thumbnail/', views.video_edit_thumbnail, name='video-edit-thumbnail'),
#   path('video/<int:pk>/select/thumbnail/', views.video_select_thumbnail, name='video-select-thumbnail'),
#   path('video/<int:pk>/delete/', views.video_delete, name='video-delete'),
#   path('setup/<int:pk>/video/', views.setup_add_video, name='setup-add-video'),
#   path('video/<int:pk>/demo/', views.VideoSelectDemo.as_view(), name='video-select-demo'),
#   path('video/<int:pk>/setup/<int:setup>/', views.video_add_setup, name='video-add-setup'),
  
#   # Document
#   path('mydocuments/', views.MyDocuments.as_view(), name='my-documents'),
#   path('setup/<int:pk>/document/', views.setup_add_document, name='setup-add-document'),
#   path('course/<int:pk>/document/', views.course_add_document, name='course-add-document'),
#   path('document/<int:pk>/convert/', views.document_convert, name='document-convert'),
#   path('document/<int:pk>/edit/', views.document_edit, name='document-edit'),
#   path('document/<int:pk>/delete/', views.document_delete, name='document-delete'),
#   path('setup/<int:pk>/document/<int:document>/', views.setup_remove_document, name='setup-remove-document'),
#   path('course/<int:pk>/document/<int:document>/', views.course_remove_document, name='course-remove-document'),

#   # Note
#   path('setup/<int:pk>/note/', views.setup_add_note, name='setup-add-note'),
#   path('video/<int:pk>/note/', views.video_add_note, name='video-add-note'),
#   path('picture/<int:pk>/note/', views.picture_add_note, name='picture-add-note'),
#   path('note/<int:pk>/edit/', views.note_edit, name='note-edit'),
#   path('note/<int:pk>/delete/', views.note_delete, name='note-delete'),

#   # Upload
#   path('upload/', views.upload, name='upload'),
#   path('upload/<str:model>/<int:pk>/', views.upload, name='upload-to'),
#   path('file/upload/', views.file_upload, name='file-upload'),

#   # Delete
#   path('delete/<str:model>/<int:pk>/', views.delete, name='delete'),

#   # Test
#   path('test/', views.test, name='test'),
#   path('modaltest/', views.modal_test, name='modal-test'),
]

