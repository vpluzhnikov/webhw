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

    supp_rhel_count = 0
    supp_rhel_cost = 0
    supp_vmware_count = 0
    supp_vmware_cost = 0
    supp_symantec_count = 0
    supp_symantec_cost = 0


    k_vm = 1.0


    lic = 0
    support = 0
    cpu_price = 0
    san_price = 0
    intdisks_price = 0
    backup_price = 0
    appliance_price = 0

#   Loading current prices from DB
    for price in Prices.objects.all():
        prices_dic[price.hw_type] = Decimal(price.price)

#   Hardware price calculation for CPUs or Appliances
    if (req_line['platform_type'] == u'x86'):
        if (int(req_line['cpu_count']) > 24):
            cpu_price = prices_dic['x86_mid']
        else:
            cpu_price = prices_dic['x86_ent']
    elif (req_line['platform_type'] == u'power'):
        if (int(req_line['cpu_count']) > 128):
            if (req_line['itemtype2'] == u'upgrade'):
                cpu_price = prices_dic['upg_ppc_hiend']
            else:
                cpu_price = prices_dic['ppc_hiend']
        else:
            if (req_line['itemtype2'] == u'upgrade'):
                cpu_price = prices_dic['upg_ppc_mid']
            else:
                cpu_price = prices_dic['ppc_mid']
    elif (u'_series' in req_line['platform_type']):
        if (int(req_line['cpu_count']) > 128):
            if (req_line['itemtype2'] == u'upgrade'):
                cpu_price = prices_dic['m_hiend']
            else:
                cpu_price = prices_dic['m_hiend']
        else:
            cpu_price = prices_dic['t_mid']
    elif (req_line['platform_type'] == u'itanium'):
        if (int(req_line['cpu_count']) > 64):
            if (req_line['itemtype2'] == u'upgrade'):
                cpu_price = prices_dic['ia_hiend']
            else:
                cpu_price = prices_dic['ia_hiend']
        else:
            cpu_price = prices_dic['ia_mid']
    else:
        if (req_line['itemtype1'] == u'dp'):
            appliance_price = prices_dic['datapower']
        elif (req_line['itemtype1'] == u'lb'):
            appliance_price = prices_dic['loadbalancer']

    if cpu_price <> 0:
#        print "cpuprice - " + str(cpu_price)
        price_hw += int(req_line['cpu_count']) * int(req_line['item_count']) * cpu_price
    elif appliance_price <> 0:
        price_hw += int(req_line['item_count']) * appliance_price

#   Hardware price calculation for internal storage
    if (req_line['platform_type'] == u'x86') and (int(req_line['cpu_count']) < 24):
        intdisks_price = prices_dic['int_stor']

    if intdisks_price <> 0:
#        print "intdisks_price - " + str(intdisks_price)
        price_hw += int(req_line['hdd_count']) * int(req_line['item_count']) * intdisks_price

#   Hardware price calculation for external storage
    if  (req_line['itemstatus'] == u'prom'):
        if (req_line['platform_type'] == u'power') or (req_line['platform_type'] == u'itanium') or \
           (u'_series' in req_line['platform_type']):
            if (req_line['itemtype1'] == u'dbarch'):
                san_price = prices_dic['san_stor_mid']
            else:
                if (req_line['cluster_type'] == u'vcs'):
                    if (req_line['backup_type'] == u'yes') and (int(req_line['san_count']) > 2048):
                        san_price = prices_dic['san_stor_full']
                    else:
                        san_price = prices_dic['san_stor_repl']
                else:
                    if (req_line['backup_type'] == u'yes') or (int(req_line['san_count']) > 2048):
                        san_price = prices_dic['san_stor_bcv']
                    else:
                        san_price = prices_dic['san_stor_hiend']

        elif (req_line['platform_type'] == u'x86'):
            if (req_line['itemtype1'] == u'db') and (int(req_line['cpu_count']) > 24):
                if (req_line['cluster_type'] == u'vcs'):
                    san_price = prices_dic['san_stor_repl']
                else:
                    san_price = prices_dic['san_stor_hiend']
            elif (int(req_line['cpu_count']) > 24) or ((req_line['itemtype1'] <> u'db') and
                                                       (req_line['cluster_type'] <> u'vcs')):
                san_price = prices_dic['san_stor_mid']
            else:
                san_price = prices_dic['san_stor_mid'] + prices_dic['san_stor_vplex']

    elif (req_line['itemstatus'] == u'test-nt'):
        san_price = prices_dic['san_stor_hiend']

    else:
        san_price = prices_dic['san_stor_mid']

    if san_price <> 0:
#        print "san_price - " + str(san_price)
        price_hw += int(req_line['san_count']) * int(req_line['item_count']) * san_price


#   Hardware price calculation for backup storage
    if (req_line['backup_type'] == u'yes') and (req_line['itemtype1'] <> u'dp') and\
       (req_line['itemtype1'] <> u'lb'):
        backup_price = prices_dic['backup_stor']

    if backup_price <> 0:
#        print "backup_price - " + str(backup_price)
        price_hw += (int(req_line['san_count']) + int(req_line['nas_count'])) * int(req_line['item_count']) * \
                    backup_price

#   Hardware price calculation for nas storage
    price_hw += int(req_line['nas_count']) * int(req_line['item_count']) * prices_dic['nas_stor']

#   Licenses and support price calculation
    if (req_line['itemtype2'] <> u'upgrade'):
        if (req_line['platform_type'] == u'x86'):
            if (int(req_line['cpu_count']) <= 24) and (req_line['ostype'] == u'windows'):
                if req_line['itemstatus'] == u'prom':
                    k_vm = 5.0
                else:
                    k_vm = 10.0

                lic_ms_cost = Decimal(ceil(float(req_line['item_count']) / 2)) * prices_dic['ms_lic_2sock']
                lic_vmware_cost = int(req_line['item_count']) * (prices_dic['vmware_lic_2sock'] / Decimal(k_vm))
                price_lic = lic_ms_cost + lic_vmware_cost
                lic_ms_count = ceil(int(req_line['item_count']) / 2)
                lic_vmware_count = int(req_line['item_count']) / k_vm
                supp_vmware_cost = int(req_line['item_count']) * (prices_dic['vmware_support_2sock'] / Decimal(k_vm))
                price_support = supp_vmware_cost
                supp_vmware_count = int(req_line['item_count']) / k_vm

            elif (int(req_line['cpu_count']) <= 24) and (req_line['ostype'] == u'linux'):
                if req_line['itemstatus'] == u'prom':
                    k_vm = 5.0
                else:
                    k_vm = 10.0
                lic_vmware_cost = int(req_line['item_count'])* (prices_dic['vmware_lic_2sock'] / Decimal(k_vm))
                price_lic = lic_vmware_cost
                lic_vmware_count = int(req_line['item_count']) / k_vm
                supp_vmware_cost = int(req_line['item_count']) * prices_dic['vmware_support_2sock'] / Decimal(k_vm)
                supp_rhel_cost = int(req_line['item_count']) * prices_dic['rhel_support_2sock'] / Decimal(k_vm)
                price_support =  supp_vmware_cost + supp_rhel_cost
                supp_vmware_count = int(req_line['item_count']) / k_vm
                supp_rhel_count += int(req_line['item_count']) / k_vm

            elif (int(req_line['cpu_count']) > 24) and (req_line['ostype'] == u'linux'):
                supp_rhel_cost = int(req_line['item_count']) * prices_dic['rhel_support_2sock']
                price_support = supp_rhel_cost
                supp_rhel_count = int(req_line['item_count'])

            elif (int(req_line['cpu_count']) > 24) and (req_line['ostype'] == u'windows'):
                lic_ms_cost = int(req_line['item_count']) * prices_dic['ms_lic_2sock']
                price_lic = lic_ms_cost
                lic_ms_count = int(req_line['item_count'])
        else:
            if (req_line['platform_type'] <> u'itanium') and (req_line['cluster_type'] == u'vcs'):
                lic_symantec_cost = int(req_line['item_count'])* int(req_line['cpu_count']) * prices_dic['symantec_lic']
                price_lic = lic_symantec_cost
                lic_symantec_count += 1
                supp_symantec_cost = int(req_line['item_count']) * int(req_line['cpu_count']) * \
                                      prices_dic['symantec_support']
                price_support = supp_symantec_cost
                supp_symantec_count += 1

#    if lic <> 0:
#        print "lic - " + str(lic)
#        price_lic = int(req_line['cpu_count']) * int(req_line['item_count']) * lic
#    if support <> 0:
#        print "support - " + str(support)
#        price_support = int(req_line['cpu_count']) * int(req_line['item_count']) * support

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

#    return {'total_price' : total_price,
#            'price_hw' : price_hw,
#            'price_lic' : price_lic,
#            'price_support' : price_support}
    return req_line
