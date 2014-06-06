# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from time import strftime
from models import TasksBaseTable


def load_tasks(filename):

    bad_keys = ['EarlyFinish',
                'Start',
                'Finish',
                'UID',
                'ID',
                'ManualDuration',
                'EarlyStart',
                'LateFinish',
                'CreateDate',
                'CalendarUID',
                'ManualStart',
                'ManualFinish',
                'LateStart',
                'LateFinish',]

    tree = ET.parse(filename)
    root = tree.getroot()
    TASKS = []
    taskid = 1
    for tasks in root.findall("Tasks"):
        for task in tasks:
            TASK = {'Task_ID' : taskid}
            taskid += 1
            i = 0
#            EA = {}
            for task_attr in task:
                if (task_attr.tag == 'PredecessorLink'):
                    for subtask_attr in task_attr:
                        if subtask_attr.tag == 'Type':
                            TASK.update({'Predecessor_'+ subtask_attr.tag : unicode(subtask_attr.text)})
                        else:
                            TASK.update({subtask_attr.tag : unicode(subtask_attr.text)})
#                    TASK.update({'PredecessorLink' : PL})
                elif (task_attr.tag == 'ExtendedAttribute'):
                    i += 1
                    for subtask_attr in task_attr:
                        TASK.update({'EA_'+subtask_attr.tag+str(i) : unicode(subtask_attr.text)})
#                    TASK.update({'ExtendedAttribute' : EA})
                else:
                    TASK.update({task_attr.tag : unicode(task_attr.text)})
            TASKS.append(TASK)
    for task in TASKS:
        if 'PredecessorUID' in task.keys():
            preuid = int(task['PredecessorUID'])
            new_preuid = None
            for subtask in TASKS:
                if int(subtask['UID']) == preuid:
                    new_preuid = subtask['Task_ID']
            if new_preuid:
                task['PredecessorUID'] = str(new_preuid)
    for task in TASKS:
        for key in bad_keys:
            if key in task:
                del task[key]
        TasksBaseTable.objects.create(**task)
    return TASKS

if __name__ == "__main__":
    print load_tasks('/users/vs/dev/webhw/bupl/test2.xml')

#python manage.py shell
#from bupl.tasks_loader import load_tasks
#print load_tasks('/users/vs/dev/webhw/bupl/test2.xml')
