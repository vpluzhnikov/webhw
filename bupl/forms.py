__author__ = 'vss'
# -*- coding: utf-8 -*-
from django import forms
from bupl.models import Project
from django.utils.translation import ugettext as _

class BocForm(forms.Form):
    PRJLIST = []
    AllProjects = Project.objects.values('prj_number').distinct()

    PRJLIST.append([0, 'Без номера'])
    for prjnum in AllProjects:
        PRJLIST.append([prjnum['prj_number'] , str(prjnum['prj_number']).split(".")[0]])
    prjselect = forms.ChoiceField(choices=PRJLIST, label='Номер проекта')
    prjname = forms.CharField(label='Название проекта',
        widget=forms.TextInput(attrs={'size':'150', 'readonly':'readonly'}))
    customer = forms.CharField(label='Заказчик',
        widget=forms.TextInput(attrs={'size':'30', 'readonly':'readonly'}))
    manager = forms.CharField(label='Руководитель проекта',
        widget=forms.TextInput(attrs={'size':'30', 'readonly':'readonly'}))

