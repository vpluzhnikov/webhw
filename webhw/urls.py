from django.conf.urls import patterns, include, url
from bupl.views import eos_get_prj_name, eos_main, calc_req, export_to_pdf, get_exported_file, \
    get_loaded_eos, get_prj_list, build_resource_plan, login_view, logout_view, check_user
from webhw import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webhw.views.home', name='home'),
    # url(r'^webhw/', include('webhw.foo.urls')),
    url(r'^eos/login$', login_view),
    url(r'^eos/logout$', logout_view),
    url(r'^eos/check_user$', check_user),
    url(r'^eos$', eos_main),
    url(r'^eos/calc_req$', calc_req),
    url(r'^eos/export_to_pdf$', export_to_pdf),
    url(r'^eos/get_loaded_eos$', get_loaded_eos),
    url(r'^eos/get_prj_list$', get_prj_list),
    url(r'^eos/get_eos_pdf/(?P<filename>\w+)$', get_exported_file),
    url(r'^eos/build_resource_plan$', build_resource_plan),
    url(r'^eos/get_resource_plan/(?P<filename>\w+)$', get_exported_file),
    url(r'^eos/get_prj_name$', eos_get_prj_name),
    url(r'^eos/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^eos/admin/', include(admin.site.urls)),
)
