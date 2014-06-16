# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from time import strftime
from models import TasksBaseTable
import datetime

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
            'Finish',
            'Duration',
            'ManualStart',
            'ManualFinish',
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
            'EarlyFinish',
            'LateStart',
            'LateFinish',
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
        if datetime.datetime.today().weekday() not in [5,6]:
            self.project_startdate = datetime.datetime.today()
        else:
            self.project_startdate = datetime.datetime.today() + \
                                     datetime.timedelta(days = (7-datetime.datetime.today().weekday())
)
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
        self.company.text = u"Сбербанк России"
        self.author =  ET.SubElement(self.xml_root, "Author")
        self.author.text =  u"EOS Calculator"
        self.schedulefromstart = ET.SubElement(self.xml_root, "ScheduleFromStart")
        self.schedulefromstart.text = u"1"
        self.startdate = ET.SubElement(self.xml_root,"StartDate")
        self.startdate.text = self.project_startdate.strftime("20%y-%m-%dT00:00:00")
#        strftime("20%y-%m-%dT00:00:00")
        self.fystartdate = ET.SubElement(self.xml_root, "FYStartDate")
        self.fystartdate.text = u"1"
        self.criticalslacklimit = ET.SubElement(self.xml_root, "CriticalSlackLimit")
        self.criticalslacklimit.text = u"0"
        self.currencydigits = ET.SubElement(self.xml_root, "CurrencyDigits")
        self.currencydigits.text = u"2"
        self.currencysymbol = ET.SubElement(self.xml_root, "CurrencySymbol")
        self.currencysymbol.text = u"р."
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
        self.currentdate.text = strftime("20%y-%m-%dT08:00:00")
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
        self.cal_basecalendaruid.text = u"-1"
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

    def add_summary_task(self, name):
        if not self.tasks:
            self.tasks = ET.SubElement(self.xml_root, "Tasks")
        summary_task = ET.SubElement(self.tasks, "Task")
        task_uid = ET.SubElement(summary_task, "UID")
        task_id = ET.SubElement(summary_task, "ID")
        task_uid.text = str(self.current_task_id)
        task_id.text = str(self.current_task_id)
        self.current_task_id += 1
        task_name = ET.SubElement(summary_task, "Name")
        task_name.text = name
        task_active = ET.SubElement(summary_task, "Active")
        task_active.text = u'1'
        task_manual = ET.SubElement(summary_task, "Manual")
        task_manual.text = u'0'
        task_active = ET.SubElement(summary_task, "Active")
        task_active.text = u'0'
        task_type = ET.SubElement(summary_task, "Type")
        task_type.text = u'1'
        task_isnull = ET.SubElement(summary_task, "IsNull")
        task_isnull.text = u'0'
        create_date = ET.SubElement(summary_task, "CreateDate")
        create_date.text = strftime("20%y-%m-%dT00:00:00")
        task_wbs = ET.SubElement(summary_task, "WBS")
        task_wbs.text = u'1'
        task_outline = ET.SubElement(summary_task, "OutlineNumber")
        task_outline.text = u'1'
        task_outlinelevel = ET.SubElement(summary_task, "OutlineLevel")
        task_outlinelevel.text = u'1'
        task_priority = ET.SubElement(summary_task, "Priority")
        task_priority.text = u'500'
#        elif (attr in ['Start', 'ManualStart', 'EarlyStart', 'LateStart']):
        start = ET.SubElement(summary_task, "Start")
        start.text = self.project_startdate.strftime("20%y-%m-%dT09:00:00")
        manual_start = ET.SubElement(summary_task, "ManualStart")
        manual_start.text = self.project_startdate.strftime("20%y-%m-%dT09:00:00")
        task_durationformat = ET.SubElement(summary_task, "DurationFormat")
        task_durationformat.text = u'21'
        task_work = ET.SubElement(summary_task, "Work")
        task_work.text = u'PT0H0M0S'
        task_resumevalid = ET.SubElement(summary_task, "ResumeValid")
        task_resumevalid.text = u'0'
        task_effortdriven = ET.SubElement(summary_task, "EffortDriven")
        task_effortdriven.text = u'0'
        task_recurring = ET.SubElement(summary_task, "Recurring")
        task_recurring.text = u'0'
        task_overallocated = ET.SubElement(summary_task, "OverAllocated")
        task_overallocated.text = u'0'
        task_estimated = ET.SubElement(summary_task, "Estimated")
        task_estimated.text = u'0'
        task_milestone = ET.SubElement(summary_task, "Milestone")
        task_milestone.text = u'0'
        task_summary = ET.SubElement(summary_task, "Summary")
        task_summary.text = u'1'
        task_displayassummary = ET.SubElement(summary_task, "DisplayAsSummary")
        task_displayassummary.text = u'0'
        task_critical = ET.SubElement(summary_task, "Critical")
        task_critical.text = u'1'
        task_issubproject = ET.SubElement(summary_task, "IsSubproject")
        task_issubproject.text = u'0'
        task_issubprojectreadonly = ET.SubElement(summary_task, "IsSubprojectReadOnly")
        task_issubprojectreadonly.text = u'0'
        task_externaltask = ET.SubElement(summary_task, "ExternalTask")
        task_externaltask.text = u'0'
        task_earlystart = ET.SubElement(summary_task, "EarlyStart")
        task_earlystart.text = self.project_startdate.strftime("20%y-%m-%dT09:00:00")
