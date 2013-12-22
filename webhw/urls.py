from django.conf.urls import patterns, include, url
from bupl.views import index, boc_grid_setup, boc_grid_form, boc_get_prj_name, boc_grid_calc, boc_xlssave, boc_main
from webhw import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webhw.views.home', name='home'),
    # url(r'^webhw/', include('webhw.foo.urls')),
    url(r'^$', boc_main),
#    url(r'^boc_setup$', boc_main),
    url(r'^boc_setup$', boc_grid_setup),
    url(r'^boc_calc', boc_grid_calc),
    url(r'^boc_xlssave', boc_xlssave),
    url(r'^boc_get_prj_name$', boc_get_prj_name),
    url(r'^boc$', boc_grid_form),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
