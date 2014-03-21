# -*- coding: utf-8 -*-
__author__ = 'vs'

from logging import getLogger
from bupl.models import Prices

from decimal import *
from webhw.settings import ARIAL_FONT_FILELOCATION, BOC_WORK_DIR, MEDIA_ROOT
from price_calcs import calculate_req_line

from time import time
from os import path

from xlrd import open_workbook
from io import BytesIO

from reportlab.lib.units import cm
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab import rl_config
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT


ru_vals = { 'new' : u'Новый',
            'upgrade' : u'Апгрейд',
            'app' : u'Сервер приложения',
            'db' : u'Сервер СУБД',
            'dbarch' : u'Сервер СУБД (архивная)',
            'term' : u'Терминальный сервер',
            'dp' : u'IBM DataPower',
            'lb' : u'Балансировщик',
            'other' : u'Другое',
            'power' : u'IBM Power',
            't_series' : u'Oracle T-series',
            'm_series' : u'Oracle M-series',
            'itanium' : u'HP Itanium',
            'x86' : u'Intel x86',
            '---' : u'---',
            'prom' : u'Пром',
            'test-nt' : u'Тест (НТ)',
            'test-other' : u'Тест (Другое)',
}

xls_vals = { 'prjrow' : 2,
             'prjcell' : 4,
             'eos_start_row' : 10,
             'itemtype1_col' : 14,
             'itemname_col' : 4,
             'servername_col': 6,
             'cpucount_col' : 7,
             'ramcount_col' : 8,
             'hddcount_col' : 9,
             'sancount_col' : 10,
             'nascount_col' : 11,
             'itemcount_col' : 5,
             'platform_type_col' : 13,
             'ostype_col' : 15,
             'swaddons_col' : 16,
             'itemstatus_col' : 3,
             'lansegment_col' : 17,
             'dbtype_col' : 16,
             'clustype_col' : 18,
             'backuptype_col' : 19,
}

logger = getLogger(__name__)

def old_calculate_req_line(req_line):
    """
    Calculates prices for requrements and modify self.data with price values
    """
    req_line['price'] = '0'
    req_line['error'] = '0'
    error_flag = False
    line_price = 0
    if req_line.keys() > 0:
#        logger.error("--------- BEFORE")
#        logger.error(req_line)

        #---------------------------------------------
        #Calculation for new systems only
        #---------------------------------------------

        #Calculation for new x86 systems

        if (not error_flag) and (req_line['itemtype2'] == u'new') and\
           ((req_line['itemtype1'] == u'app') or (req_line['itemtype1'] == u'term') or
            (req_line['itemtype1'] == u'db') or (req_line['itemtype1'] == u'dbarch') or
            (req_line['itemtype1'] == u'other')) and ((req_line['ostype'] == u'windows') or
                                                      (req_line['ostype'] == u'linux')):
            if (int(req_line['cpu_count']) <= 16):
                line_price += Prices.objects.get(hw_type='x86_ent').price * int(req_line['cpu_count']) *\
                              int(req_line['item_count'])
                line_price += Prices.objects.get(hw_type='san_stor_vmware').price * int(req_line['hdd_count']) *\
                              int(req_line['item_count'])
                line_price += Prices.objects.get(hw_type='san_stor_mid').price * int(req_line['san_count']) *\
                              int(req_line['item_count'])
                line_price += Prices.objects.get(hw_type='nas_stor').price * int(req_line['nas_count']) *\
                              int(req_line['item_count'])
                line_price += Prices.objects.get(hw_type='vmware_lic').price * int(req_line['cpu_count']) *\
                              int(req_line['item_count'])
                line_price += Prices.objects.get(hw_type='vmware_support').price * int(req_line['cpu_count']) *\
                              int(req_line['item_count'])
            elif (int(req_line['cpu_count']) > 16):
                line_price += Prices.objects.get(hw_type='x86_mid').price * int(req_line['cpu_count']) *\
                              int(req_line['item_count'])
                if (req_line['itemtype1'] == u'db') and (req_line['itemstatus'] == u'prom'):
                    line_price += Prices.objects.get(hw_type='san_stor_repl').price * int(req_line['san_count']) *\
                                  int(req_line['item_count'])
                elif (req_line['itemtype1'] == u'db') and (req_line['itemstatus'] == u'test-nt'):
                    line_price += Prices.objects.get(hw_type='san_stor_hiend').price * int(req_line['san_count']) *\
                                  int(req_line['item_count'])
                else:
                    line_price += Prices.objects.get(hw_type='san_stor_mid').price * int(req_line['san_count']) *\
                                  int(req_line['item_count'])
                line_price += Prices.objects.get(hw_type='nas_stor').price * int(req_line['nas_count']) *\
                              int(req_line['item_count'])

        #Calculation for new AIX, HPUX and Solaris systems

        if (not error_flag) and (req_line['itemtype2'] == u'new') and\
           ((req_line['itemtype1'] == u'app') or (req_line['itemtype1'] == u'db') or
            (req_line['itemtype1'] == u'dbarch') or (req_line['itemtype1'] == u'other')) and \
           ((req_line['ostype'] == u'aix') or (req_line['ostype'] == u'solaris') or (req_line['ostype'] == u'hpux')):
            if (int(req_line['cpu_count']) <= 64) and (req_line['ostype'] == u'hpux'):
                line_price += Prices.objects.get(hw_type='ia_mid').price * int(req_line['cpu_count']) * \
                              int(req_line['item_count'])
            elif (int(req_line['cpu_count']) <= 64) and (req_line['ostype'] == u'hpux'):
                line_price += Prices.objects.get(hw_type='ia_hiend').price * int(req_line['cpu_count']) *\
                              int(req_line['item_count'])
            if (int(req_line['cpu_count']) <= 128):
                if (req_line['ostype'] == u'aix'):
                    line_price += Prices.objects.get(hw_type='ppc_mid').price * int(req_line['cpu_count']) *\
                                  int(req_line['item_count'])
                if (req_line['ostype'] == u'solaris'):
                    if (req_line['platform_type'] == u't_series'):
                        line_price += Prices.objects.get(hw_type='t_mid').price * int(req_line['cpu_count']) *\
                                      int(req_line['item_count'])
                    elif (req_line['platform_type'] == u'm_series'):
                        line_price += Prices.objects.get(hw_type='m_mid').price * int(req_line['cpu_count']) *\
                                      int(req_line['item_count'])
            elif (int(req_line['cpu_count']) > 128):
                if (req_line['ostype'] == u'aix'):
                    line_price += Prices.objects.get(hw_type='ppc_hiend').price * int(req_line['cpu_count']) *\
                                  int(req_line['item_count'])
                if (req_line['ostype'] == u'solaris'):
                    line_price += Prices.objects.get(hw_type='m_hiend').price * int(req_line['cpu_count']) *\
                                  int(req_line['item_count'])
            if (req_line['itemstatus'] == u'prom'):
                if not (req_line['ostype'] == u'hpux'):
                    line_price += Prices.objects.get(hw_type='symantec_lic').price * int(req_line['cpu_count']) *\
                                  int(req_line['item_count'])
                    line_price += Prices.objects.get(hw_type='symantec_support').price *\
                                  int(req_line['cpu_count']) * int(req_line['item_count']) * 3
                if (req_line['backup_type'] == u'yes') and (int(req_line['san_count']) > 2000) and \
                   not (req_line['itemtype1'] == u'dbarch'):
                    line_price += Prices.objects.get(hw_type='san_stor_full').price *\
                                  int(req_line['san_count']) * int(req_line['item_count'])
                elif (req_line['backup_type'] == u'no') and not (req_line['itemtype1'] == u'dbarch'):
                    line_price += Prices.objects.get(hw_type='san_stor_repl').price *\
                                  int(req_line['san_count']) * int(req_line['item_count'])
                elif (req_line['itemtype1'] == u'dbarch'):
                    line_price += Prices.objects.get(hw_type='san_stor_vmware').price *\
                                  int(req_line['san_count']) * int(req_line['item_count'])
            elif (req_line['itemstatus'] == u'test-nt'):
                line_price += Prices.objects.get(hw_type='san_stor_hiend').price *\
                              int(req_line['san_count']) * int(req_line['item_count'])
            else:
                line_price += Prices.objects.get(hw_type='san_stor_mid').price *\
                              int(req_line['san_count']) * int(req_line['item_count'])
            line_price += Prices.objects.get(hw_type='nas_stor').price * int(req_line['nas_count']) *\
                          int(req_line['item_count'])
        #Calculation for Alteons
        if (not error_flag) and (req_line['itemtype2'] == u'new') and\
           (req_line['itemtype1'] == u'lb'):
            line_price += Prices.objects.get(hw_type='loadbalancer').price * int(req_line['item_count'])

        #Calculation for Datapowers
        if (not error_flag) and (req_line['itemtype2'] == u'new') and\
           (req_line['itemtype1'] == u'dp'):
            line_price += Prices.objects.get(hw_type='datapower').price * int(req_line['item_count'])

        # ---------------------------------------------
        # Calculation for upgrades only
        # ---------------------------------------------

        # Calculation for new x86 systems

        if (not error_flag) and (req_line['itemtype2'] == u'upgrade') and\
           ((req_line['itemtype1'] == u'app') or (req_line['itemtype1'] == u'term') or\
            (req_line['itemtype1'] == u'db')  or (req_line['itemtype1'] == u'other')) and \
           ((req_line['ostype'] == u'windows') or (req_line['ostype'] == u'linux')):
            if (Prices.objects.get(hw_type='x86_ent').price > Prices.objects.get(hw_type='x86_mid').price):
                cpu_price = Prices.objects.get(hw_type='x86_ent').price
            else:
                cpu_price = Prices.objects.get(hw_type='x86_mid').price

            line_price += cpu_price * int(req_line['cpu_count']) * int(req_line['item_count'])
            line_price += Prices.objects.get(hw_type='san_stor_vmware').price * int(req_line['hdd_count']) * \
                          int(req_line['item_count'])
            line_price += Prices.objects.get(hw_type='nas_stor').price * int(req_line['nas_count']) *\
                          int(req_line['item_count'])
            line_price += Prices.objects.get(hw_type='vmware_lic').price * int(req_line['cpu_count']) *\
                          int(req_line['item_count'])
            line_price += Prices.objects.get(hw_type='vmware_support').price * int(req_line['cpu_count']) *\
                          int(req_line['item_count'])
            if (req_line['itemtype1'] == u'db') and (req_line['itemstatus'] == u'prom'):
                line_price += Prices.objects.get(hw_type='san_stor_repl').price * int(req_line['san_count']) *\
                              int(req_line['item_count'])
            elif (req_line['itemtype1'] == u'db') and (req_line['itemstate'] == u'тест(НТ)'):
                line_price += Prices.objects.get(hw_type='san_stor_hiend').price * int(req_line['san_count']) *\
                              int(req_line['item_count'])
            else:
                line_price += Prices.objects.get(hw_type='san_stor_mid').price * int(req_line['san_count']) * \
                              int(req_line['item_count'])

        #Calculation for AIX, HPUX and Solaris upgrades

