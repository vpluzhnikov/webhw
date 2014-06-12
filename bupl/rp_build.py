# -*- coding: utf-8 -*-
from bupl.rp import ProjectPlan

from os import path
from time import time

from webhw.settings import BOC_WORK_DIR

def prepare_resource_plan(eos_items):
    print "prepare plan"
    project_id = str(eos_items['project_id'])
    project_name = eos_items['project_name']
    eos_items.pop("project_id", None)
    eos_items.pop("project_name", None)

    #    filename = path.join(BOC_WORK_DIR, str(int(time())) + ".pdf")
    if project_id == u'0':
        filename = 'tp_' + str(int(time()))
    else:
        filename = 'tp_' + project_id

    for key in eos_items.keys():
        print eos_items[key]

    techporject = ProjectPlan(project_id, path.join(BOC_WORK_DIR, filename + ".xml"))
    techporject.add_extednded_attrs()
    techporject.add_calendar()
    techporject.add_task("1.2.1")
    techporject.add_task("1.2.1",1,3)
    techporject.add_task("1.2.1",1)
    techporject.export_project_xml()

    return filename