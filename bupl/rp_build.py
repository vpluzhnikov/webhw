# -*- coding: utf-8 -*-
from bupl.rp import ProjectPlan

from os import path
from time import time

from bupl.eos import ru_vals

from webhw.settings import BOC_WORK_DIR

tasks_id_values  = { "aix_standalone" : "1.2.1",
                     "aix_cluster" : "1.2.2",
                     "aix_upgrade" : "1.2.11",
                     "x86_vm" : "1.2.8",
                     "windows_standalone" : "1.2.9",
                     'windows_cluster' : "1.2.10",
                     "linux" : "1.2.5",
                     "solaris_standalone" : "1.2.6",
                     "solaris_cluster" : "1.2.7",
                     "solaris_upgrade" : "1.2.13",
                     "hpux_standalone" : "1.2.3",
                     "hpux_cluster" : "1.2.4",
                     "hpux_upgrade" : "1.2.12",
                     "loadbalancer" : "1.2.17",
                     "datapower" : "1.2.16",
                     "san_upgrade_cluster" : "1.2.15",
                     "san_upgrade_standalone" : "1.2.14",
                     "nas_upgrade" : "1.2.18",
}

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

    techporject = ProjectPlan(project_id, path.join(BOC_WORK_DIR, filename + ".xml"))
    techporject.add_extednded_attrs()
    techporject.add_calendar()

    for key in eos_items.keys():

        req_line_tasks = []

        print eos_items[key]
        if (eos_items[key]['platform_type'] == 'x86'):
            if (int(eos_items[key]['cpu_count']) > 24) or (eos_items[key]['itemtype1'] == u'mqdmz'):
                if ((eos_items[key]['itemtype1'] == u'mqdmz') or (eos_items[key]['ostype'] == u'windows')):
                    if (eos_items[key]['cluster_type'] == u'vcs'):
                        req_line_tasks.append(tasks_id_values["windows_cluster"])
                    else:
                        req_line_tasks.append(tasks_id_values["windows_standalone"])
                        if int(eos_items[key]['san_count']) > 0:
                            req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                        if int(eos_items[key]['nas_count']) > 0:
                            req_line_tasks.append(tasks_id_values["nas_upgrade"])
                elif (eos_items[key]['ostype'] == u'linux'):
                    req_line_tasks.append(tasks_id_values["linux"])
                    if int(eos_items[key]['san_count']) > 0:
                        req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                    if int(eos_items[key]['nas_count']) > 0:
                        req_line_tasks.append(tasks_id_values["nas_upgrade"])
            elif (int(eos_items[key]['cpu_count']) < 24):
                if (eos_items[key]['ostype'] == u'windows'):
                    req_line_tasks.append(tasks_id_values["x86_vm"])
                    req_line_tasks.append(tasks_id_values["windows_standalone"])
                    if int(eos_items[key]['san_count']) > 0:
                        req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                    if int(eos_items[key]['nas_count']) > 0:
                        req_line_tasks.append(tasks_id_values["nas_upgrade"])
                elif (eos_items[key]['ostype'] == u'linux'):
                    req_line_tasks.append(tasks_id_values["x86_vm"])
                    req_line_tasks.append(tasks_id_values["linux"])
                    if int(eos_items[key]['san_count']) > 0:
                        req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                    if int(eos_items[key]['nas_count']) > 0:
                        req_line_tasks.append(tasks_id_values["nas_upgrade"])
        elif (eos_items[key]['platform_type'] == 'power'):
            if (eos_items[key]['itemtype2'] == u'upgrade'):
                req_line_tasks.append(tasks_id_values["aix_upgrade"])
                if int(eos_items[key]['san_count']) > 0:
                    if (eos_items[key]['cluster_type'] == u'vcs'):
                        req_line_tasks.append(tasks_id_values["san_upgrade_cluster"])
                    else:
                        req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                if int(eos_items[key]['nas_count']) > 0:
                    req_line_tasks.append(tasks_id_values["nas_upgrade"])
            elif (eos_items[key]['cluster_type'] == u'vcs'):
                req_line_tasks.append(tasks_id_values["aix_cluster"])
            else:
                req_line_tasks.append(tasks_id_values["aix_standalone"])
        elif (u'_series' in  eos_items[key]['platform_type']):
            if (eos_items[key]['itemtype2'] == u'upgrade'):
                req_line_tasks.append(tasks_id_values["solaris_upgrade"])
                if int(eos_items[key]['san_count']) > 0:
                    if (eos_items[key]['cluster_type'] == u'vcs'):
                        req_line_tasks.append(tasks_id_values["san_upgrade_cluster"])
                    else:
                        req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                if int(eos_items[key]['nas_count']) > 0:
                    req_line_tasks.append(tasks_id_values["nas_upgrade"])
            elif (eos_items[key]['cluster_type'] == u'vcs'):
                req_line_tasks.append(tasks_id_values["solaris_cluster"])
            else:
                req_line_tasks.append(tasks_id_values["solaris_standalone"])
        elif (eos_items[key]['platform_type'] == 'itanium'):
            if (eos_items[key]['itemtype2'] == u'upgrade'):
                req_line_tasks.append(tasks_id_values["hpux_upgrade"])
                if int(eos_items[key]['san_count']) > 0:
                    if (eos_items[key]['cluster_type'] == u'vcs'):
                        req_line_tasks.append(tasks_id_values["san_upgrade_cluster"])
                    else:
                        req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                if int(eos_items[key]['nas_count']) > 0:
                    req_line_tasks.append(tasks_id_values["nas_upgrade"])
            elif (eos_items[key]['cluster_type'] == u'vcs'):
                req_line_tasks.append(tasks_id_values["hpux_cluster"])
            else:
                req_line_tasks.append(tasks_id_values["hpux_standalone"])
        else:
            if (eos_items[key]['itemtype1'] == u'dp'):
                req_line_tasks.append(tasks_id_values["datapower"])
            elif (eos_items[key]['itemtype1'] == u'lb'):
                req_line_tasks.append(tasks_id_values["loadbalancer"])

            #        print req_line_tasks
        for i in range(int(eos_items[key]['item_count'])):
            block_id = None
            for task in req_line_tasks:
#                print task, block_id
                task_details = unicode(ru_vals[eos_items[key]['itemtype1']]) + u' CPU/RAM/SAN : ' + \
                               str(eos_items[key]['cpu_count']) + u"/" + str(eos_items[key]['ram_count']) + u"/" + \
                               str(eos_items[key]['san_count'])
                block_id = techporject.add_task(taskid=task, linked_with_block=block_id,
                    task_additional_name = task_details)
#                print block_id
#        print techporject.block_structure
#    techporject.add_task("1.2.1")
#    techporject.add_task("1.2.1",1,3)
#    techporject.add_task("1.2.1",1)

    techporject.export_project_xml()

    return filename