#        task_earlyfinish = ET.SubElement(summary_task, "EarlyFinish")
#        task_earlyfinish.text = u'2014-06-16T12:00:00'
        task_latestart = ET.SubElement(summary_task, "LateStart")
        task_latestart.text = self.project_startdate.strftime("20%y-%m-%dT09:00:00")
#        task_latefinish = ET.SubElement(summary_task, "LateFinish")
#        task_latefinish.text = u'2014-06-16T12:00:00'
        task_startvariance = ET.SubElement(summary_task, "StartVariance")
        task_startvariance.text = u'0'
        task_finishvariance = ET.SubElement(summary_task, "FinishVariance")
        task_finishvariance.text = u'0'
        task_workvariance = ET.SubElement(summary_task, "WorkVariance")
        task_workvariance.text = u'0.00'
        task_freeslack = ET.SubElement(summary_task, "FreeSlack")
        task_freeslack.text = u'0'
        task_totalslack = ET.SubElement(summary_task, "TotalSlack")
        task_totalslack.text = u'0'
        task_startslack = ET.SubElement(summary_task, "StartSlack")
        task_startslack.text = u'0'
        task_finishslack = ET.SubElement(summary_task, "FinishSlack")
        task_finishslack.text = u'0'
        task_fixedcost = ET.SubElement(summary_task, "FixedCost")
        task_fixedcost.text = u'0'
        task_fixedcostaccrual = ET.SubElement(summary_task, "FixedCostAccrual")
        task_fixedcostaccrual.text = u'3'
        task_percentcomplete = ET.SubElement(summary_task, "PercentComplete")
        task_percentcomplete.text = u'0'
        task_percentworkcomplete = ET.SubElement(summary_task, "PercentWorkComplete")
        task_percentworkcomplete.text = u'0'
        task_cost = ET.SubElement(summary_task, "Cost")
        task_cost.text = u'0'
        task_overtimecost = ET.SubElement(summary_task, "OvertimeCost")
        task_overtimecost.text = u'0'
        task_overtimework = ET.SubElement(summary_task, "OvertimeWork")
        task_overtimework.text = u'PT0H0M0S'
        task_actualduration = ET.SubElement(summary_task, "ActualDuration")
        task_actualduration.text = u'PT0H0M0S'
        task_actualcost = ET.SubElement(summary_task, "ActualCost")
        task_actualcost.text = u'0'
        task_actualovertimecost = ET.SubElement(summary_task, "ActualOvertimeCost")
        task_actualovertimecost.text = u'0'
        task_actualwork = ET.SubElement(summary_task, "ActualWork")
        task_actualwork.text = u'PT0H0M0S'
        task_actualovertimework = ET.SubElement(summary_task, "ActualOvertimeWork")
        task_actualovertimework.text = u'PT0H0M0S'
        task_regularwork = ET.SubElement(summary_task, "RegularWork")
        task_regularwork.text = u'PT0H0M0S'
        task_remainingduration = ET.SubElement(summary_task, "RemainingDuration")
        task_remainingduration.text = u'PT3H0M0S'
        task_remainingcost = ET.SubElement(summary_task, "RemainingCost")
        task_remainingcost.text = u'0'
        task_remainingwork = ET.SubElement(summary_task, "RemainingWork")
        task_remainingwork.text = u'PT0H0M0S'
        task_remainingovertimecost = ET.SubElement(summary_task, "RemainingOvertimeCost")
        task_remainingovertimecost.text = u'0'
        task_remainingovertimework = ET.SubElement(summary_task, "RemainingOvertimeWork")
        task_remainingovertimework.text = u'PT0H0M0S'
        task_acwp = ET.SubElement(summary_task, "ACWP")
        task_acwp.text = u'0.00'
        task_cv = ET.SubElement(summary_task, "CV")
        task_cv.text = u'0.00'
        task_constrainttype = ET.SubElement(summary_task, "ConstraintType")
        task_constrainttype.text = u'0'
        task_calendaruid = ET.SubElement(summary_task, "CalendarUID")
        task_calendaruid.text = u'-1'
        task_levelassignments = ET.SubElement(summary_task, "LevelAssignments")
        task_levelassignments.text = u'1'
        task_levelingcansplit = ET.SubElement(summary_task, "LevelingCanSplit")
        task_levelingcansplit.text = u'1'
        task_levelingdelay = ET.SubElement(summary_task, "LevelingDelay")
        task_levelingdelay.text = u'0'
        task_levelingdelayformat = ET.SubElement(summary_task, "LevelingDelayFormat")
        task_levelingdelayformat.text = u'8'
        task_ignoreresourcecalendar = ET.SubElement(summary_task, "IgnoreResourceCalendar")
        task_ignoreresourcecalendar.text = u'0'
        task_hidebar = ET.SubElement(summary_task, "HideBar")
        task_hidebar.text = u'0'
        task_rollup = ET.SubElement(summary_task, "Rollup")
        task_rollup.text = u'1'
        task_bcws = ET.SubElement(summary_task, "BCWS")
        task_bcws.text = u'0.00'
        task_bcwp = ET.SubElement(summary_task, "BCWP")
        task_bcwp.text = u'0.00'
        task_physicalpercentcomplete = ET.SubElement(summary_task, "PhysicalPercentComplete")
        task_physicalpercentcomplete.text = u'0'
        task_earnedvaluemethod = ET.SubElement(summary_task, "EarnedValueMethod")
        task_earnedvaluemethod.text = u'0'
        task_ispublished = ET.SubElement(summary_task, "IsPublished")
        task_ispublished.text = u'0'
        task_commitmenttype = ET.SubElement(summary_task, "CommitmentType")
        task_commitmenttype.text = u'0'



    def add_task(self, taskid, linked_with_block = None, link_type = 1, task_additional_name = None):
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
                    if (attr == 'Name') and (task['Summary'] == u'1'):
                        current_attr = ET.SubElement(current_task, attr)
                        current_attr.text = unicode(task[attr] + u" (" + unicode(task_additional_name) + u")")
                    else:
                        current_attr = ET.SubElement(current_task, attr)
                        current_attr.text = unicode(task[attr])
                elif attr == 'CreateDate':
                    create_date = ET.SubElement(current_task, "CreateDate")
                    create_date.text = strftime("20%y-%m-%dT00:00:00")
                elif (attr in ['Start', 'ManualStart', 'EarlyStart', 'LateStart']):
                    start = ET.SubElement(current_task, attr)
                    start.text = self.project_startdate.strftime("20%y-%m-%dT09:00:00")
