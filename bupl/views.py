# Create your views here.
from django.template.context import RequestContext
from models import Workbooks
import django.utils.simplejson as json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from webhw.settings import MEDIA_URL
from bupl.grids import BOC_Grid
from django.utils.simplejson import dumps

def index(request):
#    app_action = request.POST.get('app_action')
#    posted_data = request.POST.get('json_data')
#    if posted_data is not None and app_action == 'save':
#    elif app_action == 'get_sheets':
#    elif app_action == 'list':
    return render_to_response("example3-editing.html", {'MEDIA_URL' : MEDIA_URL})

def boc_grid_setup(request):
    boc_grid_obj = BOC_Grid()
    SLICK_GRID = {}
    SLICK_GRID['data'] = boc_grid_obj.get_grid_data()
    SLICK_GRID['options'] = boc_grid_obj.get_grid_options()
    SLICK_GRID['columns'] = boc_grid_obj.get_grid_columns()
    print SLICK_GRID
    return HttpResponse(dumps(SLICK_GRID))

def boc_grid_show(request):
    return render_to_response("boc_grid.html", {'MEDIA_URL' : MEDIA_URL})