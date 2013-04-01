# -*- coding: utf-8 -*-
__author__ = 'vs'

from webhw.slickgrid import SlickGrid

class BOC_Grid(SlickGrid):
    queryset = None
    columns = ['code', 'name', 'choice']
    cosmo_grid = True
    col_options = [{'id' : 'code', 'name': 'Код', 'width': 120, 'cssClass' : 'cell-title', 'editor': 'Slick.Editors.Text',  'validator': 'requiredFieldValidator'
                    },
                   {'id' : 'name', 'name': 'Наименование', 'width': 120, 'cssClass' : 'cell-title', 'editor':  'Slick.Editors.Text'},

                   {'id' : 'choice', 'name': 'Выбор', 'width': 120, 'cssClass' : 'cell-title', 'options': 'Red,Green,Blue,Black,White', 'editor':  'SelectCellEditor'}
                   #    , 'validator': 'requiredFieldValidator'},
                   ]