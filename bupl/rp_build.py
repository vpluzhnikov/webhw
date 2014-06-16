# -*- coding: utf-8 -*-
from bupl.rp import ProjectPlan

from os import path
from time import time

from bupl.eos import ru_vals

from webhw.settings import BOC_WORK_DIR

ru_vals_4project = {'prom': u'ПРОМ',
                    'test-nt': u'НТ',
                    'test-dev': u'DEV',
                    'test-sst1': u'ССТ1',
                    'test-sst2': u'ССТ2',
                    'test-ift': u'ИФТ',
                    'test-obuch': u'ОБУЧ',
                    'test-psi': u'ПСИ',
                    'test-hf': u'HF',
                    'test-other': u'Тест (Другое)',
}

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
                     "oracle_standalone" : "1.3.2",
                     "oracle_cluster" : "1.3.3",
                     "mssql" : "1.3.1",
                     "db2_standalone" : "1.3.17",
                     "db2_cluster" : "1.3.18",
                     "was_standalone" : "1.3.10",
                     "was_cluster" : "1.3.11",
                     "wmb_standalone" : "1.3.20",
                     "wmb_cluster" : "1.3.21",
                     "wls_standalone" : "1.3.12",
                     "wls_cluster" : "1.3.13",
                     "mq_standalone" : "1.3.4",
                     "mq_cluster" : "1.3.5",
                     "sybase_standalone" : "1.3.14",
                     "sybase_cluster" : "1.3.15",
                     "iis" : "1.3.16",
                     "prpc" : "1.3.19",
                     "ad" : "1.3.7",
                     "dns" : "1.3.8",
                     "sudir" : "1.3.9",
                     "citrix" : "1.3.6",
                     "aix_standalone_test" : "2.2.1",
                     "aix_cluster_test" : "2.2.2",
                     "aix_upgrade_test" : "2.2.11",
                     "x86_vm_test" : "2.2.8",
                     "windows_standalone_test" : "2.2.9",
                     'windows_cluster_test' : "2.2.10",
                     "linux_test" : "2.2.5",
                     "solaris_standalone_test" : "2.2.6",
                     "solaris_cluster_test" : "2.2.7",
                     "solaris_upgrade_test" : "2.2.13",
                     "hpux_standalone_test" : "2.2.3",
                     "hpux_cluster_test" : "2.2.4",
                     "hpux_upgrade_test" : "2.2.12",
                     "loadbalancer_test" : "2.2.17",
                     "datapower_test" : "2.2.16",
                     "san_upgrade_cluster_test" : "2.2.15",
                     "san_upgrade_standalone_test" : "2.2.14",
                     "nas_upgrade_test" : "2.2.18",
                     }

def prepare_resource_plan(eos_items):
    project_id = str(eos_items['project_id'])
    project_name = eos_items['project_name']
    eos_items.pop("project_id", None)
    eos_items.pop("project_name", None)

    if project_id == u'0':
        filename = 'tp_' + str(int(time()))
    else:
        filename = 'tp_' + project_id

    techporject = ProjectPlan(project_id, path.join(BOC_WORK_DIR, filename + ".xml"))
    techporject.add_extednded_attrs()
    techporject.add_calendar()

    project_tasks = {
        'prom' : [],
        'test-nt' : [],
        'test-dev' : [],
        'test-sst1' : [],
        'test-sst2' : [],
        'test-ift' : [],
        'test-obuch' : [],
        'test-psi' : [],
        'test-hf' : [],
        'test-other' : [],
    }

    for key in eos_items.keys():

        req_line_tasks = []

