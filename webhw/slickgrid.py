# -*- coding: utf-8 -*-
__author__ = 'vs'
from django.core.exceptions import ImproperlyConfigured

class SlickGrid(object):
    queryset = None
    columns = None
    cosmo_grid = True # allows to create grid withot db on back-end
    col_options = None
    grid_options = None

    def get_default_grid_options(self):
        self.grid_options = {
            'editable': True,
            'enableAddRow': True,
            'enableCellNavigation': True,
            'asyncEditorLoading': False,
            'autoEdit': False
        }
        return self.grid_options

    def get_dbdata(self):
        return None

    def get_grid_data(self):
        GRID_DATA = []
        if hasattr(self, 'queryset') and self.queryset == None and hasattr(self, 'cosmo_grid') and self.cosmo_grid and \
           hasattr(self, 'columns') and self.columns is not None:
#            COLS = {}
#            for col in self.columns:
#                COLS.update({col : ''})
#            GRID_DATA.append(COLS)
            GRID_DATA = []
        elif hasattr(self, 'queryset') and self.queryset is not None:
            GRID_DATA = self.get_dbdata()
        return GRID_DATA

    def get_grid_columns(self):
        GRID_COLUMS = []
        if hasattr(self, 'queryset') and self.queryset == None and hasattr(self, 'cosmo_grid') and self.cosmo_grid and \
           hasattr(self, 'columns') and self.columns is not None:
            for col in self.columns:
                GRID_COLUMS.append({'id' : col, 'field' : col})
        elif hasattr(self, 'queryset') and self.queryset is not None:
            GRID_COLUMS = self.get_dbdata()
        else:
            raise ImproperlyConfigured("No queryset or model defined.")
        if hasattr(self, 'col_options') and self.col_options is not None:
            for col in GRID_COLUMS:
                for opts in self.col_options:
                    if col.get('id') == opts.get('id'):
                        col.update(opts)
        return GRID_COLUMS

    def get_grid_options(self):
        if hasattr(self, 'grid_options') and self.grid_options is not None:
            return self.grid_options
        else:
            return self.get_default_grid_options()
