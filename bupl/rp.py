# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from time import strftime
from models import TasksBaseTable

class ProjectPlan:
    def __init__(self, project_number, project_filename):
        """
        __init__ class constructor
        Following class attributes initialized in __init__:
        """
        self.task_attr = [
            'UID',
            'ID',
            'Name',
            'Active',
            'Manual',
            'Type',
            'IsNull',
            'CreateDate',
            'WBS',
            'OutlineNumber',
            'OutlineLevel',
            'Priority',
            'Start',
            'Duration',
            'ManualStart',
            'ManualDuration',
            'DurationFormat',
            'Work',
            'ResumeValid',
            'EffortDriven',
            'Recurring',
            'OverAllocated',
            'Estimated',
            'Milestone',
            'Summary',
            'DisplayAsSummary',
            'Critical',
            'IsSubproject',
            'IsSubprojectReadOnly',
            'ExternalTask',
            'EarlyStart',
            'LateStart',
            'StartVariance',
            'FinishVariance',
            'WorkVariance',
            'FreeSlack',
            'TotalSlack',
            'StartSlack',
            'FinishSlack',
            'FixedCost',
            'FixedCostAccrual',
            'PercentComplete',
            'PercentWorkComplete',
            'Cost',
            'OvertimeCost',
            'OvertimeWork',
            'ActualDuration',
            'ActualCost',
            'ActualOvertimeCost',
            'ActualWork',
            'ActualOvertimeWork',
            'RegularWork',
            'RemainingDuration',
            'RemainingCost',
            'RemainingWork',
            'RemainingOvertimeCost',
            'RemainingOvertimeWork',
            'ACWP',
            'CV',
            'ConstraintType',
            'CalendarUID',
            'LevelAssignments',
            'LevelingCanSplit',
            'LevelingDelay',
            'LevelingDelayFormat',
            'IgnoreResourceCalendar',
            'HideBar',
            'Rollup',
            'BCWS',
            'BCWP',
            'PhysicalPercentComplete',
            'EarnedValueMethod',
            'IsPublished',
            'CommitmentType',
        ]
        self.current_task_id = 1
        self.tasks = None
        self.project_number = project_number
