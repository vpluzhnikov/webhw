# -*- coding: utf-8 -*-
__author__ = 'vs'

from webhw.settings import UPLOAD_DIR
from os import remove

def handle_xls_file(f, name):
    with open(UPLOAD_DIR + name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        if check_filetype(f, name):
            return {'filename': UPLOAD_DIR + name}
        else:
#            logger.info("File type %s is not valid" % (name))
            remove(UPLOAD_DIR + name)
            return None

def check_filetype(f, name):
    if ( ('xls' in name) and not ('xlsx' in name) ):
        return True
    else:
        return False
