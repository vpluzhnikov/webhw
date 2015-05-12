# -*- coding: utf-8 -*-
__author__ = 'vs'
from models import Prices
from decimal import *
from math import ceil




def calculate_req_line(req_line):
    """
    calculate_req_line(req_line) calculates three prices (hw, licenses, support) for line of requirements
    """
    prices_dic = {}
    price_hw = 0
    price_lic = 0
    price_support = 0
    total_price = 0

    lic_vmware_count = 0
    lic_vmware_cost = 0
    lic_ms_count = 0
    lic_ms_cost = 0
    lic_symantec_count = 0
    lic_symantec_cost = 0
    lic_oracle_count = 0
    lic_oracle_cost = 0
    lic_mssql_count = 0
    lic_mssql_cost = 0

    supp_rhel_count = 0
    supp_rhel_cost = 0
    supp_vmware_count = 0
    supp_vmware_cost = 0
    supp_symantec_count = 0
    supp_symantec_cost = 0
    supp_oracle_count = 0
    supp_oracle_cost = 0


    k_vm = 1.0


    lic = 0
    support = 0
    cpu_price = 0
    dcmcod_rent_price = 0
    drdc_rent_price = 0
    dc_book_price = 0
    dc_startup_price = 0
    dc_price = 0
    san_price = 0
    intdisks_price = 0
    backup_price = 0
    appliance_price = 0

#   Loading current prices from DB
    for price in Prices.objects.all():
        prices_dic[price.hw_type] = {'price' : Decimal(price.price),
                                     'dcmcod_rent_price' : Decimal(price.dcmcod_rent_price),
                                     'drdc_rent_price' : Decimal(price.drdc_rent_price),
                                     'dc_book_price' : Decimal(price.dc_book_price),
                                     'dc_startup_price' : Decimal(price.dc_startup_price),
                                     }


