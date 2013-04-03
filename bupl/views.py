# Create your views here.
from django.template.context import RequestContext
import django.utils.simplejson as json
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response
from webhw.settings import MEDIA_URL
from bupl.grids import BOC_Grid
from django.utils.simplejson import dumps
from bupl.forms import BocForm
from bupl.models import Project

def index(request):
#    app_action = request.POST.get('app_action')
#    posted_data = request.POST.get('json_data')
#    if posted_data is not None and app_action == 'save':
#    elif app_action == 'get_sheets':
#    elif app_action == 'list':
    return render_to_response("example3-editing.html", {'MEDIA_URL' : MEDIA_URL})

def boc_grid_setup(request):
    boc_grid_obj = BOC_Grid()
    return HttpResponse(dumps(boc_grid_obj.get_grid()))

def boc_get_prj_name(request):
    if 'project_id' in request.GET:
        project_id = request.GET['project_id']
    else:
        return HttpResponseServerError('Server Error: You must provide project-id header.')
    try:
        project = Project.objects.get(prj_number = project_id)
        print project
        if project:
            return HttpResponse(dumps({'project_name' : project.prj_name, 'customer' : project.customer,
                                       'manager' : project.manager}))
        else:
            return HttpResponse(dumps({'project_name' : '', 'customer' : '', 'manager' : ''}))
    except:
        return HttpResponse(dumps({'project_name' : '', 'customer' : '', 'manager' : ''}))



def boc_grid_show(request):
    form = BocForm() # A empty, unbound form
    return render_to_response('boc_grid.html', {'form': form, 'MEDIA_URL' : MEDIA_URL},
        context_instance=RequestContext(request))

#return render_to_response("boc_grid.html", {'MEDIA_URL' : MEDIA_URL})