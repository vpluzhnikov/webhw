# -*- coding: utf-8 -*-
__author__ = 'vs'
from os import remove
from xlrd import open_workbook
from webhw.slickgrid import SlickGrid
from logging import getLogger
from bupl.models import Prices
from decimal import *

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
                               'hddcount' : 28,
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
                        'ex_sancount', 'ex_nascount', 'cpucount', 'ramcount', 'hddcount','sancount', 'nascount',
                        'itemcount', 'platformtype', 'ostype', 'swaddons', 'itemstate', 'lansegment', 'dbtype',
                        'clustype', 'backuptype', 'comment']
        self.col_options = [
            #        {'id' : 'code', 'name': '№ п/п', 'width': 40, 'cssClass' : 'cell-title', 'editor':
            #        'Slick.Editors.Text',  'validator': 'requiredFieldValidator'},
            #                   {'id': "#", 'name': '', 'width': 30, 'behavior': 'selectAndMove', 'selectable': 'false',
            #                    'resizable': 'false' },
            {'id' : 'price', 'name': 'Общая стоимость', 'width': 100, 'cssClass' : 'cell-title'},
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
            {'id' : 'hddcount', 'name': 'Требуется СХД (внутренее), Гб', 'width': 120, 'cssClass' : 'cell-title',
             'editor': 'Slick.Editors.Text'},
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
             'options': ',пром,тест(НТ),тест(другое)', 'editor': 'SelectCellEditor',
             'validator': 'requiredFieldValidator'},
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
        error_flag = False
        new_data = []
        for line in self.data:
            if line.keys() > 0:
                line_price = 0
                logger.error(line)

# ---------------------------------------------
# Check for input data
# ---------------------------------------------

#Checking for cells contents
                if not 'itemtype1' in line.keys():
                    line['itemtype1'] = u'Требуется указать'
                    error_flag = True

#Checking for row types
                if not 'itemtype2' in line.keys():
                    line['itemtype2'] = u'Требуется указать'
                    error_flag = True

#Checking fot OS type
                if not 'ostype' in line.keys() and (line['itemtype1'] <> u'IBM DataPower') and \
                   (line['itemtype1'] <> u'Балансировщик'):
                    line['ostype'] = u'Требуется указать'
                    error_flag = True

#Checking for CPU count
                if not 'cpucount' in line.keys():
                    if ('itemtype2' in line.keys()):
                        if line['itemtype2'] == u'модернизация':
                            line['cpucount'] = 0
                        elif line['itemtype2'] == u'новая позиция':
                            line['cpucount'] = 0
                            error_flag = True
                        else:
                            line['cpucount'] = u'Требуется указать'
                            error_flag = True
                elif (line['itemtype1'] <> u'IBM DataPower') and (line['itemtype1'] <> u'Балансировщик'):
                    try:
                        int(line['cpucount'])
                    except:
                        line['cpucount'] = u'Укажите целое число'
                        error_flag = True

#Checking for count
                if not 'itemcount' in line.keys():
                    line['itemcount'] = 1
                else:
                    try:
                        int(line['itemcount'])
                    except:
                        line['itemcount'] = u'Укажите целое число'
                        error_flag = True

#Checking for RAM requirenments
                if 'ramcount' in line.keys() and (line['itemtype1'] <> u'IBM DataPower') and\
                   (line['itemtype1'] <> u'Балансировщик'):
                    try:
                        int(line['ramcount'])
                    except:
                        line['ramcount'] = u'Укажите целое число'
                        error_flag = True
                elif (not 'ramcount' in line.keys()) and ('itemtype2' in line.keys()):
                    if (line['itemtype2'] == u'новая позиция') and ('cpucount' in line.keys()) and (not error_flag):
                        try:
                            line['ramcount'] = int(line['cpucount']) * 2
                        except:
                            error_flag = True
                    elif (line['itemtype2'] == u'модернизация'):
                        line['ramcount'] = 0
                    else:
                        line['ramcount'] = u'Требуется указать'
                        error_flag = True
                elif (line['itemtype1'] <> u'IBM DataPower') and (line['itemtype1'] <> u'Балансировщик'):
                    line['ramcount'] = u'Требуется указать'
                    error_flag = True

#Checking for internal disk requirenments
                if 'hddcount' in line.keys() and (line['itemtype1'] <> u'IBM DataPower') and\
                   (line['itemtype1'] <> u'Балансировщик'):
                    try:
                        int(line['hddcount'])
                    except:
                        line['hddcount'] = u'Укажите целое число'
                        error_flag = True
                elif (not 'hddcount' in line.keys()) and ('itemtype2' in line.keys()):
                    if line['itemtype2'] == u'модернизация':
                        line['hddcount'] = 0
                    else:
                        line['hddcount'] = u'Требуется указать'
                        error_flag = True
                elif (line['itemtype1'] <> u'IBM DataPower') and (line['itemtype1'] <> u'Балансировщик'):
                    line['hddcount'] = u'Требуется указать'
                    error_flag = True