#   Hardware price calculation for CPUs or Appliances
    if (u'x86' in req_line['platform_type']) and (req_line['itemtype1'] <> u'mqdmz'):
        if (req_line['platform_type'] == 'x86'):
            cpu_price = prices_dic['x86_mid']['price']
            dc_book_price = prices_dic['x86_mid']['dc_book_price']
            dcmcod_rent_price = prices_dic['x86_mid']['dcmcod_rent_price']
            drdc_rent_price = prices_dic['x86_mid']['drdc_rent_price']
            dc_startup_price = prices_dic['x86_mid']['dc_startup_price']
        elif (req_line['platform_type'] == 'x86_vm'):
            cpu_price = prices_dic['x86_ent']['price']
            dc_book_price = prices_dic['x86_ent']['dc_book_price']
            dcmcod_rent_price = prices_dic['x86_ent']['dcmcod_rent_price']
            drdc_rent_price = prices_dic['x86_ent']['drdc_rent_price']
            dc_startup_price = prices_dic['x86_ent']['dc_startup_price']
    elif (req_line['platform_type'] == u'power'):
        if (int(req_line['cpu_count']) > 128):
            if (req_line['itemtype2'] == u'upgrade'):
                cpu_price = prices_dic['upg_ppc_hiend']['price']
                dc_book_price = prices_dic['upg_ppc_hiend']['dc_book_price']
                dcmcod_rent_price = prices_dic['upg_ppc_hiend']['dcmcod_rent_price']
                drdc_rent_price = prices_dic['upg_ppc_hiend']['drdc_rent_price']
                dc_startup_price = prices_dic['upg_ppc_hiend']['dc_startup_price']
            else:
                cpu_price = prices_dic['ppc_hiend']['price']
                dc_book_price = prices_dic['ppc_hiend']['dc_book_price']
                dcmcod_rent_price = prices_dic['ppc_hiend']['dcmcod_rent_price']
                drdc_rent_price = prices_dic['ppc_hiend']['drdc_rent_price']
                dc_startup_price = prices_dic['ppc_hiend']['dc_startup_price']
        else:
            if (req_line['itemtype2'] == u'upgrade'):
                cpu_price = prices_dic['upg_ppc_mid']['price']
                dc_book_price = prices_dic['upg_ppc_mid']['dc_book_price']
                dcmcod_rent_price = prices_dic['upg_ppc_mid']['dcmcod_rent_price']
                drdc_rent_price = prices_dic['upg_ppc_mid']['drdc_rent_price']
                dc_startup_price = prices_dic['upg_ppc_mid']['dc_startup_price']
            else:
                cpu_price = prices_dic['ppc_mid']['price']
                dc_book_price = prices_dic['ppc_mid']['dc_book_price']
                dcmcod_rent_price = prices_dic['ppc_mid']['dcmcod_rent_price']
                drdc_rent_price = prices_dic['ppc_mid']['drdc_rent_price']
                dc_startup_price = prices_dic['ppc_mid']['dc_startup_price']
    elif (u'_series' in req_line['platform_type']):
        if (int(req_line['cpu_count']) > 128):
            if (req_line['itemtype2'] == u'upgrade'):
                cpu_price = prices_dic['m_hiend']['price']
                dc_book_price = prices_dic['m_hiend']['dc_book_price']
                dcmcod_rent_price = prices_dic['m_hiend']['dcmcod_rent_price']
                drdc_rent_price = prices_dic['m_hiend']['drdc_rent_price']
                dc_startup_price = prices_dic['m_hiend']['dc_startup_price']
                req_line['platform_type'] = u'm_series'
            else:
                cpu_price = prices_dic['m_hiend']['price']
                dc_book_price = prices_dic['m_hiend']['dc_book_price']
                dcmcod_rent_price = prices_dic['m_hiend']['dcmcod_rent_price']
                drdc_rent_price = prices_dic['m_hiend']['drdc_rent_price']
                dc_startup_price = prices_dic['m_hiend']['dc_startup_price']
                req_line['platform_type'] = u'm_series'
        else:
            cpu_price = prices_dic['t_mid']['price']
            dc_book_price = prices_dic['t_mid']['dc_book_price']
            dcmcod_rent_price = prices_dic['t_mid']['dcmcod_rent_price']
            drdc_rent_price = prices_dic['t_mid']['drdc_rent_price']
            dc_startup_price = prices_dic['t_mid']['dc_startup_price']
            req_line['platform_type'] = u't_series'
    elif (req_line['platform_type'] == u'itanium'):
        if (int(req_line['cpu_count']) > 64):
            if (req_line['itemtype2'] == u'upgrade'):
                cpu_price = prices_dic['ia_hiend']['price']
                dc_book_price = prices_dic['ia_hiend']['dc_book_price']
                dcmcod_rent_price = prices_dic['ia_hiend']['dcmcod_rent_price']
                drdc_rent_price = prices_dic['ia_hiend']['drdc_rent_price']
                dc_startup_price = prices_dic['ia_hiend']['dc_startup_price']
            else:
                cpu_price = prices_dic['ia_hiend']['price']
                dc_book_price = prices_dic['ia_hiend']['dc_book_price']
                dcmcod_rent_price = prices_dic['ia_hiend']['dcmcod_rent_price']
                drdc_rent_price = prices_dic['ia_hiend']['drdc_rent_price']
                dc_startup_price = prices_dic['ia_hiend']['dc_startup_price']
        else:
            cpu_price = prices_dic['ia_mid']['price']
            dc_book_price = prices_dic['ia_mid']['dc_book_price']
            dcmcod_rent_price = prices_dic['ia_mid']['dcmcod_rent_price']
            drdc_rent_price = prices_dic['ia_mid']['drdc_rent_price']
            dc_startup_price = prices_dic['ia_mid']['dc_startup_price']
    else:
        if (req_line['itemtype1'] == u'dp'):
            appliance_price = prices_dic['datapower']['price']
            dc_book_price = prices_dic['datapower']['dc_book_price']
            dcmcod_rent_price = prices_dic['datapower']['dcmcod_rent_price']
            drdc_rent_price = prices_dic['datapower']['drdc_rent_price']
            dc_startup_price = prices_dic['datapower']['dc_startup_price']
        elif (req_line['itemtype1'] == u'lb'):
            appliance_price = prices_dic['loadbalancer']['price']
            dc_book_price = prices_dic['loadbalancer']['dc_book_price']
            dcmcod_rent_price = prices_dic['loadbalancer']['dcmcod_rent_price']
            drdc_rent_price = prices_dic['loadbalancer']['drdc_rent_price']
            dc_startup_price = prices_dic['loadbalancer']['dc_startup_price']
        elif (req_line['itemtype1'] == u'mqdmz'):
            appliance_price = prices_dic['mqdmz']['price']
            dc_book_price = prices_dic['mqdmz']['dc_book_price']
            dcmcod_rent_price = prices_dic['mqdmz']['dcmcod_rent_price']
            drdc_rent_price = prices_dic['mqdmz']['drdc_rent_price']
            dc_startup_price = prices_dic['mqdmz']['dc_startup_price']

    if cpu_price <> 0:
#        print "cpuprice - " + str(cpu_price)
#        print "cpu dc_book_price - " + str(dc_book_price)
#        print "cpu dcmcod_rent_price - " + str(dcmcod_rent_price)
#        print "cpu drdc_rent_price - " + str(drdc_rent_price)
#        print "cpu dc_startup_price - " + str(dc_startup_price)
        price_hw += int(req_line['cpu_count']) * int(req_line['item_count']) * cpu_price
        if (req_line['itemstatus'] == u'prom') and (req_line['cluster_type'] <> u'none'):
            dc_price += int(req_line['cpu_count']) * (int(req_line['item_count']) / 2) *\
                        (12 * drdc_rent_price  + 3 * dc_book_price + dc_startup_price)
            dc_price += int(req_line['cpu_count']) * \
                        (int(req_line['item_count']) - int(req_line['item_count']) / 2) *\
                        (12 * dcmcod_rent_price + 3 * dc_book_price + dc_startup_price)
        else:
            dc_price += int(req_line['cpu_count']) * int(req_line['item_count']) *\
                        (12 * dcmcod_rent_price + 3 * dc_book_price + dc_startup_price)

    elif appliance_price <> 0:
        price_hw += int(req_line['item_count']) * appliance_price * (int(req_line['utilization']) / Decimal(100))
#        print "applicance price - " + str(appliance_price)
#        print "applicance dc_book_price - " + str(dc_book_price)
#        print "applicance dcmcod_rent_price - " + str(dcmcod_rent_price)
#        print "applicance drdc_rent_price - " + str(drdc_rent_price)
#        print "applicance dc_startup_price - " + str(dc_startup_price)
        if (req_line['itemtype1'] == u'mqdmz'):
#            print req_line
            lic_ms_cost = int(req_line['item_count']) * prices_dic['ms_lic_2sock']['price']
            price_lic = lic_ms_cost
            lic_ms_count = int(req_line['item_count'])
        if (req_line['itemstatus'] == u'prom'):
            dc_price += (int(req_line['item_count']) / 2) *\
                        (12 * drdc_rent_price  + 3 * dc_book_price + dc_startup_price)
            dc_price += (int(req_line['item_count']) - int(req_line['item_count']) / 2) *\
                        (12 * dcmcod_rent_price + 3 * dc_book_price + dc_startup_price)
        else:
            dc_price += int(req_line['item_count']) *\
                        (12 * dcmcod_rent_price + 3 * dc_book_price + dc_startup_price)

#   Hardware price calculation for internal storage
    if (req_line['platform_type'] == u'x86_vm') and (req_line['itemtype1'] <> u'mqdmz'):
        intdisks_price = prices_dic['int_stor']['price']
        dc_book_price = prices_dic['int_stor']['dc_book_price']
        dcmcod_rent_price = prices_dic['int_stor']['dcmcod_rent_price']
        drdc_rent_price = prices_dic['int_stor']['drdc_rent_price']
        dc_startup_price = prices_dic['int_stor']['dc_startup_price']

    if intdisks_price <> 0:
#        print "intdisks_price - " + str(intdisks_price)
#        print "intdisks dc_book_price - " + str(dc_book_price)
#        print "intdisks dcmcod_rent_price - " + str(dcmcod_rent_price)
#        print "intdisks dc_startup_price - " + str(dc_startup_price)
        price_hw += int(req_line['hdd_count']) * int(req_line['item_count']) * intdisks_price
        if (req_line['itemstatus'] == u'prom') and (req_line['cluster_type'] <> u'none'):
            dc_price += int(req_line['hdd_count']) * (int(req_line['item_count']) / 2) *\
                        (12 * drdc_rent_price + 3 * dc_book_price + dc_startup_price)
            dc_price += int(req_line['hdd_count']) * \
                        (int(req_line['item_count']) - (int(req_line['item_count']) / 2)) *\
                        (12 * dcmcod_rent_price + 3 * dc_book_price + dc_startup_price)
        else:
            dc_price += int(req_line['hdd_count']) * int(req_line['item_count']) *\
                        (12 * dcmcod_rent_price + 3 * dc_book_price + dc_startup_price)