#                    strftime("20%y-%m-%dT09:00:00")
#                elif (attr in ['Finish', 'ManualFinish', 'EarlyFinish', 'LateFinish']):
#                    start_date = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month,
#                        datetime.datetime.today().day, 9, 00, 00)
#                    delta_days = 0
#                    delta_hours = 0
#                    delta_minutes = 0
#                    delta_hours = int(task['Duration'].split('T')[1].split('H')[0])
#                    delta_minutes = int(task['Duration'].split('T')[1].split('H')[1].split('M')[0])
#                    if delta_hours > 8:
#                        delta_days = delta_hours / 8
#                        delta_hours = delta_hours - (8 * delta_days)
#                    finish_date = start_date + datetime.timedelta(days = delta_days, hours = delta_hours,
#                        minutes = delta_minutes)
#                    finish = ET.SubElement(current_task, attr)
#                    finish.text = finish_date.strftime("20%y-%m-%dT%H:%M:%S")
                elif attr == 'CalendarUID':
                    calendar_uid = ET.SubElement(current_task, "CalendarUID")
                    calendar_uid.text = "-1"
#                elif attr == 'ManualDuration':
#                    manual_duration = ET.SubElement(current_task, attr)
#                    manual_duration.text = unicode(task['Duration'])

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
        return self.current_block_id

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