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


class Project(models.Model):
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
        db_table = u'Project'
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
    prj_number = models.ForeignKey(Project, null=True, db_column='prj_number', blank=True)
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