#   Hardware price calculation for external storage
    if  (req_line['itemstatus'] == u'prom') and (req_line['itemtype1'] <> u'mqdmz'):
        if (req_line['platform_type'] == u'power') or (req_line['platform_type'] == u'itanium') or \
           (u'_series' in req_line['platform_type']):
            if (req_line['itemtype1'] == u'dbarch'):
                san_price = prices_dic['san_stor_mid']['price']
                dc_book_price = prices_dic['san_stor_mid']['dc_book_price']
                dcmcod_rent_price = prices_dic['san_stor_mid']['dcmcod_rent_price']
                drdc_rent_price = prices_dic['san_stor_mid']['drdc_rent_price']
                dc_startup_price = prices_dic['san_stor_mid']['dc_startup_price']
            else:
                if (req_line['cluster_type'] == u'vcs'):
                    if (req_line['backup_type'] == u'yes') and (int(req_line['san_count']) > 2048):
                        san_price = prices_dic['san_stor_full']['price']
                        dc_book_price = prices_dic['san_stor_full']['dc_book_price']
                        dcmcod_rent_price = prices_dic['san_stor_full']['dcmcod_rent_price']
                        drdc_rent_price = prices_dic['san_stor_full']['drdc_rent_price']
                        dc_startup_price = prices_dic['san_stor_full']['dc_startup_price']
                    else:
                        san_price = prices_dic['san_stor_repl']['price']
                        dc_book_price = prices_dic['san_stor_repl']['dc_book_price']
                        dcmcod_rent_price = prices_dic['san_stor_repl']['dcmcod_rent_price']
                        drdc_rent_price = prices_dic['san_stor_repl']['drdc_rent_price']
                        dc_startup_price = prices_dic['san_stor_repl']['dc_startup_price']
                else:
                    if (req_line['backup_type'] == u'yes') or (int(req_line['san_count']) > 2048):
                        san_price = prices_dic['san_stor_bcv']['price']
                        dc_book_price = prices_dic['san_stor_bcv']['dc_book_price']
                        dcmcod_rent_price = prices_dic['san_stor_bcv']['dcmcod_rent_price']
                        drdc_rent_price = prices_dic['san_stor_bcv']['drdc_rent_price']
                        dc_startup_price = prices_dic['san_stor_bcv']['dc_startup_price']
                    else:
                        san_price = prices_dic['san_stor_hiend']['price']
                        dc_book_price = prices_dic['san_stor_hiend']['dc_book_price']
                        dcmcod_rent_price = prices_dic['san_stor_hiend']['dcmcod_rent_price']
                        drdc_rent_price = prices_dic['san_stor_hiend']['drdc_rent_price']
                        dc_startup_price = prices_dic['san_stor_hiend']['dc_startup_price']

        elif (u'x86' in req_line['platform_type']):
            if (req_line['itemtype1'] == u'db') and (req_line['platform_type'] == 'x86'):
                if (req_line['cluster_type'] == u'vcs'):
                    san_price = prices_dic['san_stor_repl']['price']
                    dc_book_price = prices_dic['san_stor_repl']['dc_book_price']
                    dcmcod_rent_price = prices_dic['san_stor_repl']['dcmcod_rent_price']
                    drdc_rent_price = prices_dic['san_stor_repl']['drdc_rent_price']
                    dc_startup_price = prices_dic['san_stor_repl']['dc_startup_price']
                else:
                    san_price = prices_dic['san_stor_hiend']['price']
                    dc_book_price = prices_dic['san_stor_hiend']['dc_book_price']
                    dcmcod_rent_price = prices_dic['san_stor_hiend']['dcmcod_rent_price']
                    drdc_rent_price = prices_dic['san_stor_hiend']['drdc_rent_price']
                    dc_startup_price = prices_dic['san_stor_hiend']['dc_startup_price']
            elif (req_line['platform_type'] == 'x86') or ((req_line['itemtype1'] <> u'db') and
                                                       (req_line['cluster_type'] <> u'vcs')):
                san_price = prices_dic['san_stor_mid']['price']
                dc_book_price = prices_dic['san_stor_mid']['dc_book_price']
                dcmcod_rent_price = prices_dic['san_stor_mid']['dcmcod_rent_price']
                drdc_rent_price = prices_dic['san_stor_mid']['drdc_rent_price']
                dc_startup_price = prices_dic['san_stor_mid']['dc_startup_price']
