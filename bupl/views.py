# -*- coding: utf-8 -*-
# Create your views here.
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render_to_response, redirect
from django.utils.simplejson import dumps, loads

from webhw.settings import MEDIA_URL
from webhw.common import get_session_key, whoami, get_client_ip
from webhw.settings import BOC_WORK_DIR
from webhw.xlsfiles import handle_xls_file

from bupl.forms import BocForm, EosForm
from bupl.models import Projects

from logging import getLogger
from eos import export_eos_to_pdf, load_eos_from_xls, load_eos_from_xls_new
from price_calcs import calculate_req_line
from os import path
import mimetypes


mimetypes.init()
logger = getLogger(__name__)


def eos_main(request):

    if request.method == 'POST':
        form = EosForm(request.POST, request.FILES)
        if form.is_valid():
            UF_FORM = form.cleaned_data
        if 'X-Progress-ID' in request.GET:
            request.session['X-Progress-ID'] = request.GET['X-Progress-ID']
        logger.info("Starting file  %s proccessing in %s for user from %s" % (request.FILES['xls_file'].name, whoami(),
                                                                              get_client_ip(request)))
        fileattr = handle_xls_file(request.FILES['xls_file'], get_session_key(request) + '_' +
                                                          request.FILES['xls_file'].name)
        if not fileattr == None:
            request.session['xlsfilepath'] = fileattr['filename']
            logger.info("Sucsessfully handeled file  %s in %s" % (request.FILES['xls_file'].name, whoami()))
            request.session['eos_data'] = load_eos_from_xls_new(fileattr['filename'])
            logger.error(request.session['eos_data'])
            return redirect('/eos')
        else:
            logger.info("File type %s is not good, reported from %s" % (request.FILES['xls_file'].name, whoami()))
            return HttpResponse('Bad file type or file corrupted')
    else:
        logger.info("Empty upload form prepared from %s for user from %s, "
                "session id %s" % (whoami(), get_client_ip(request), get_session_key(request)))
        form = EosForm()
#        return render_to_response('confupload_form.html', {'form': form, 'MEDIA_URL' : MEDIA_URL},
#            context_instance=RequestContext(request))
        return render_to_response("new_start.html", {'form': form, 'MEDIA_URL' : MEDIA_URL},
            context_instance=RequestContext(request))


def get_loaded_eos(request):
    if 'eos_data' in request.session.keys():
        if request.session['eos_data'] <> []:
            EOS_DATA = request.session['eos_data']
            request.session['eos_data'] = {}
            return HttpResponse(dumps(EOS_DATA))


def get_prj_list(request):
    """
    Returns a JSON with project details to client
    """
    try:
        PROJECTS_DICT = {}
        AllProjects = Projects.objects.values('prj_number').order_by('prj_number').distinct()
        PROJECTS_DICT["0"] = u'Другой'
        prjcount = 0
        for prj in AllProjects:
            prjnum = prj['prj_number']
            PROJECTS_DICT[prjcount] = prjnum
            prjcount += 1
        PROJECTS_DICT['prjcount'] = prjcount
        return HttpResponse(dumps(PROJECTS_DICT))
    except:
        return HttpResponse(dumps({}))



def calc_req(request):
    req_line = loads(request.POST['json'])
    return HttpResponse(dumps(calculate_req_line(req_line)))


def export_to_pdf(request):
    eos_items = loads(request.POST['json'])
    print 'export ---------'
    print eos_items
    return HttpResponse(dumps({'filename' : export_eos_to_pdf(eos_items)}))


def get_eos_pdf(request, filename):
    try:
        file_path = path.join(BOC_WORK_DIR, filename + ".pdf")
        print file_path
        fsock = open(file_path,"r")
        file_name = path.basename(file_path)
        file_size = path.getsize(file_path)
        print "file size is: " + str(file_size)
        mime_type_guess = mimetypes.guess_type(file_name)
        if mime_type_guess is not None:
            response = HttpResponse(fsock, mimetype=mime_type_guess[0])
        response['Content-Disposition'] = 'attachment; filename=' + file_name
    except IOError:
        response = HttpResponseNotFound()
    return response

def eos_get_prj_name(request):
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
            return HttpResponse(dumps({'project_name' : project.prj_name, 'project_id' :
                project_id}))
        else:
            return HttpResponse(dumps({'project_name' : ''}))
    except:
        return HttpResponse(dumps({'project_name' : '', 'project_id' : ''}))

