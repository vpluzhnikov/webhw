import unittest
from eos import load_eos_from_xls_new
from models import Prices
from decimal import *

class EosTestCase(unittest.TestCase):
    def setUp(self):
        self.valid_prices_for_lines = [399168,
                                       96272,
                                       103216.8,
                                       69216.8,
                                       146336,
                                       46336,
                                       61940.2,
                                       23940.2,
                                       68512,
                                       13170.1,
                                       13170.1,
                                       217952,
                                       103472,
                                       103216.8,
                                       69216.8,
                                       149936,
                                       49936,
                                       60740.2,
                                       22740.2,
                                       72112,
                                       11370.1,
                                       11370.1,
                                       17118208,
                                       1338944,
                                       44786,
                                       5928960,
                                       320640,
                                       12964,
                                       2636800,
                                       320640,
                                       12964,
                                       11376640,
                                       487424,
                                       18176,
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

        Prices.objects.create(id=1, hw_class=1.00, hw_type="x86_ent", price=556.000000000000000000000000000000)
        Prices.objects.create(id=10, hw_class=1.00, hw_type="t4_mid", price=4900.000000000000000000000000000000)
        Prices.objects.create(id=11, hw_class=1.00, hw_type="ia_hiend", price=20100.000000000000000000000000000000)
        Prices.objects.create(id=12, hw_class=1.00, hw_type="ia_mid", price=6016.000000000000000000000000000000)
        Prices.objects.create(id=13, hw_class=2.00, hw_type="upg_ia_hiend", price=6700.000000000000000000000000000000)
        Prices.objects.create(id=14, hw_class=2.00, hw_type="upg_ia_mid", price=6016.000000000000000000000000000000)
        Prices.objects.create(id=15, hw_class=1.00, hw_type="t_mid", price=3410.000000000000000000000000000000)
        Prices.objects.create(id=16, hw_class=2.00, hw_type="t_mid_upg", price=3410.000000000000000000000000000000)
        Prices.objects.create(id=17, hw_class=1.00, hw_type="m_mid", price=10000.000000000000000000000000000000)
        Prices.objects.create(id=18, hw_class=1.00, hw_type="m_hiend", price=6810.000000000000000000000000000000)
        Prices.objects.create(id=19, hw_class=3.00, hw_type="san_stor_hiend", price=25.000000000000000000000000000000)
        Prices.objects.create(id=2, hw_class=1.00, hw_type="x86_mid", price=1298.000000000000000000000000000000)
        Prices.objects.create(id=20, hw_class=3.00, hw_type="san_stor_mid", price=6.000000000000000000000000000000)
        Prices.objects.create(id=21, hw_class=3.00, hw_type="san_stor_vmware", price=6.000000000000000000000000000000)
        Prices.objects.create(id=22, hw_class=3.00, hw_type="nas_stor", price=12.000000000000000000000000000000)
        Prices.objects.create(id=23, hw_class=3.00, hw_type="int_stor", price=6.000000000000000000000000000000)
        Prices.objects.create(id=24, hw_class=3.00, hw_type="san_stor_full", price=44.000000000000000000000000000000)
        Prices.objects.create(id=25, hw_class=3.00, hw_type="san_stor_repl", price=29.000000000000000000000000000000)
        Prices.objects.create(id=26, hw_class=3.00, hw_type="san_stor_bcv", price=41.000000000000000000000000000000)
        Prices.objects.create(id=27, hw_class=3.00, hw_type="backup_stor", price=9.000000000000000000000000000000)
        Prices.objects.create(id=28, hw_class=4.00, hw_type="ms_lic", price=150.000000000000000000000000000000)
        Prices.objects.create(id=29, hw_class=4.00, hw_type="db2_hpux", price=28544.000000000000000000000000000000)
        Prices.objects.create(id=3, hw_class=1.00, hw_type="ppc_hiend", price=28664.000000000000000000000000000000)
        Prices.objects.create(id=30, hw_class=4.00, hw_type="db2_aix", price=34253.000000000000000000000000000000)
        Prices.objects.create(id=31, hw_class=4.00, hw_type="vmware_lic", price=235.000000000000000000000000000000)
        Prices.objects.create(id=32, hw_class=5.00, hw_type="vmware_support", price=55.000000000000000000000000000000)
        Prices.objects.create(id=33, hw_class=4.00, hw_type="symantec_lic", price=2000.000000000000000000000000000000)
        Prices.objects.create(id=34, hw_class=5.00, hw_type="symantec_support", price=650.000000000000000000000000000000)
        Prices.objects.create(id=35, hw_class=5.00, hw_type="rhel_support", price=375.000000000000000000000000000000)
        Prices.objects.create(id=36, hw_class=6.00, hw_type="loadbalancer", price=120700.000000000000000000000000000000)
        Prices.objects.create(id=37, hw_class=6.00, hw_type="datapower", price=111670.000000000000000000000000000000)
        Prices.objects.create(id=38, hw_class=3.00, hw_type="san_stor_vplex", price=4.000000000000000000000000000000)
        Prices.objects.create(id=39, hw_class=5.00, hw_type="ms_lic_2sock", price=2400.000000000000000000000000000000)
        Prices.objects.create(id=4, hw_class=2.00, hw_type="upg_ppc_hiend", price=28664.000000000000000000000000000000)
        Prices.objects.create(id=40, hw_class=5.00, hw_type="vmware_lic_2sock", price=6682.000000000000000000000000000000)
        Prices.objects.create(id=41, hw_class=5.00, hw_type="vmware_support_2sock", price=1659.000000000000000000000000000000)
        Prices.objects.create(id=42, hw_class=5.00, hw_type="rhel_support_2sock", price=6000.000000000000000000000000000000)
        Prices.objects.create(id=43, hw_class=6.00, hw_type="mqdmz", price=18000.000000000000000000000000000000)
        Prices.objects.create(id=5, hw_class=1.00, hw_type="ppc_mid", price=19321.000000000000000000000000000000)
        Prices.objects.create(id=6, hw_class=2.00, hw_type="upg_ppc_mid", price=19321.000000000000000000000000000000)
        Prices.objects.create(id=7, hw_class=2.00, hw_type="upg_sparc_hiend", price=12800.000000000000000000000000000000)
        Prices.objects.create(id=8, hw_class=2.00, hw_type="upg_t4_mid", price=6700.000000000000000000000000000000)
        Prices.objects.create(id=9, hw_class=1.00, hw_type="sparc_hiend", price=28000.000000000000000000000000000000)

        self.eos_vals = load_eos_from_xls_new(u'Testcase_v2.xlsx')



    def testEosCalc(self):
        for i in range(int(self.eos_vals['req_count'])):
            self.assertEqual(float(self.eos_vals['price_'+str(i+1)]),self.valid_prices_for_lines[i])