#                print "+++++" + str(san_price)
            else:
                san_price = prices_dic['san_stor_mid']['price'] + prices_dic['san_stor_vplex']['price']
                dc_book_price = prices_dic['san_stor_mid']['dc_book_price'] + \
                                prices_dic['san_stor_vplex']['dc_book_price']
                dcmcod_rent_price = prices_dic['san_stor_mid']['dcmcod_rent_price'] + \
                                    prices_dic['san_stor_vplex']['dcmcod_rent_price']
                drdc_rent_price = prices_dic['san_stor_mid']['drdc_rent_price'] + \
                                  prices_dic['san_stor_vplex']['drdc_rent_price']
                dc_startup_price = prices_dic['san_stor_mid']['dc_startup_price'] + \
                                   prices_dic['san_stor_vplex']['dc_startup_price']
#                print "====" + str(san_price)

    elif (req_line['itemstatus'] == u'test-nt') and (req_line['itemtype1'] <> u'mqdmz'):
        san_price = prices_dic['san_stor_hiend']['price']
        dc_book_price = prices_dic['san_stor_hiend']['dc_book_price']
        dcmcod_rent_price = prices_dic['san_stor_hiend']['dcmcod_rent_price']
        drdc_rent_price = prices_dic['san_stor_hiend']['drdc_rent_price']
        dc_startup_price = prices_dic['san_stor_hiend']['dc_startup_price']

    elif (req_line['itemtype1'] <> u'mqdmz'):
        san_price = prices_dic['san_stor_mid']['price']
        dc_book_price = prices_dic['san_stor_mid']['dc_book_price']
        dcmcod_rent_price = prices_dic['san_stor_mid']['dcmcod_rent_price']
        drdc_rent_price = prices_dic['san_stor_mid']['drdc_rent_price']
        dc_startup_price = prices_dic['san_stor_mid']['dc_startup_price']

    if san_price <> 0:
#        print "san_price - " + str(san_price)
#        print "san dc_book_price - " + str(dc_book_price)
#        print "san dcmcod_rent_price - " + str(dcmcod_rent_price)
#        print "san drdc - " + str(drdc_rent_price)
#        print "san dc_startup_price - " + str(dc_startup_price)
        price_hw += int(req_line['san_count']) * int(req_line['item_count']) * san_price
        if (req_line['itemstatus'] == u'prom') and (req_line['cluster_type'] <> u'none'):
            dc_price += int(req_line['san_count']) * (int(req_line['item_count'])/2) *\
                        (12 * drdc_rent_price + 3 * dc_book_price + dc_startup_price)
            dc_price += int(req_line['san_count']) * \
                        (int(req_line['item_count']) - (int(req_line['item_count'])/2))*\
                        (12 * dcmcod_rent_price + 3 * dc_book_price + dc_startup_price)
        else:
            dc_price += int(req_line['san_count']) * int(req_line['item_count']) *\
                        (12 * dcmcod_rent_price + 3 * dc_book_price + dc_startup_price)

#   Hardware price calculation for backup storage
    if (req_line['backup_type'] == u'yes') and (req_line['itemtype1'] <> u'dp') and\
       (req_line['itemtype1'] <> u'lb') and (req_line['itemtype1'] <> u'mqdmz'):
        backup_price = prices_dic['backup_stor']['price']
        dc_book_price = prices_dic['backup_stor']['dc_book_price']
        dcmcod_rent_price = prices_dic['backup_stor']['dcmcod_rent_price']
        drdc_rent_price = prices_dic['backup_stor']['drdc_rent_price']
        dc_startup_price = prices_dic['backup_stor']['dc_startup_price']

    if backup_price <> 0:
#        print "backup_price - " + str(backup_price)
#        print "backup dc_book_price - " + str(dc_book_price)
#        print "backup dcmcod_rent_price - " + str(dcmcod_rent_price)
#        print "backup drdc_rent_price - " + str(drdc_rent_price)
#        print "backup dc_startup_price - " + str(dc_startup_price)
        price_hw += (int(req_line['san_count']) + int(req_line['nas_count'])) * int(req_line['item_count']) * \
                    backup_price
        if (req_line['itemstatus'] == u'prom') and (req_line['cluster_type'] <> u'none'):
            dc_price += (int(req_line['san_count']) + int(req_line['nas_count'])) * (int(req_line['item_count'])/2) *\
                        (12 * drdc_rent_price + 3 * dc_book_price + dc_startup_price)
            dc_price += (int(req_line['san_count']) + int(req_line['nas_count'])) * \
                        (int(req_line['item_count']) - (int(req_line['item_count'])/2)) *\
                        (12 * dcmcod_rent_price + 3 * dc_book_price + dc_startup_price)
        else:
            dc_price += (int(req_line['san_count']) + int(req_line['nas_count'])) * int(req_line['item_count']) *\
                        (12 * dcmcod_rent_price + 3 * dc_book_price + dc_startup_price)

