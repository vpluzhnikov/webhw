# Create your views here.
from django.template.context import RequestContext
import django.utils.simplejson as json
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response, redirect
from webhw.settings import MEDIA_URL
from bupl.grids import BOC_Grid
from django.utils.simplejson import dumps
from bupl.forms import BocForm
from bupl.models import Project
from bupl.xlsfiles import handle_xls_file
from webhw.common import get_session_key
from bupl.boc import XlsBOC

def index(request):
#    app_action = request.POST.get('app_action')
#    posted_data = request.POST.get('json_data')
#    if posted_data is not None and app_action == 'save':
#    elif app_action == 'get_sheets':
#    elif app_action == 'list':
    return render_to_response("example3-editing.html", {'MEDIA_URL' : MEDIA_URL})

def boc_grid_setup(request):
    boc_grid_obj = BOC_Grid()
    GRID_DATA = boc_grid_obj.get_grid()
    if not request.session['grid_data'] == []:
        GRID_DATA['data'] = request.session['grid_data']
        request.session['grid_data'] = []
    return HttpResponse(dumps(GRID_DATA))

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


def upload_xls_file(request):
    if 'X-Progress-ID' in request.GET:
        request.session['X-Progress-ID'] = request.GET['X-Progress-ID']
    print request.FILES['file']
#    fileattr = handle_uploaded_file(request.FILES['file'], get_session_key(request) + '_' +
#                                                           request.FILES['file'].name, UF_FORM['ostype'])
#    if not ( fileattr == None ):
#                request.session['archpath'] = fileattr['archpath']
#                logger.info("Sucsessfully handeled file  %s in %s" % (request.FILES['file'].name, whoami()))
#                if fileattr['archpath'] == 'counfdump none':
#                    with open(fileattr['dumpfilename']) as infile:
#                        AIXSNAP = load(infile)
#                else:
#                    snap = AixSnap(fileattr['archpath'])
#                    AIXSNAP = snap.snap_analyze(request.FILES['file'].name)
#                    snap.dump_snap_to_json(request.FILES['file'].name, fileattr['dumpfilename'])
#                    snap.snap_destroy()
#                request.session['AIXSNAP'] = AIXSNAP
#                request.session['dumpfilename'] = fileattr['dumpfilename']
#
#                return redirect('/upload/anal_acc/')
#            else:
#                logger.info("File type %s is not good, reported from %s" % (request.FILES['file'].name, whoami()))
#                return HttpResponse(_('Bad file type or file corrupted'))
#
#    else:
#        logger.info("Empty upload form prepared from %s for user from %s, "
#                    "session id %s" % (whoami(), get_client_ip(request), get_session_key(request)))
#        form = ConfUploadForm() # A empty, unbound form
#
#    return render_to_response('confupload_form.html', {'form': form, 'MEDIA_URL' : MEDIA_URL},
#        context_instance=RequestContext(request))

def boc_grid_form(request):
    if request.method == 'POST':
        form = BocForm(request.POST, request.FILES)
        if form.is_valid():
            UF_FORM = form.cleaned_data
            if 'X-Progress-ID' in request.GET:
                request.session['X-Progress-ID'] = request.GET['X-Progress-ID']
            fileattr = handle_xls_file(request.FILES['file'], get_session_key(request) + '_' +
                                                              request.FILES['file'].name)
            if not fileattr == None:
                request.session['xlsfilepath'] = fileattr['filename']
                #            logger.info("Sucsessfully handeled file  %s in %s" % (request.FILES['file'].name, whoami()))
                boc = XlsBOC(fileattr['filename'])
                request.session['grid_data'] = boc.grid_fields()
                # print boc.grid_fields()
                return redirect('/boc')
            else:
            #                logger.info("File type %s is not good, reported from %s" % (request.FILES['file'].name, whoami()))
                return HttpResponse('Bad file type or file corrupted')
        else:
            print "%s" % repr(form.errors)

    else:
        form = BocForm() # A empty, unbound form
        try:
            if request.session['grid_data']:
                print 'Found data'
        except:
            request.session['grid_data'] = []

        return render_to_response('boc_grid.html', {'form': form, 'MEDIA_URL' : MEDIA_URL},
            context_instance=RequestContext(request))



#return render_to_response("boc_grid.html", {'MEDIA_URL' : MEDIA_URL})