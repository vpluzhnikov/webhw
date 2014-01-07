# -*- coding: utf-8 -*-
__author__ = 'vs'

from logging import getLogger
from bupl.models import Prices
from decimal import *
from time import time

logger = getLogger(__name__)

def calculate_req_line(req_line):
    """
    Calculates prices for requrements and modify self.data with price values
    """
    req_line['price'] = '0'
    req_line['error'] = '0'
    error_flag = False
    line_price = 0
    if req_line.keys() > 0:
        logger.error("--------- BEFORE")
        logger.error(req_line)

#        ---------------------------------------------
#        Calculation for new systems only
#        ---------------------------------------------

#        Calculation for new x86 systems
        if (not error_flag) and (req_line['itemtype2'] == u'new') and\
           ((req_line['itemtype1'] == u'app') or (req_line['itemtype1'] == u'term') or
            (req_line['itemtype1'] == u'db')) and\
           ((req_line['ostype'] == u'windows') or (req_line['ostype'] == u'linux')):
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

        #Calculation for new AIX and Solaris systems
        if (not error_flag) and (req_line['itemtype2'] == u'new') and\
           ((req_line['itemtype1'] == u'app') or (req_line['itemtype1'] == u'db')) and\
           ((req_line['ostype'] == u'aix') or (req_line['ostype'] == u'solaris')):
            if (int(req_line['cpu_count']) <= 128):
                if (req_line['ostype'] == u'aix'):
                    line_price += Prices.objects.get(hw_type='ppc_mid').price * int(req_line['cpu_count']) *\
                                  int(req_line['item_count'])
                if (req_line['ostype'] == u'solaris'):
                    line_price += Prices.objects.get(hw_type='t_mid').price * int(req_line['cpu_count']) *\
                                  int(req_line['item_count'])
            elif (int(req_line['cpu_count']) > 128):
                if (req_line['ostype'] == u'aix'):
                    line_price += Prices.objects.get(hw_type='ppc_hiend').price * int(req_line['cpu_count']) *\
                                  int(req_line['item_count'])
                if (req_line['ostype'] == u'solaris'):
                    line_price += Prices.objects.get(hw_type='sparc_hiend').price * int(req_line['cpu_count']) *\
                                  int(req_line['item_count'])
            logger.error("--------- 111111111111")
            logger.error(line_price)
            if (req_line['itemstatus'] == u'prom'):
                logger.error("--------- 222222222222")
                logger.error(line_price)
                line_price += Prices.objects.get(hw_type='symantec_lic').price * int(req_line['cpu_count']) *\
                              int(req_line['item_count'])
                logger.error("--------- 333333333333")
                logger.error(line_price)
                line_price += Prices.objects.get(hw_type='symantec_support').price *\
                              int(req_line['cpu_count']) * int(req_line['item_count']) * 3
                if (req_line['backup_type'] == u'yes') and (int(req_line['san_count']) > 2000):
                    line_price += Prices.objects.get(hw_type='san_stor_full').price *\
                                  int(req_line['san_count']) * int(req_line['item_count'])
                else:
                    line_price += Prices.objects.get(hw_type='san_stor_repl').price *\
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
        #Calculation for new x86 systems
#        if (not error_flag) and (req_line['itemtype2'] == u'upgrade') and\
#           ((req_line['itemtype1'] == u'app') or (req_line['itemtype1'] == u'term') or
#            (req_line['itemtype1'] == u'db')) and\
#           ((req_line['ostype'] == u'windows') or (req_line['ostype'] == u'linux')):
#            if (int(req_line['cpu_count']) + int(req_line['ex_cpucount']) <= 16) and (not int(req_line['ex_cpucount']) == 0):
            #                        logger.error("excpucount = %s" % (int(line['ex_cpucount'])))