#   Hardware price calculation for nas storage
    if int(req_line['nas_count']) > 0:
        dc_book_price = prices_dic['nas_stor']['dc_book_price']
        dcmcod_rent_price = prices_dic['nas_stor']['dcmcod_rent_price']
        drdc_rent_price = prices_dic['nas_stor']['drdc_rent_price']
        dc_startup_price = prices_dic['nas_stor']['dc_startup_price']
        price_hw += int(req_line['nas_count']) * int(req_line['item_count']) * prices_dic['nas_stor']['price']
        if (req_line['itemstatus'] == u'prom') and (req_line['cluster_type'] <> u'none'):
            dc_price += int(req_line['nas_count']) * (int(req_line['item_count'])/2) *\
                        (12 * drdc_rent_price + 3 * dc_book_price + dc_startup_price)
            dc_price += int(req_line['nas_count']) * (int(req_line['item_count']) - (int(req_line['item_count'])/2) ) *\
                        (12 * dcmcod_rent_price + 3 * dc_book_price + dc_startup_price)
        else:
            dc_price += int(req_line['nas_count']) * int(req_line['item_count']) *\
                        (12 * dcmcod_rent_price + 3 * dc_book_price + dc_startup_price)
#        print "nas price - " + str(prices_dic['nas_stor']['price'])
#        print "nas dc_book_price - " + str(dc_book_price)
#        print "nas dcmcod_rent_price - " + str(dcmcod_rent_price)
#        print "nas dc_startup_price - " + str(dc_startup_price)

#   Licenses and support price calculation
    if (req_line['itemtype2'] <> u'upgrade'):
        if (u'x86' in req_line['platform_type']):
            if (req_line['platform_type'] == 'x86_vm') and (req_line['ostype'] == u'windows') and\
               (int(req_line['cpu_count']) > 0):
                if req_line['itemstatus'] == u'prom':
                    k_vm = 5.0
                else:
                    k_vm = 10.0

                lic_ms_cost = Decimal(ceil(float(req_line['item_count']) / 2.0)) * prices_dic['ms_lic_2sock']['price']
                lic_vmware_cost = int(req_line['item_count']) * \
                                  (prices_dic['vmware_lic_2sock']['price'] / Decimal(k_vm))
                price_lic = lic_ms_cost + lic_vmware_cost
                lic_ms_count = ceil(int(req_line['item_count']) / 2.0)
#                print 'liccount = ' + str(lic_ms_count) + '  ' + 'reqline = ' + req_line['item_count']
                lic_vmware_count = int(req_line['item_count']) / k_vm
                supp_vmware_cost = int(req_line['item_count']) * \
                                   (prices_dic['vmware_support_2sock']['price'] / Decimal(k_vm))
                price_support = supp_vmware_cost
                supp_vmware_count = int(req_line['item_count']) / k_vm
            elif (req_line['platform_type'] == 'x86_vm') and (req_line['ostype'] == u'linux') and \
                 (int(req_line['cpu_count']) > 0):
                if req_line['itemstatus'] == u'prom':
                    k_vm = 5.0
                else:
                    k_vm = 10.0
                lic_vmware_cost = int(req_line['item_count'])* (prices_dic['vmware_lic_2sock']['price'] / Decimal(k_vm))
                price_lic = lic_vmware_cost
                lic_vmware_count = int(req_line['item_count']) / k_vm
                supp_vmware_cost = int(req_line['item_count']) * \
                                   prices_dic['vmware_support_2sock']['price'] / Decimal(k_vm)
                supp_rhel_cost = int(req_line['item_count']) * \
                                 prices_dic['rhel_support_2sock']['price'] / Decimal(k_vm)
                price_support =  supp_vmware_cost + supp_rhel_cost
                supp_vmware_count = int(req_line['item_count']) / k_vm
                supp_rhel_count += int(req_line['item_count']) / k_vm

            elif (req_line['platform_type'] == 'x86') and (req_line['ostype'] == u'linux'):
                supp_rhel_cost = int(req_line['item_count']) * prices_dic['rhel_support_2sock']['price']
                price_support = supp_rhel_cost
                supp_rhel_count = int(req_line['item_count'])

            elif (req_line['platform_type'] == 'x86') and (req_line['ostype'] == u'windows'):
                lic_ms_cost = int(req_line['item_count']) * prices_dic['ms_lic_2sock']['price']
                price_lic = lic_ms_cost
                lic_ms_count = int(req_line['item_count'])