#        logger.error('LOGGER')
#        logger.error(line_price)
        if (not error_flag) and (req_line['itemtype2'] == u'upgrade') and\
           ((req_line['itemtype1'] == u'app') or (req_line['itemtype1'] == u'db') or\
            (req_line['itemtype1'] == u'dbarch') or (req_line['itemtype1'] == u'other')) and\
           ((req_line['ostype'] == u'aix') or (req_line['ostype'] == u'solaris') or (req_line['ostype'] == u'hpux')):
            if (Prices.objects.get(hw_type='upg_ppc_mid').price > Prices.objects.get(hw_type='upg_ppc_hiend').price):
                aix_cpu_price = Prices.objects.get(hw_type='upg_ppc_mid').price
            else:
                aix_cpu_price = Prices.objects.get(hw_type='upg_ppc_hiend').price
            if (Prices.objects.get(hw_type='upg_t4_mid').price > Prices.objects.get(hw_type='upg_sparc_hiend').price):
                solaris_cpu_price = Prices.objects.get(hw_type='upg_t4_mid').price
            else:
                solaris_cpu_price = Prices.objects.get(hw_type='upg_sparc_hiend').price
            hpux_cpu_price = Prices.objects.get(hw_type='ia_hiend').price
            if (req_line['ostype'] == u'aix'):
                line_price += aix_cpu_price * int(req_line['cpu_count']) * int(req_line['item_count'])
            elif (req_line['ostype'] == u'solaris'):
                line_price += solaris_cpu_price * int(req_line['cpu_count']) * int(req_line['item_count'])
            elif (req_line['ostype'] == u'hpux'):
                line_price += hpux_cpu_price * int(req_line['cpu_count']) * int(req_line['item_count'])
            if (req_line['itemstatus'] == u'prom'):
                if not (req_line['ostype'] == u'hpux'):
                    line_price += Prices.objects.get(hw_type='symantec_lic').price * int(req_line['cpu_count']) *\
                                  int(req_line['item_count'])
                    line_price += Prices.objects.get(hw_type='symantec_support').price *\
                                  int(req_line['cpu_count']) * int(req_line['item_count']) * 3
                if (req_line['backup_type'] == u'yes') and not (req_line['itemtype1'] == u'dbarch'):
                    line_price += Prices.objects.get(hw_type='san_stor_full').price *\
                                  int(req_line['san_count']) * int(req_line['item_count'])
                    line_price += Prices.objects.get(hw_type='san_stor_full').price *\
                                  int(req_line['san_count']) * int(req_line['item_count'])
                elif (req_line['backup_type'] == u'no') and not (req_line['itemtype1'] == u'dbarch'):
                    line_price += Prices.objects.get(hw_type='san_stor_repl').price *\
                                  int(req_line['san_count']) * int(req_line['item_count'])
                elif (req_line['itemtype1'] == u'dbarch'):
                    logger.error('LOGGER')
                    logger.error(line_price)
                    logger.error(Prices.objects.get(hw_type='san_stor_vmware').price)
                    logger.error(int(req_line['san_count']) * int(req_line['item_count']))
                    line_price += Prices.objects.get(hw_type='san_stor_vmware').price *\
                                  int(req_line['san_count']) * int(req_line['item_count'])
                    logger.error(line_price)

            if (req_line['itemstatus'] == u'test-nt'):
                line_price += Prices.objects.get(hw_type='san_stor_hiend').price *\
                              int(req_line['san_count']) * int(req_line['item_count'])
            elif (req_line['itemstatus'] == u'test-other'):
                line_price += Prices.objects.get(hw_type='san_stor_mid').price *\
                              int(req_line['san_count']) * int(req_line['item_count'])
            line_price += Prices.objects.get(hw_type='nas_stor').price * int(req_line['nas_count']) *\
                          int(req_line['item_count'])
#
        # ---------------------------------------------
        # Common position for new systems and upgrades
        # ---------------------------------------------

        #Calculation for windows license (new systems and upgrade)
        if (req_line['ostype'] == u'windows'):
            line_price += Prices.objects.get(hw_type='ms_lic').price * int(req_line['cpu_count'])\
                          * int(req_line['item_count'])

        #Calculation for RHEL support (new systems and upgrade)
        elif (req_line['ostype'] == u'linux'):
            line_price += Prices.objects.get(hw_type='rhel_support').price * int(req_line['cpu_count']) *\
                          int(req_line['item_count'])

        #Calculation for backup (new systems and upgrade)
        if (req_line['backup_type'] == u'yes') and (req_line['itemtype1'] <> u'dp') and\
           (req_line['itemtype1'] <> u'lb'):
            line_price += Prices.objects.get(hw_type='backup_stor').price *\
                          (int(req_line['hdd_count']) + int(req_line['nas_count']) + int(req_line['san_count'])) *\
                          int(req_line['item_count'])


        if ('price' in req_line.keys()) and (req_line['price'] <> u'Ошибка данных') and (not error_flag) and\
           (line_price <> 0):
            req_line['price'] = str(line_price.quantize(Decimal(10) ** -2))
        elif error_flag:
            req_line['price'] = 'Ошибка данных'
            req_line['error'] = '1'

#        logger.error("--------- AFTER")
#        logger.error(req_line)
#        logger.error(error_flag)
#
#        logger.error("--------- ENDED ----------")
        return req_line


def eos_xls_check(xls_filename):
    if not ('xlsx' in xls_filename)  and ('xls' in xls_filename):
        try:
            xls_workbook = open_workbook(xls_filename)
            xls_worksheet = xls_workbook.sheet_by_name(u'Технические требования')
        except:
            return False
        if xls_workbook:
            return True
        else:
            return False
    else:
        return False


def xls_print_content(xls_filename):
    """
    Print all content from worksheet (for testing only)
    """
    try:
        xls_workbook = open_workbook(xls_filename)
        xls_worksheet = xls_workbook.sheet_by_name(u'Технические требования')
    except:
        return False
    num_rows = xls_worksheet.nrows - 1
    num_cells = xls_worksheet.ncols - 1
    curr_row = -1
    while curr_row < num_rows:
        curr_row += 1
        row = xls_worksheet.row(curr_row)
        logger.info("Row - %s" % curr_row)
#        print 'Row:', curr_row
        curr_cell = -1
        while curr_cell < num_cells:
            curr_cell += 1
            # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
            cell_type = xls_worksheet.cell_type(curr_row, curr_cell)
            cell_value = xls_worksheet.cell_value(curr_row, curr_cell)
#            print '	', cell_type, ':', cell_value
            logger.info("%s  -  %s : %s" % (curr_cell, cell_type, cell_value))


def load_eos_from_xls(xls_file):
    EOS_VALS = {}
    if eos_xls_check(xls_file):
