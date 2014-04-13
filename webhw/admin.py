# -*- coding: utf-8 -*-
from django.contrib import admin
from bupl.models import Prices

class PricesAdmin(admin.ModelAdmin):
#    fields = [u'Код оборудования', u'Тип оборудования', u'Цена', u'Описание']
    list_display = ['hw_class', 'hw_type', 'price', 'hw_full_name']
    search_fields = ['hw_type']

admin.site.register(Prices, PricesAdmin)
