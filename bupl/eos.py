# -*- coding: utf-8 -*-
__author__ = 'vs'

from logging import getLogger
from bupl.models import Prices
from decimal import *
from webhw.settings import ARIAL_FONT_FILELOCATION, BOC_WORK_DIR, MEDIA_ROOT
from time import time
from os import path


from io import BytesIO
from reportlab.lib.units import cm
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab import rl_config
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT


ru_vals = { 'new' : u'Новый',
            'upgrade' : u'Апгрейд',
            'app' : u'Сервер приложения',
            'db' : u'Сервер СУБД',
            'term' : u'Терминальный сервер',
            'dp' : u'IBM DataPower',
            'lb' : u'Балансировщик',
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

        #---------------------------------------------
        #Calculation for new systems only
        #---------------------------------------------

        #Calculation for new x86 systems

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

        #Calculation for new AIX, HPUX and Solaris systems

        if (not error_flag) and (req_line['itemtype2'] == u'new') and\
           ((req_line['itemtype1'] == u'app') or (req_line['itemtype1'] == u'db')) and\
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
            if (req_line['itemstatus'] == u'prom') and not (req_line['ostype'] == u'hpux'):
                line_price += Prices.objects.get(hw_type='symantec_lic').price * int(req_line['cpu_count']) *\
                              int(req_line['item_count'])
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

        # Calculation for new x86 systems

        if (not error_flag) and (req_line['itemtype2'] == u'upgrade') and\
           ((req_line['itemtype1'] == u'app') or (req_line['itemtype1'] == u'term') or\
            (req_line['itemtype1'] == u'db')) and ((req_line['ostype'] == u'windows') or\
                                                   (req_line['ostype'] == u'linux')):
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
            elif (req_line['itemtype1'] == u'Сервер СУБД') and (req_line['itemstate'] == u'тест(НТ)'):
                line_price += Prices.objects.get(hw_type='san_stor_hiend').price * int(req_line['san_count']) *\
                              int(req_line['item_count'])
            else:
                line_price += Prices.objects.get(hw_type='san_stor_mid').price * int(req_line['san_count']) * \
                              int(req_line['item_count'])

        #Calculation for AIX, HPUX and Solaris upgrades

        if (not error_flag) and (req_line['itemtype2'] == u'upgrade') and\
           ((req_line['itemtype1'] == u'app') or (req_line['itemtype1'] == u'db')) and\
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
                if (req_line['backup_type'] == u'yes'):
                    line_price += Prices.objects.get(hw_type='san_stor_full').price *\
                                  int(req_line['san_count']) * int(req_line['item_count'])
                    line_price += Prices.objects.get(hw_type='san_stor_full').price *\
                                  int(req_line['san_count']) * int(req_line['item_count'])
                else:
                    line_price += Prices.objects.get(hw_type='san_stor_repl').price *\
                                  int(req_line['san_count']) * int(req_line['item_count'])
            if (req_line['itemstatus'] == u'test-nt'):
                line_price += Prices.objects.get(hw_type='san_stor_hiend').price *\
                              int(req_line['san_count']) * int(req_line['item_count'])
            else:
                line_price += Prices.objects.get(hw_type='san_stor_mid').price *\
                              int(req_line['san_count']) * int(req_line['item_count'])
            line_price += Prices.objects.get(hw_type='nas_stor').price * int(req_line['nas_count']) *\
                          int(req_line['item_count'])
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
    test_nt_cost = 0
    test_cost = 0
    project_id = eos_items['project_id']
    project_name = eos_items['project_name']
    eos_items.pop("project_id", None)
    eos_items.pop("project_name", None)

#    filename = path.join(BOC_WORK_DIR, str(int(time())) + ".pdf")
    if project_id == u'0':
        filename = 'eos_' + str(int(time()))
    else:
        filename = 'eos_' + project_id.split(".")[0]
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
        Title = Paragraph(u'Экспресс-оценка для проекта №' + project_id.split(".")[0], styles["Heading1"])
        SubTitle = Paragraph(project_name, styles["SubTitle"])

    Elements = [Sblogo, Title, SubTitle]

    for key in eos_items.keys():
        logger.error(eos_items[key])
        if (eos_items[key]['itemstatus'] == u'prom'):
            prom_items.append(eos_items[key])
            prom_cost += Decimal(eos_items[key]['price'])
        elif (eos_items[key]['itemstatus'] == u'test-nt'):
            test_nt_items.append(eos_items[key])
            test_nt_cost += Decimal(eos_items[key]['price'])
        elif (eos_items[key]['itemstatus'] == u'test-other'):
            test_items.append(eos_items[key])
            test_cost += Decimal(eos_items[key]['price'])
    total_cost = prom_cost + test_nt_cost + test_cost

    ts = [('GRID', (0,0), (-1,-1), 0.25, colors.black),
          ('ALIGN', (1,1), (-1,-1), 'LEFT'),
          ('FONT', (0,0), (-1,-1), 'Arial')]

    reqts = [('GRID', (0,0), (-1,-1), 0.25, colors.black),
               ('ALIGN', (1,1), (-1,-1), 'LEFT'),
               ('FONT', (0,0), (-1,-1), 'Arial'),
               ('FONTSIZE', (0,0), (-1,-1), 10)]

    #Таблица стоимсоти
    Elements.append(Spacer(0, 0.5 * cm))
    Elements.append(Paragraph(u'Оценка стоимости', styles["Heading2"]))
    Elements.append(Spacer(0, 0.1 * cm))
    data = [[ u'Стоимость промышленных сред', str(prom_cost)+' $'],
            [ u'Стоимость сред нарузочного тестирования', str(test_nt_cost)+' $'],
            [ u'Стоимость прочих тестовых сред', str(test_cost)+' $'],
            [ u'ИТОГО', str(total_cost)+' $'],
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
                Paragraph(item['cpu_count'], styles["Code"]),
                Paragraph(item['ram_count'], styles["Code"]),
                Paragraph(item['hdd_count'], styles["Code"]),
                Paragraph(item['san_count'], styles["Code"]),
                Paragraph(item['nas_count'], styles["Code"]),
                Paragraph(item['price'], styles["Code"])
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
                Paragraph(item['cpu_count'], styles["Code"]),
                Paragraph(item['ram_count'], styles["Code"]),
                Paragraph(item['hdd_count'], styles["Code"]),
                Paragraph(item['san_count'], styles["Code"]),
                Paragraph(item['nas_count'], styles["Code"]),
                Paragraph(item['price'], styles["Code"])
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
                Paragraph(item['cpu_count'], styles["Code"]),
                Paragraph(item['ram_count'], styles["Code"]),
                Paragraph(item['hdd_count'], styles["Code"]),
                Paragraph(item['san_count'], styles["Code"]),
                Paragraph(item['nas_count'], styles["Code"]),
                Paragraph(item['price'], styles["Code"])
            ])
        table = Table(data, style=reqts, hAlign='LEFT', repeatRows=1, splitByRow=1)
        Elements.append(table)
    else:
        Elements.append(Paragraph(u'Прочих сред тестирования нет', styles["Heading3"]))

    doc.build(Elements)

#    response.write(buffer.getvalue())
#    buffer.close()
    return filename