#        xls_print_content(xls_file)
        try:
            xls_workbook = open_workbook(xls_file)
            xls_worksheet = xls_workbook.sheet_by_name(u'Технические требования')
        except:
            return None

        EOS_VALS['prjnum'] = str(xls_worksheet.cell_value(xls_vals['prjrow'], xls_vals['prjcell'])).split(".")[0]
        num_rows = xls_worksheet.nrows - 1
        curr_row = xls_vals['eos_start_row']
        req_count = 0
        while curr_row <= num_rows:
            req_count += 1
            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['itemtype1_col'])
            if xls_value == u'Сервер БД':
                EOS_VALS['itemtype1_'+str(req_count)]='db'
            elif xls_value ==  u'Сервер приложений':
                EOS_VALS['itemtype1_'+str(req_count)]='app'
            elif xls_value ==  u'TS':
                EOS_VALS['itemtype1_'+str(req_count)]='term'
            else:
                EOS_VALS['itemtype1_'+str(req_count)]='other'

            EOS_VALS['itemname_'+str(req_count)]=xls_worksheet.cell_value(curr_row, xls_vals['itemname_col'])

            EOS_VALS['servername_'+str(req_count)]=xls_worksheet.cell_value(curr_row, xls_vals['servername_col'])
            if EOS_VALS['servername_'+str(req_count)] == '':
                EOS_VALS['itemtype2_'+str(req_count)] = 'new'
            else:
                EOS_VALS['itemtype2_'+str(req_count)] = 'upgrade'

            EOS_VALS['cpucount_'+str(req_count)]=\
            str(xls_worksheet.cell_value(curr_row, xls_vals['cpucount_col'])).split(".")[0]
            if EOS_VALS['cpucount_'+str(req_count)] == '':
                EOS_VALS['cpucount_'+str(req_count)] = 0
            EOS_VALS['ramcount_'+str(req_count)]=\
            str(xls_worksheet.cell_value(curr_row, xls_vals['ramcount_col'])).split(".")[0]
            if EOS_VALS['ramcount_'+str(req_count)] == '':
                EOS_VALS['ramcount_'+str(req_count)] = 0
            EOS_VALS['hddcount_'+str(req_count)]=\
            str(xls_worksheet.cell_value(curr_row, xls_vals['hddcount_col'])).split(".")[0]
            if EOS_VALS['hddcount_'+str(req_count)] == '':
                EOS_VALS['hddcount_'+str(req_count)] = 0
            EOS_VALS['sancount_'+str(req_count)]=\
            str(xls_worksheet.cell_value(curr_row, xls_vals['sancount_col'])).split(".")[0]
            if EOS_VALS['sancount_'+str(req_count)] == '':
                EOS_VALS['sancount_'+str(req_count)] = 0
            EOS_VALS['nascount_'+str(req_count)]=\
            str(xls_worksheet.cell_value(curr_row, xls_vals['nascount_col'])).split(".")[0]
            if EOS_VALS['nascount_'+str(req_count)] == '':
                EOS_VALS['nascount_'+str(req_count)] = 0
            EOS_VALS['itemcount_'+str(req_count)]=\
            str(xls_worksheet.cell_value(curr_row, xls_vals['itemcount_col'])).split(".")[0]
            if EOS_VALS['itemcount_'+str(req_count)] == '':
                EOS_VALS['itemcount_'+str(req_count)] = 0

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['platform_type_col'])
            if xls_value == u'x86':
                EOS_VALS['platformtype_'+str(req_count)]='x86'
            elif xls_value == u'Power':
                EOS_VALS['platformtype_'+str(req_count)]='power'
            elif xls_value == u'SPARC T':
                EOS_VALS['platformtype_'+str(req_count)]='t_series'
            elif xls_value == u'SPARC 64':
                EOS_VALS['platformtype_'+str(req_count)]='m_series'
            elif xls_value == u'Itanium':
                EOS_VALS['platformtype_'+str(req_count)]='itanium'
            elif xls_value == u'DataPower':
                EOS_VALS['platformtype_'+str(req_count)]='---'
                EOS_VALS['ostype_'+str(req_count)]='---'
                EOS_VALS['itemtype1_'+str(req_count)]='dp'
            elif xls_value == u'Alteon':
                EOS_VALS['platformtype_'+str(req_count)]='---'
                EOS_VALS['ostype_'+str(req_count)]='---'
                EOS_VALS['itemtype1_'+str(req_count)]='lb'
            elif xls_value == u'Другое':
                EOS_VALS['platformtype_'+str(req_count)]='---'
            else:
                EOS_VALS['platformtype_'+str(req_count)]='---'

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['ostype_col'])
            if u'aix' in  xls_value.lower():
                EOS_VALS['ostype_'+str(req_count)]='aix'
            elif u'solaris' in  xls_value.lower():
                EOS_VALS['ostype_'+str(req_count)]='solaris'
            elif (u'linux' in  xls_value.lower()) or (u'rhel' in  xls_value.lower()) or \
                 (u'sles' in  xls_value.lower()):
                EOS_VALS['ostype_'+str(req_count)]='linux'
            elif u'win' in  xls_value.lower():
                EOS_VALS['ostype_'+str(req_count)]='windows'
            elif (u'hp' in  xls_value.lower()) and (u'ux' in  xls_value.lower()):
                EOS_VALS['ostype_'+str(req_count)]='hpux'
            else:
                if not(EOS_VALS['platformtype_'+str(req_count)] == '---'):
                    if EOS_VALS['platformtype_'+str(req_count)] == 'itanium':
                        EOS_VALS['ostype_'+str(req_count)]='hpux'
                    elif EOS_VALS['platformtype_'+str(req_count)] == 'power':
                        EOS_VALS['ostype_'+str(req_count)]='aix'
                    elif (EOS_VALS['platformtype_'+str(req_count)] == 't_series') or \
                         (EOS_VALS['platformtype_'+str(req_count)] == 'm_series'):
                        EOS_VALS['ostype_'+str(req_count)]='solaris'
                    elif EOS_VALS['platformtype_'+str(req_count)] == 'x86':
                        EOS_VALS['ostype_'+str(req_count)]='linux'
                else:
                    EOS_VALS['ostype_'+str(req_count)]='---'

            EOS_VALS['swaddons_'+str(req_count)]=xls_worksheet.cell_value(curr_row, xls_vals['swaddons_col'])

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['itemstatus_col'])
            if xls_value == u'ПРОМ':
                EOS_VALS['itemstatus_'+str(req_count)] = 'prom'
            elif xls_value == u'НТ':
                EOS_VALS['itemstatus_'+str(req_count)] = 'test-nt'
            else:
                EOS_VALS['itemstatus_'+str(req_count)] = 'test-other'

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['lansegment_col'])
            if xls_value == u'ALPHA':
                EOS_VALS['lansegment_'+str(req_count)] = 'alpha'
            elif xls_value == u'SIGMA':
                EOS_VALS['lansegment_'+str(req_count)] = 'sigma'
            elif xls_value == u'TAU':
                EOS_VALS['lansegment_'+str(req_count)] = 'tay'
            else:
                EOS_VALS['lansegment_'+str(req_count)] = 'other'

            EOS_VALS['req_dbtype_'+str(req_count)]=xls_worksheet.cell_value(curr_row, xls_vals['dbtype_col'])

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['clustype_col'])
            if (u'ТР' in xls_value) or (u'ЛОК' in xls_value):
                EOS_VALS['clustype_'+str(req_count)] = 'vcs'
            elif ('На уровне приложения' in xls_value) :
                EOS_VALS['clustype_'+str(req_count)] = 'app'
            else:
                EOS_VALS['clustype_'+str(req_count)] = 'none'

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['backuptype_col'])
            if xls_value == u'НЕТ':
                EOS_VALS['backuptype_'+str(req_count)] = 'no'
            else:
                EOS_VALS['backuptype_'+str(req_count)] = 'yes'
            curr_row += 1
        EOS_VALS['req_count'] = req_count
        logger.error(req_count)
        logger.error(EOS_VALS)
        for i in range(1,req_count+1):
            req_line = {}
            req_line['itemtype2'] = EOS_VALS['itemtype2_'+str(i)]
            req_line['itemtype1'] = EOS_VALS['itemtype1_'+str(i)]
            req_line['itemstatus'] = EOS_VALS['itemstatus_'+str(i)]
            req_line['servername'] = EOS_VALS['servername_'+str(i)]
            req_line['cpu_count'] = EOS_VALS['cpucount_'+str(i)]
            req_line['ram_count'] = EOS_VALS['ramcount_'+str(i)]
            req_line['hdd_count'] = EOS_VALS['hddcount_'+str(i)]
            req_line['san_count'] = EOS_VALS['sancount_'+str(i)]
            req_line['nas_count'] = EOS_VALS['nascount_'+str(i)]
            req_line['item_count'] = EOS_VALS['itemcount_'+str(i)]
            req_line['ostype'] = EOS_VALS['ostype_'+str(i)]
            req_line['platform_type'] = EOS_VALS['platformtype_'+str(i)]
            req_line['lan_segment'] = EOS_VALS['lansegment_'+str(i)]
            req_line['db_type'] = ""
            req_line['cluster_type'] = EOS_VALS['clustype_'+str(i)]
            req_line['backup_type'] = EOS_VALS['backuptype_'+str(i)]
            new_req_line = calculate_req_line(req_line)
            EOS_VALS['price_'+str(i)] = new_req_line['price']
            EOS_VALS['price_hw_'+str(i)] = new_req_line['price_hw']
            EOS_VALS['price_lic_'+str(i)] = new_req_line['price_lic']
            EOS_VALS['price_support_'+str(i)] = new_req_line['price_support']

        return EOS_VALS
    else:
        return None


