
from django.conf.urls.defaults import patterns, url

from .views import settings_view
from .views import missing_setting

urlpatterns = patterns('devilry_authenticateduserinfo',
                       url(r'^settings.js$', settings_view, name="devilry-settings"),
                       url(r'^missing_setting/(\w+)$', missing_setting),
                      )

