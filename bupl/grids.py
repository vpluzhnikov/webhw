# -*- coding: utf-8 -*-
__author__ = 'vs'

from webhw.slickgrid import SlickGrid

class BOC_Grid(SlickGrid):
    queryset = None
    columns = ['id', 'name']
    cosmo_grid = True
    col_options = [{'id' : 'id', 'name': 'Код', 'width': 20, 'cssClass' : 'cell-title', 'editor': 'Slick.Editors.Text'},
#                    'validator': 'requiredFieldValidator'},
                   {'id' : 'name', 'name': 'Название', 'width': 120, 'cssClass' : 'cell-title', 'editor':
                       'Slick.Editors.Text'},
#    , 'validator': 'requiredFieldValidator'},
                   ]