def getReportStyleSheet(font):
    """Returns a stylesheet object"""
    stylesheet = StyleSheet1()

    #    styles.add(ParagraphStyle(name='hhh2',
    #        fontName = 'Arial',
    #        fontSize=14,
    #        leading=18,
    #        spaceBefore=12,
    #        spaceAfter=6))

    stylesheet.add(ParagraphStyle(name='Normal',
        fontName=font,
        fontSize=10,
        leading=12)
    )

    stylesheet.add(ParagraphStyle(name='BodyText',
        parent=stylesheet['Normal'],
        spaceBefore=6)
    )

    stylesheet.add(ParagraphStyle(name='Italic',
        parent=stylesheet['BodyText'],
        fontName = font)
    )

    stylesheet.add(ParagraphStyle(name='Heading1',
        parent=stylesheet['Normal'],
        fontName = font,
        alignment = TA_CENTER,
        fontSize=18,
        leading=22,
        spaceAfter=6),
        alias='h1')

    stylesheet.add(ParagraphStyle(name='SubTitle',
        parent=stylesheet['Normal'],
        fontName = font,
        alignment = TA_CENTER,
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=6),
        alias='subtitle')

    stylesheet.add(ParagraphStyle(name='Title',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=6),
        alias='title')

    stylesheet.add(ParagraphStyle(name='TableTitle',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=6),
        alias='tabletitle')

    stylesheet.add(ParagraphStyle(name='TableTitleSmall',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=8,
        alignment=TA_CENTER,
        spaceAfter=6),
        alias='tabletitlesmall')

    stylesheet.add(ParagraphStyle(name='Heading2',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=6),
        alias='h2')

    stylesheet.add(ParagraphStyle(name='Heading3',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=12,
        leading=14,
        spaceBefore=12,
        spaceAfter=6),
        alias='h3')

    stylesheet.add(ParagraphStyle(name='Heading4',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=10,
        leading=12,
        spaceBefore=10,
        spaceAfter=4),
        alias='h4')

    stylesheet.add(ParagraphStyle(name='Heading5',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=9,
        leading=10.8,
        spaceBefore=8,
        spaceAfter=4),
        alias='h5')

    stylesheet.add(ParagraphStyle(name='Heading6',
        parent=stylesheet['Normal'],
        fontName = font,
        fontSize=7,
        leading=8.4,
        spaceBefore=6,
        spaceAfter=2),
        alias='h6')

    stylesheet.add(ParagraphStyle(name='Bullet',
        parent=stylesheet['Normal'],
        firstLineIndent=0,
        spaceBefore=3),
        alias='bu')

    stylesheet.add(ParagraphStyle(name='Definition',
        parent=stylesheet['Normal'],
        firstLineIndent=0,
        leftIndent=36,
        bulletIndent=0,
        spaceBefore=6,
        bulletFontName=font),
        alias='df')

    stylesheet.add(ParagraphStyle(name='Code',
        parent=stylesheet['Normal'],
        fontName=font,
        fontSize=7,
        #        leading=8.8,
        firstLineIndent=0
        #        leftIndent=36
    ))

    return stylesheet


def export_eos_to_pdf(eos_items):

    prom_items = []
    test_nt_items = []
    test_items = []
    prom_cost = 0
    prom_cost_hw = 0
    prom_cost_sw = 0
    prom_cost_sup = 0

    test_nt_cost = 0
    test_nt_cost_hw = 0
    test_nt_cost_sw = 0
    test_nt_cost_sup = 0

    test_cost = 0
    test_cost_hw = 0
    test_cost_sw = 0
    test_cost_sup = 0

    project_id = str(eos_items['project_id'])
    project_name = eos_items['project_name']
    eos_items.pop("project_id", None)
    eos_items.pop("project_name", None)

#    filename = path.join(BOC_WORK_DIR, str(int(time())) + ".pdf")
    if project_id == u'0':
        filename = 'eos_' + str(int(time()))
    else:
        filename = 'eos_' + project_id
#        ).split(".")[0]
    rl_config.warnOnMissingFontGlyphs = 0
    pdfmetrics.registerFont(ttfonts.TTFont('Arial', ARIAL_FONT_FILELOCATION))

