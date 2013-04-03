from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('SerloBox.views',
    # Examples:
    # url(r'^$', 'SerloBox.views.home', name='home'),
    # url(r'^SerloBox/', include('SerloBox.foo.urls')),
	url(r'^$', 'index'),
	url(r'index', 'index'),
    url(r'upload','upload'),
	url(r'login', 'login'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
