# Create your views here.
from django.template.context import RequestContext
import django.utils.simplejson as json
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, redirect
from webhw.settings import MEDIA_URL
from django.utils.simplejson import dumps, load, loads
from bupl.forms import BocForm
from bupl.models import Projects
from bupl.xlsfiles import handle_xls_file
from webhw.common import get_session_key, whoami
from webhw.settings import BOC_WORK_DIR
from bupl.boc import BOC, EMPTY, IN_XLS, IN_DB, IN_SESSION
from logging import getLogger



logger = getLogger(__name__)


def index(request):
#    app_action = request.POST.get('app_action')
#    posted_data = request.POST.get('json_data')
#    if posted_data is not None and app_action == 'save':
#    elif app_action == 'get_sheets':
#    elif app_action == 'list':
    return render_to_response("example3-editing.html", {'MEDIA_URL' : MEDIA_URL})

def boc_main(request):
    return render_to_response("new_start.html", {'MEDIA_URL' : MEDIA_URL})

def boc_grid_setup(request):
    """
    Returns a JSON with grid data to new form or to loaded from file form
    """
    boc = BOC(type=EMPTY)
#    print request.session.keys()
    if 'grid_data' in request.session.keys():
        if request.session['grid_data'] <> []:
            boc.type = IN_SESSION
            boc.data = request.session['grid_data']
            request.session['grid_data'] = []
    return HttpResponse(dumps(boc.get_grid()))

def boc_xlssave(request):
    """
    Saves all boc data to XLS file
    """
    print "IN XLS SAVE"
    data = {}
    boc = BOC(type=EMPTY, bocworkdir = BOC_WORK_DIR)
    try:
        boc.data = loads(request.POST['json'])
        boc.calculate()
        data['filename'] = boc.save_in_xls()
        data['error'] = "None"
        logger.error(data)
#        print data
        return HttpResponse(dumps(data))
#        fsock = open(BOC_WORK_DIR + data['filename'],"r")
#        response = HttpResponse(fsock, mimetype = "application/ms-excel")
#        response['Content-Disposition'] = 'attachment; filename = %s' % data['filename']
#        return response
    except:
        return HttpResponse(dumps({'error' : 'Unknown error'}))


def boc_grid_calc(request):
    """
    Returns a JSON with calculated grid data or errors to client
    """
    boc = BOC(type=EMPTY)
    try:
        boc.data = loads(request.POST['json'])
        boc.calculate()
        data = boc.get_grid()
        data['totalcost'] = boc.totalcost
        print data
        return HttpResponse(dumps(data))
    except:
        return HttpResponse(dumps({'error' : 'Unknown error'}))

def boc_get_prj_name(request):
    """
    Returns a JSON with project details to client
    """
    if 'project_id' in request.GET:
        project_id = request.GET['project_id']
    else:
        return HttpResponseServerError('Server Error: You must provide project-id header.')
    try:
        project = Projects.objects.get(prj_number = project_id)
        if project:
            return HttpResponse(dumps({'project_name' : project.prj_name, 'customer' : project.customer,
                                       'manager' : project.manager}))
        else:
            return HttpResponse(dumps({'project_name' : '', 'customer' : '', 'manager' : ''}))
    except:
        return HttpResponse(dumps({'project_name' : '', 'customer' : '', 'manager' : ''}))

def boc_grid_form(request):
    """
    Main boc view
    """
    if request.method == 'POST':
        form = BocForm(request.POST, request.FILES)
        if form.is_valid():
            UF_FORM = form.cleaned_data
            if (not 'xlsexport' in request.POST) and ('calc' not in request.POST):
                if 'X-Progress-ID' in request.GET:
                    request.session['X-Progress-ID'] = request.GET['X-Progress-ID']
                fileattr = handle_xls_file(request.FILES['file'], get_session_key(request) + '_' +
                                                                  request.FILES['file'].name)
                if not fileattr == None:
                    request.session['xlsfilepath'] = fileattr['filename']
                    logger.info("Sucsessfully handeled file  %s in %s" % (request.FILES['file'].name, whoami()))
                    boc = BOC(type = IN_XLS, filename = fileattr['filename'])
                    request.session['grid_data'] = boc.data
                    return redirect('/boc')
                else:
                    logger.info("File type %s is not good, reported from %s" % (request.FILES['file'].name, whoami()))
                    return HttpResponse('Bad file type or file corrupted')
            elif 'xlsexport' in request.POST:
                logger.error("Starting export to XLS")
                if 'xlsfilename' in request.POST:
                    fsock = open(BOC_WORK_DIR + request.POST['xlsfilename'], "r")
                    response = HttpResponse(fsock, mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename = %s' % request.POST['xlsfilename']
                    form.clean()
                    return response
                else:
                    logger.error("No xlsfilename")

        else:
            print "%s" % repr(form.errors)

    else:
        form = BocForm() # A empty, unbound form

        return render_to_response('boc_grid.html', {'form': form, 'MEDIA_URL' : MEDIA_URL},
            context_instance=RequestContext(request))