#    buffer = BytesIO()
    doc = SimpleDocTemplate(path.join(BOC_WORK_DIR, filename + ".pdf"), rightMargin=1*cm,leftMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm)
    styles = getReportStyleSheet('Arial')
    #REPORT TITLE
    Sblogo = Image(path.join(MEDIA_ROOT,'images/sb-logo.jpg'),1 * cm, 1 * cm)
    Sblogo.hAlign='RIGHT'
    if project_id == u'0':
        Title = Paragraph(u'Экспресс-оценка для проекта без номера', styles["Heading1"])
        SubTitle = Paragraph(u' ', styles["SubTitle"])
    else:
        Title = Paragraph(u'Экспресс-оценка для проекта №' + project_id, styles["Heading1"])
        SubTitle = Paragraph(project_name, styles["SubTitle"])
    Elements = [Sblogo, Title, SubTitle]
    logger.error("FINNNNISSHHHH")

    for key in eos_items.keys():
        logger.error(eos_items[key])
        if (eos_items[key]['itemstatus'] == u'prom'):
            prom_items.append(eos_items[key])
            prom_cost += Decimal(eos_items[key]['price'])
            prom_cost_hw += Decimal(eos_items[key]['price_hw'])
            prom_cost_sw += Decimal(eos_items[key]['price_lic'])
            prom_cost_sup += Decimal(eos_items[key]['price_support'])
        elif (eos_items[key]['itemstatus'] == u'test-nt'):
            test_nt_items.append(eos_items[key])
            test_nt_cost += Decimal(eos_items[key]['price'])
            test_nt_cost_hw += Decimal(eos_items[key]['price_hw'])
            test_nt_cost_sw += Decimal(eos_items[key]['price_lic'])
            test_nt_cost_sup += Decimal(eos_items[key]['price_support'])
        elif (eos_items[key]['itemstatus'] == u'test-other'):
            test_items.append(eos_items[key])
            test_cost += Decimal(eos_items[key]['price'])
            test_cost_hw += Decimal(eos_items[key]['price_hw'])
            test_cost_sw += Decimal(eos_items[key]['price_lic'])
            test_cost_sup += Decimal(eos_items[key]['price_support'])

    total_cost = prom_cost + test_nt_cost + test_cost
    total_cost_hw = prom_cost_hw + test_nt_cost_hw + test_cost_hw
    total_cost_sw = prom_cost_sw + test_nt_cost_sw + test_cost_sw
    total_cost_sup = prom_cost_sup + test_nt_cost_sup + test_cost_sup

    ts = [('GRID', (0,0), (-1,-1), 0.25, colors.black),
          ('ALIGN', (1,1), (-1,-1), 'LEFT'),
          ('FONT', (0,0), (-1,-1), 'Arial')]

    reqts = [('GRID', (0,0), (-1,-1), 0.25, colors.black),
               ('ALIGN', (1,1), (-1,-1), 'LEFT'),
               ('FONT', (0,0), (-1,-1), 'Arial'),
               ('FONTSIZE', (0,0), (-1,-1), 9)]

    #Таблица стоимсоти
    Elements.append(Spacer(0, 0.5 * cm))
    Elements.append(Paragraph(u'Оценка стоимости', styles["Heading2"]))
    Elements.append(Spacer(0, 0.1 * cm))
    data = [['Среды', 'Общая стоимость', 'Оборудование', 'Лицензии', 'Поддержка за год'],
            [ u'Промышленные среды', str(prom_cost)+' $', str(prom_cost_hw)+' $', str(prom_cost_sw)+' $',
              str(prom_cost_sup)+' $'],
            [ u'Среды нарузочного тестирования', str(test_nt_cost)+' $', str(test_nt_cost_hw)+' $',
              str(test_nt_cost_sw)+' $', str(test_nt_cost_sup)+' $'],
            [ u'Прочих тестовые среды', str(test_cost)+' $', str(test_cost_hw)+' $', str(test_cost_sw)+' $',
              str(test_cost_sup)+' $'],
            [ u'Итого', str(total_cost)+' $', str(total_cost_hw)+' $', str(total_cost_sw)+' $',
              str(total_cost_sup)+' $'],
    ]
    table = Table(data, style=ts, hAlign='CENTER')
    Elements.append(table)

    #Промышелнные среды
    Elements.append(Spacer(0, 0.5 * cm))
    Elements.append(Paragraph(u'Промышленные среды', styles["Heading2"]))
    Elements.append(Spacer(0, 0.1 * cm))
    if prom_items:
        data = [[Paragraph(u'Кол-во позиций', styles["TableTitleSmall"]),
                 Paragraph(u'Тип позиции', styles["TableTitleSmall"]),
                 Paragraph(u'Название позиции', styles["TableTitleSmall"]),
                 Paragraph(u'Статус', styles["TableTitleSmall"]),
                 Paragraph(u'Платформа', styles["TableTitleSmall"]),
                 Paragraph(u'ОС', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во ядер', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во ОЗУ', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во СХД, Гб', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во СХД,SAN Гб', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во СХД,NAS Гб', styles["TableTitleSmall"]),
                 Paragraph(u'Стоимость, $', styles["TableTitleSmall"])
                ]]
        for item in prom_items:
            data.append([Paragraph(item['item_count'], styles["Code"]),
                Paragraph(ru_vals[item['itemtype2']], styles["Code"]),
                Paragraph(ru_vals[item['itemtype1']], styles["Code"]),
                Paragraph(ru_vals[item['itemstatus']], styles["Code"]),
                Paragraph(ru_vals[item['platform_type']], styles["Code"]),
                Paragraph(ru_vals[item['ostype']], styles["Code"]),
                Paragraph(str(item['cpu_count']), styles["Code"]),
                Paragraph(str(item['ram_count']), styles["Code"]),
                Paragraph(str(item['hdd_count']), styles["Code"]),
                Paragraph(str(item['san_count']), styles["Code"]),
                Paragraph(str(item['nas_count']), styles["Code"]),
                Paragraph(str(item['price']), styles["Code"])
            ])
        table = Table(data, style=reqts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)
    else:
        Elements.append(Paragraph(u'Промышленных сред нет', styles["Heading3"]))

    #Среды НТ
    Elements.append(Spacer(0, 0.5 * cm))
    Elements.append(Paragraph(u'Среды нагрузочного тестирования', styles["Heading2"]))
    Elements.append(Spacer(0, 0.1 * cm))
    if test_nt_items:
        data = [[Paragraph(u'Кол-во позиций', styles["TableTitleSmall"]),
                 Paragraph(u'Тип позиции', styles["TableTitleSmall"]),
                 Paragraph(u'Название позиции', styles["TableTitleSmall"]),
                 Paragraph(u'Статус', styles["TableTitleSmall"]),
                 Paragraph(u'Платформа', styles["TableTitleSmall"]),
                 Paragraph(u'ОС', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во ядер', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во ОЗУ', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во СХД, Гб', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во СХД,SAN Гб', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во СХД,NAS Гб', styles["TableTitleSmall"]),
                 Paragraph(u'Стоимость, $', styles["TableTitleSmall"])
                ]]
        for item in test_nt_items:
            data.append([Paragraph(item['item_count'], styles["Code"]),
                Paragraph(ru_vals[item['itemtype2']], styles["Code"]),
                Paragraph(ru_vals[item['itemtype1']], styles["Code"]),
                Paragraph(ru_vals[item['itemstatus']], styles["Code"]),
                Paragraph(ru_vals[item['platform_type']], styles["Code"]),
                Paragraph(ru_vals[item['ostype']], styles["Code"]),
                Paragraph(str(item['cpu_count']), styles["Code"]),
                Paragraph(str(item['ram_count']), styles["Code"]),
                Paragraph(str(item['hdd_count']), styles["Code"]),
                Paragraph(str(item['san_count']), styles["Code"]),
                Paragraph(str(item['nas_count']), styles["Code"]),
                Paragraph(str(item['price']), styles["Code"])
            ])
        table = Table(data, style=reqts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)
    else:
        Elements.append(Paragraph(u'Cред нагрузочного тестирования нет', styles["Heading3"]))

    #Тестовые среды
    Elements.append(Spacer(0, 0.5 * cm))
    Elements.append(Paragraph(u'Прочие тестовые среды', styles["Heading2"]))
    Elements.append(Spacer(0, 0.1 * cm))
    if test_items:
        data = [[Paragraph(u'Кол-во позиций', styles["TableTitleSmall"]),
                 Paragraph(u'Тип позиции', styles["TableTitleSmall"]),
                 Paragraph(u'Название позиции', styles["TableTitleSmall"]),
                 Paragraph(u'Статус', styles["TableTitleSmall"]),
                 Paragraph(u'Платформа', styles["TableTitleSmall"]),
                 Paragraph(u'ОС', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во ядер', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во ОЗУ', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во СХД, Гб', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во СХД,SAN Гб', styles["TableTitleSmall"]),
                 Paragraph(u'Кол-во СХД,NAS Гб', styles["TableTitleSmall"]),
                 Paragraph(u'Стоимость, $', styles["TableTitleSmall"])
                ]]
        for item in test_items:
            data.append([Paragraph(item['item_count'], styles["Code"]),
                Paragraph(ru_vals[item['itemtype2']], styles["Code"]),
                Paragraph(ru_vals[item['itemtype1']], styles["Code"]),
                Paragraph(ru_vals[item['itemstatus']], styles["Code"]),
                Paragraph(ru_vals[item['platform_type']], styles["Code"]),
                Paragraph(ru_vals[item['ostype']], styles["Code"]),
                Paragraph(str(item['cpu_count']), styles["Code"]),
                Paragraph(str(item['ram_count']), styles["Code"]),
                Paragraph(str(item['hdd_count']), styles["Code"]),
                Paragraph(str(item['san_count']), styles["Code"]),
                Paragraph(str(item['nas_count']), styles["Code"]),
                Paragraph(str(item['price']), styles["Code"])
            ])
        table = Table(data, style=reqts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)
    else:
        Elements.append(Paragraph(u'Прочих сред тестирования нет', styles["Heading3"]))

    doc.pagesize = landscape(A4)
    doc.build(Elements)
#    response.write(buffer.getvalue())
#    buffer.close()
    return filename



def load_eos_from_xls_new(xls_file):
    EOS_VALS = {}
    if eos_xls_check(xls_file):
    #        xls_print_content(xls_file)
        try:
            xls_workbook = open_workbook(xls_file)
            xls_worksheet = xls_workbook.sheet_by_name(u'Технические требования')
        except:
            return None

        EOS_VALS['prjnum'] = str(xls_worksheet.cell_value(xls_vals['prjrow'], xls_vals['prjcell'])).split(".")[0]
        num_rows = xls_worksheet.nrows - 1
        curr_row = xls_vals['eos_start_row']
        req_count = 0
        while curr_row <= num_rows:
            req_line = {}
            req_count += 1
            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['itemtype1_col'])
            if xls_value == u'Сервер БД':
                req_line['itemtype1']='db'
            elif xls_value ==  u'Сервер приложений':
                req_line['itemtype1']='app'
            elif xls_value ==  u'TS':
                req_line['itemtype1']='term'
            else:
                req_line['itemtype1']='other'

            req_line['itemname']=xls_worksheet.cell_value(curr_row, xls_vals['itemname_col'])

            req_line['servername']=xls_worksheet.cell_value(curr_row, xls_vals['servername_col'])
            if req_line['servername'] == '':
                req_line['itemtype2'] = 'new'
            else:
                req_line['itemtype2'] = 'upgrade'

            req_line['cpu_count']= str(xls_worksheet.cell_value(curr_row, xls_vals['cpucount_col'])).split(".")[0]
            if req_line['cpu_count'] == '':
                req_line['cpu_count'] = 0
            req_line['ram_count']= str(xls_worksheet.cell_value(curr_row, xls_vals['ramcount_col'])).split(".")[0]
            if req_line['ram_count'] == '':
                req_line['ram_count'] = 0
            req_line['hdd_count']= str(xls_worksheet.cell_value(curr_row, xls_vals['hddcount_col'])).split(".")[0]
            if req_line['hdd_count'] == '':
                req_line['hdd_count'] = 0
            req_line['san_count']= str(xls_worksheet.cell_value(curr_row, xls_vals['sancount_col'])).split(".")[0]
            if req_line['san_count'] == '':
                req_line['san_count'] = 0
            req_line['nas_count']= str(xls_worksheet.cell_value(curr_row, xls_vals['nascount_col'])).split(".")[0]
            if req_line['nas_count'] == '':
                req_line['nas_count'] = 0
            req_line['item_count']= str(xls_worksheet.cell_value(curr_row, xls_vals['itemcount_col'])).split(".")[0]
            if req_line['item_count'] == '':
                req_line['item_count'] = 0

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['platform_type_col'])
            if xls_value == u'x86':
                req_line['platform_type']='x86'
            elif xls_value == u'Power':
                req_line['platform_type']='power'
            elif xls_value == u'SPARC T':
                req_line['platform_type']='t_series'
            elif xls_value == u'SPARC 64':
                req_line['platform_type']='m_series'
            elif xls_value == u'Itanium':
                req_line['platform_type']='itanium'
            elif xls_value == u'DataPower':
                req_line['platform_type']='---'
                req_line['ostype']='---'
                req_line['itemtype1']='dp'
            elif xls_value == u'Alteon':
                req_line['platform_type']='---'
                req_line['ostype']='---'
                req_line['itemtype1']='lb'
            elif xls_value == u'Другое':
                req_line['platform_type']='---'
            else:
                req_line['platform_type']='---'

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['ostype_col'])
            if u'aix' in  xls_value.lower():
                req_line['ostype']='aix'
            elif u'solaris' in  xls_value.lower():
                req_line['ostype']='solaris'
            elif (u'linux' in  xls_value.lower()) or (u'rhel' in  xls_value.lower()) or\
                 (u'sles' in  xls_value.lower()):
                req_line['ostype']='linux'
            elif u'win' in  xls_value.lower():
                req_line['ostype']='windows'
            elif (u'hp' in  xls_value.lower()) and (u'ux' in  xls_value.lower()):
                req_line['ostype']='hpux'
            else:
                if not(req_line['platform_type'] == '---'):
                    if req_line['platform_type'] == 'itanium':
                        req_line['ostype']='hpux'
                    elif req_line['platform_type'] == 'power':
                        req_line['ostype']='aix'
                    elif (req_line['platform_type'] == 't_series') or (req_line['platform_type'] == 'm_series'):
                        req_line['ostype']='solaris'
                    elif req_line['platform_type'] == 'x86':
                        req_line['ostype']='linux'
                else:
                    req_line['ostype']='---'

            req_line['swaddons']=xls_worksheet.cell_value(curr_row, xls_vals['swaddons_col'])

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['itemstatus_col'])
            if xls_value == u'ПРОМ':
                req_line['itemstatus'] = 'prom'
            elif xls_value == u'НТ':
                req_line['itemstatus'] = 'test-nt'
            else:
                req_line['itemstatus'] = 'test-other'

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['lansegment_col'])
            if xls_value == u'ALPHA':
                req_line['lan_segment'] = 'alpha'
            elif xls_value == u'SIGMA':
                req_line['lan_segment'] = 'sigma'
            elif xls_value == u'TAU':
                req_line['lan_segment'] = 'tay'
            else:
                req_line['lan_segment'] = 'other'

            req_line['req_dbtype']=xls_worksheet.cell_value(curr_row, xls_vals['dbtype_col'])

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['clustype_col'])
            if (u'ТР' in xls_value) or (u'ЛОК' in xls_value):
                req_line['cluster_type'] = 'vcs'
            elif (u'На уровне приложения' in xls_value) :
                req_line['cluster_type'] = 'app'
            else:
                req_line['cluster_type'] = 'none'

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['backuptype_col'])
            if xls_value == u'НЕТ':
                req_line['backup_type'] = 'no'
            else:
                req_line['backup_type'] = 'yes'
            curr_row += 1
            if (req_line['item_count'] <> 0) and (req_line['item_count'] <> ""):
                req_line = calculate_req_line(req_line)
                for key in req_line.keys():
                    EOS_VALS[key+'_'+str(req_count)] = req_line[key]
        EOS_VALS['req_count'] = req_count

