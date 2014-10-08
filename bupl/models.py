# -*- coding: utf-8 -*-

from django.db import models

class Arch(models.Model):
#    id = models.IntegerField(primary_key=True)
    arch_type = models.CharField(max_length=765, blank=True)
    def __unicode__(self):
        return u"%s" % (self.arch_type)
    class Meta:
        db_table = u'Arch'
        verbose_name_plural = "Архитектуры"

class Backup(models.Model):
#    id = models.IntegerField(primary_key=True)
    backup_type = models.CharField(max_length=765, blank=True)
    def __unicode__(self):
        return u"%s" % (self.backup_type)
    class Meta:
        db_table = u'Backup'
        verbose_name_plural = "Резервное копирование"

class Bankingsystem(models.Model):
#    id = models.IntegerField(primary_key=True)
    abs_type = models.CharField(max_length=765, blank=True)
    def __unicode__(self):
        return u"%s" % (self.abs_type)
    class Meta:
        db_table = u'BankingSystem'
        verbose_name_plural = "Автоматизированные системы"

class Cluster(models.Model):
#    id = models.IntegerField(primary_key=True)
    cluster_type = models.CharField(max_length=765, blank=True)
    def __unicode__(self):
        return u"%s" % (self.cluster_type)
    class Meta:
        db_table = u'Cluster'
        verbose_name_plural = "Тип кластеризации"


class Envtype(models.Model):
#    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    env_parent_name = models.CharField(max_length=765, blank=True)
    def __unicode__(self):
        return u"%s" % (self.env_parent_name)
    class Meta:
        db_table = u'EnvType'
        verbose_name_plural = "Тип сред (основной)"

class Env(models.Model):
#    id = models.IntegerField(primary_key=True)
    env_name = models.CharField(max_length=765, blank=True)
    env_short_name = models.CharField(max_length=10, unique=True, blank=True)
    parent_type = models.ForeignKey(Envtype, null=True, db_column='parent_type', blank=True)
    def __unicode__(self):
        return u"%s - %s - %s" % (self.env_type, self.env_short_name, self.parent_type)
    class Meta:
        db_table = u'Env'
        verbose_name_plural = "Тип сред"


class Network(models.Model):
#    id = models.IntegerField(primary_key=True)
    lan_segment = models.CharField(max_length=765, blank=True)
    def __unicode__(self):
        return u"%s" % (self.lan_segment)
    class Meta:
        db_table = u'Network'
        verbose_name_plural = "Сетевые сегменты"


class Projects(models.Model):
#    id = models.IntegerField(primary_key=True)
    priority = models.CharField(max_length=765, blank=True)
    customer = models.CharField(max_length=765, blank=True)
    prj_name = models.CharField(max_length=765, blank=True)
    prj_number = models.FloatField(unique=True, null=True, blank=True)
    manager = models.CharField(max_length=765, blank=True)
    state = models.CharField(max_length=765, blank=True)
    comments = models.CharField(max_length=765, blank=True)
    def __unicode__(self):
        return u"%s - %s - %s - %s - %s - %s - %s" % (self.priority, self.customer, self.prj_name, self.prj_number,
                                                      self.manager, self.state, self.comments)
    class Meta:
        db_table = u'projects'
        verbose_name_plural = "Проекты"