#Checking for san disk requienments
                if 'sancount' in line.keys() and (line['itemtype1'] <> u'IBM DataPower') and\
                   (line['itemtype1'] <> u'Балансировщик'):
                    try:
                        int(line['sancount'])
                    except:
                        line['sancount'] = u'Укажите целое число'
                        error_flag = True
                elif (line['itemtype1'] <> u'IBM DataPower') and (line['itemtype1'] <> u'Балансировщик'):
                    line['sancount'] = 0

#Checking for san disk requienments
                if 'nascount' in line.keys() and (line['itemtype1'] <> u'IBM DataPower') and \
                   (line['itemtype1'] <> u'Балансировщик'):
                    try:
                        int(line['nascount'])
                    except:
                        line['nascount'] = u'Укажите целое число'
                        error_flag = True
                elif (line['itemtype1'] <> u'IBM DataPower') and (line['itemtype1'] <> u'Балансировщик'):
                    line['nascount'] = 0

#Checking for type of item
                if not 'itemstate' in line.keys():
                    line['itemstate'] = u'тест(другое)'
                elif not(line['itemstate'] in [u'пром' , u'тест(НТ)', u'тест(другое)']):
                    line['itemstate'] = u'Не верно'
                    error_flag = True

#Checking for lan segment
                if not 'lansegment' in line.keys():
                    line['lansegment'] = u'Альфа'
                elif not(line['lansegment'] in [u'Альфа' , u'Сигма' , u'Тау' ]):
                    line['lansegment'] = u'Не верно'
                    error_flag = True

#Checking for cluster requirenments
                if not 'clustype' in line.keys():
                    if line['itemstate'] == u'пром':
                        line['clustype'] = u'да'
                    else:
                        line['clustype'] = u'нет'
                elif not(line['clustype'] in [u'да', u'нет']):
                    line['clustype'] = u'Не верно'
                    error_flag = True

#Checking for backup requirenments
                if not 'backuptype' in line.keys():
                    if line['itemstate'] == u'пром':
                        line['backuptype'] = u'да'
                    else:
                        line['backuptype'] = u'нет'
                elif not(line['backuptype'] in [u'да', u'нет']):
                    line['backuptype'] = u'Не верно'
                    error_flag = True

# ---------------------------------------------
# Calculation for new systems only
# ---------------------------------------------

#Calculation for new x86 systems
                if (not error_flag) and (line['itemtype2'] == u'новая позиция') and \
                   ((line['itemtype1'] == u'Сервер приложения') or (line['itemtype1'] == u'Терминальный сервер') or
                    (line['itemtype1'] == u'Сервер СУБД')) and \
                   ((line['ostype'] == u'Windows') or (line['ostype'] == u'Linux (RHEL)')):
                    if (int(line['cpucount']) <= 16):
                        line_price += Prices.objects.get(hw_type = 'x86_ent').price * int(line['cpucount']) * \
                                      int(line['itemcount'])
                        line_price += Prices.objects.get(hw_type = 'san_stor_vmware').price * int(line['hddcount']) *\
                                      int(line['itemcount'])
                        line_price += Prices.objects.get(hw_type = 'san_stor_mid').price * int(line['sancount']) *\
                                      int(line['itemcount'])
                        line_price += Prices.objects.get(hw_type = 'nas_stor').price * int(line['nascount']) *\
                                      int(line['itemcount'])
                        line_price += Prices.objects.get(hw_type = 'vmware_lic').price * int(line['cpucount']) * \
                                      int(line['itemcount'])
                        line_price += Prices.objects.get(hw_type = 'vmware_support').price * int(line['cpucount']) * \
                                      int(line['itemcount'])
                    elif (int(line['cpucount']) > 16):
                        line_price += Prices.objects.get(hw_type = 'x86_mid').price * int(line['cpucount']) *\
                                      int(line['itemcount'])
                        if (line['itemtype1'] == u'Сервер СУБД') and (line['itemstate'] == u'пром'):
                            line_price += Prices.objects.get(hw_type = 'san_stor_repl').price * int(line['sancount']) *\
                                                                            int(line['itemcount'])
                        elif (line['itemtype1'] == u'Сервер СУБД') and (line['itemstate'] == u'тест(НТ)'):
                            line_price += Prices.objects.get(hw_type = 'san_stor_hiend').price * int(line['sancount'])*\
                                          int(line['itemcount'])
                        else:
                            line_price += Prices.objects.get(hw_type = 'san_stor_mid').price * int(line['sancount']) *\
                                          int(line['itemcount'])
                        line_price += Prices.objects.get(hw_type = 'nas_stor').price * int(line['nascount']) *\
                                      int(line['itemcount'])

