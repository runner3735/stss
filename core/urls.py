
from django.urls import path
from . import views

urlpatterns = [
  # Home
  path('', views.home, name='home'),
  path('assets', views.AssetList.as_view(), name='assets'),
  path('people', views.PersonList.as_view(), name='people'),
  path('purchases', views.PurchaseList.as_view(), name='purchases'),
  path('purchase/new/', views.purchase_new, name='purchase-new'),

#   # Course
#   path('course/new/', views.course_new, name='course-new'),
#   path('courses/', views.CourseList.as_view(), name='courses'),
#   path('course/<int:pk>/', views.CourseDetail.as_view(), name='course'),
#   path('uncourse/<str:model>/<int:pk>/<int:course>/', views.uncourse, name='uncourse'),
#   path('addcourse/<str:model>/<int:pk>/<int:course>/', views.addcourse, name='addcourse'),
  path('contacts/<str:model>/<int:pk>/', views.edit_contacts, name='edit-contacts'),

#   # Asset
#   path('demos/', views.DemoList.as_view(), name='demos'),
#   path('demosbypicture/', views.DemosByPicture.as_view(), name='demos-by-picture'),
#   path('demo/new/', views.demo_new, name='demo-new'),

  # Asset
  path('asset/<int:pk>/', views.AssetDetail.as_view(), name='asset'),
  path('asset/new/', views.asset_new, name='asset-new'),
  path('asset/<int:pk>/name/edit/', views.asset_edit_name, name='asset-edit-name'),
  path('asset/<int:pk>/name/', views.asset_name, name='asset-name'),
  path('asset/<int:pk>/location/edit/', views.asset_edit_location, name='asset-edit-location'),
  path('asset/<int:pk>/location/', views.asset_location, name='asset-location'),
  path('asset/<int:pk>/nickname/edit', views.asset_edit_nickname, name='asset-edit-nickname'),
  path('asset/<int:pk>/nickname/', views.asset_nickname, name='asset-nickname'),
  path('asset/<int:pk>/notes/', views.asset_notes, name='asset-notes'),
  path('asset/<int:pk>/info/edit/', views.asset_edit_info, name='asset-edit-info'),
  path('asset/<int:pk>/clone/', views.asset_clone, name='asset-clone'),

  path('asset/<int:pk>/manufacturer/edit/', views.asset_edit_manufacturer, name='asset-edit-manufacturer'),
  path('asset/<int:pk>/manufacturer/', views.asset_manufacturer, name='asset-manufacturer'),
  path('asset/<int:pk>/model/edit/', views.asset_edit_model, name='asset-edit-model'),
  path('asset/<int:pk>/model/', views.asset_model, name='asset-model'),
  path('asset/model/options', views.asset_model_options, name='asset-model-options'),
  path('asset/name/options', views.asset_name_options, name='asset-name-options'),
  path('asset/<int:pk>/serial/edit/', views.asset_edit_serial, name='asset-edit-serial'),
  path('asset/<int:pk>/serial/', views.asset_serial, name='asset-serial'),
  path('asset/<int:pk>/status/edit/', views.asset_edit_status, name='asset-edit-status'),
  path('asset/<int:pk>/status/', views.asset_status, name='asset-status'),
  path('asset/<int:pk>/department/edit/', views.asset_edit_department, name='asset-edit-department'),
  path('asset/<int:pk>/department/', views.asset_department, name='asset-department'),
  path('asset/<int:pk>/inventoried/edit/', views.asset_edit_inventoried, name='asset-edit-inventoried'),
  path('asset/<int:pk>/inventoried/', views.asset_inventoried, name='asset-inventoried'),

#   # Activity
  path('vendors/', views.VendorList.as_view(), name='vendors'),
  path('rooms/', views.RoomList.as_view(), name='rooms'),
#   path('activitiesbypicture/', views.ActivitiesByPicture.as_view(), name='activities-by-picture'),
#   path('activity/new/', views.activity_new, name='activity-new'),

  # Room
#   path('rooms/', views.rooms, name='rooms'),
#   path('room/<int:pk>/', views.RoomDetail.as_view(), name='room'),
#   path('unroom/<str:model>/<int:pk>/<int:room>/', views.unroom, name='unroom'),
  path('selectroom/<str:model>/<int:pk>/<int:room>/', views.select_room, name='selectroom'),
  path('room/<str:model>/<int:pk>/', views.edit_room, name='edit-room'),

  # Person
  # path('people/', views.people, name='people'),
  path('person/<int:pk>/', views.PersonDetail.as_view(), name='person'),
  path('vendor/<int:pk>/', views.VendorDetail.as_view(), name='vendor'),
  path('room/<int:pk>/', views.RoomDetail.as_view(), name='room'),
  # path('person/<int:pk>/edit/', views.person_edit, name='person-edit'),
  # path('person/<int:pk>/delete/', views.person_delete, name='person-delete'),
  path('uncontact/<str:model>/<int:pk>/<int:contact>/', views.uncontact, name='uncontact'),
  path('addcontact/<str:model>/<int:pk>/<int:contact>/', views.addcontact, name='addcontact'),
  # path('people/<str:model>/<int:pk>/', views.edit_people, name='edit-people'),

  path('person/<int:pk>/phone/edit/', views.person_edit_phone, name='person-edit-phone'),
  path('person/<int:pk>/phone/', views.person_phone, name='person-phone'),
  path('person/<int:pk>/email/edit/', views.person_edit_email, name='person-edit-email'),
  path('person/<int:pk>/email/', views.person_email, name='person-email'),
  path('person/<int:pk>/department/edit/', views.person_edit_department, name='person-edit-department'),
  path('person/<int:pk>/departments', views.person_departments, name='person-departments'),
  path('person/<int:pk>/status/edit/', views.person_edit_status, name='person-edit-status'),
  path('person/<int:pk>/status/', views.person_status, name='person-status'),
  # Purchase
  path('purchase/<int:pk>/', views.PurchaseDetail.as_view(), name='purchase'),
  # path('purchase/<int:pk>/', views.purchase_detail, name='purchase'),
  path('purchase/<int:pk>/asset', views.purchase_add_asset, name='purchase-add-asset'),
  path('purchase/<int:pk>/total', views.purchase_update_total, name='purchase-update-total'),

#   # Tag
#   path('tags/', views.tags, name='tags'),
#   path('tag/<int:pk>/', views.TagDetail.as_view(), name='tag'),
#   path('tag/<int:tag>/edit/', views.tag_edit, name='tag-edit'),
#   path('tag/<int:tag>/delete/', views.tag_delete, name='tag-delete'),
  path('untag/<str:model>/<int:pk>/<int:tag>/', views.untag, name='untag'),
  path('addtag/<str:model>/<int:pk>/<int:tag>/', views.addtag, name='addtag'),
  path('tags/<str:model>/<int:pk>/', views.edit_tags, name='edit-tags'),

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
  path('picture/<int:pk>/', views.picture_detail, name='picture'),
  path('picture/<int:pk>/edit/', views.picture_edit, name='picture-edit'),
#   path('picture/<int:pk>/rotate/<int:degrees>/', views.picture_rotate, name='picture-rotate'),
  path('picture/<int:pk>/delete/', views.picture_delete, name='picture-delete'),
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
  path('note/<str:model>/<int:pk>/', views.add_note, name='add-note'),
#   path('setup/<int:pk>/note/', views.setup_add_note, name='setup-add-note'),
#   path('video/<int:pk>/note/', views.video_add_note, name='video-add-note'),
#   path('picture/<int:pk>/note/', views.picture_add_note, name='picture-add-note'),
  path('note/<int:pk>/edit/', views.note_edit, name='note-edit'),
#   path('note/<int:pk>/delete/', views.note_delete, name='note-delete'),

#   # Upload
#   path('upload/', views.upload, name='upload'),
  path('upload/<str:model>/<int:pk>/', views.upload, name='upload-to'),
  path('file/upload/', views.file_upload, name='file-upload'),

#   # Delete
#   path('delete/<str:model>/<int:pk>/', views.delete, name='delete'),

#   # Test
#   path('test/', views.test, name='test'),
#   path('modaltest/', views.modal_test, name='modal-test'),
]

