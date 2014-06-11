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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
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
            'mqdmz' : u'Сервер MQ (DMZ)',
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
            'aix' : u'AIX',
            'solaris' : u'Solaris',
            'hpux' : u'HP-UX',
            'linux' : u'Linux (RHEL)',
            'windows' : u'Windows',
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

    lic_and_support_data = {
        'lic_vmware_count' : 0,
        'lic_vmware_cost' : 0,
        'lic_ms_count' : 0,
        'lic_ms_cost' : 0,
        'lic_symantec_count' : 0,
        'lic_symantec_cost' : 0,
        'supp_rhel_count' : 0,
        'supp_rhel_cost' : 0,
        'supp_vmware_count' : 0,
        'supp_vmware_cost' : 0,
        'supp_symantec_count' : 0,
        'supp_symantec_cost' : 0,
    }

    total_lic_counter = 0
    total_supp_counter = 0

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
    Sblogo = Image(path.join(MEDIA_ROOT,'images/sb-logo-new.jpg'), 10 * cm, 1.5 * cm)
    Sblogo.hAlign='RIGHT'
    lh1 = Paragraph(u'Приложение №', styles["Normal"])
    lh2 = Paragraph(u'к решению КПП от ___.20__ г. № __ §__', styles["Normal"])
    if project_id == u'0':
        Title = Paragraph(u'Экспресс-оценка для проекта без номера', styles["Heading1"])
#        Title = Paragraph(u'Экспресс оценка для Программы ТАБС', styles["Heading1"])
        SubTitle = Paragraph(u' ', styles["SubTitle"])
    else:
        Title = Paragraph(u'Экспресс-оценка для проекта №' + project_id, styles["Heading1"])
#        Title = Paragraph(u'Экспресс оценка для Программы ТАБС', styles["Heading1"])
        SubTitle = Paragraph(project_name, styles["SubTitle"])
    Elements = [Sblogo, lh1, lh2, Spacer(0, 0.2 * cm), Title, SubTitle]
    logger.error("FINNNNISSHHHH")

    for key in eos_items.keys():
        for val in lic_and_support_data.keys():
#            print eos_items[key]
            lic_and_support_data[val] += Decimal(eos_items[key][val])
            if 'count' in val:
                if 'lic' in val:
                    total_lic_counter += lic_and_support_data[val]
                else:
                    total_supp_counter += lic_and_support_data[val]

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

