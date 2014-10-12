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
        self.valid_dcprices_for_lines = [
            536999.408444444,
            190033.225512153,
            109326.879036458,
            55996.694140625,
            227542.122222222,
            93016.7308224826,
            74662.2588541667,
            17998.9374023437,
            145626.958222222,
            8999.46870117187,
            8999.46870117187,
            373169.080444444,
            190033.225512153,
            109326.879036458,
            55996.694140625,
            227542.122222222,
            93016.7308224826,
            74662.2588541667,
            17998.9374023437,
            145626.958222222,
            8999.46870117187,
            8999.46870117187,
            3959232.92666667,
            546101.093333333,
            26451.7717083333,
            3617919.74333333,
            294054.434871795,
            18575.3136314103,
            1517530.92282051,
            294054.434871795,
            18575.3136314103,
            5231542.23666667,
            307181.865,
            18985.5458229167,
            964209.742916667,
            174923.006458333,
            26451.7717083333,
            639962.21875,
            639962.21875,
            63996.221875,
            63996.221875,
            127992.44375,
            63996.221875,
            63996.221875,
        ]

        Prices.objects.create(hw_class=1.00, hw_type="x86_ent", price=556.000000000000000000000000000000,
            dc_rent_price=30.1376779513889, dc_book_price=19.3028819444444,
            dc_startup_price=24.8574262152778)
        Prices.objects.create(hw_class=1.00, hw_type="x86_mid", price=1298.000000000000000000000000000000,
            dc_rent_price=192.881138888889000000000000000000, dc_book_price=123.538444444444000000000000000000,
            dc_startup_price=159.087527777778000000000000000000)
        Prices.objects.create(hw_class=1.00, hw_type="ppc_hiend", price=28664.000000000000000000000000000000,
            dc_rent_price=406.858652343750000000000000000000, dc_book_price=260.588906250000000000000000000000,
            dc_startup_price=335.575253906250000000000000000000)
        Prices.objects.create(hw_class=2.00, hw_type="upg_ppc_hiend", price=28664.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=1.00, hw_type="ppc_mid", price=19321.000000000000000000000000000000,
            dc_rent_price=433.982562500000000000000000000000, dc_book_price=277.961500000000000000000000000000,
            dc_startup_price=357.946937500000000000000000000000)
        Prices.objects.create(hw_class=2.00, hw_type="upg_ppc_mid", price=19321.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=2.00, hw_type="upg_sparc_hiend",
            price=12800.000000000000000000000000000000, dc_rent_price=0E-30, dc_book_price=0E-30,
            dc_startup_price=0E-30)
        Prices.objects.create(hw_class=2.00, hw_type="upg_t4_mid", price=6700.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=1.00, hw_type="sparc_hiend", price=28000.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=1.00, hw_type="t4_mid", price=4900.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=1.00, hw_type="ia_hiend", price=20100.000000000000000000000000000000,
            dc_rent_price=542.478203125000000000000000000000, dc_book_price=542.478203125000000000000000000000,
            dc_startup_price=347.451875000000000000000000000000)
        Prices.objects.create(hw_class=1.00, hw_type="ia_mid", price=6016.000000000000000000000000000000,
            dc_rent_price=180.826067708333000000000000000000, dc_book_price=115.817291666667000000000000000000,
            dc_startup_price=149.144557291667000000000000000000)
        Prices.objects.create(hw_class=2.00, hw_type="upg_ia_hiend", price=6700.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=2.00, hw_type="upg_ia_mid", price=6016.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=1.00, hw_type="t_mid", price=3410.000000000000000000000000000000,
            dc_rent_price=166.916370192308000000000000000000, dc_book_price=106.908269230769000000000000000000,
            dc_startup_price=137.671899038462000000000000000000)
        Prices.objects.create(hw_class=2.00, hw_type="t_mid_upg", price=3410.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=1.00, hw_type="m_mid", price=10000.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=1.00, hw_type="m_hiend", price=6810.000000000000000000000000000000,
            dc_rent_price=361.652135416667000000000000000000, dc_book_price=231.634583333333000000000000000000,
            dc_startup_price=298.289114583333000000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_hiend", price=25.000000000000000000000000000000,
            dc_rent_price=2.260325846354170000000000000000, dc_book_price=1.447716145833330000000000000000,
            dc_startup_price=1.864306966145830000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_mid", price=6.000000000000000000000000000000,
            dc_rent_price=0.904130338541667000000000000000, dc_book_price=0.579086458333333000000000000000,
            dc_startup_price=0.745722786458333000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_vmware", price=6.000000000000000000000000000000,
            dc_rent_price=0.904130338541667000000000000000, dc_book_price=0.579086458333333000000000000000,
            dc_startup_price=0.745722786458333000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="nas_stor", price=12.000000000000000000000000000000,
            dc_rent_price=0.678097753906250000000000000000, dc_book_price=0.434314843750000000000000000000,
            dc_startup_price=0.559292089843750000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="int_stor", price=6.000000000000000000000000000000,
            dc_rent_price=0.904130338541667000000000000000, dc_book_price=0.579086458333333000000000000000,
            dc_startup_price=0.745722786458333000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_full", price=44.000000000000000000000000000000,
            dc_rent_price=2.260325846354170000000000000000, dc_book_price=1.447716145833330000000000000000,
            dc_startup_price=1.864306966145830000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_repl", price=29.000000000000000000000000000000,
            dc_rent_price=2.260325846354170000000000000000, dc_book_price=1.447716145833330000000000000000,
            dc_startup_price=1.864306966145830000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_bcv", price=41.000000000000000000000000000000,
            dc_rent_price=2.260325846354170000000000000000, dc_book_price=1.447716145833330000000000000000,
            dc_startup_price=1.864306966145830000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="backup_stor", price=9.000000000000000000000000000000,
            dc_rent_price=0.678097753906250000000000000000, dc_book_price=0.434314843750000000000000000000,
            dc_startup_price=0.559292089843750000000000000000)
        Prices.objects.create(hw_class=4.00, hw_type="ms_lic", price=150.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=4.00, hw_type="db2_hpux", price=28544.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=4.00, hw_type="db2_aix", price=34253.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=4.00, hw_type="vmware_lic", price=235.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=5.00, hw_type="vmware_support", price=55.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=4.00, hw_type="symantec_lic", price=2000.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=5.00, hw_type="symantec_support",
            price=650.000000000000000000000000000000, dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=5.00, hw_type="rhel_support", price=375.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=6.00, hw_type="loadbalancer", price=120700.000000000000000000000000000000,
            dc_rent_price=4339.825625000000000000000000000000, dc_book_price=2779.615000000000000000000000000000,
            dc_startup_price=3579.469375000000000000000000000000)
        Prices.objects.create(hw_class=6.00, hw_type="datapower", price=111670.000000000000000000000000000000,
            dc_rent_price=4339.825625000000000000000000000000, dc_book_price=2779.615000000000000000000000000000,
            dc_startup_price=3579.469375000000000000000000000000)
        Prices.objects.create(hw_class=3.00, hw_type="san_stor_vplex", price=4.000000000000000000000000000000,
            dc_rent_price=0.452065169270833000000000000000, dc_book_price=0.289543229166667000000000000000,
            dc_startup_price=0.372861393229167000000000000000)
        Prices.objects.create(hw_class=5.00, hw_type="ms_lic_2sock", price=2400.000000000000000000000000000000,
            dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=5.00, hw_type="vmware_lic_2sock",
            price=6682.000000000000000000000000000000, dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=5.00, hw_type="vmware_support_2sock",
            price=1659.000000000000000000000000000000, dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=5.00, hw_type="rhel_support_2sock",
            price=6000.000000000000000000000000000000, dc_rent_price=0E-30, dc_book_price=0E-30, dc_startup_price=0E-30)
        Prices.objects.create(hw_class=6.00, hw_type="mqdmz", price=18000.000000000000000000000000000000,
            dc_rent_price=4339.825625000000000000000000000000, dc_book_price=2779.615000000000000000000000000000,
            dc_startup_price=3579.469375000000000000000000000000)


        self.eos_vals = load_eos_from_xls_new(u'Testcase_v3.xlsx')



    def testEosCalc(self):
        print "Validating HW/SW prices calculation"
        for i in range(int(self.eos_vals['req_count'])):
            self.assertEqual(float(self.eos_vals['price_'+str(i+1)]),self.valid_prices_for_lines[i])

    def testDCCalc(self):
        print "Validating DC prices calculation"
        for i in range(int(self.eos_vals['req_count'])):
            self.assertEqual(self.eos_vals['dc_price_'+str(i+1)],
                str(Decimal(self.valid_dcprices_for_lines[i]).quantize(Decimal(10) ** -2)))