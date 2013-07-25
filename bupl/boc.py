# -*- coding: utf-8 -*-
__author__ = 'vs'
from os import remove
from xlrd import open_workbook
from webhw.slickgrid import SlickGrid
from logging import getLogger

logger = getLogger(__name__)

EMPTY = 0
IN_XLS = 1
IN_DB = 2
IN_SESSION = 3

class BOC:
    def __init__(self, type = EMPTY, filename = None):
        self.type = type
        self.data = None
        self.xls_filename = filename
        self.xls_workbook = None
        self.xls_worksheet = None
        if self.type == IN_XLS and not self.xls_filename  == None:
            self.xls_valid = self.__xls_check()
        self.xls_colnumbers = { 'itemname' : 6,
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
        self.queryset = None
        self.columns = ['price', 'itemtype1', 'itemname', 'itemtype2', 'servername', 'ex_cpucount', 'ex_ramcount',
                        'ex_sancount', 'ex_nascount', 'cpucount', 'ramcount', 'sancount', 'nascount', 'itemcount',
                        'platformtype', 'ostype', 'swaddons', 'itemstate', 'lansegment', 'dbtype', 'clustype',
                        'backuptype', 'comment']
        self.col_options = [
            #        {'id' : 'code', 'name': '№ п/п', 'width': 40, 'cssClass' : 'cell-title', 'editor':
            #        'Slick.Editors.Text',  'validator': 'requiredFieldValidator'},
            #                   {'id': "#", 'name': '', 'width': 30, 'behavior': 'selectAndMove', 'selectable': 'false',
            #                    'resizable': 'false' },
            {'id' : 'price', 'name': 'Общая стоимость', 'width': 100, 'cssClass' : 'cell-title',
             'editor': 'Slick.Editors.Text'},
            {'id' : 'itemtype1', 'name': 'Тип позиции', 'width': 160, 'cssClass' : 'cell-title',
             'options': ',Сервер СУБД,Сервер приложения,Терминальный сервер,Балансировщик,IBM DataPower',
             'editor':  'SelectCellEditor'},
            {'id' : 'itemname', 'name': 'Наименование позиции', 'width': 220, 'cssClass' : 'cell-title',
             'editor' : 'Slick.Editors.Text',  'validator': 'requiredFieldValidator'},
            {'id' : 'itemtype2', 'name': 'Новый/апгрейд', 'width': 120, 'cssClass' : 'cell-title',
             'options': ',новая позиция,модернизация', 'editor':  'SelectCellEditor'},
            {'id' : 'servername', 'name': 'Имя сервера', 'width': 100, 'cssClass' : 'cell-title', 'editor':
                'Slick.Editors.Text'},
            {'id' : 'ex_cpucount', 'name': 'Кол-во CPU', 'width': 100, 'cssClass' : 'cell-title', 'editor':
                'Slick.Editors.Text'},
            {'id' : 'ex_ramcount', 'name': 'Кол-во ОЗУ, Гб', 'width': 100, 'cssClass' : 'cell-title', 'editor':
                'Slick.Editors.Text'},
            {'id' : 'ex_sancount', 'name': 'Кол-во СХД (SAN), Гб', 'width': 100, 'cssClass' : 'cell-title',
             'editor': 'Slick.Editors.Text'},
            {'id' : 'ex_nascount', 'name': 'Кол-во СХД (NAS), Гб', 'width': 100, 'cssClass' : 'cell-title',
             'editor': 'Slick.Editors.Text'},
            {'id' : 'cpucount', 'name': 'Требуется CPU', 'width': 100, 'cssClass' : 'cell-title', 'editor':
                'Slick.Editors.Text'},
            {'id' : 'ramcount', 'name': 'Требуется ОЗУ, Гб', 'width': 100, 'cssClass' : 'cell-title', 'editor':
                'Slick.Editors.Text'},
            {'id' : 'sancount', 'name': 'Требуется СХД (SAN), Гб', 'width': 100, 'cssClass' : 'cell-title',
             'editor': 'Slick.Editors.Text'},
            {'id' : 'nascount', 'name': 'Требуется СХД (NAS), Гб', 'width': 100, 'cssClass' : 'cell-title',
             'editor': 'Slick.Editors.Text'},
            {'id' : 'itemcount', 'name': 'Кол-во', 'width': 60, 'cssClass' : 'cell-title',
             'editor': 'Slick.Editors.Text',  'validator': 'requiredFieldValidator'},
            {'id' : 'platformtype', 'name': 'Тип платформы', 'width': 150, 'cssClass' : 'cell-title',
             'options': ',Intel x86,Oracle SPARC,IBM Power', 'editor': 'SelectCellEditor',
             'validator': 'requiredFieldValidator'},
            {'id' : 'ostype', 'name': 'Тип ОС', 'width': 150, 'cssClass' : 'cell-title',
             'options': ',Windows,Linux (RHEL),Oracle Solaris,IBM AIX', 'editor': 'SelectCellEditor',
             'validator': 'requiredFieldValidator'},
            {'id' : 'swaddons', 'name': 'Дополнительное ПО', 'width': 150, 'cssClass' : 'cell-title',
             'editor': 'Slick.Editors.LongText'},
            {'id' : 'itemstate', 'name': 'Статус (пром/тест)', 'width': 100, 'cssClass' : 'cell-title',
             'options': ',пром,тест', 'editor': 'SelectCellEditor', 'validator': 'requiredFieldValidator'},
            {'id' : 'lansegment', 'name': 'Сегмент сети', 'width': 120, 'cssClass' : 'cell-title',
             'options': ',Альфа,Сигма,Тау', 'editor': 'SelectCellEditor'},
            {'id' : 'dbtype', 'name': 'Тип СУБД', 'width': 120, 'cssClass' : 'cell-title',
             'options': ',MSSQL,Oracle DB,IBM DB2', 'editor': 'SelectCellEditor'},
            {'id' : 'clustype', 'name': 'Территориальная защита', 'width': 120, 'cssClass' : 'cell-title',
             'options': ',нет,да', 'editor': 'SelectCellEditor'},
            {'id' : 'backuptype', 'name': 'Резервное копирование', 'width': 120, 'cssClass' : 'cell-title',
             'options': ',нет,да', 'editor': 'SelectCellEditor'},
            {'id' : 'comment', 'name': 'Дополнительные требования', 'width': 250, 'cssClass' : 'cell-title',
             'editor': 'Slick.Editors.LongText'},
            ]

        if self.type == IN_XLS:
            if self.xls_valid:
                GRID_FIELDS = []
                curr_row = 2
                while curr_row < self.xls_worksheet.nrows:
                    ROW = {}
                    for key in self.xls_colnumbers.keys():
                        if not self.xls_worksheet.cell_type(curr_row, self.xls_colnumbers[key]) == 0:
                            ROW.update({key : self.xls_worksheet.cell_value(curr_row, self.xls_colnumbers[key])})
                    if 'servername' in ROW.keys():
                        ROW.update({'itemtype2' : 'модернизация'})
                    else:
                        ROW.update({'itemtype2' : 'новая позиция'})
                    GRID_FIELDS.append(ROW)
                    curr_row += 1
            self.data = GRID_FIELDS

#    def grid_fields(self):
#        if self.xls_valid:
#            GRID_FIELDS = []
#            curr_row = 2
#            while curr_row < self.xls_worksheet.nrows:
#                ROW = {}
#                for key in self.xls_colnumbers.keys():
#                    if not self.xls_worksheet.cell_type(curr_row, self.xls_colnumbers[key]) == 0:
#                        ROW.update({key : self.xls_worksheet.cell_value(curr_row, self.xls_colnumbers[key])})
#                if 'servername' in ROW.keys():
#                    ROW.update({'itemtype2' : 'модернизация'})
#                else:
#                    ROW.update({'itemtype2' : 'новая позиция'})
#                GRID_FIELDS.append(ROW)
#                curr_row += 1
#            return GRID_FIELDS
#        else:
#            return None
    def get_grid(self):
        """
        Returns dict with columns, griddata, options via SlickGrid object
        """
        gridview = SlickGrid(columns = self.columns, col_options = self.col_options, griddata = self.data)
#        logger.error("Grid %s", (gridview.get_grid()))
        return gridview.get_grid()

    def xls_file_destroy(self):
        """
        Removes xls file
        """
        remove(self.xls_filename)
        return True

    def xls_print_content(self):
        """
        Print all content from worksheet (for testing only)
        """
        num_rows = self.xls_worksheet.nrows - 1
        num_cells = self.xls_worksheet.ncols - 1
        curr_row = -1
        while curr_row < num_rows:
            curr_row += 1
            row = self.xls_worksheet.row(curr_row)
            print 'Row:', curr_row
            curr_cell = -1
            while curr_cell < num_cells:
                curr_cell += 1
                # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                cell_type = self.xls_worksheet.cell_type(curr_row, curr_cell)
                cell_value = self.xls_worksheet.cell_value(curr_row, curr_cell)
                print '	', cell_type, ':', cell_value

    def calculate(self):
        """
        Calculates prices for requrements and modify self.data with price values
        """
        return True

    def __xls_check(self):
        """
        Checks if xls file is correctly filled up
        """
        if not ('xlsx' in self.xls_filename)  and ('xls' in self.xls_filename):
            try:
                self.xls_workbook = open_workbook(self.xls_filename)
                self.xls_worksheet = self.xls_workbook.sheet_by_name(u'Бюджетная оценка')
            except:
                return False
            if self.xls_workbook:
                return True
            else:
                return False
        else:
            return False