#                EOS_VALS['itemtype2_' + str(i)] = req_line['itemtype2']
#                EOS_VALS['itemtype1_' + str(i)] = req_line['itemtype1']
#                EOS_VALS['itemstatus_' + str(i)] = req_line['itemstatus']
#                EOS_VALS['servername_' + str(i)] = req_line['servername']
#                EOS_VALS['cpucount_' + str(i)] = req_line['cpu_count']
#                EOS_VALS['ramcount_' + str(i)] = req_line['ram_count']
#                EOS_VALS['hddcount_' + str(i)] = req_line['hdd_count']
#                EOS_VALS['sancount_' + str(i)] = req_line['san_count']
#                req_line['nas_count'] = EOS_VALS['nascount_' + str(i)]
#                req_line['item_count'] = EOS_VALS['itemcount_' + str(i)]
#                req_line['ostype'] = EOS_VALS['ostype_' + str(i)]
#                req_line['platform_type'] = EOS_VALS['platformtype_' + str(i)]
#                req_line['lan_segment'] = EOS_VALS['lansegment_' + str(i)]
#                req_line['db_type'] = ""
#                req_line['cluster_type'] = EOS_VALS['clustype_' + str(i)]
#                req_line['backup_type'] = EOS_VALS['backuptype_' + str(i)]
#                new_req_line = calculate_req_line(req_line)
#                EOS_VALS['price_' + str(i)] = new_req_line['price']
#                EOS_VALS['price_hw_' + str(i)] = new_req_line['price_hw']
#                EOS_VALS['price_lic_' + str(i)] = new_req_line['price_lic']
#                EOS_VALS['price_support_' + str(i)] = new_req_line['price_support']

                #        EOS_VALS['req_count'] = req_count