#        print eos_items[key]
        if (eos_items[key]['platform_type'] == 'x86'):
            if (int(eos_items[key]['cpu_count']) > 24) or (eos_items[key]['itemtype1'] == u'mqdmz'):
                if ((eos_items[key]['itemtype1'] == u'mqdmz') or (eos_items[key]['ostype'] == u'windows')):
                    if (eos_items[key]['cluster_type'] == u'vcs'):
                        if eos_items[key]['itemstatus'] == u'prom':
                            req_line_tasks.append(tasks_id_values["windows_cluster"])
                        else:
                            req_line_tasks.append(tasks_id_values["windows_cluster_test"])
                    else:
                        if eos_items[key]['itemstatus'] == u'prom':
                            req_line_tasks.append(tasks_id_values["windows_standalone"])
                        else:
                            req_line_tasks.append(tasks_id_values["windows_standalone_test"])
                        if int(eos_items[key]['san_count']) > 0:
                            if eos_items[key]['itemstatus'] == u'prom':
                                req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                            else:
                                req_line_tasks.append(tasks_id_values["san_upgrade_standalone_test"])
                        if int(eos_items[key]['nas_count']) > 0:
                            if eos_items[key]['itemstatus'] == u'prom':
                                req_line_tasks.append(tasks_id_values["nas_upgrade"])
                            else:
                                req_line_tasks.append(tasks_id_values["nas_upgrade_test"])
                elif (eos_items[key]['ostype'] == u'linux'):
                    if eos_items[key]['itemstatus'] == u'prom':
                        req_line_tasks.append(tasks_id_values["linux"])
                    else:
                        req_line_tasks.append(tasks_id_values["linux_test"])
                        if int(eos_items[key]['san_count']) > 0:
                            if eos_items[key]['itemstatus'] == u'prom':
                                if (eos_items[key]['cluster_type'] == u'vcs'):
                                    req_line_tasks.append(tasks_id_values["san_upgrade_cluster"])
                                else:
                                    req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                            else:
                                if (eos_items[key]['cluster_type'] == u'vcs'):
                                    req_line_tasks.append(tasks_id_values["san_upgrade_cluster_test"])
                                else:
                                    req_line_tasks.append(tasks_id_values["san_upgrade_standalone_test"])
                        if int(eos_items[key]['nas_count']) > 0:
                            if eos_items[key]['itemstatus'] == u'prom':
                                req_line_tasks.append(tasks_id_values["nas_upgrade"])
                            else:
                                req_line_tasks.append(tasks_id_values["nas_upgrade_test"])
            elif (int(eos_items[key]['cpu_count']) < 24):
                if (eos_items[key]['ostype'] == u'windows'):
                    if eos_items[key]['itemstatus'] == u'prom':
                        req_line_tasks.append(tasks_id_values["x86_vm"])
                        req_line_tasks.append(tasks_id_values["windows_standalone"])
                    else:
                        req_line_tasks.append(tasks_id_values["x86_vm_test"])
                        req_line_tasks.append(tasks_id_values["windows_standalone_test"])
                    if int(eos_items[key]['san_count']) > 0:
                        if eos_items[key]['itemstatus'] == u'prom':
                            req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                        else:
                            req_line_tasks.append(tasks_id_values["san_upgrade_standalone_test"])
                    if int(eos_items[key]['nas_count']) > 0:
                        if eos_items[key]['itemstatus'] == u'prom':
                            req_line_tasks.append(tasks_id_values["nas_upgrade"])
                        else:
                            req_line_tasks.append(tasks_id_values["nas_upgrade_test"])
                elif (eos_items[key]['ostype'] == u'linux'):
                    if eos_items[key]['itemstatus'] == u'prom':
                        req_line_tasks.append(tasks_id_values["x86_vm"])
                        req_line_tasks.append(tasks_id_values["linux"])
                    else:
                        req_line_tasks.append(tasks_id_values["x86_vm_test"])
                        req_line_tasks.append(tasks_id_values["linux_test"])
                    if int(eos_items[key]['san_count']) > 0:
                        if eos_items[key]['itemstatus'] == u'prom':
                            req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                        else:
                            req_line_tasks.append(tasks_id_values["san_upgrade_standalone_test"])
                    if int(eos_items[key]['nas_count']) > 0:
                        if eos_items[key]['itemstatus'] == u'prom':
                            req_line_tasks.append(tasks_id_values["nas_upgrade"])
                        else:
                            req_line_tasks.append(tasks_id_values["nas_upgrade_test"])
        elif (eos_items[key]['platform_type'] == 'power'):
            if (eos_items[key]['itemtype2'] == u'upgrade'):
                if eos_items[key]['itemstatus'] == u'prom':
                    req_line_tasks.append(tasks_id_values["aix_upgrade"])
                else:
                    req_line_tasks.append(tasks_id_values["aix_upgrade_test"])
                if int(eos_items[key]['san_count']) > 0:
                    if (eos_items[key]['cluster_type'] == u'vcs'):
                        if eos_items[key]['itemstatus'] == u'prom':
                            req_line_tasks.append(tasks_id_values["san_upgrade_cluster"])
                        else:
                            req_line_tasks.append(tasks_id_values["san_upgrade_cluster_test"])
                    else:
                        if eos_items[key]['itemstatus'] == u'prom':
                            req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                        else:
                            req_line_tasks.append(tasks_id_values["san_upgrade_standalone_test"])
                if int(eos_items[key]['nas_count']) > 0:
                    if eos_items[key]['itemstatus'] == u'prom':
                        req_line_tasks.append(tasks_id_values["nas_upgrade"])
                    else:
                        req_line_tasks.append(tasks_id_values["nas_upgrade_test"])
            elif (eos_items[key]['cluster_type'] == u'vcs'):
                if eos_items[key]['itemstatus'] == u'prom':
                    req_line_tasks.append(tasks_id_values["aix_cluster"])
                else:
                    req_line_tasks.append(tasks_id_values["aix_cluster_test"])
            else:
                if eos_items[key]['itemstatus'] == u'prom':
                    req_line_tasks.append(tasks_id_values["aix_standalone"])
                else:
                    req_line_tasks.append(tasks_id_values["aix_standalone_test"])

        elif (u'_series' in  eos_items[key]['platform_type']):
            if (eos_items[key]['itemtype2'] == u'upgrade'):
                if eos_items[key]['itemstatus'] == u'prom':
                    req_line_tasks.append(tasks_id_values["solaris_upgrade"])
                else:
                    req_line_tasks.append(tasks_id_values["solaris_upgrade_test"])
                if int(eos_items[key]['san_count']) > 0:
                    if (eos_items[key]['cluster_type'] == u'vcs'):
                        if eos_items[key]['itemstatus'] == u'prom':
                            req_line_tasks.append(tasks_id_values["san_upgrade_cluster"])
                        else:
                            req_line_tasks.append(tasks_id_values["san_upgrade_cluster_test"])
                    else:
                        if eos_items[key]['itemstatus'] == u'prom':
                            req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                        else:
                            req_line_tasks.append(tasks_id_values["san_upgrade_standalone_test"])
                if int(eos_items[key]['nas_count']) > 0:
                    if eos_items[key]['itemstatus'] == u'prom':
                        req_line_tasks.append(tasks_id_values["nas_upgrade"])
                    else:
                        req_line_tasks.append(tasks_id_values["nas_upgrade_test"])
            elif (eos_items[key]['cluster_type'] == u'vcs'):
                if eos_items[key]['itemstatus'] == u'prom':
                    req_line_tasks.append(tasks_id_values["solaris_cluster"])
                else:
                    req_line_tasks.append(tasks_id_values["solaris_cluster_test"])
            else:
                if eos_items[key]['itemstatus'] == u'prom':
                    req_line_tasks.append(tasks_id_values["solaris_standalone"])
                else:
                    req_line_tasks.append(tasks_id_values["solaris_standalone_test"])
        elif (eos_items[key]['platform_type'] == 'itanium'):
            if (eos_items[key]['itemtype2'] == u'upgrade'):
                if eos_items[key]['itemstatus'] == u'prom':
                    req_line_tasks.append(tasks_id_values["hpux_upgrade"])
                else:
                    req_line_tasks.append(tasks_id_values["hpux_upgrade_test"])
                if int(eos_items[key]['san_count']) > 0:
                    if (eos_items[key]['cluster_type'] == u'vcs'):
                        if eos_items[key]['itemstatus'] == u'prom':
                            req_line_tasks.append(tasks_id_values["san_upgrade_cluster"])
                        else:
                            req_line_tasks.append(tasks_id_values["san_upgrade_cluster_test"])
                    else:
                        if eos_items[key]['itemstatus'] == u'prom':
                            req_line_tasks.append(tasks_id_values["san_upgrade_standalone"])
                        else:
                            req_line_tasks.append(tasks_id_values["san_upgrade_standalone_test"])
                if int(eos_items[key]['nas_count']) > 0:
                    if eos_items[key]['itemstatus'] == u'prom':
                        req_line_tasks.append(tasks_id_values["nas_upgrade"])
                    else:
                        req_line_tasks.append(tasks_id_values["nas_upgrade_test"])
            elif (eos_items[key]['cluster_type'] == u'vcs'):
                if eos_items[key]['itemstatus'] == u'prom':
                    req_line_tasks.append(tasks_id_values["hpux_cluster"])
                else:
                    req_line_tasks.append(tasks_id_values["hpux_cluster_test"])
            else:
                if eos_items[key]['itemstatus'] == u'prom':
                    req_line_tasks.append(tasks_id_values["hpux_standalone"])
                else:
                    req_line_tasks.append(tasks_id_values["hpux_standalone_test"])
        else:
            if (eos_items[key]['itemtype1'] == u'dp'):
                if eos_items[key]['itemstatus'] == u'prom':
                    req_line_tasks.append(tasks_id_values["datapower"])
                else:
                    req_line_tasks.append(tasks_id_values["datapower_test"])
            elif (eos_items[key]['itemtype1'] == u'lb'):
                if eos_items[key]['itemstatus'] == u'prom':
                    req_line_tasks.append(tasks_id_values["loadbalancer"])
                else:
                    req_line_tasks.append(tasks_id_values["loadbalancer_test"])

        if (eos_items[key]['db_type'] <> '---'):
            if eos_items[key]['db_type'] == 'mssql':
                req_line_tasks.append(tasks_id_values["mssql"])
            elif eos_items[key]['db_type'] == 'db2':
                if (eos_items[key]['cluster_type'] == u'vcs'):
                    req_line_tasks.append(tasks_id_values["db2_cluster"])
                else:
                    req_line_tasks.append(tasks_id_values["db2_standalone"])
            elif eos_items[key]['db_type'] == 'oracle':
                if (eos_items[key]['cluster_type'] == u'vcs'):
                    req_line_tasks.append(tasks_id_values["oracle_cluster"])
                else:
                    req_line_tasks.append(tasks_id_values["oracle_standalone"])

        if (eos_items[key]['app_type'] <> '---'):
            if eos_items[key]['app_type'] == 'was':
                if (eos_items[key]['cluster_type'] == u'app'):
                    req_line_tasks.append(tasks_id_values["was_cluster"])
                else:
                    req_line_tasks.append(tasks_id_values["was_standalone"])
            if eos_items[key]['app_type'] == 'mb':
                if (eos_items[key]['cluster_type'] == u'app'):
                    req_line_tasks.append(tasks_id_values["wmb_cluster"])
                else:
                    req_line_tasks.append(tasks_id_values["wmb_standalone"])
            if eos_items[key]['app_type'] == 'wls':
                if (eos_items[key]['cluster_type'] == u'app'):
                    req_line_tasks.append(tasks_id_values["wls_cluster"])
                else:
                    req_line_tasks.append(tasks_id_values["wls_standalone"])
            if eos_items[key]['app_type'] == 'mq':
                if (eos_items[key]['cluster_type'] == u'app'):
                    req_line_tasks.append(tasks_id_values["mq_cluster"])
                else:
                    req_line_tasks.append(tasks_id_values["mq_standalone"])
            if eos_items[key]['app_type'] == 'sybase_as':
                if (eos_items[key]['cluster_type'] == u'app'):
                    req_line_tasks.append(tasks_id_values["sybase_cluster"])
                else:
                    req_line_tasks.append(tasks_id_values["sybase_standalone"])
            if eos_items[key]['app_type'] == 'iis':
                req_line_tasks.append(tasks_id_values["iis"])
            if eos_items[key]['app_type'] == 'prpc':
                req_line_tasks.append(tasks_id_values["prpc"])
            if eos_items[key]['app_type'] == 'ad':
                req_line_tasks.append(tasks_id_values["ad"])
            if eos_items[key]['app_type'] == 'dns':
                req_line_tasks.append(tasks_id_values["dns"])
            if eos_items[key]['app_type'] == 'sudir':
                req_line_tasks.append(tasks_id_values["sudir"])
        if eos_items[key]['itemtype1'] == 'term':
            req_line_tasks.append(tasks_id_values["citrix"])

                #        print req_line_tasks