#        self.project_reqs = project_reqs
        self.xml_root = ET.Element("Project")
        self.project_filename = project_filename
        self.current_block_id = 0
        self.block_structure = {}


        #
        #   Standart hedaer for all projects
        #

        self.save_version = ET.SubElement(self.xml_root, "SaveVersion")
        self.save_version.text = u"14"
        self.name = ET.SubElement(self.xml_root, "Name")
        self.name.text = self.project_filename
        self.title = ET.SubElement(self.xml_root, "Title")
        self.title.text = u"Проект №"+self.project_number
        self.company = ET.SubElement(self.xml_root, "Company")
        self.title.text = u"Сбербанк России"
        self.author =  ET.SubElement(self.xml_root, "Author")
        self.author.text =  u"EOS Calculator"
        self.schedulefromstart = ET.SubElement(self.xml_root, "ScheduleFromStart")
        self.schedulefromstart.text = u"1"
        self.startdate = ET.SubElement(self.xml_root,"StartDate")
        self.startdate.text = strftime("20%y-%m-%dT%00:00:00")
        self.fystartdate = ET.SubElement(self.xml_root, "FYStartDate")
        self.fystartdate.text = u"1"
        self.criticalslacklimit = ET.SubElement(self.xml_root, "CriticalSlackLimit")
        self.criticalslacklimit.text = u"0"
        self.currencydigits = ET.SubElement(self.xml_root, "CurrencyDigits")
        self.currencydigits = u"2"
        self.currencysymbol = ET.SubElement(self.xml_root, "CurrencySymbol")
        self.currencysymbol = u"р."
        self.currencycode = ET.SubElement(self.xml_root, "CurrencyCode")
        self.currencycode.text = u"RUB"
        self.currencysymbolposition = ET.SubElement(self.xml_root, "CurrencySymbolPosition")
        self.currencysymbolposition.text = u"1"
        self.calendaruid = ET.SubElement(self.xml_root, "CalendarUID")
        self.calendaruid.text = u"1"
        self.defaultstarttime = ET.SubElement(self.xml_root, "DefaultStartTime")
        self.defaultstarttime.text = u"09:00:00"
        self.defaultfinishtime = ET.SubElement(self.xml_root, "DefaultFinishTime")
        self.defaultfinishtime.text = u"18:00:00"
        self.minutesperday = ET.SubElement(self.xml_root, "MinutesPerDay")
        self.minutesperday.text = u"480"
        self.minutesperweek = ET.SubElement(self.xml_root, "MinutesPerWeek")
        self.minutesperweek.text = u"2400"
        self.dayspermonth = ET.SubElement(self.xml_root, "DaysPerMonth")
        self.dayspermonth.text = u"20"
        self.defaulttasktype = ET.SubElement(self.xml_root, "DefaultTaskType")
        self.defaulttasktype.text = u"0"
        self.defaultfixedcostaccrual = ET.SubElement(self.xml_root, "DefaultFixedCostAccrual")
        self.defaultfixedcostaccrual.text = u"3"

        self.defaultstandardrate = ET.SubElement(self.xml_root, "DefaultStandardRate")
        self.defaultstandardrate.text = u"0"
        self.defaultovertimerate = ET.SubElement(self.xml_root, "DefaultOvertimeRate")
        self.defaultovertimerate.text = u"0"
        self.durationformat = ET.SubElement(self.xml_root, "DurationFormat")
        self.durationformat.text = u"5"
        self.workformat = ET.SubElement(self.xml_root, "WorkFormat")
        self.workformat.text = u"2"
        self.editableactualcosts = ET.SubElement(self.xml_root, "EditableActualCosts")
        self.editableactualcosts.text = u"0"
        self.honorconstraints = ET.SubElement(self.xml_root, "HonorConstraints")
        self.honorconstraints.text = u"0"
        self.insertedprojectslikesummary = ET.SubElement(self.xml_root, "InsertedProjectsLikeSummary")
        self.insertedprojectslikesummary.text = u"1"
        self.multiplecriticalpaths = ET.SubElement(self.xml_root, "MultipleCriticalPaths")
        self.multiplecriticalpaths.text = u"0"
        self.newtaskseffortdriven = ET.SubElement(self.xml_root, "NewTasksEffortDriven")
        self.newtaskseffortdriven.text = u"0"
        self.newtasksestimated = ET.SubElement(self.xml_root, "NewTasksEstimated")
        self.newtasksestimated.text = u"1"
        self.splitsinprogresstasks = ET.SubElement(self.xml_root, "SplitsInProgressTasks")
        self.splitsinprogresstasks.text = u"1"
        self.spreadactualcost = ET.SubElement(self.xml_root, "SpreadActualCost")
        self.spreadactualcost.text = u"0"
        self.spreadpercentcomplete = ET.SubElement(self.xml_root, "SpreadPercentComplete")
        self.spreadpercentcomplete.text = u"0"
        self.taskupdatesresource = ET.SubElement(self.xml_root, "TaskUpdatesResource")
        self.taskupdatesresource.text = u"1"
        self.fiscalyearstart = ET.SubElement(self.xml_root, "FiscalYearStart")
        self.fiscalyearstart.text = u"0"
        self.weekstartday = ET.SubElement(self.xml_root, "WeekStartDay")
        self.weekstartday.text = u"1"
        self.movecompletedendsback = ET.SubElement(self.xml_root, "MoveCompletedEndsBack")
        self.movecompletedendsback.text = u"0"
        self.moveremainingstartsback = ET.SubElement(self.xml_root, "MoveRemainingStartsBack")
        self.moveremainingstartsback.text = u"0"
        self.moveremainingstartsforward = ET.SubElement(self.xml_root, "MoveRemainingStartsForward")
        self.moveremainingstartsforward.text = u"0"
        self.movecompletedendsforward = ET.SubElement(self.xml_root, "MoveCompletedEndsForward")
        self.movecompletedendsforward.text = u"0"
        self.baselineforearnedvalue = ET.SubElement(self.xml_root, "BaselineForEarnedValue")
        self.baselineforearnedvalue.text = u"0"
        self.autoaddnewresourcesandtasks = ET.SubElement(self.xml_root, "AutoAddNewResourcesAndTasks")
        self.autoaddnewresourcesandtasks.text = u"1"
        self.currentdate = ET.SubElement(self.xml_root, "CurrentDate")
        self.currentdate.text = strftime("20%y-%m-%dT%00:00:00")
        self.microsoftprojectserverurl = ET.SubElement(self.xml_root, "MicrosoftProjectServerURL")
        self.microsoftprojectserverurl.text = u"1"
        self.autolink = ET.SubElement(self.xml_root, "Autolink")
        self.autolink.text = u"0"
        self.newtaskstartdate = ET.SubElement(self.xml_root, "NewTaskStartDate")
        self.newtaskstartdate.text = u"0"
        self.newtasksaremanual = ET.SubElement(self.xml_root, "NewTasksAreManual")
        self.newtasksaremanual.text = u"0"
        self.defaulttaskevmethod = ET.SubElement(self.xml_root, "DefaultTaskEVMethod")
        self.defaulttaskevmethod.text = u"0"
        self.projectexternallyedited = ET.SubElement(self.xml_root, "ProjectExternallyEdited")
        self.projectexternallyedited.text = u"0"
        self.extendedcreationdate = ET.SubElement(self.xml_root, "ExtendedCreationDate")
        self.extendedcreationdate.text = u"1984-01-01T00:00:00"
        self.actualsinsync = ET.SubElement(self.xml_root, "ActualsInSync")
        self.actualsinsync.text = u"1"
        self.removefileproperties = ET.SubElement(self.xml_root, "RemoveFileProperties")
        self.removefileproperties.text = u"0"
        self.adminproject = ET.SubElement(self.xml_root, "AdminProject")
        self.adminproject.text = u"0"
        self.updatemanuallyscheduledtaskswheneditinglinks = ET.SubElement(self.xml_root,
            "UpdateManuallyScheduledTasksWhenEditingLinks")
        self.updatemanuallyscheduledtaskswheneditinglinks.text = u"1"
        self.keeptaskonnearestworkingtimewhenmadeautoscheduled = ET.SubElement(self.xml_root,
            "KeepTaskOnNearestWorkingTimeWhenMadeAutoScheduled")
        self.keeptaskonnearestworkingtimewhenmadeautoscheduled.text = u"0"

    def add_extednded_attrs(self):

        ExtendedAttrs = [{"FieldID" : u"188743747",
                        "FieldName" : u"Текст7",
                        "Alias" : u"Направление",
                        "Guid" : u"000039B7-8BBE-4CEB-82C4-FA8C0B400043",
                        "SecondaryPID" : u"255869034",
                        "SecondaryGuid" : u"000039B7-8BBE-4CEB-82C4-FA8C0F40406A",
                        },
                         {"FieldID" : u"188743748",
                          "FieldName" : u"Текст8",
                          "Alias" : u"Отдел",
                          "Guid" : u"000039B7-8BBE-4CEB-82C4-FA8C0B400044",
                          "SecondaryPID" : u"255869035",
                          "SecondaryGuid" : u"000039B7-8BBE-4CEB-82C4-FA8C0F40406B",
                          },
                         {"FieldID" : u"188743749",
                          "FieldName" : u"Текст9",
                          "Alias" : u"Согласование",
                          "Guid" : u"000039B7-8BBE-4CEB-82C4-FA8C0B400045",
                          "SecondaryPID" : u"255869036",
                          "SecondaryGuid" : u"000039B7-8BBE-4CEB-82C4-FA8C0F40406C",
                          },
        ]
        self.extendedattributes = ET.SubElement(self.xml_root, "ExtendedAttributes")
        for ea in ExtendedAttrs:
            self.extendedattribute = ET.SubElement(self.extendedattributes, "ExtendedAttribute")
            self.ea_fieldid = ET.SubElement(self.extendedattribute, "FieldID")
            self.ea_fieldid.text = ea['FieldID']
            self.ea_fieldname = ET.SubElement(self.extendedattribute, "FieldName")
            self.ea_fieldname.text = ea['FieldName']
            self.ea_alias = ET.SubElement(self.extendedattribute, "Alias")
            self.ea_alias.text = ea['Alias']
            self.ea_guid = ET.SubElement(self.extendedattribute, "Guid")
            self.ea_guid.text = ea['Guid']
            self.ea_secondarypid = ET.SubElement(self.extendedattribute, "SecondaryPID")
            self.ea_secondarypid.text = ea['SecondaryPID']
            self.ea_secondaryguid = ET.SubElement(self.extendedattribute, "SecondaryGuid")
            self.ea_secondaryguid.text = ea['SecondaryGuid']

    def add_calendar(self):
        self.calendars = ET.SubElement(self.xml_root, "Calendars")
        self.calendar = ET.SubElement(self.calendars, "Calendar")
        self.cal_uid = ET.SubElement(self.calendar, "UID")
        self.cal_uid.text = u"1"
        self.cal_name = ET.SubElement(self.calendar, "Name")
        self.cal_name.text = u"Стандартный"
        self.cal_isbasecalendar = ET.SubElement(self.calendar, "IsBaseCalendar")
        self.cal_isbasecalendar.text = u"1"
        self.cal_isbaselinecalendar = ET.SubElement(self.calendar, "IsBaselineCalendar")
        self.cal_isbaselinecalendar.text = u"0"
        self.cal_basecalendaruid = ET.SubElement(self.calendar, "BaseCalendarUID")
        self.cal_basecalendaruid.text = u"0"
        self.weekdays = ET.SubElement(self.calendar, "WeekDays")
        for i in range(1, 8):
            self.weekday = ET.SubElement(self.weekdays, "WeekDay")
            if i in [1,7]:
                self.daytype = ET.SubElement(self.weekday, "DayType")
                self.daytype.text = str(i)
                self.dayworking = ET.SubElement(self.weekday, "DayWorking")
                self.dayworking.text = u"0"
            else:
                self.daytype = ET.SubElement(self.weekday, "DayType")
                self.daytype.text = str(i)
                self.dayworking = ET.SubElement(self.weekday, "DayWorking")
                self.dayworking.text = u"1"
                self.workingtimes = ET.SubElement(self.weekday, "WorkingTimes")
                self.workingtime_1 = ET.SubElement(self.workingtimes, "WorkingTime")
                self.fromtime_1 = ET.SubElement(self.workingtime_1, "FromTime")
                self.fromtime_1.text = u"09:00:00"
                self.totime_1 = ET.SubElement(self.workingtime_1, "ToTime")
                self.totime_1.text = u"13:00:00"
                self.workingtime_2 = ET.SubElement(self.workingtimes, "WorkingTime")
                self.fromtime_2 = ET.SubElement(self.workingtime_2, "FromTime")
                self.fromtime_2.text = u"14:00:00"
                self.totime_2 = ET.SubElement(self.workingtime_2, "ToTime")
                self.totime_2.text = u"18:00:00"

    def add_task(self, taskid, linked_with_block = None, link_type = 1):
        TASKS = []
        if not self.tasks:
            self.tasks = ET.SubElement(self.xml_root, "Tasks")
        summary_task = TasksBaseTable.objects.get(WBS=taskid)
        tasks = TasksBaseTable.objects.filter(WBS__contains=taskid+'.').order_by('Task_ID')
        TASKS.append(summary_task.__dict__)
        summary_task_id = self.current_task_id
        for task in tasks:
            TASKS.append(task.__dict__)
        for task in TASKS:
            current_task = ET.SubElement(self.tasks, "Task")
            task_uid = ET.SubElement(current_task, "UID")
            task_id = ET.SubElement(current_task, "ID")
            task_uid.text = str(self.current_task_id)
            task_id.text = str(self.current_task_id)
            for subtask in TASKS:
                if ('PredecessorUID' in subtask) and subtask['PredecessorUID']:
                    if int(subtask['PredecessorUID']) == int(task['Task_ID']):
                        subtask['PredecessorUID'] = str(self.current_task_id)
            self.current_task_id += 1

            for attr in self.task_attr:
                if attr in task.keys():
                    current_attr = ET.SubElement(current_task, attr)
                    current_attr.text = unicode(task[attr])
                elif attr == 'CreateDate':
                    create_date = ET.SubElement(current_task, "CreateDate")
                    create_date.text = strftime("20%y-%m-%dT%00:00:00")
                elif attr == 'Start':
                    start = ET.SubElement(current_task, "Start")
                    start.text = strftime("20%y-%m-%dT%00:00:00")
                elif attr == 'CalendarUID':
                    calendar_uid = ET.SubElement(current_task, "CalendarUID")
                    calendar_uid.text = "1"

            if ('PredecessorUID' in task) and task['PredecessorUID']:
                prelink = ET.SubElement(current_task, "PredecessorLink")
                for key in ['PredecessorUID', 'Predecessor_Type', 'CrossProject', 'LinkLag', 'LagFormat']:
                    if key == 'Predecessor_Type':
                        link_attr = ET.SubElement(prelink, "Type")
                    else:
                        link_attr = ET.SubElement(prelink, key)
                    link_attr.text = task[key]
            elif (task['Summary'] == '1'):
                if linked_with_block:
                    prelink = ET.SubElement(current_task, "PredecessorLink")
                    preuid = ET.SubElement(prelink, 'PredecessorUID')
                    preuid.text = self.block_structure['block_task_uid_'+str(linked_with_block)]
                    pretype = ET.SubElement(prelink, "Type")
                    if link_type:
                        pretype.text = str(link_type)
                    precross = ET.SubElement(prelink, "CrossProject")
                    precross.text = '0'
                    prelag = ET.SubElement(prelink, "LinkLag")
                    prelag.text = '0'
                    prelagformat = ET.SubElement(prelink, "LagFormat")
                    prelagformat.text = '5'

            if ('EA_FieldID1' in task) and task['EA_FieldID1']:
                extended_attr = ET.SubElement(current_task, "ExtendedAttribute")
                extended_attrname = ET.SubElement(extended_attr, "FieldID")
                extended_attrname.text = task['EA_FieldID1']
                extended_value = ET.SubElement(extended_attr, "Value")
                extended_value.text = task['EA_Value1']
            if ('EA_FieldID2' in task) and task['EA_FieldID2']:
                extended_attr = ET.SubElement(current_task, "ExtendedAttribute")
                extended_attrname = ET.SubElement(extended_attr, "FieldID")
                extended_attrname.text = task['EA_FieldID2']
                extended_value = ET.SubElement(extended_attr, "Value")
                extended_value.text = task['EA_Value2']
            if ('EA_FieldID3' in task) and task['EA_FieldID3']:
                extended_attr = ET.SubElement(current_task, "ExtendedAttribute")
                extended_attrname = ET.SubElement(extended_attr, "FieldID")
                extended_attrname.text = task['EA_FieldID3']
                extended_value = ET.SubElement(extended_attr, "Value")
                extended_value.text = task['EA_Value3']
            if ('EA_FieldID4' in task) and task['EA_FieldID4']:
                extended_attr = ET.SubElement(current_task, "ExtendedAttribute")
                extended_attrname = ET.SubElement(extended_attr, "FieldID")
                extended_attrname.text = task['EA_FieldID4']
                extended_value = ET.SubElement(extended_attr, "Value")
                extended_value.text = task['EA_Value4']
            if ('EA_FieldID5' in task) and task['EA_FieldID5']:
                extended_attr = ET.SubElement(current_task, "ExtendedAttribute")
                extended_attrname = ET.SubElement(extended_attr, "FieldID")
                extended_attrname.text = task['EA_FieldID5']
                extended_value = ET.SubElement(extended_attr, "Value")
                extended_value.text = task['EA_Value5']

        self.current_block_id += 1
        self.block_structure.update({'block_task_uid_'+str(self.current_block_id) : str(summary_task_id)})

    def export_project_xml(self):
        tree = ET.ElementTree(self.xml_root)
        tree.write(self.project_filename)
        #        tree.write("/Users/vs/tmp/filename.xml")


if __name__ == "__main__":
    testproject = ProjectPlan("123456", [], "/Users/vs/tmp/filename.xml")
    testproject.add_extednded_attrs()
    testproject.add_calendar()
    testproject.export_project_xml()



#python manage.py shell
#from bupl.respl import ProjectPlan
#k = ProjectPlan("123456", [], "/Users/vs/tmp/filename.xml")
#k.add_task('1.2.1.')
#print k


#root = ET.Element("Project")
#
#tasks = ET.SubElement(root, "Tasks")
#
#SaveVersion = ET.SubElement(root, "SaveVersion")
#SaveVersion.set("name", "blah")
#SaveVersion.text = "12"
#
#uid = ET.SubElement(tasks, "UID")
#field2.set("name", "asdfasd")
#uid.text = "123"
#
#tree = ET.ElementTree(root)
#tree.write("/Users/vs/tmp/filename.xml")