#                print req_line['item_count']
        else:
            if (req_line['platform_type'] <> u'itanium') and (req_line['itemtype1'] <> u'lb') and\
               (req_line['itemtype1'] <> u'dp') and (req_line['cluster_type'] == u'vcs') and \
               (req_line['itemstatus'] == u'prom') and (req_line['itemtype1'] <> u'mqdmz'):
                if int(req_line['cpu_count']) > 0:
                    lic_symantec_cost = int(req_line['item_count'])* int(req_line['cpu_count']) * \
                                        prices_dic['symantec_lic']['price']
                    lic_symantec_count += int(req_line['item_count'])
                    price_lic = lic_symantec_cost
                    supp_symantec_cost = int(req_line['item_count']) * int(req_line['cpu_count']) * \
                                      prices_dic['symantec_support']['price']
                    price_support = supp_symantec_cost
                    supp_symantec_count += int(req_line['item_count'])

    if (req_line['db_type'] == 'mssql') and (u'x86' in req_line['platform_type']):
        lic_mssql_count = ceil((int(req_line['item_count'])* int(req_line['cpu_count'])) / 2.0)
        lic_mssql_cost = int(lic_mssql_count) * prices_dic['mssql_lic_2core']['price']
        price_lic = price_lic + lic_mssql_cost

    if ('oracle' in req_line['db_type']):

        lic_oracle_count = int(req_line['item_count'])* int(req_line['cpu_count'])
        supp_oracle_count = lic_oracle_count

        if (u'x86' in req_line['platform_type']):
            if (req_line['db_type'] == 'oracle'):
                lic_oracle_cost = lic_oracle_count * prices_dic['oracle_lic_x86']['price']
                supp_oracle_cost = supp_oracle_count * prices_dic['oracle_supp_x86']['price']
            elif (req_line['db_type'] == 'oracle_part'):
                lic_oracle_cost = lic_oracle_count * (prices_dic['oracle_lic_x86']['price'] +
                                                      prices_dic['oracle_lic_part_x86']['price'])
                supp_oracle_cost = supp_oracle_count * (prices_dic['oracle_supp_x86']['price'] +
                                                        prices_dic['oracle_supp_part_x86']['price'])
            elif (req_line['db_type'] == 'oracle_rac'):
                lic_oracle_cost = lic_oracle_count * (prices_dic['oracle_lic_x86']['price'] +
                                                      prices_dic['oracle_lic_part_x86']['price'] +
                                                      prices_dic['oracle_lic_rac_x86']['price'])
                supp_oracle_cost = supp_oracle_count * (prices_dic['oracle_supp_x86']['price'] +
                                                        prices_dic['oracle_supp_part_x86']['price'] +
                                                        prices_dic['oracle_supp_rac_x86']['price'])
        elif (u'_series' in req_line['platform_type']):
            if (req_line['db_type'] == 'oracle'):
                lic_oracle_cost = lic_oracle_count * prices_dic['oracle_lic_sparc']['price']
                supp_oracle_cost = supp_oracle_count * prices_dic['oracle_supp_sparc']['price']
            elif (req_line['db_type'] == 'oracle_part'):
                lic_oracle_cost = lic_oracle_count * (prices_dic['oracle_lic_sparc']['price'] +
                                                      prices_dic['oracle_lic_part_sparc']['price'])
                supp_oracle_cost = supp_oracle_count * (prices_dic['oracle_supp_sparc']['price'] +
                                                        prices_dic['oracle_supp_part_sparc']['price'])
            elif (req_line['db_type'] == 'oracle_rac'):
                lic_oracle_cost = lic_oracle_count * (prices_dic['oracle_lic_sparc']['price'] +
                                                      prices_dic['oracle_lic_part_sparc']['price'] +
                                                      prices_dic['oracle_lic_rac_sparc']['price'])
                supp_oracle_cost = supp_oracle_count * (prices_dic['oracle_supp_sparc']['price'] +
                                                        prices_dic['oracle_supp_part_sparc']['price'] +
                                                        prices_dic['oracle_supp_rac_sparc']['price'])
        elif (req_line['platform_type'] == u'power'):
            if (req_line['db_type'] == 'oracle'):
                lic_oracle_cost = lic_oracle_count * prices_dic['oracle_lic_power']['price']
                supp_oracle_cost = supp_oracle_count * prices_dic['oracle_supp_power']['price']
            elif (req_line['db_type'] == 'oracle_part'):
                lic_oracle_cost = lic_oracle_count * (prices_dic['oracle_lic_power']['price'] +
                                                      prices_dic['oracle_lic_part_power']['price'])
                supp_oracle_cost = supp_oracle_count * (prices_dic['oracle_supp_power']['price'] +
                                                        prices_dic['oracle_supp_part_power']['price'])
            elif (req_line['db_type'] == 'oracle_rac'):
                lic_oracle_cost = lic_oracle_count * (prices_dic['oracle_lic_power']['price'] +
                                                      prices_dic['oracle_lic_part_power']['price'] +
                                                      prices_dic['oracle_lic_rac_power']['price'])
                supp_oracle_cost = supp_oracle_count * (prices_dic['oracle_supp_power']['price'] +
                                                        prices_dic['oracle_supp_part_power']['price'] +
                                                        prices_dic['oracle_supp_rac_power']['price'])
        elif (req_line['platform_type'] == u'itanium'):
            if (req_line['db_type'] == 'oracle'):
                lic_oracle_cost = lic_oracle_count * prices_dic['oracle_lic_itanium']['price']
                supp_oracle_cost = supp_oracle_count * prices_dic['oracle_supp_itanium']['price']
            elif (req_line['db_type'] == 'oracle_part'):
                lic_oracle_cost = lic_oracle_count * (prices_dic['oracle_lic_itanium']['price'] +
                                                      prices_dic['oracle_lic_part_itanium']['price'])
                supp_oracle_cost = supp_oracle_count * (prices_dic['oracle_supp_itanium']['price'] +
                                                        prices_dic['oracle_supp_part_itanium']['price'])
            elif (req_line['db_type'] == 'oracle_rac'):
                lic_oracle_cost = lic_oracle_count * (prices_dic['oracle_lic_itanium']['price'] +
                                                      prices_dic['oracle_lic_part_itanium']['price'] +
                                                      prices_dic['oracle_lic_rac_itanium']['price'])
                supp_oracle_cost = supp_oracle_count * (prices_dic['oracle_supp_itanium']['price'] +
                                                        prices_dic['oracle_supp_part_itanium']['price'] +
                                                        prices_dic['oracle_supp_rac_itanium']['price'])
        price_lic = price_lic + lic_oracle_cost
        price_support = price_support + supp_oracle_cost

    total_price = price_hw + price_lic + price_support
    req_line['price'] = str(Decimal(total_price).quantize(Decimal(10) ** -2))
    req_line['price_hw'] = str(Decimal(price_hw).quantize(Decimal(10) ** -2))
    req_line['price_lic'] = str(Decimal(price_lic).quantize(Decimal(10) ** -2))
    req_line['price_support'] = str(Decimal(price_support).quantize(Decimal(10) ** -2))
    req_line['lic_ms_cost'] = str(lic_ms_cost)
    req_line['lic_ms_count'] = str(lic_ms_count)
    req_line['supp_rhel_cost'] = str(supp_rhel_cost)
    req_line['supp_rhel_count'] = str(supp_rhel_count)
    req_line['lic_vmware_cost'] = str(lic_vmware_cost)
    req_line['lic_vmware_count'] = str(lic_vmware_count)
    req_line['supp_vmware_cost'] = str(supp_vmware_cost)
    req_line['supp_vmware_count'] = str(supp_vmware_count)
    req_line['lic_symantec_cost'] = str(lic_symantec_cost)
    req_line['lic_symantec_count'] = str(lic_symantec_count)
    req_line['supp_symantec_cost'] = str(supp_symantec_cost)
    req_line['supp_symantec_count'] = str(supp_symantec_count)

    req_line['lic_oracle_count'] = str(lic_oracle_count)
    req_line['lic_oracle_cost'] = str(lic_oracle_cost)
    req_line['lic_mssql_count'] = str(lic_mssql_count)
    req_line['lic_mssql_cost'] = str(lic_mssql_cost)
    req_line['supp_oracle_count'] = str(supp_oracle_count)
    req_line['supp_oracle_cost'] = str(supp_oracle_cost)

    req_line['dc_price'] = str(Decimal(dc_price).quantize(Decimal(10) ** -2))
#    print 'Full DC price - ' + req_line['dc_price']
#    print "-----------------------------------------------------------------"
#    return {'total_price' : total_price,
#            'price_hw' : price_hw,
#            'price_lic' : price_lic,
#            'price_support' : price_support}
#    print req_line
    return req_line
