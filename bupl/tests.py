import unittest
from eos import load_eos_from_xls_new
from models import Prices
from decimal import *

class EosTestCase(unittest.TestCase):
    def setUp(self):
        self.valid_prices_for_lines = [897664,
                                       88064,
                                       136320.8,
                                       76320.8,
                                       162112,
                                       42232,
                                       72492.2,
                                       27492.2,
                                       96576,
                                       14946.1,
                                       14946.1,
                                       274080,
                                       95264,
                                       136320.8,
                                       76320.8,
                                       165712,
                                       45832,
                                       71292.2,
                                       26292.2,
                                       100176,
                                       13146.1,
                                       13146.1,
                                       22953472,
                                       1543488,
                                       58730,
                                       8379392,
                                       385088,
                                       22530,
                                       3980032,
                                       385088,
                                       22530,
                                       12544000,
                                       485504,
                                       25668,
                                       1454204,
                                       256062,
                                       58730,
                                       1108910,
                                       1207000,
                                       110891,
                                       120700,
                                       40800,
                                       20400,
                                       20400,
                                       ]
        Prices.objects.create(id=1, hw_class=1, hw_type="x86_ent", price=602)
        Prices.objects.create(id=10, hw_class=1, hw_type="t4_mid", price=4900)
        Prices.objects.create(id=11, hw_class=1, hw_type="ia_hiend", price=20100)
        Prices.objects.create(id=12, hw_class=1, hw_type="ia_mid", price=5666)
        Prices.objects.create(id=13, hw_class=2, hw_type="upg_ia_hiend", price=6700)
        Prices.objects.create(id=14, hw_class=2, hw_type="upg_ia_mid", price=8550)
        Prices.objects.create(id=15, hw_class=1, hw_type="t_mid", price=4097)
        Prices.objects.create(id=16, hw_class=2, hw_type="t_mid_upg", price=4000)
        Prices.objects.create(id=17, hw_class=1, hw_type="m_mid", price=10000)
        Prices.objects.create(id=18, hw_class=1, hw_type="m_hiend", price=9316)
        Prices.objects.create(id=19, hw_class=3, hw_type="san_stor_hiend", price=30)
        Prices.objects.create(id=2, hw_class=1, hw_type="x86_mid", price=1151)
        Prices.objects.create(id=20, hw_class=3, hw_type="san_stor_mid", price=14)
        Prices.objects.create(id=21, hw_class=3, hw_type="san_stor_vmware", price=14)
        Prices.objects.create(id=22, hw_class=3, hw_type="nas_stor", price=15)
        Prices.objects.create(id=23, hw_class=3, hw_type="int_stor", price=6)
        Prices.objects.create(id=24, hw_class=3, hw_type="san_stor_full", price=101)
        Prices.objects.create(id=25, hw_class=3, hw_type="san_stor_repl", price=91)
        Prices.objects.create(id=26, hw_class=3, hw_type="san_stor_bcv", price=49)
        Prices.objects.create(id=27, hw_class=3, hw_type="backup_stor", price=9)
        Prices.objects.create(id=28, hw_class=4, hw_type="ms_lic", price=150)
        Prices.objects.create(id=29, hw_class=4, hw_type="db2_hpux", price=28544)
        Prices.objects.create(id=3, hw_class=1, hw_type="ppc_hiend", price=37781)
        Prices.objects.create(id=30, hw_class=4, hw_type="db2_aix", price=34253)
        Prices.objects.create(id=31, hw_class=4, hw_type="vmware_lic", price=235)
        Prices.objects.create(id=32, hw_class=5, hw_type="vmware_support", price=55)
        Prices.objects.create(id=33, hw_class=4, hw_type="symantec_lic", price=2000)
        Prices.objects.create(id=34, hw_class=5, hw_type="symantec_support", price=650)
        Prices.objects.create(id=35, hw_class=5, hw_type="rhel_support", price=375)
        Prices.objects.create(id=36, hw_class=6, hw_type="loadbalancer", price=120700)
        Prices.objects.create(id=37, hw_class=6, hw_type="datapower", price=110891)
        Prices.objects.create(id=38, hw_class=3, hw_type="san_stor_vplex", price=4)
        Prices.objects.create(id=39, hw_class=5, hw_type="ms_lic_2sock", price=2400)
        Prices.objects.create(id=4, hw_class=2, hw_type="upg_ppc_hiend", price=36725)
        Prices.objects.create(id=40, hw_class=5, hw_type="vmware_lic_2sock", price=6682)
        Prices.objects.create(id=41, hw_class=5, hw_type="vmware_support_2sock", price=1659)
        Prices.objects.create(id=42, hw_class=5, hw_type="rhel_support_2sock", price=6000)
        Prices.objects.create(id=43, hw_class=6, hw_type="mqdmz", price=18000)
        Prices.objects.create(id=5, hw_class=1, hw_type="ppc_mid", price=22197)
        Prices.objects.create(id=6, hw_class=2, hw_type="upg_ppc_mid", price=12800)
        Prices.objects.create(id=7, hw_class=2, hw_type="upg_sparc_hiend", price=12800)
        Prices.objects.create(id=8, hw_class=2, hw_type="upg_t4_mid", price=6700)
        Prices.objects.create(id=9, hw_class=1, hw_type="sparc_hiend", price=28000)
        self.eos_vals = load_eos_from_xls_new(u'Testcase_v2.xlsx')



    def testEosCalc(self):
        for i in range(int(self.eos_vals['req_count'])):
            self.assertEqual(float(self.eos_vals['price_'+str(i+1)]),self.valid_prices_for_lines[i])