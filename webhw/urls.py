from django.conf.urls import patterns, include, url
from bupl.views import index, boc_grid_setup, boc_grid_form, boc_get_prj_name, boc_grid_calc, boc_xlssave, eos_main,\
    calc_req, export_to_pdf, get_eos_pdf, get_loaded_eos, get_prj_list
from webhw import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webhw.views.home', name='home'),
    # url(r'^webhw/', include('webhw.foo.urls')),
    url(r'^eos$', eos_main),
    url(r'^eos/calc_req$', calc_req),
    url(r'^eos/export_to_pdf$', export_to_pdf),
    url(r'^eos/get_loaded_eos$', get_loaded_eos),
    url(r'^eos/get_prj_list$', get_prj_list),
    url(r'^eos/get_eos_pdf/(?P<filename>\w+)$', get_eos_pdf),
#url(r'^articles/(?P<year>\d{4})/$', 'news.views.year_archive'),
    #    url(r'^boc_setup$', boc_main),
    url(r'^eos/boc_setup$', boc_grid_setup),
    url(r'^eos/boc_calc', boc_grid_calc),
    url(r'^eos/boc_xlssave', boc_xlssave),
    url(r'^eos/boc_get_prj_name$', boc_get_prj_name),
    url(r'^eos/boc$', boc_grid_form),
    url(r'^eos/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