#    print lic_and_support_data
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
    Elements.append(Spacer(0, 0.2 * cm))
    Elements.append(Paragraph(u'Оценка стоимости (без НДС)', styles["Heading2"]))
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
    Elements.append(Spacer(0, 0.5 * cm))
    Elements.append(Paragraph(u'Информация о лицензиях и поддержке СПО', styles["Heading2"]))
    Elements.append(Spacer(0, 0.1 * cm))
    if total_lic_counter == 0:
        Elements.append(Paragraph(u'Дополнительных лицензий на СПО не требуется', styles["Heading3"]))
    else:
        data_lic = [['Наименование лицензии', 'Кол-во лицензий', 'Стоимость'],
                ]
        if lic_and_support_data['lic_ms_count'] > 0:
            data_lic.append([
                Paragraph(u'Microsoft Core Infrastructure Server (CIS) Suite Standard (2CPU)', styles["Normal"]),
                Paragraph(str(lic_and_support_data['lic_ms_count']), styles["Normal"]),
                Paragraph(str(lic_and_support_data['lic_ms_cost'].quantize(Decimal(10) ** -2)), styles["Normal"]),
                ])
        if lic_and_support_data['lic_vmware_count'] > 0:
            data_lic.append([
                Paragraph(u'VMware vSphere 5 Enterprise Plus (2CPU)', styles["Normal"]),
                Paragraph(str(lic_and_support_data['lic_vmware_count']), styles["Normal"]),
                Paragraph(str(lic_and_support_data['lic_vmware_cost'].quantize(Decimal(10) ** -2)), styles["Normal"]),
            ])
        if lic_and_support_data['lic_symantec_count'] > 0:
            data_lic.append([
                Paragraph(u'Symantec Storage Foundation HA/DR', styles["Normal"]),
                Paragraph(str(lic_and_support_data['lic_symantec_count']), styles["Normal"]),
                Paragraph(str(lic_and_support_data['lic_symantec_cost'].quantize(Decimal(10) ** -2)), styles["Normal"]),
            ])
        table_lic = Table(data_lic, style=ts, hAlign='LEFT')
        Elements.append(Paragraph(u'Лицензии на СПО:', styles["Heading3"]))
        Elements.append(table_lic)
        Elements.append(Spacer(0, 0.2 * cm))

    if total_supp_counter == 0:
        Elements.append(Paragraph(u'Дополнительной поддержки на СПО не требуется', styles["Heading3"]))
    else:
        data_supp = [['Наименование позиции', 'Кол-во едеиниц', 'Стоимость'],
                ]
        if lic_and_support_data['supp_rhel_count'] > 0:
            data_supp.append([
                Paragraph(u'Red Hat Enterprise Linux Server 6 (2CPU)', styles["Normal"]),
                Paragraph(str(lic_and_support_data['supp_rhel_count']), styles["Normal"]),
                Paragraph(str(lic_and_support_data['supp_rhel_cost'].quantize(Decimal(10) ** -2)), styles["Normal"]),
            ])
        if lic_and_support_data['supp_vmware_count'] > 0:
            data_supp.append([
                Paragraph(u'VMware vSphere 5 Enterprise Plus (2CPU)', styles["Normal"]),
                Paragraph(str(lic_and_support_data['supp_vmware_count']), styles["Normal"]),
                Paragraph(str(lic_and_support_data['supp_vmware_cost'].quantize(Decimal(10) ** -2)), styles["Normal"]),
            ])
        if lic_and_support_data['supp_symantec_count'] > 0:
            data_supp.append([
                Paragraph(u'Symantec Storage Foundation HA/DR', styles["Normal"]),
                Paragraph(str(lic_and_support_data['supp_symantec_count']), styles["Normal"]),
                Paragraph(str(lic_and_support_data['supp_symantec_cost'].quantize(Decimal(10) ** -2)),styles["Normal"]),
            ])
        table_supp = Table(data_supp, style=ts, hAlign='LEFT')
        Elements.append(Paragraph(u'Поддержка на СПО:', styles["Heading3"]))
        Elements.append(table_supp)
        Elements.append(Spacer(0, 0.2 * cm))


    Elements.append(PageBreak())

    #Промышелнные среды
    Elements.append(Spacer(0, 0.5 * cm))
    Elements.append(Paragraph(u'Промышленные среды', styles["Heading2"]))
    Elements.append(Spacer(0, 0.1 * cm))
    if prom_items:
        data = [[Paragraph(u'Кол-во', styles["TableTitleSmall"]),
                 Paragraph(u'Тип позиции', styles["TableTitleSmall"]),
                 Paragraph(u'Наименование', styles["TableTitleSmall"]),
                 Paragraph(u'Статус', styles["TableTitleSmall"]),
                 Paragraph(u'Платформа', styles["TableTitleSmall"]),
                 Paragraph(u'ОС', styles["TableTitleSmall"]),
                 Paragraph(u'Ядер', styles["TableTitleSmall"]),
                 Paragraph(u'ОЗУ (Гб)', styles["TableTitleSmall"]),
                 Paragraph(u'СХД (Гб)', styles["TableTitleSmall"]),
                 Paragraph(u'СХД,SAN (Гб)', styles["TableTitleSmall"]),
                 Paragraph(u'СХД,NAS (Гб)', styles["TableTitleSmall"]),
                 Paragraph(u'Стоимость оборудования ($)', styles["TableTitleSmall"]),
                 Paragraph(u'Стоимость лицензий ($)', styles["TableTitleSmall"]),
                 Paragraph(u'Стоимость поддержки ($)', styles["TableTitleSmall"])
                ]]
        for item in prom_items:
            if item['itemtype1'] in [u'mqdmz', u'lb', u'dp']:
                itemname = ru_vals[item['itemtype1']] + u" (Загрузка " + item["utilization"] + u"%)"
            else:
                itemname = ru_vals[item['itemtype1']]
            data.append([Paragraph(item['item_count'], styles["Code"]),
                Paragraph(ru_vals[item['itemtype2']], styles["Code"]),
                Paragraph(itemname, styles["Code"]),
                Paragraph(ru_vals[item['itemstatus']], styles["Code"]),
                Paragraph(ru_vals[item['platform_type']], styles["Code"]),
                Paragraph(ru_vals[item['ostype']], styles["Code"]),
                Paragraph(str(item['cpu_count']), styles["Code"]),
                Paragraph(str(item['ram_count']), styles["Code"]),
                Paragraph(str(item['hdd_count']), styles["Code"]),
                Paragraph(str(item['san_count']), styles["Code"]),
                Paragraph(str(item['nas_count']), styles["Code"]),
                Paragraph(str(item['price_hw']), styles["Code"]),
                Paragraph(str(item['price_lic']), styles["Code"]),
                Paragraph(str(item['price_support']), styles["Code"]),
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
        data = [[Paragraph(u'Кол-во', styles["TableTitleSmall"]),
                 Paragraph(u'Тип позиции', styles["TableTitleSmall"]),
                 Paragraph(u'Наименование', styles["TableTitleSmall"]),
                 Paragraph(u'Статус', styles["TableTitleSmall"]),
                 Paragraph(u'Платформа', styles["TableTitleSmall"]),
                 Paragraph(u'ОС', styles["TableTitleSmall"]),
                 Paragraph(u'Ядер', styles["TableTitleSmall"]),
                 Paragraph(u'ОЗУ (Гб)', styles["TableTitleSmall"]),
                 Paragraph(u'СХД (Гб)', styles["TableTitleSmall"]),
                 Paragraph(u'СХД,SAN (Гб)', styles["TableTitleSmall"]),
                 Paragraph(u'СХД,NAS (Гб)', styles["TableTitleSmall"]),
                 Paragraph(u'Стоимость оборудования ($)', styles["TableTitleSmall"]),
                 Paragraph(u'Стоимость лицензий ($)', styles["TableTitleSmall"]),
                 Paragraph(u'Стоимость поддержки ($)', styles["TableTitleSmall"])
                ]]
        for item in test_nt_items:
            if item['itemtype1'] in [u'mqdmz', u'lb', u'dp']:
                itemname = ru_vals[item['itemtype1']] + u" (Загрузка " + item["utilization"] + u"%)"
            else:
                itemname = ru_vals[item['itemtype1']]
            data.append([Paragraph(item['item_count'], styles["Code"]),
                Paragraph(ru_vals[item['itemtype2']], styles["Code"]),
                Paragraph(itemname, styles["Code"]),
                Paragraph(ru_vals[item['itemstatus']], styles["Code"]),
                Paragraph(ru_vals[item['platform_type']], styles["Code"]),
                Paragraph(ru_vals[item['ostype']], styles["Code"]),
                Paragraph(str(item['cpu_count']), styles["Code"]),
                Paragraph(str(item['ram_count']), styles["Code"]),
                Paragraph(str(item['hdd_count']), styles["Code"]),
                Paragraph(str(item['san_count']), styles["Code"]),
                Paragraph(str(item['nas_count']), styles["Code"]),
                Paragraph(str(item['price_hw']), styles["Code"]),
                Paragraph(str(item['price_lic']), styles["Code"]),
                Paragraph(str(item['price_support']), styles["Code"]),
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
        data = [[Paragraph(u'Кол-во', styles["TableTitleSmall"]),
                 Paragraph(u'Тип позиции', styles["TableTitleSmall"]),
                 Paragraph(u'Наименование', styles["TableTitleSmall"]),
                 Paragraph(u'Статус', styles["TableTitleSmall"]),
                 Paragraph(u'Платформа', styles["TableTitleSmall"]),
                 Paragraph(u'ОС', styles["TableTitleSmall"]),
                 Paragraph(u'Ядер', styles["TableTitleSmall"]),
                 Paragraph(u'ОЗУ (Гб)', styles["TableTitleSmall"]),
                 Paragraph(u'СХД (Гб)', styles["TableTitleSmall"]),
                 Paragraph(u'СХД,SAN (Гб)', styles["TableTitleSmall"]),
                 Paragraph(u'СХД,NAS (Гб)', styles["TableTitleSmall"]),
                 Paragraph(u'Стоимость оборудования ($)', styles["TableTitleSmall"]),
                 Paragraph(u'Стоимость лицензий ($)', styles["TableTitleSmall"]),
                 Paragraph(u'Стоимость поддержки ($)', styles["TableTitleSmall"])
                ]]
        for item in test_items:
            if item['itemtype1'] in [u'mqdmz', u'lb', u'dp']:
                itemname = ru_vals[item['itemtype1']] + u" (Загрузка " + item["utilization"] + u"%)"
            else:
                itemname = ru_vals[item['itemtype1']]
            data.append([Paragraph(item['item_count'], styles["Code"]),
                Paragraph(ru_vals[item['itemtype2']], styles["Code"]),
                Paragraph(itemname, styles["Code"]),
                Paragraph(ru_vals[item['itemstatus']], styles["Code"]),
                Paragraph(ru_vals[item['platform_type']], styles["Code"]),
                Paragraph(ru_vals[item['ostype']], styles["Code"]),
                Paragraph(str(item['cpu_count']), styles["Code"]),
                Paragraph(str(item['ram_count']), styles["Code"]),
                Paragraph(str(item['hdd_count']), styles["Code"]),
                Paragraph(str(item['san_count']), styles["Code"]),
                Paragraph(str(item['nas_count']), styles["Code"]),
                Paragraph(str(item['price_hw']), styles["Code"]),
                Paragraph(str(item['price_lic']), styles["Code"]),
                Paragraph(str(item['price_support']), styles["Code"]),
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
            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['itemtype1_col'])
            if xls_value == u'Сервер БД':
                req_line['itemtype1']='db'
            elif xls_value ==  u'Сервер приложений':
                req_line['itemtype1']='app'
            elif xls_value ==  u'TS':
                req_line['itemtype1']='term'
            elif xls_value ==  u'Сервер MQ (DMZ)':
                req_line['itemtype1']='mqdmz'
                req_line['platform_type']='---'
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
            if xls_value == u'x86' and req_line['itemtype1'] <> 'mqdmz':
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
                req_line['utilization']='100'
            elif xls_value == u'Alteon':
                req_line['platform_type']='---'
                req_line['ostype']='---'
                req_line['itemtype1']='lb'
                req_line['utilization']='100'
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
            if u'пром' in xls_value.lower():
                req_line['itemstatus'] = 'prom'
            elif u'нт' in xls_value.lower():
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
            elif xls_value == u'DMZ':
                req_line['lan_segment'] = 'DMZ'
            else:
                req_line['lan_segment'] = 'other'

            req_line['req_dbtype']=xls_worksheet.cell_value(curr_row, xls_vals['dbtype_col'])

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['clustype_col'])
            if (u'тр' in xls_value.lower()) or (u'лок' in xls_value.lower()):
                req_line['cluster_type'] = 'vcs'
            elif (u'на уровне приложения' in xls_value.lower()) :
                req_line['cluster_type'] = 'app'
            else:
                req_line['cluster_type'] = 'none'

            xls_value = xls_worksheet.cell_value(curr_row, xls_vals['backuptype_col'])
            if xls_value == u'НЕТ':
                req_line['backup_type'] = 'no'
            else:
                req_line['backup_type'] = 'yes'
            req_line['utilization']='100'
            curr_row += 1
            if (req_line['item_count'] <> 0) and (req_line['item_count'] <> ""):
                req_line = calculate_req_line(req_line)
                req_count += 1
                for key in req_line.keys():
                    EOS_VALS[key+'_'+str(req_count)] = req_line[key]
        EOS_VALS['req_count'] = req_count
        return EOS_VALS
    else:
        return None