class Dates(models.Model):
#    id = models.ForeignKey(Project, null=True, db_column='id', blank=True)
    env_type = models.ForeignKey(Env, null=True, db_column='env_type', blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    def __unicode__(self):
        return u"%s - %s - %s" % (self.env_type, self.start_date, self.end_date)
    class Meta:
        db_table = u'Dates'
        verbose_name_plural = "Даты готовности сред"


class Role(models.Model):
#    id = models.IntegerField(primary_key=True)
    server_role = models.CharField(max_length=765, blank=True)
    def __unicode__(self):
        return u"%s" % (self.server_role)
    class Meta:
        db_table = u'Role'
        verbose_name_plural = "Роль серверов"

class Prjneeds(models.Model):
#    id = models.IntegerField(primary_key=True)
    prj_number = models.ForeignKey(Projects, null=True, db_column='prj_number', blank=True)
    abs_type = models.ForeignKey(Bankingsystem, null=True, db_column='abs_type', blank=True)
    ent_name = models.ForeignKey(Env, null=True, db_column='ent_name', blank=True)
    item_name = models.CharField(max_length=765, blank=True)
    item_count = models.IntegerField(null=True, blank=True)
    cpu_count = models.IntegerField(null=True, blank=True)
    ram_count = models.IntegerField(null=True, blank=True)
    internal_storage_count = models.IntegerField(null=True, blank=True)
    sna_storage_count = models.IntegerField(null=True, blank=True)
    nas_storage_count = models.IntegerField(null=True, blank=True)
    iops = models.IntegerField(null=True, db_column='IOPS', blank=True) # Field name made lowercase.
    arch_type = models.ForeignKey(Arch, null=True, db_column='arch_type', blank=True)
    item_model = models.CharField(max_length=765, blank=True)
    server_role = models.ForeignKey(Role, null=True, db_column='server_role', blank=True)
    os_version = models.CharField(max_length=765, blank=True)
    app_version = models.CharField(max_length=765, blank=True)
    lan_segment = models.ForeignKey(Network, null=True, db_column='lan_segment', blank=True)
    cluster_type = models.ForeignKey(Cluster, null=True, db_column='cluster_type', blank=True)
    backup_type = models.ForeignKey(Backup, null=True, db_column='backup_type', blank=True)
    lan_ifaces = models.CharField(max_length=765, blank=True)
    existing_server_name = models.CharField(max_length=765, blank=True)
    existing_cpu_count = models.IntegerField(null=True, blank=True)
    existing_ram_count = models.IntegerField(null=True, blank=True)
    existing_sanst_count = models.IntegerField(null=True, blank=True)
    existing_nasstcount = models.IntegerField(null=True, blank=True)
    def __unicode__(self):
        return u"%s - %s" % (self.prj_number, self.item_name)
    class Meta:
        db_table = u'PrjNeeds'
        verbose_name_plural = "Требования по проектам"

class Prices(models.Model):
#    id = models.CharField(max_length=765, primary_key=True)
    hw_class = models.DecimalField(u'Код оборудования', max_digits=14, decimal_places=2)
    hw_type = models.CharField(u'Тип оборудования', max_length=765)
    price = models.DecimalField(u'Стоимость (без НДС, $)', max_digits=65, decimal_places=30)
    dc_rent_price = models.DecimalField(u'Стоимость аренды (без НДС, руб.)', max_digits=65, decimal_places=30)
    dc_book_price = models.DecimalField(u'Стоимость бронирования (без НДС, руб.)', max_digits=65, decimal_places=30)
    dc_startup_price = models.DecimalField(u'Стоимость подключения (без НДС, руб.)', max_digits=65, decimal_places=30)
    hw_full_name = models.CharField(u'Описание', max_length=765)
    class Meta:
        db_table = u'prices'
        verbose_name_plural = u'Цены на типы оборудования'

#class TasksManager(models.Manager):
#    def create_task(self, TASK):
#        task = self.create(Task_ID = )
#        return task

class TasksBaseTable(models.Model):
    Task_ID = models.IntegerField(u'TASK_UNIQUE_ID')
    Name = models.CharField(u'Name', max_length=765)
    Active = models.CharField(u'Active', max_length=2)
    Manual = models.CharField(u'Manual', max_length=2)
    Type = models.CharField(u'Type', max_length=2)
    IsNull = models.CharField(u'IsNull', max_length=2)
    WBS = models.CharField(u'WBS', max_length=15)
    OutlineNumber = models.CharField(u'OutlineNumber', max_length=15)
    OutlineLevel = models.CharField(u'OutlineLevel', max_length=5)
    Priority = models.CharField(u'Priority', max_length=10)
    Duration = models.CharField(u'Duration', max_length=20)
    DurationFormat = models.CharField(u'DurationFormat', max_length=5)
    Work = models.CharField(u'Work', max_length=20)
    ResumeValid = models.CharField(u'ResumeValid', max_length=5)
    EffortDriven = models.CharField(u'EffortDriven', max_length=5)
    Recurring = models.CharField(u'Recurring', max_length=5)
    OverAllocated = models.CharField(u'OverAllocated', max_length=5)
    Estimated = models.CharField(u'Estimated', max_length=5)
    Milestone = models.CharField(u'Milestone', max_length=5)
    Summary = models.CharField(u'Summary', max_length=5)
    DisplayAsSummary = models.CharField(u'DisplayAsSummary', max_length=5)
    Critical = models.CharField(u'Critical', max_length=5)
    IsSubproject = models.CharField(u'IsSubproject', max_length=5)
    IsSubprojectReadOnly = models.CharField(u'IsSubprojectReadOnly', max_length=5)
    ExternalTask = models.CharField(u'ExternalTask', max_length=5)
    StartVariance = models.CharField(u'StartVariance', max_length=5)
    FinishVariance = models.CharField(u'FinishVariance', max_length=5)
    WorkVariance = models.CharField(u'WorkVariance', max_length=20)
    FreeSlack = models.CharField(u'FreeSlack', max_length=20)
    TotalSlack = models.CharField(u'TotalSlack', max_length=20)
    StartSlack = models.CharField(u'StartSlack', max_length=20)
    FinishSlack = models.CharField(u'FinishSlack', max_length=20)
    FixedCost = models.CharField(u'FixedCost', max_length=5)
    FixedCostAccrual = models.CharField(u'FixedCostAccrual', max_length=5)
    PercentComplete = models.CharField(u'PercentComplete', max_length=5)
    PercentWorkComplete = models.CharField(u'PercentWorkComplete', max_length=5)
    Cost = models.CharField(u'Cost', max_length=40)
    OvertimeCost = models.CharField(u'OvertimeCost', max_length=40)
    OvertimeWork = models.CharField(u'OvertimeWork', max_length=20)
    ActualDuration = models.CharField(u'ActualDuration', max_length=20)
    ActualCost = models.CharField(u'ActualCost', max_length=40)
    ActualOvertimeCost = models.CharField(u'ActualOvertimeCost', max_length=40)
    ActualWork = models.CharField(u'ActualWork', max_length=20)
    ActualOvertimeWork = models.CharField(u'Work', max_length=20)
    RegularWork = models.CharField(u'RegularWork', max_length=20)
    RemainingDuration = models.CharField(u'RemainingDuration', max_length=20)
    RemainingCost = models.CharField(u'RemainingCost', max_length=40)
    RemainingWork = models.CharField(u'RemainingWork', max_length=20)
    RemainingOvertimeCost = models.CharField(u'RemainingOvertimeCost', max_length=40)
    RemainingOvertimeWork = models.CharField(u'RemainingOvertimeWork', max_length=20)
    ACWP = models.CharField(u'ACWP', max_length=40)
    CV = models.CharField(u'CV', max_length=40)
    ConstraintType = models.CharField(u'ConstraintType', max_length=5)
    LevelAssignments = models.CharField(u'LevelAssignments', max_length=5)
    LevelingCanSplit = models.CharField(u'LevelingCanSplit', max_length=5)
    LevelingDelay = models.CharField(u'LevelingDelay', max_length=5)
    LevelingDelayFormat = models.CharField(u'LevelingDelayFormat', max_length=5)
    IgnoreResourceCalendar = models.CharField(u'IgnoreResourceCalendar', max_length=5)
    HideBar = models.CharField(u'HideBar', max_length=5)
    Rollup = models.CharField(u'Rollup', max_length=5)
    BCWS = models.CharField(u'BCWS', max_length=40)
    BCWP = models.CharField(u'BCWP', max_length=40)
    PhysicalPercentComplete = models.CharField(u'PhysicalPercentComplete', max_length=5)
    EarnedValueMethod = models.CharField(u'EarnedValueMethod', max_length=5)
    PredecessorUID = models.CharField(u'PredecessorUID', max_length=20, default=None, null=True, blank=True)
    Predecessor_Type = models.CharField(u'Predecessor_Type', max_length=5, default=None, null=True, blank=True)
    CrossProject = models.CharField(u'CrossProject', max_length=5, default=None, null=True, blank=True)
    LinkLag = models.CharField(u'LinkLag', max_length=5, default=None, null=True, blank=True)
    LagFormat = models.CharField(u'LagFormat', max_length=5, default=None, null=True, blank=True)
    IsPublished = models.CharField(u'IsPublished', max_length=5)
    CommitmentType = models.CharField(u'CommitmentType', max_length=5)
    EA_FieldID1 = models.CharField(u'EA_FieldID1', max_length=20, default=None, null=True, blank=True)
    EA_Value1 = models.CharField(u'EA_Value1', max_length=50, default=None, null=True, blank=True)
    EA_FieldID2 = models.CharField(u'EA_FieldID2', max_length=20, default=None, null=True, blank=True)
    EA_Value2 = models.CharField(u'EA_Value2', max_length=50, default=None, null=True, blank=True)
    EA_FieldID3 = models.CharField(u'EA_FieldID3', max_length=20, default=None, null=True, blank=True)
    EA_Value3 = models.CharField(u'EA_Value3', max_length=50, default=None, null=True, blank=True)
    EA_FieldID4 = models.CharField(u'EA_FieldID4', max_length=20, default=None, null=True, blank=True)
    EA_Value4 = models.CharField(u'EA_Value4', max_length=50, default=None, null=True, blank=True)
    EA_FieldID5 = models.CharField(u'EA_FieldID5', max_length=20, default=None, null=True, blank=True)
    EA_Value5 = models.CharField(u'EA_Value5', max_length=50, default=None, null=True, blank=True)

#    objects = TasksManager()

