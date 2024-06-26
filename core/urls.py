
from django.urls import path
from . import views

urlpatterns = [
# Home
  path('', views.home, name='home'),

# Background Tasks
  path("task/<task_id>/status/", views.get_status, name="task_status"),
  path("task/run/", views.run_task, name="task_run"),
  
# List Views
  path('assets/', views.assets, name='assets'),
  path('asset/table/', views.asset_table, name='asset-table'),
  path('asset/page/', views.asset_page, name='asset-page'),
  path('jobs/', views.jobs, name='jobs'),
  path('job/table/', views.job_table, name='job-table'),
  path('job/page/', views.job_page, name='job-page'),
  path('people/', views.people, name='people'),
  path('people/list/', views.people_list, name='people-list'),
  path('purchases/', views.purchases, name='purchases'),
  path('purchase/table/', views.purchase_table, name='purchase-table'),
  path('purchase/page/', views.purchase_page, name='purchase-page'),
  path('vendors/', views.vendors, name='vendors'),
  path('vendors/<int:page>/', views.vendor_list, name='vendor-list'),
  path('rooms/', views.RoomList.as_view(), name='rooms'),
  path('tags/', views.TagList.as_view(), name='tags'),
  path('pmis/', views.PMIList.as_view(), name='pmis'),

# Asset
  path('asset/new/', views.asset_new, name='asset-new'),
  path('asset/<int:pk>/', views.AssetDetail.as_view(), name='asset'),
  path('asset/<int:pk>/name/edit/', views.asset_edit_name, name='asset-edit-name'),
  path('asset/<int:pk>/name/', views.asset_name, name='asset-name'),
  path('asset/<int:pk>/location/edit/', views.asset_edit_location, name='asset-edit-location'),
  path('asset/<int:pk>/location/', views.asset_location, name='asset-location'),
  path('asset/<int:pk>/nickname/edit', views.asset_edit_nickname, name='asset-edit-nickname'),
  path('asset/<int:pk>/nickname/', views.asset_nickname, name='asset-nickname'),
  path('asset/<int:pk>/info/edit/', views.asset_edit_info, name='asset-edit-info'),
  path('asset/model/options', views.asset_model_options, name='asset-model-options'),
  path('asset/name/options', views.asset_name_options, name='asset-name-options'),
  path('asset/<int:pk>/clone/', views.asset_clone, name='asset-clone'),
  path('asset/<int:pk>/notes/', views.asset_notes, name='asset-notes'),
  path('asset/<int:pk>/files/', views.asset_files, name='asset-files'),
  path('asset/<int:pk>/jobs/', views.asset_jobs, name='asset-jobs'),
  path('asset/<int:pk>/gallery/', views.asset_gallery, name='asset-gallery'),
  path('asset/<int:pk>/purchases/', views.asset_purchases, name='asset-purchases'),
  path('asset/<int:pk>/manufacturer/edit/', views.asset_edit_manufacturer, name='asset-edit-manufacturer'),
  path('asset/<int:pk>/manufacturer/', views.asset_manufacturer, name='asset-manufacturer'),
  path('asset/<int:pk>/model/edit/', views.asset_edit_model, name='asset-edit-model'),
  path('asset/<int:pk>/model/', views.asset_model, name='asset-model'),
  path('asset/<int:pk>/serial/edit/', views.asset_edit_serial, name='asset-edit-serial'),
  path('asset/<int:pk>/serial/', views.asset_serial, name='asset-serial'),
  path('asset/<int:pk>/status/edit/', views.asset_edit_status, name='asset-edit-status'),
  path('asset/<int:pk>/status/', views.asset_status, name='asset-status'),
  path('asset/<int:pk>/department/edit/', views.asset_edit_department, name='asset-edit-department'),
  path('asset/<int:pk>/department/', views.asset_department, name='asset-department'),
  path('asset/<int:pk>/inventoried/edit/', views.asset_edit_inventoried, name='asset-edit-inventoried'),
  path('asset/<int:pk>/inventoried/', views.asset_inventoried, name='asset-inventoried'),
  path('asset/<int:asset>/remove/<str:model>/<int:pk>/', views.asset_remove, name='asset-remove'),

# Job
  path('job/new/', views.job_new, name='job-new'),
  path('job/<int:pk>/', views.JobDetail.as_view(), name='job'),
  path('job/<int:pk>/less/', views.job_data_less, name='job-data-less'),
  path('job/<int:pk>/more/', views.job_data_more, name='job-data-more'),
  path('job/find/', views.job_find, name='job-find'),
  path('job/get/<str:identifier>/', views.job_get, name='job-get'),
  path('job/<int:pk>/details/', views.job_details, name='job-details'),
  path('job/<int:pk>/assets/', views.job_assets, name='job-assets'),
  path('job/<int:pk>/works/', views.job_works, name='job-works'),
  path('job/<int:pk>/notes/', views.job_notes, name='job-notes'),
  path('job/<int:pk>/files/', views.job_files, name='job-files'),
  path('job/<int:pk>/gallery/', views.job_gallery, name='job-gallery'),
  path('job/<int:pk>/delete/', views.job_delete, name='job-delete'),

  path('job/<int:pk>/name/', views.job_name, name='job-name'),
  path('job/<int:pk>/budget/', views.job_budget, name='job-budget'),
  path('job/<int:pk>/course/', views.job_course, name='job-course'),
  path('job/<int:pk>/location/', views.job_location, name='job-location'),
  path('job/<int:pk>/opened/', views.job_opened, name='job-opened'),
  path('job/<int:pk>/deadline/', views.job_deadline, name='job-deadline'),
  path('job/<int:pk>/closed/', views.job_closed, name='job-closed'),
  path('job/<int:pk>/status/', views.job_status, name='job-status'),
  path('job/<int:pk>/kind/', views.job_kind, name='job-kind'),
  path('job/<int:pk>/category/', views.job_category, name='job-category'),
  path('job/<int:pk>/departments/', views.job_departments, name='job-departments'),
  path('job/<int:pk>/rooms/', views.job_rooms, name='job-rooms'),

  path('job/<int:pk>/name/edit/', views.job_name_edit, name='job-name-edit'),
  path('job/<int:pk>/budget/edit/', views.job_budget_edit, name='job-budget-edit'),
  path('job/<int:pk>/course/edit/', views.job_course_edit, name='job-course-edit'),
  path('job/<int:pk>/location/edit/', views.job_location_edit, name='job-location-edit'),
  path('job/<int:pk>/opened/edit/', views.job_opened_edit, name='job-opened-edit'),
  path('job/<int:pk>/deadline/edit/', views.job_deadline_edit, name='job-deadline-edit'),
  path('job/<int:pk>/closed/edit/', views.job_closed_edit, name='job-closed-edit'),
  path('job/<int:pk>/status/edit/', views.job_status_edit, name='job-status-edit'),
  path('job/<int:pk>/kind/edit/', views.job_kind_edit, name='job-kind-edit'),
  path('job/<int:pk>/category/edit/', views.job_category_edit, name='job-category-edit'),
  path('job/<int:pk>/departments/edit/', views.job_departments_edit, name='job-departments-edit'),
  path('job/<int:pk>/rooms/edit/', views.job_rooms_edit, name='job-rooms-edit'),
  path('job/<int:pk>/details/edit/', views.job_details_edit, name='job-details-edit'),
  path('job/<int:pk>/assets/edit/', views.job_assets_edit, name='job-assets-edit'),
  path('job/<int:pk>/assets/list/', views.job_assets_list, name='job-assets-list'),
  path('job/<int:pk>/asset/<int:asset>/add/', views.job_asset_add, name='job-asset-add'),
  path('job/<int:pk>/asset/<int:asset>/remove/', views.job_asset_remove, name='job-asset-remove'),
  path('job/<int:pk>/work/new/', views.work_new, name='work-new'),

# PMI

  path('pmi/new/', views.pmi_new, name='pmi-new'),
  path('pmi/<int:pk>/', views.PMIDetail.as_view(), name='pmi'),

  path('pmi/<int:pk>/frequency/', views.pmi_frequency, name='pmi-frequency'),
  path('pmi/<int:pk>/next/', views.pmi_next, name='pmi-next'),
  path('pmi/<int:pk>/name/', views.pmi_name, name='pmi-name'),
  path('pmi/<int:pk>/location/', views.pmi_location, name='pmi-location'),
  path('pmi/<int:pk>/departments/', views.pmi_departments, name='pmi-departments'),
  path('pmi/<int:pk>/rooms/', views.pmi_rooms, name='pmi-rooms'),
  path('pmi/<int:pk>/files/', views.pmi_files, name='pmi-files'),
  path('pmi/<int:pk>/assets/', views.pmi_assets, name='pmi-assets'),

  path('pmi/<int:pk>/frequency/edit/', views.pmi_frequency_edit, name='pmi-frequency-edit'),
  path('pmi/<int:pk>/next/edit/', views.pmi_next_edit, name='pmi-next-edit'),
  path('pmi/<int:pk>/name/edit/', views.pmi_name_edit, name='pmi-name-edit'),
  path('pmi/<int:pk>/location/edit/', views.pmi_location_edit, name='pmi-location-edit'),
  path('pmi/<int:pk>/departments/edit/', views.pmi_departments_edit, name='pmi-departments-edit'),
  path('pmi/<int:pk>/rooms/edit/', views.pmi_rooms_edit, name='pmi-rooms-edit'),
  path('pmi/<int:pk>/details/edit/', views.pmi_details_edit, name='pmi-details-edit'),

  path('pmi/<int:pk>/asset/add/', views.pmi_asset_add, name='pmi-asset-add'),
  path('pmi/<int:pk>/schedule/', views.pmi_schedule, name='pmi-schedule'),
  path('pmi/<int:pk>/completed/', views.pmi_completed, name='pmi-completed'),

# Room
  path('room/<int:pk>/', views.RoomDetail.as_view(), name='room'),
  path('room/<str:model>/<int:pk>/', views.edit_room, name='edit-room'),
  path('selectroom/<str:model>/<int:pk>/<int:room>/', views.select_room, name='selectroom'),

# Vendor
  path('vendor/<int:pk>/', views.VendorDetail.as_view(), name='vendor'),

# Person
  path('me/', views.me, name='me'),
  path('person/new/', views.person_new, name='person-new'),
  path('person/<int:pk>/', views.PersonDetail.as_view(), name='person'),
  path('person/<int:pk>/assets/', views.person_assets, name='person-assets'),
  path('person/<int:pk>/jobs/sortby/<int:column>/', views.person_jobs, name='person-jobs'),
  path('person/<int:pk>/tasks/sortby/<int:column>/', views.person_tasks, name='person-tasks'),
  path('person/<int:pk>/phone/edit/', views.person_edit_phone, name='person-edit-phone'),
  path('person/<int:pk>/phone/', views.person_phone, name='person-phone'),
  path('person/<int:pk>/email/edit/', views.person_edit_email, name='person-edit-email'),
  path('person/<int:pk>/email/', views.person_email, name='person-email'),
  path('person/<int:pk>/departments/', views.person_departments, name='person-departments'),
  path('person/<int:pk>/department/edit/', views.person_edit_department, name='person-edit-department'),
  path('person/<int:pk>/status/edit/', views.person_edit_status, name='person-edit-status'),
  path('person/<int:pk>/status/', views.person_status, name='person-status'),
  path('people/select/<str:model>/<int:pk>/', views.people_select, name='people-select'),
  path('people/tags/<str:model>/<int:pk>/', views.people_tags, name='people-tags'),

  path('person/<int:person>/remove/<str:model>/<int:pk>/', views.person_remove, name='person-remove'),
  path('person/<int:person>/add/<str:model>/<int:pk>/', views.person_add, name='person-add'),

  path('technicians/edit/<int:pk>/', views.edit_technicians, name='edit-technicians'),
  path('technician/list/<int:pk>/', views.technician_list, name='technician-list'),
  path('add/technician/<int:pk>/<int:technician>/', views.add_technician, name='add-technician'),
  path('remove/technician/<int:pk>/<int:technician>/', views.remove_technician, name='remove-technician'),
  path('first/names', views.first_names, name='first-names'),
  path('last/names', views.last_names, name='last-names'),

# Purchase
  path('purchase/new/', views.purchase_new, name='purchase-new'),
  path('purchase/<int:pk>/', views.PurchaseDetail.as_view(), name='purchase'),
  path('purchase/<int:pk>/assets/', views.purchase_assets, name='purchase-assets'),
  path('purchase/<int:pk>/files/', views.purchase_files, name='purchase-files'),
  path('purchase/<int:pk>/edit/', views.purchase_edit, name='purchase-edit'),
  path('purchase/<int:pk>/asset', views.purchase_add_asset, name='purchase-add-asset'),
  path('purchase/<int:pk>/total', views.purchase_update_total, name='purchase-update-total'),

# Tag
  path('tag/<int:pk>/', views.TagDetail.as_view(), name='tag'),
  path('tag/<int:tag>/remove/<str:model>/<int:pk>/', views.tag_remove, name='tag-remove'),
  path('tag/<int:tag>/add/<str:model>/<int:pk>/', views.tag_add, name='tag-add'),
  path('tags/edit/<str:model>/<int:pk>/', views.tags_edit, name='tags-edit'),

# Note
  path('note/new/<str:model>/<int:pk>/', views.add_note, name='add-note'),
  path('note/<int:pk>/edit/', views.note_edit, name='note-edit'),

# Upload
  path('upload/', views.upload, name='upload'),
  path('upload/to/<str:model>/<int:pk>/', views.upload_to, name='upload-to'),
  path('upload/file/', views.upload_file, name='upload-file'),
  path('upload/file/to/<str:model>/<int:pk>/', views.upload_file_to, name='upload-file-to'),

# Youtube
  path('youtube/new/', views.youtube_new, name='youtube-new'),
  path('download/new/', views.download_new, name='download-new'),
  path('download/new/to/<str:model>/<int:pk>/', views.download_new_to, name='download-new-to'),
  
# File
  path('file/<int:pk>/', views.do_nothing, name='file'),
  path('my/files/', views.my_files, name='my-files'),
  path('my/downloads/', views.my_downloads, name='my-downloads'),
  path('download/<int:pk>/row/', views.download_row, name='download-row'),
  path('download/<int:pk>/delete/', views.download_delete, name='download-delete'),
  path('downloads/delete/', views.downloads_delete, name='downloads-delete'),
  path('file/<int:pk>/name/edit/', views.file_name_edit, name='file-name-edit'),
  path('file/<int:file>/remove/<str:model>/<int:pk>/', views.file_remove, name='file-remove'),
  path('picture/<int:file>/remove/<str:model>/<int:pk>/', views.picture_remove, name='picture-remove'),
  path('picture/<int:picture>/modal/<str:model>/<int:pk>/', views.picture_modal, name='picture-modal'),

# Work
  path('work/<int:pk>/edit/', views.work_edit, name='work-edit'),

]

