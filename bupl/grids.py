# -*- coding: utf-8 -*-
__author__ = 'vs'

from webhw.slickgrid import SlickGrid

class BOC_Grid(SlickGrid):
    queryset = None
    columns = ['itemtype1', 'itemname', 'itemtype2', 'servername', 'ex_cpucount', 'ex_ramcount', 'ex_sancount',
               'ex_nascount', 'cpucount', 'ramcount', 'sancount', 'nascount', 'itemcount', 'platformtype', 'ostype',
               'swaddons', 'itemstate', 'lansegment', 'dbtype', 'clustype', 'backuptype', 'comment']
    cosmo_grid = True
    col_options = [
#        {'id' : 'code', 'name': '№ п/п', 'width': 40, 'cssClass' : 'cell-title', 'editor':
#        'Slick.Editors.Text',  'validator': 'requiredFieldValidator'},
                   {'id' : 'itemtype1', 'name': 'Тип позиции', 'width': 160, 'cssClass' : 'cell-title',
                    'options': ',Сервер СУБД,Сервер приложения,Терминальный сервер,Балансировщик,IBM DataPower',
                    'editor':  'SelectCellEditor'},
                   {'id' : 'itemname', 'name': 'Наименование позиции', 'width': 220, 'cssClass' : 'cell-title',
                    'editor' : 'Slick.Editors.Text',  'validator': 'requiredFieldValidator'},
                   {'id' : 'itemtype2', 'name': 'Новый/апгрейд', 'width': 120, 'cssClass' : 'cell-title',
                    'options': ',новая позиция,апгрейд', 'editor':  'SelectCellEditor'},
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
                   {'id' : 'clustype', 'name': 'Системная кластризация', 'width': 120, 'cssClass' : 'cell-title',
                    'options': ',нет,да', 'editor': 'SelectCellEditor'},
                   {'id' : 'backuptype', 'name': 'Резервное копирование', 'width': 120, 'cssClass' : 'cell-title',
                    'options': ',нет,да', 'editor': 'SelectCellEditor'},
                   {'id' : 'comment', 'name': 'Дополнительные требования', 'width': 250, 'cssClass' : 'cell-title',
                    'editor': 'Slick.Editors.LongText'},
                   ]
