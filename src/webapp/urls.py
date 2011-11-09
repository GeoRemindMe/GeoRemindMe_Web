from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': ('webapp',),
}


urlpatterns = patterns('',
   url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict, 'jsi18n'),
   url(r'^accounts/', include('userena.urls')),
   url(r'^messages/', include('userena.contrib.umessages.urls')),
   url(r'^social/', include('socialregistration.urls',namespace = 'socialregistration')),
   url(r'^notifications/', include('timelines.urls')), # notificaciones timeline
   url(r'', include('profiles.urls')), # perfiles
   url(r'', include('mainApp.urls')),
   url(r'^sentry/', include('sentry.web.urls')),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^admin_tools/', include('admin_tools.urls')),
)
