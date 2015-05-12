import unittest
from eos import load_eos_from_xls_new
from models import Prices
from decimal import *

class EosTestCase(unittest.TestCase):
    def setUp(self):
        self.valid_prices_for_lines = [611079.58,
                                       96272,
                                       103216.8,
                                       69216.8,
                                       252291.79,
                                       46336,
                                       61940.2,
                                       23940.2,
                                       174467.79,
                                       13170.1,
                                       13170.1,
                                       217952,
                                       103472,
                                       798616.8,
                                       69216.8,
                                       1077136,
                                       49936,
                                       60740.2,
                                       22740.2,
                                       999312,
                                       11370.1,
                                       11370.1,
                                       46788608,
                                       5047744,
                                       160686,
                                       20764160,
                                       2175040,
                                       70914,
                                       10054400,
                                       2175040,
                                       70914,
                                       41047040,
                                       4196224,
                                       134076,
                                       1255852,
                                       218326,
                                       44786,
                                       1116700,
                                       1207000,
                                       111670,
                                       120700,
                                       40800,
                                       20400,
                                       20400,
        ]
        self.valid_dcprices_for_lines = [
            410032.523664,
            212826.048008681,
            104888.995859375,
            55582.2029340278,
            189721.172264,
            120985.801292101,
            48222.1515546875,
            20519.275015191,
            151603.676466667,
            10259.6375075955,
            10259.6375075955,
            344251.063333333,
            212826.048008681,
            104888.995859375,
            55582.2029340278,
            189721.172264,
            120985.801292101,
            48222.1515546875,
            20519.275015191,
            151603.676466667,
            10259.6375075955,
            10259.6375075955,
            3606964.28416,
            548782.511264,
            22940.0299916667,
            2574211.09416,
            254168.079264,
            13733.3289916666,
            1144245.13877538,
            254168.079264,
            13733.3289916666,
            3262713.22082667,
            468991.102597333,
            20446.5484708333,
            586161.20341,
            114916.726639,
            22940.0299916667,
            645470.74375,
            645470.74375,
            74804.445625,
            74804.445625,
            129094.14875,
            74804.445625,
            74804.445625,
        ]


        #print 'Prices.objects.create(hw_class='+str(price.hw_class)+',hw_type="'+str(price.hw_type)+'", price='+str(price.price)+', dcmcod_rent_price='+str(price.dcmcod_rent_price)+', dc_book_price='+str(price.dc_book_price)+', dc_startup_price='+str(price.dc_startup_price)+',drdc_rent_price='+str(price.drdc_rent_price)+')'

        Prices.objects.create(hw_class=1.00, hw_type="x86_ent", price=556.000000000000000000000000000000,
            dcmcod_rent_price=69.8463454861111, dc_book_price=47.376987847222200000000000000000,
            dc_startup_price=58.663524305555600000000000000000, drdc_rent_price=46.102430555555600000000000000000)
        Prices.objects.create(hw_class=1.00, hw_type="x86_mid", price=1298.000000000000000000000000000000,
            dcmcod_rent_price=251.44684375, dc_book_price=170.557156250000000000000000000000,
            dc_startup_price=211.188687500000000000000000000000, drdc_rent_price=165.968750000000000000000000000000)
        Prices.objects.create(hw_class=1.00, hw_type="ppc_hiend", price=28664.000000000000000000000000000000,
            dcmcod_rent_price=471.462832031250000000000000000000, dc_book_price=319.794667968750000000000000000000,
            dc_startup_price=395.978789062500000000000000000000, drdc_rent_price=311.191406250000000000000000000000)
        Prices.objects.create(hw_class=2.00, hw_type="upg_ppc_hiend", price=28664.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=1.00, hw_type="ppc_mid", price=19321.000000000000000000000000000000,
            dcmcod_rent_price=502.8936875, dc_book_price=341.114312500000000000000000000000,
            dc_startup_price=422.377375000000000000000000000000, drdc_rent_price=331.9375)
        Prices.objects.create(hw_class=2.00, hw_type="upg_ppc_mid", price=19321.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=2.00, hw_type="upg_sparc_hiend", price=12800.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=2.00, hw_type="upg_t4_mid", price=6700.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=1.00, hw_type="sparc_hiend", price=28000.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=1.00, hw_type="t4_mid", price=4900.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=1.00, hw_type="ia_hiend", price=20100.000000000000000000000000000000,
            dcmcod_rent_price=419.078072916667000000000000000000, dc_book_price=284.261927083333000000000000000000,
            dc_startup_price=351.981145833333000000000000000000, drdc_rent_price=276.614583333333000000000000000000)
        Prices.objects.create(hw_class=1.00, hw_type="ia_mid", price=6016.000000000000000000000000000000,
            dcmcod_rent_price=419.078072916667000000000000000000, dc_book_price=284.261927083333000000000000000000,
            dc_startup_price=351.981145833333000000000000000000, drdc_rent_price=276.614583333333000000000000000000)
        Prices.objects.create(hw_class=2.00, hw_type="upg_ia_hiend", price=6700.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=2.00, hw_type="upg_ia_mid", price=6016.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=1.00, hw_type="t_mid", price=3410.000000000000000000000000000000,
            dcmcod_rent_price=193.420649038462000000000000000000, dc_book_price=131.197812500000000000000000000000,
            dc_startup_price=162.452836538462000000000000000000, drdc_rent_price=127.668269230769000000000000000000)
        Prices.objects.create(hw_class=2.00, hw_type="t_mid_upg", price=3410.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=1.00, hw_type="m_mid", price=10000.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=1.00, hw_type="m_hiend", price=6810.000000000000000000000000000000,
            dcmcod_rent_price=314.308554687500000000000000000000, dc_book_price=213.196445312500000000000000000000,
            dc_startup_price=263.985859375000000000000000000000, drdc_rent_price=207.460937500000000000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_hiend", price=25.000000000000000000000000000000,
            dcmcod_rent_price=1.149471285714290000000000000000, dc_book_price=0.779689857142857000000000000000,
            dc_startup_price=0.965434000000000000000000000000, drdc_rent_price=0.758714285714286000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_mid", price=6.000000000000000000000000000000,
            dcmcod_rent_price=0.523847591145833000000000000000, dc_book_price=0.355327408854167000000000000000,
            dc_startup_price=0.439976432291667000000000000000, drdc_rent_price=0.345768229166667000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_vmware", price=6.000000000000000000000000000000,
            dcmcod_rent_price=0.523847591145833000000000000000, dc_book_price=0.355327408854167000000000000000,
            dc_startup_price=0.439976432291667000000000000000, drdc_rent_price=0.345768229166667000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="nas_stor", price=12.000000000000000000000000000000,
            dcmcod_rent_price=0.436539659288194000000000000000, dc_book_price=0.296106174045139000000000000000,
            dc_startup_price=0.366647026909722000000000000000, drdc_rent_price=0.288140190972222000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="int_stor", price=6.000000000000000000000000000000,
            dcmcod_rent_price=0.523847591145833000000000000000, dc_book_price=0.355327408854167000000000000000,
            dc_startup_price=0.439976432291667000000000000000, drdc_rent_price=0.345768229166667000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_full", price=44.000000000000000000000000000000,
            dcmcod_rent_price=1.149471285714290000000000000000, dc_book_price=0.779689857142857000000000000000,
            dc_startup_price=0.965434000000000000000000000000, drdc_rent_price=0.758714285714286000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_repl", price=29.000000000000000000000000000000,
            dcmcod_rent_price=1.149471285714290000000000000000, dc_book_price=0.779689857142857000000000000000,
            dc_startup_price=0.965434000000000000000000000000, drdc_rent_price=0.758714285714286000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_bcv", price=41.000000000000000000000000000000,
            dcmcod_rent_price=1.149471285714290000000000000000, dc_book_price=0.779689857142857000000000000000,
            dc_startup_price=0.965434000000000000000000000000, drdc_rent_price=0.758714285714286000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="backup_stor", price=9.000000000000000000000000000000,
            dcmcod_rent_price=0.785771386718750000000000000000, dc_book_price=0.532991113281250000000000000000,
            dc_startup_price=0.659964648437500000000000000000, drdc_rent_price=0.518652343750000000000000000000)
        Prices.objects.create(hw_class=4.00, hw_type="ms_lic", price=150.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="db2_hpux", price=28544.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="db2_aix", price=34253.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="vmware_lic", price=235.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="vmware_support", price=55.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="symantec_lic", price=2000.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="symantec_support", price=650.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="rhel_support", price=375.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=6.00, hw_type="loadbalancer", price=120700.000000000000000000000000000000,
            dcmcod_rent_price=5028.936875, dc_book_price=3411.143125000000000000000000000000,
            dc_startup_price=4223.773750000000000000000000000000, drdc_rent_price=3319.375)
        Prices.objects.create(hw_class=6.00, hw_type="datapower", price=111670.000000000000000000000000000000,
            dcmcod_rent_price=5028.936875, dc_book_price=3411.143125000000000000000000000000,
            dc_startup_price=4223.773750000000000000000000000000, drdc_rent_price=3319.375)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_vplex", price=4.000000000000000000000000000000,
            dcmcod_rent_price=0.261923796000000000000000000000, dc_book_price=0.177663704427083000000000000000,
            dc_startup_price=0.219988216145833000000000000000, drdc_rent_price=0.172884115000000000000000000000)
        Prices.objects.create(hw_class=5.00, hw_type="ms_lic_2sock", price=2400.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="vmware_lic_2sock", price=6682.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="vmware_support_2sock", price=1659.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="rhel_support_2sock", price=6000.000000000000000000000000000000,
            dcmcod_rent_price=0, dc_book_price=0, dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=6.00, hw_type="mqdmz", price=18000.000000000000000000000000000000,
            dcmcod_rent_price=5028.936875000000000000000000000000, dc_book_price=3411.143125000000000000000000000000,
            dc_startup_price=4223.773750000000000000000000000000, drdc_rent_price=3319.375000000000000000000000000000)
        Prices.objects.create(hw_class=4.00, hw_type="mssql_lic_2core",
            price=6622.236800000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="oracle_lic_x86",
            price=23750.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="oracle_supp_x86",
            price=5225.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="oracle_lic_part_x86",
            price=5750.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="oracle_supp_part_x86",
            price=1175.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="oracle_lic_rac_x86",
            price=11500.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="oracle_supp_rac_x86",
            price=2530.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="oracle_lic_sparc",
            price=23750.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="oracle_supp_sparc",
            price=5225.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="oracle_lic_part_sparc",
            price=5750.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="oracle_supp_part_sparc",
            price=1175.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="oracle_lic_rac_sparc",
            price=11500.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="oracle_supp_rac_sparc",
            price=2530.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="oracle_lic_power",
            price=47500.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="oracle_supp_power",
            price=10450.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="oracle_lic_part_power",
            price=11500.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="oracle_supp_part_power",
            price=2350.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="oracle_lic_rac_power",
            price=23000.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="oracle_supp_rac_power",
            price=5060.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="oracle_lic_itanium",
            price=47500.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="oracle_supp_itanium",
            price=10450.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="oracle_lic_part_itanium",
            price=11500.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="oracle_supp_part_itanium",
            price=2350.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=4.00, hw_type="oracle_lic_rac_itanium",
            price=23000.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        Prices.objects.create(hw_class=5.00, hw_type="oracle_supp_rac_itanium",
            price=5060.000000000000000000000000000000, dcmcod_rent_price=0, dc_book_price=0,
            dc_startup_price=0, drdc_rent_price=0)
        self.eos_vals = load_eos_from_xls_new(u'Testcase_v5.xlsx')


    def testEosCalc(self):
        print "Validating HW/SW prices calculation"
        for i in range(int(self.eos_vals['req_count'])):
            self.assertEqual(float(self.eos_vals['price_'+str(i+1)]),self.valid_prices_for_lines[i])

    def testDCCalc(self):
        print "Validating DC prices calculation"
        for i in range(int(self.eos_vals['req_count'])):
            self.assertEqual(self.eos_vals['dc_price_'+str(i+1)],
                str(Decimal(self.valid_dcprices_for_lines[i]).quantize(Decimal(10) ** -2)))


#from bupl.models import Prices
#for price in Prices.objects.all():
#    print 'Prices.objects.create(id='+str(price.id)+', hw_class='+str(price.hw_class)+',hw_type="'+str(price.hw_type)+'", price='+str(price.price)+', dcmcod_rent_price='+str(price.dcmcod_rent_price)+', dc_book_price='+str(price.dc_book_price)+', dc_startup_price='+str(price.dc_startup_price)+',drdc_rent_price='+str(price.drdc_rent_price)+')'
#    print 'Prices.objects.create(id='+str(price.id)+', hw_class='+str(price.hw_class)+',hw_type="'+str(price. hw_type)+'", price='+str(price.price)+', dc_rent_price=0, dc_book_price=0, dc_startup_price=0)'