#        logger.error(req_count)
#        logger.error(EOS_VALS)
#        for i in range(1,req_count+1):
#            req_line = {}
#            req_line['itemtype2'] = EOS_VALS['itemtype2_'+str(i)]
#            req_line['itemtype1'] = EOS_VALS['itemtype1_'+str(i)]
#            req_line['itemstatus'] = EOS_VALS['itemstatus_'+str(i)]
#            req_line['servername'] = EOS_VALS['servername_'+str(i)]
#            req_line['cpu_count'] = EOS_VALS['cpucount_'+str(i)]
#            req_line['ram_count'] = EOS_VALS['ramcount_'+str(i)]
#            req_line['hdd_count'] = EOS_VALS['hddcount_'+str(i)]
#            req_line['san_count'] = EOS_VALS['sancount_'+str(i)]
#            req_line['nas_count'] = EOS_VALS['nascount_'+str(i)]
#            req_line['item_count'] = EOS_VALS['itemcount_'+str(i)]
#            req_line['ostype'] = EOS_VALS['ostype_'+str(i)]
#            req_line['platform_type'] = EOS_VALS['platformtype_'+str(i)]
#            req_line['lan_segment'] = EOS_VALS['lansegment_'+str(i)]
#            req_line['db_type'] = ""
#            req_line['cluster_type'] = EOS_VALS['clustype_'+str(i)]
#            req_line['backup_type'] = EOS_VALS['backuptype_'+str(i)]
#            new_req_line = calculate_req_line(req_line)
#            EOS_VALS['price_'+str(i)] = new_req_line['price']
#            EOS_VALS['price_hw_'+str(i)] = new_req_line['price_hw']
#            EOS_VALS['price_lic_'+str(i)] = new_req_line['price_lic']
#            EOS_VALS['price_support_'+str(i)] = new_req_line['price_support']

        return EOS_VALS
    else:
        return None
