# -*- coding: utf-8 -*-
__author__ = 'vs'
from os import remove
from xlrd import open_workbook

class XlsBOC:
    def __init__(self, filename):
        self.filename = filename
        self.boc_workbook = None
        self.boc_worksheet = None
        self.valid = self.__boc_check()
        self.xlscolnumbers = { 'itemname' : 6,
                               'itemtype1' : 6,
#                               'itemtype2': 2,
                               'servername': 7,
                               'ex_cpucount': 8,
                               'ex_ramcount': 9,
                               'ex_sancount': 10,
                               'ex_nascount': 11,
                               'cpucount': 24,
                               'ramcount': 26,
                               'sancount': 30,
                               'nascount': 32,
                               'itemcount': 34,
                               'platformtype': 35,
                               'ostype': 37,
                               'swaddons': 38,
                               'itemstate': 5,
                               'lansegment': 39,
                               'dbtype': 38,
                               'clustype': 41,
                               'backuptype': 42,
                               'comment': 45
        }

    def grid_fields(self):
        if self.valid:
            GRID_FIELDS = []
            curr_row = 2
            while curr_row < self.boc_worksheet.nrows:
                ROW = {}
                for key in self.xlscolnumbers.keys():
                    if not self.boc_worksheet.cell_type(curr_row, self.xlscolnumbers[key]) == 0:
                        ROW.update({key : self.boc_worksheet.cell_value(curr_row, self.xlscolnumbers[key])})
                if 'servername' in ROW.keys():
                    ROW.update({'itemtype2' : 'модернизация'})
                else:
                    ROW.update({'itemtype2' : 'новая позиция'})
                GRID_FIELDS.append(ROW)
                curr_row += 1
            return GRID_FIELDS
        else:
            return None

    def file_destroy(self):
        remove(self.filename)
        return True

    def print_content(self):
        num_rows = self.boc_worksheet.nrows - 1
        num_cells = self.boc_worksheet.ncols - 1
        curr_row = -1
        while curr_row < num_rows:
            curr_row += 1
            row = self.boc_worksheet.row(curr_row)
            print 'Row:', curr_row
            curr_cell = -1
            while curr_cell < num_cells:
                curr_cell += 1
                # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                cell_type = self.boc_worksheet.cell_type(curr_row, curr_cell)
                cell_value = self.boc_worksheet.cell_value(curr_row, curr_cell)
                print '	', cell_type, ':', cell_value

    def __boc_check(self):
        if not ('xlsx' in self.filename)  and ('xls' in self.filename):
            try:
                self.boc_workbook = open_workbook(self.filename)
                self.boc_worksheet = self.boc_workbook.sheet_by_name(u'Бюджетная оценка')
            except:
                return False
            if self.boc_workbook:
                return True
            else:
                return False
        else:
            return False