#        print eos_items[key]
        for i in range(int(eos_items[key]['item_count'])):
            task_details = unicode(ru_vals[eos_items[key]['itemtype1']])
            project_tasks[eos_items[key]['itemstatus']].append({'task_details' : task_details,'tasks' : req_line_tasks})
#            block_id = None
#            for task in req_line_tasks:
#                task_details = unicode(ru_vals[eos_items[key]['itemtype1']]) + u' CPU/RAM/SAN : ' + \
#                               str(eos_items[key]['cpu_count']) + u"/" + str(eos_items[key]['ram_count']) + u"/" + \
#                               str(eos_items[key]['san_count'])
#                block_id = techporject.add_task(taskid=task, linked_with_block=block_id,
#                    task_additional_name = task_details)
#    print project_tasks
    for key in project_tasks:
        if project_tasks[key]:
            techporject.add_summary_task(name=project_id + "_" + ru_vals_4project[key])
            for req_line_tasks in project_tasks[key]:
                block_id = None
                for task in req_line_tasks['tasks']:
#                    print task
    #            task_details = unicode(ru_vals[eos_items[key]['itemtype1']]) + u' CPU/RAM/SAN : ' + \
    #                           str(eos_items[key]['cpu_count']) + u"/" + str(eos_items[key]['ram_count']) + u"/" + \
    #                           str(eos_items[key]['san_count'])
                    block_id = techporject.add_task(taskid=task, linked_with_block=block_id,
                        task_additional_name = req_line_tasks['task_details'])
    techporject.export_project_xml()

    return filename