#                line_price += Prices.objects.get(hw_type='x86_ent').price * int(req_line['cpu_count']) *\
#                              int(req_line['item_count'])
#                line_price += Prices.objects.get(hw_type='san_stor_vmware').price * int(req_line['hdd_count']) *\
#                              int(req_line['item_count'])
#                line_price += Prices.objects.get(hw_type='san_stor_mid').price * int(req_line['san_count']) *\
#                              int(req_line['item_count'])
#                line_price += Prices.objects.get(hw_type='nas_stor').price * int(req_line['nas_count']) *\
#                              int(req_line['item_count'])
#                line_price += Prices.objects.get(hw_type='vmware_lic').price * int(req_line['cpu_count']) *\
#                              int(req_line['item_count'])
#                line_price += Prices.objects.get(hw_type='vmware_support').price * int(req_line['cpu_count']) *\
#                              int(req_line['item_count'])
#            elif ((int(req_line['ex_cpucount']) > 16) or (int(req_line['ex_cpucount']) == 0)):
#                req_line['cpu_count'] = 0
#                req_line['hdd_count'] = 0
#                if (req_line['itemtype1'] == u'Сервер СУБД') and (req_line['itemstate'] == u'пром'):
#                    line_price += Prices.objects.get(hw_type='san_stor_repl').price * int(req_line['san_count']) *\
#                                  int(req_line['item_count'])
#                elif (req_line['itemtype1'] == u'Сервер СУБД') and (req_line['itemstate'] == u'тест(НТ)'):
#                    line_price += Prices.objects.get(hw_type='san_stor_hiend').price * int(req_line['san_count']) *\
#                                  int(req_line['item_count'])
#                else:
#                    line_price += Prices.objects.get(hw_type='san_stor_mid').price * int(req_line['san_count']) *\
#                                  int(req_line['item_count'])
#                line_price += Prices.objects.get(hw_type='nas_stor').price * int(req_line['nas_count']) *\
#                              int(req_line['item_count'])
#            else:
#                logger("Error in x86 upgrade calculation for line = %s" % (req_line))
#                error_flag = True

                #Calculation for AIX and Solaris upgrades
#        if (not error_flag) and (req_line['itemtype2'] == u'модернизация') and\
#           ((req_line['itemtype1'] == u'Сервер приложения') or (req_line['itemtype1'] == u'Сервер СУБД')) and\
#           ((req_line['ostype'] == u'IBM AIX') or (req_line['ostype'] == u'Oracle Solaris')):
#            if (int(req_line['cpu_count']) + int(req_line['ex_cpucount']) <= 128)and(not int(req_line['ex_cpucount']) == 0):
#                if (req_line['ostype'] == u'IBM AIX'):
#                    line_price += Prices.objects.get(hw_type='ppc_mid').price * int(req_line['cpu_count']) *\
#                                  int(req_line['item_count'])
#                if (req_line['ostype'] == u'Oracle Solaris'):
#                    line_price += Prices.objects.get(hw_type='t_mid').price * int(req_line['cpu_count']) *\
#                                  int(req_line['item_count'])
#            else:
#                if (req_line['ostype'] == u'IBM AIX'):
#                    line_price += Prices.objects.get(hw_type='ppc_hiend').price * int(req_line['cpu_count']) *\
#                                  int(req_line['item_count'])
#                if (req_line['ostype'] == u'Oracle Solaris'):
#                    line_price += Prices.objects.get(hw_type='sparc_hiend').price * int(req_line['cpu_count']) *\
#                                  int(req_line['item_count'])
#            if (req_line['itemstate'] == u'пром'):
#                line_price += Prices.objects.get(hw_type='symantec_lic').price * int(req_line['cpu_count']) *\
#                              int(req_line['item_count'])
#                line_price += Prices.objects.get(hw_type='symantec_support').price *\
#                              int(req_line['cpu_count']) * int(req_line['item_count']) * 3
#                if (req_line['backup_type'] == u'да')and((int(req_line['san_count']) + int(req_line['ex_san_count'])) > 2000):
#                    line_price += Prices.objects.get(hw_type='san_stor_full').price *\
#                                  int(req_line['san_count']) * int(req_line['item_count'])
#                else:
#                    line_price += Prices.objects.get(hw_type='san_stor_repl').price *\
#                                  int(req_line['san_count']) * int(req_line['item_count'])
#            elif (req_line['itemstate'] == u'тест(НТ)'):
#                line_price += Prices.objects.get(hw_type='san_stor_hiend').price *\
#                              int(req_line['san_count']) * int(req_line['item_count'])
#            else:
#                line_price += Prices.objects.get(hw_type='san_stor_mid').price *\
#                              int(req_line['san_count']) * int(req_line['item_count'])
#            line_price += Prices.objects.get(hw_type='nas_stor').price * int(req_line['nas_count']) *\
#                          int(req_line['item_count'])
#
        # ---------------------------------------------
        # Common position for new systems and upgrades
        # ---------------------------------------------

        #Calculation for windows licence (new systems and upgrade)
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

        logger.error("--------- AFTER")
        logger.error(req_line)
        logger.error(error_flag)

        if ('price' in req_line.keys()) and (req_line['price'] <> u'Ошибка данных') and (not error_flag) and\
           (line_price <> 0):
            req_line['price'] = str(line_price.quantize(Decimal(10) ** -2))
        elif error_flag:
            req_line['price'] = 'Ошибка данных'
            req_line['error'] = '1'


        logger.error("--------- ENDED ----------")
        return req_line
