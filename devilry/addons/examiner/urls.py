from django.conf.urls.defaults import *



urlpatterns = patterns('devilry.addons.examiner',
    url(r'^$',
        'views.list_assignments',
        name='devilry-examiner-list_assignments'),

    url(r'^list-groups/(?P<assignment_id>\d+)$',
        'views.list_assignmentgroups',
        name='devilry-examiner-list_assignmentgroups'),
    url(r'^list-groups/json/(?P<assignment_id>\d+)$',
        'views.list_assignmentgroups_json',
        name='devilry-examiner-list_assignmentgroups_json'),

    url(r'^show-group/(?P<assignmentgroup_id>\d+)$',
        'views.show_assignmentgroup',
        name='devilry-examiner-show_assignmentgroup'),
    url(r'^open-group/(?P<assignmentgroup_id>\d+)$',
        'views.open_assignmentgroup',
        name='devilry-examiner-open_assignmentgroup'),
    url(r'^close-group/(?P<assignmentgroup_id>\d+)$',
        'views.close_assignmentgroup',
        name='devilry-examiner-close_assignmentgroup'),
    url(r'^delete-deadline/(?P<assignmentgroup_id>\d+)/(?P<deadline_id>\d+)$',
        'views.delete_deadline',
        name='devilry-examiner-delete_deadline'),

    url(r'^assignments/(?P<assignment_id>\d+)/download_file_collection_as_zip$',
        'views.download_file_collection_as_zip',
        name='devilry-examiner-download_file_collection_as_zip'),
    url(r'^assignments/(?P<assignment_id>\d+)/download_file_collection_as_tar$',
        'views.download_file_collection_as_tar',
        name='devilry-examiner-download_file_collection_as_tar'),
    url(r'^edit-feedback/(?P<delivery_id>\d+)$',
        'views.edit_feedback',
        name='devilry-examiner-edit-feedback'),
)
