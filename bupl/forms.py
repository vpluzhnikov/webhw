__author__ = 'vss'
# -*- coding: utf-8 -*-
from django import forms
from bupl.models import Projects
from django.utils.translation import ugettext as _

class BocForm(forms.Form):
    PRJLIST = []
    AllProjects = Projects.objects.values('prj_number').distinct()

#    PRJLIST.append([0, 'Без номера'])
#    for prjnum in AllProjects:
#        PRJLIST.append([prjnum['prj_number'] , str(prjnum['prj_number']).split(".")[0]])

    file = forms.FileField(label='Загрузить из xls', required=False)
#    prjselect = forms.ChoiceField(choices=PRJLIST, label='Номер проекта', required=False)
#    prjname = forms.CharField(label='Название проекта',
#        widget=forms.TextInput(attrs={'size':'150', 'readonly':'readonly'}), required=False)
    customer = forms.CharField(label='Заказчик',
        widget=forms.TextInput(attrs={'size':'30', 'readonly':'readonly'}), required=False)
    manager = forms.CharField(label='Руководитель проекта',
        widget=forms.TextInput(attrs={'size':'30', 'readonly':'readonly'}), required=False)

class EosForm(forms.Form):
#    PRJLIST = []
#    AllProjects = Projects.objects.values('prj_number').distinct()

#    PRJLIST.append([0, u'Другой'])
#    for prjnum in AllProjects:
#        PRJLIST.append([prjnum['prj_number'] , str(prjnum['prj_number']).split(".")[0]])
#    prjselect = forms.ChoiceField(choices=PRJLIST, label='Номер проекта:', required=False)
#    prjname = forms.CharField(label='Название проекта',
#        widget=forms.TextInput(attrs={'size':'70', 'readonly':'readonly'}), required=False)
    xls_file = forms.FileField(label='', required=False, )
    file_type = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput())

class LoginForm(forms.Form):
    user = forms.CharField(label=u'Имя пользователя:',
        widget=forms.TextInput(attrs={'size':'30'}), required=True)
    password = forms.CharField(label=u'Пароль:', widget=forms.PasswordInput())