#Calculation for new AIX and Solaris systems
                if (not error_flag) and (line['itemtype2'] == u'новая позиция') and\
                   ((line['itemtype1'] == u'Сервер приложения') or (line['itemtype1'] == u'Сервер СУБД')) and\
                   ((line['ostype'] == u'IBM AIX') or (line['ostype'] == u'Oracle Solaris')):
                    if (int(line['cpucount']) <= 128):
                        if (line['ostype'] == u'IBM AIX'):
                            line_price += Prices.objects.get(hw_type = 'ppc_mid').price * int(line['cpucount']) *\
                                      int(line['itemcount'])
                        if (line['ostype'] == u'Oracle Solaris'):
                            line_price += Prices.objects.get(hw_type = 't_mid').price * int(line['cpucount']) *\
                                          int(line['itemcount'])
                    elif (int(line['cpucount']) > 128):
                        if (line['ostype'] == u'IBM AIX'):
                            line_price += Prices.objects.get(hw_type = 'ppc_hiend').price * int(line['cpucount']) *\
                                      int(line['itemcount'])
                        if (line['ostype'] == u'Oracle Solaris'):
                            line_price += Prices.objects.get(hw_type = 'sparc_hiend').price * int(line['cpucount']) *\
                                          int(line['itemcount'])
                    if (line['itemstate'] == u'пром'):
                        if (line['backuptype'] == u'да') and (int(line['sancount']) > 2000):
                            line_price += Prices.objects.get(hw_type = 'san_stor_full').price *\
                                      int(line['sancount']) * int(line['itemcount'])
                        else:
                            line_price += Prices.objects.get(hw_type = 'san_stor_repl').price *\
                                      int(line['sancount']) * int(line['itemcount'])
                    elif (line['itemstate'] == u'тест(НТ)'):
                        line_price += Prices.objects.get(hw_type = 'san_stor_hiend').price *\
                                  int(line['sancount']) * int(line['itemcount'])
                    else:
                        line_price += Prices.objects.get(hw_type = 'san_stor_mid').price *\
                                  int(line['sancount']) * int(line['itemcount'])
                    line_price += Prices.objects.get(hw_type = 'nas_stor').price * int(line['nascount']) *\
                              int(line['itemcount'])
                    if (line['itemstate'] == u'пром'):
                        line_price += Prices.objects.get(hw_type = 'symantec_lic').price * int(line['cpucount']) *\
                                  int(line['itemcount'])
                        line_price += Prices.objects.get(hw_type = 'symantec_support').price *\
                                  int(line['cpucount']) * int(line['itemcount']) * 3
#Calculation for Alteons
                if (not error_flag) and (line['itemtype2'] == u'новая позиция') and\
                           (line['itemtype1'] == u'Балансировщик'):
                    line_price += Prices.objects.get(hw_type = 'loadbalancer').price * int(line['itemcount'])

#Calculation for Datapowers
                if (not error_flag) and (line['itemtype2'] == u'новая позиция') and \
                   (line['itemtype1'] == u'IBM DataPower'):
                    line_price += Prices.objects.get(hw_type = 'datapower').price * int(line['itemcount'])

                logger.error(line)
                logger.error(error_flag)

# ---------------------------------------------
# Calculation for upgrades only
# ---------------------------------------------




# ---------------------------------------------
# Common position for new systems and upgrades
# ---------------------------------------------
#Calculation for windows licence (new systems and upgrade)
                if (line['ostype'] == u'Windows'):
                    line_price += Prices.objects.get(hw_type = 'ms_lic').price * int(line['cpucount']) \
                                  * int(line['itemcount'])
#Calculation for RHEL support (new systems and upgrade)
                elif (line['ostype'] == u'Linux (RHEL)'):
                    line_price += Prices.objects.get(hw_type = 'rhel_support').price * int(line['cpucount']) * \
                                  int(line['itemcount'])

#Calculation for backup (new systems and upgrade)
                if (line['backuptype'] == u'да') and (line['itemtype1'] <> u'IBM DataPower') and \
                   (line['itemtype1'] <> u'Балансировщик') :
                    line_price += Prices.objects.get(hw_type='backup_stor').price * \
                                  (int(line['hddcount']) + int(line['nascount']) + int(line['sancount'])) * \
                                  int(line['itemcount'])

                line['price'] = str(line_price.quantize(Decimal(10) ** -2))

                if error_flag:
                    line['price'] = 'Ошибка данных'
                new_data.append(line)
        self.data = new_data
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


