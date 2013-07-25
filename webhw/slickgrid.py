# -*- coding: utf-8 -*-
__author__ = 'vs'
from django.core.exceptions import ImproperlyConfigured
from logging import getLogger

logger = getLogger(__name__)

class SlickGrid:

    def __init__(self, queryset = None, columns = None, col_options = None, grid_options = None, griddata = None):
        self.queryset = queryset
        self.columns = columns
        self.col_options = col_options
        self.grid_options = grid_options
        self.frame = None
        self.data = griddata


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
        FIRST_LINE = {}
        if hasattr(self, 'queryset') and self.queryset == None and hasattr(self, 'data') and self.data == None:
            GRID_DATA = []
        elif hasattr(self, 'queryset') and self.queryset is not None:
            GRID_DATA = self.get_dbdata()
        elif hasattr(self, 'data'):
            GRID_DATA = self.data
        return GRID_DATA

    def get_grid_columns(self):
        GRID_COLUMS = []
        if hasattr(self, 'queryset') and self.queryset == None and hasattr(self, 'columns') and self.columns <> None:
            for col in self.columns:
                GRID_COLUMS.append({'id' : col, 'field' : col})
        elif hasattr(self, 'queryset') and self.queryset is not None:
            GRID_COLUMS = self.get_dbdata()
        else:
            raise ImproperlyConfigured("No queryset or model defined.")
        if hasattr(self, 'col_options') and self.col_options <> None:
            for col in GRID_COLUMS:
                for opts in self.col_options:
                    if col.get('id') == opts.get('id'):
                        col.update(opts)
        return GRID_COLUMS

    def get_grid_options(self):
        if hasattr(self, 'grid_options') and self.grid_options <> None:
            return self.grid_options
        else:
            return self.get_default_grid_options()

    def get_grid(self):
        self.frame = {}
        self.frame['data'] = self.get_grid_data()
        self.frame['options'] = self.get_grid_options()
        self.frame['columns'] = self.get_grid_columns()
        return self.frame

